import sdRDM

from typing import Optional, Union
from typing import List
from typing import Optional
from pydantic import PrivateAttr
from pydantic import Field
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator
from pydantic.types import PositiveFloat
from .concentrationunits import ConcentrationUnits
from .device import Device
from .series import Series
from .spectrum import Spectrum
from .standard import Standard
from .temperatureunits import TemperatureUnits


@forge_signature
class Calibration(sdRDM.DataModel):
    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("calibrationINDEX"),
        xml="@id",
    )

    reactant_id: Optional[str] = Field(
        description="Unique identifier of the calibrated reactant.", default=None
    )

    date: Optional[str] = Field(
        description="Date when the calibration data was measured", default=None
    )

    pH: Optional[PositiveFloat] = Field(description="pH of solution.", default=None)

    temperature: Optional[PositiveFloat] = Field(
        description="Temperature during calibration.", default=None
    )

    temperature_unit: Optional[TemperatureUnits] = Field(
        description="Temperature unit.", default=None
    )

    device: Optional[Device] = Field(
        description="Device object, containing information about the analytic device.",
        default=None,
    )

    standard: List[Standard] = Field(
        description="Standard data of a substance.", default_factory=ListPlus
    )

    spectrum: Optional[Spectrum] = Field(
        description="Spectrum data of a substance.", default=None
    )

    __repo__: Optional[str] = PrivateAttr(
        default="git://github.com/FAIRChemistry/CaliPytion.git"
    )

    __commit__: Optional[str] = PrivateAttr(
        default="e91d9d7fe97fce7a8c92c13d98ece45137e71ff2"
    )

    def add_to_standard(
        self,
        concentration: List[float],
        absorption: List[Series],
        wavelength: Optional[float] = None,
        concentration_unit: Optional[ConcentrationUnits] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        Adds an instance of 'Standard' to the attribute 'standard'.

        Args:


            id (str): Unique identifier of the 'Standard' object. Defaults to 'None'.


            concentration (List[float]): Concentration of the reactant.


            absorption (List[Series]): Measured absorption, corresponding to the applied concentration of the reactant.


            wavelength (Optional[float]): Detection wavelength. Defaults to None


            concentration_unit (Optional[ConcentrationUnits]): Concentration unit. Defaults to None
        """

        params = {
            "concentration": concentration,
            "absorption": absorption,
            "wavelength": wavelength,
            "concentration_unit": concentration_unit,
        }
        if id is not None:
            params["id"] = id
        standard = [Standard(**params)]
        self.standard = self.standard + standard
