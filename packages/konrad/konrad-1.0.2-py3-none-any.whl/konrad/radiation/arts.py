import logging
import os
from os.path import join, dirname, isfile

import numpy as np
import typhon as ty
from scipy.interpolate import PchipInterpolator

from konrad.utils import get_quadratic_pgrid
from konrad.atmosphere import Atmosphere
from konrad.cloud import ClearSky
from .rrtmg import RRTMG
from .common import fluxes2heating


logger = logging.getLogger(__name__)


class _ARTS:
    def __init__(self, ws=None, threads=None, nstreams=4, scale_vmr=True, verbosity=0):
        """Initialize a wrapper for an ARTS workspace.

        Parameters:
            ws (pyarts.workspace.Workspace): An ARTS workspace.
            threads (int): Number of threads to use.
                Default is all available threads.
            nstreams (int): Number of viewing angles to base the radiative
                flux calculation on.
            scale_vmr (bool): Control whether dry volume mixing ratios are
                scaled with the water-vapor concentration (default is `False.`)
            verbosity (int): Control the ARTS verbosity from 0 (quiet) to 2.
        """
        from pyarts.workspace import Workspace

        self.nstreams = nstreams
        self.scale_vmr = scale_vmr

        if ws is None:
            self.ws = Workspace(verbosity=verbosity)

        self.ws.PlanetSet(option="Earth")
        self.ws.AtmosphereSet1D()

        self.ws.water_p_eq_agendaSet()
        self.ws.gas_scattering_agendaSet()
        self.ws.iy_main_agendaSet(option="Emission")
        self.ws.iy_space_agendaSet()
        self.ws.iy_surface_agendaSet()

        # Number of Stokes components to be computed
        self.ws.IndexSet(self.ws.stokes_dim, 1)

        self.ws.jacobianOff()  # No jacobian calculation
        self.ws.cloudboxOff()  # Clearsky = No scattering

        # Set Absorption Species
        self.ws.abs_speciesSet(
            species=[
                "O2, O2-CIAfunCKDMT100",
                "H2O, H2O-SelfContCKDMT252, H2O-ForeignContCKDMT252",
                "O3",
                "CO2, CO2-CKDMT252",
                "N2, N2-CIAfunCKDMT252, N2-CIArotCKDMT252",
                "N2O",
                "CH4",
                "CO",
            ]
        )

        # Surface handling
        self.ws.VectorSetConstant(self.ws.surface_scalar_reflectivity, 1, 0.0)
        self.ws.surface_rtprop_agendaSet(
            option="Specular_NoPol_ReflFix_SurfTFromt_surface",
        )

        # Read lookup table
        abs_lookup = os.getenv(
            "KONRAD_LOOKUP_TABLE", join(dirname(__file__), "data/abs_lookup.xml")
        )

        if not isfile(abs_lookup):
            raise FileNotFoundError(
                "Could not find ARTS absorption lookup table.\n"
                "To perform ARTS calculations you have to download the lookup "
                "table at:\n\n    https://doi.org/10.5281/zenodo.3885410\n\n"
                "Afterwards, use the following environment variable to tell "
                "konrad where to find it:\n\n"
                "    $ export KONRAD_LOOKUP_TABLE='/path/to/abs_lookup.xml'"
            )

        self.ws.abs_lines_per_speciesSetEmpty()
        self.ws.ReadXML(self.ws.abs_lookup, abs_lookup)
        self.ws.f_gridFromGasAbsLookup()
        self.ws.abs_lookupAdapt()
        self.ws.propmat_clearsky_agendaAuto(use_abs_lookup=1)

        self.ws.sensorOff()  # No sensor properties

        # Set number of OMP threads
        if threads is not None:
            self.ws.SetNumberOfThreads(threads)

    def calc_lookup_table(self, filename=None, fnum=2 ** 15, wavenumber=None):
        """Calculate an absorption lookup table.

        The lookup table is constructed to cover surface temperatures
        between 200 and 400 K, and water vapor mixing ratio up to 40%.

        The frequency grid covers the whole outgoing longwave spectrum
        from 10 to 3,250 cm^-1.

        References:
            An absorption lookup table can be found at
                https://doi.org/10.5281/zenodo.3885410

        Parameters:
            filename (str): (Optional) path to an ARTS XML file
                to store the lookup table.
            fnum (int): Number of frequencies in frequency grid.
                Ignored if `wavenumber` is set.
            wavenumber (ndarray): Wavenumber grid [m-1].
        """
        # Create a frequency grid
        if wavenumber is None:
            wavenumber = np.linspace(10e2, 3_250e2, fnum)
        self.ws.f_grid = ty.physics.wavenumber2frequency(wavenumber)

        # Read line catagloge and create absorption lines.
        self.ws.abs_lines_per_speciesReadSpeciesSplitCatalog(
            basename="lines/"
        )

        # Set line shape and cut off.
        self.ws.LegacyContinuaInit()
        self.ws.abs_lines_per_speciesCompact()  # Throw away lines outside f_grid
        self.ws.abs_lines_per_speciesLineShapeType(self.ws.abs_lines_per_species, "VP")
        self.ws.abs_lines_per_speciesNormalization(self.ws.abs_lines_per_species, "VVH")
        self.ws.abs_lines_per_speciesCutoff(self.ws.abs_lines_per_species, "ByLine", 750e9)
        self.ws.propmat_clearsky_agendaAuto(use_abs_lookup=0)

        # Create a standard atmosphere
        p_grid = get_quadratic_pgrid(1_200e2, 0.5, 80)

        atmosphere = Atmosphere(p_grid)
        atmosphere["T"][-1, :] = 300.0 + 5.0 * np.log(atmosphere["plev"] / 1000e2)
        atmosphere.tracegases_rcemip()
        atmosphere["O2"][:] = 0.2095
        atmosphere["CO2"][:] = 1.5 * 348e-6

        h2o = 0.01 * (p_grid / 1000e2) ** 0.2
        atmosphere["H2O"][:] = h2o[:-1]

        # Convert the konrad atmosphere into an ARTS atm_fields_compact.
        atm_fields_compact = atmosphere.to_atm_fields_compact()
        self.ws.atm_fields_compact = atm_fields_compact

        self.ws.atm_fields_compactAddConstant(
            atm_fields_compact=self.ws.atm_fields_compact,
            name="abs_species-N2",
            value=0.7808,
            condensibles=["abs_species-H2O"],
        )

        # Setup the lookup table calculation
        self.ws.AtmFieldsAndParticleBulkPropFieldFromCompact()
        self.ws.vmr_field.value = self.ws.vmr_field.value.value.clip(min=0.0)
        self.ws.atmfields_checkedCalc()
        self.ws.abs_lookupSetup(p_step=1.0)  # Do not refine p_grid
        self.ws.abs_t_pert = np.arange(-160, 61, 20)

        nls_idx = [
            i for i, tag in enumerate(self.ws.abs_species.value) if "H2O" in tag
        ][0]
        self.ws.abs_nls = [self.ws.abs_species.value[nls_idx]]

        self.ws.abs_nls_pert = np.array(
            [10 ** x for x in [-9, -7, -5, -3, -1, 0, 0.5, 1, 1.5, 2]]
        )

        # Run checks
        self.ws.propmat_clearsky_agenda_checkedCalc()
        self.ws.lbl_checked = 1  # self.ws.lbl_checkedCalc()

        # Calculate actual lookup table.
        self.ws.abs_lookupCalc()

        if filename is not None:
            self.ws.WriteXML("binary", self.ws.abs_lookup, filename)

    def set_atmospheric_state(self, atmosphere, t_surface):
        """Set and check the atmospheric fields."""
        import pyarts

        atm_fields_compact = atmosphere.to_atm_fields_compact()

        # Scale dry-air VMRs with H2O and CO2 content.
        if self.scale_vmr:
            variable_vmrs = (
                atm_fields_compact.get("abs_species-H2O")[0]
                + atm_fields_compact.get("abs_species-CO2")[0]
            )
        else:
            t3_shape = atm_fields_compact.get("abs_species-H2O")[0].shape
            variable_vmrs = np.zeros(t3_shape)

        for species in map(str, atm_fields_compact.grids[0]):
            if (
                species.startswith("abs_species-")
                and "H2O" not in species
                and "CO2" not in species
            ):
                atm_fields_compact.scale(species, 1 - variable_vmrs)

        # Compute the N2 VMR as a residual of the full atmosphere composition.
        n2 = pyarts.arts.GriddedField3(
            grids=atm_fields_compact.grids[1:],
            data=0.7808 * (1 - variable_vmrs),
        )

        self.ws.atm_fields_compact = atm_fields_compact
        self.ws.atm_fields_compactAddSpecies(
            atm_fields_compact=self.ws.atm_fields_compact,
            name="abs_species-N2",
            value=n2,
        )
        self.ws.AtmFieldsAndParticleBulkPropFieldFromCompact()
        self.ws.vmr_field = self.ws.vmr_field.value.value.clip(min=0)

        # Surface & TOA
        # Add pressure layers to the surface and top-of-the-atmosphere to
        # ensure consistent atmosphere boundaries between ARTS and RRTMG.
        self.ws.t_surface = np.array([[t_surface]])
        self.ws.z_surface = np.array([[0.0]])
        self.ws.z_field.value[0, 0, 0] = 0.0

        # Perform configuration and atmosphere checks
        self.ws.atmfields_checkedCalc()
        self.ws.propmat_clearsky_agenda_checkedCalc()
        self.ws.atmgeom_checkedCalc()
        self.ws.cloudbox_checkedCalc()

    def calc_spectral_irradiance_field(self, atmosphere, t_surface):
        """Calculate the spectral irradiance field."""
        self.set_atmospheric_state(atmosphere, t_surface)

        # get the zenith angle grid and the integrations weights
        self.ws.AngularGridsSetFluxCalc(
            N_za_grid=self.nstreams, N_aa_grid=1, za_grid_type="double_gauss"
        )

        # calculate intensity field
        self.ws.Tensor3Create("trans_field")
        self.ws.spectral_radiance_fieldClearskyPlaneParallel(
            trans_field=self.ws.trans_field,
            use_parallel_za=0,
        )
        self.ws.spectral_irradiance_fieldFromSpectralRadianceField()

        return (
            self.ws.f_grid.value[:].copy(),
            self.ws.p_grid.value[:].copy(),
            self.ws.spectral_irradiance_field.value[:].copy(),
            self.ws.trans_field.value[:, 1:, 0].copy().prod(axis=1),
        )

    def calc_optical_thickness(self, atmosphere, t_surface):
        """Calculate the spectral irradiance field."""
        self.set_atmospheric_state(atmosphere, t_surface)

        self.ws.propmat_clearsky_fieldCalc()

        tau = np.trapz(
            y=self.ws.propmat_clearsky_field.value[:, :, 0, 0, :, 0, 0],
            x=self.ws.z_field.value[:, 0, 0],
            axis=-1,
        )

        return self.ws.f_grid.value[:].copy(), tau

    @staticmethod
    def integrate_spectral_irradiance(frequency, irradiance):
        """Integrate the spectral irradiance field over the frequency.

        Parameters:
            frequency (ndarray): Frequency [Hz].
            irradiance (ndarray): Spectral irradiance [W m^-2 / Hz].

        Returns:
            ndarray, ndarray: Downward flux, upward, flux [W m^-2]
        """
        F = np.trapz(irradiance, frequency, axis=0)[:, 0, 0, :]

        # Fluxes
        lw_down = -F[:, 0]
        lw_up = F[:, 1]

        return lw_down, lw_up

    def calc_spectral_olr(self, atmosphere, surface):
        """Calculate the outgoing longwave radiation as function of wavenumber.

        Parameters:
            atmosphere (konrad.atmosphere.Atmosphere): Atmosphere model.
            surface (konrad.surface.Surface): Surface model.

        Returns:
           ndarray: Outgoing longwave radiation [W m^-2 / cm^-1]
        """
        f, _, irradiance_field, _ = self.calc_spectral_irradiance_field(
            atmosphere=atmosphere, t_surface=surface["temperature"][0]
        )
        return f, irradiance_field[:, -1, 0, 0, 1]


class ARTS(RRTMG):
    def __init__(self, store_spectral_olr=False, *args, arts_kwargs={}, **kwargs):
        """Radiation class to provide line-by-line longwave fluxes.

        Parameters:
            store_spectral_olr (bool): Store spectral OLR in netCDF file.
                This will significantly increase the output size.
            args: Positional arguments are used to initialize
                `konrad.radiation.RRTMG`.
            arts_kwargs (dict): Keyword arguments that are used to initialize
                `konrad.radiation.arts._ARTS`.
            kwargs: Keyword arguments are used to initialize
                `konrad.radiation.RRTMG`.
        """
        super().__init__(*args, **kwargs)

        self.store_spectral_olr = store_spectral_olr
        self._arts = _ARTS(**arts_kwargs)

    def calc_radiation(self, atmosphere, surface, cloud):
        # Perform RRTMG simulation
        # Add a virtual layer ontop of the atmosphere column to improve the
        # accuracy of top-of-the-atmosphere fluxes.
        # The fluxes/heating rates in this level are ignored afterwards.
        ph_rrtmg = np.append(atmosphere["phlev"], 1e-2)
        atmosphere_rrtmg = atmosphere.refine_plev(ph_rrtmg, kind="nearest")

        lw_dT_fluxes, sw_dT_fluxes = self.radiative_fluxes(
            atmosphere_rrtmg,
            surface,
            ClearSky.from_atmosphere(atmosphere_rrtmg),
        )
        sw_fluxes = sw_dT_fluxes[1]

        # Perform ARTS simulation
        f, _, irradiance_field, _ = self._arts.calc_spectral_irradiance_field(
            atmosphere=atmosphere, t_surface=surface["temperature"][0]
        )
        Fd, Fu = self._arts.integrate_spectral_irradiance(f, irradiance_field)

        # Interpolate RT results on fine original grid
        def _reshape(x, trim=-1):
            return x[:trim].reshape(1, -1)

        self["lw_flxu"] = _reshape(Fu, trim=None)
        self["lw_flxd"] = _reshape(Fd, trim=None)
        self["lw_flxu_clr"] = _reshape(Fu, trim=None)
        self["lw_flxd_clr"] = _reshape(Fd, trim=None)
        self["sw_flxu"] = _reshape(sw_fluxes["upwelling_shortwave_flux_in_air"].data)
        self["sw_flxd"] = _reshape(sw_fluxes["downwelling_shortwave_flux_in_air"].data)
        self["sw_flxu_clr"] = _reshape(
            sw_fluxes["upwelling_shortwave_flux_in_air_assuming_clear_sky"].data
        )
        self["sw_flxd_clr"] = _reshape(
            sw_fluxes["downwelling_shortwave_flux_in_air_assuming_clear_sky"].data
        )

        self["lw_htngrt"] = np.zeros((1, atmosphere["plev"].size))
        self["lw_htngrt_clr"] = np.zeros((1, atmosphere["plev"].size))
        self["sw_htngrt"] = np.zeros((1, atmosphere["plev"].size))
        self["sw_htngrt_clr"] = np.zeros((1, atmosphere["plev"].size))

        self.coords = {
            "time": np.array([0]),
            "phlev": atmosphere["phlev"],
            "plev": atmosphere["plev"],
        }

        if self.store_spectral_olr:
            self.coords.update({"frequency": f})
            self.create_variable(
                name="outgoing_longwave_radiation",
                data=irradiance_field[:, -1, 0, 0, 1].reshape(1, -1),
                dims=("time", "frequency"),
            )

    def update_heatingrates(self, atmosphere, surface, cloud=None):
        """Returns `xr.Dataset` containing radiative transfer results."""
        self.calc_radiation(atmosphere, surface, cloud)

        def fluxes(net_fluxes, pressure):
            Q = fluxes2heating(net_fluxes, pressure, method="gradient")
            f = PchipInterpolator(np.log(pressure[::-1]), Q[::-1])
            return f(np.log(atmosphere["plev"]))

        self["sw_htngrt"][-1] = fluxes(
            net_fluxes=self["sw_flxu"][-1] - self["sw_flxd"][-1],
            pressure=atmosphere["phlev"],
        )

        self["sw_htngrt_clr"][-1] = fluxes(
            net_fluxes=self["sw_flxu_clr"][-1] - self["sw_flxd_clr"][-1],
            pressure=atmosphere["phlev"],
        )

        self["lw_htngrt"][-1] = fluxes(
            net_fluxes=self["lw_flxu"][-1] - self["lw_flxd"][-1],
            pressure=atmosphere["phlev"],
        )

        self["lw_htngrt_clr"][-1] = fluxes(
            net_fluxes=self["lw_flxu_clr"][-1] - self["lw_flxd_clr"][-1],
            pressure=atmosphere["phlev"],
        )

        self.derive_diagnostics()
