import sdRDM

from typing import Optional, Union
from typing import Optional
from pydantic import PrivateAttr
from pydantic import Field
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


@forge_signature
class Device(sdRDM.DataModel):
    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("deviceINDEX"),
        xml="@id",
    )

    manufacturer: Optional[str] = Field(
        description="Device manufacturer.", default=None
    )

    model: Optional[str] = Field(description="Model name of the device.", default=None)

    software_version: Optional[str] = Field(
        description="Software version of the device.", default=None
    )

    __repo__: Optional[str] = PrivateAttr(
        default="git://github.com/FAIRChemistry/CaliPytion.git"
    )

    __commit__: Optional[str] = PrivateAttr(
        default="8ba8afd30279f7d6b62b70194361c1f4f60b603b"
    )
