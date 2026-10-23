from .types import Coordinate, ZoneType, HubType
from pydantic import (BaseModel, Field, PositiveInt)


class Hub(BaseModel):
    name: str = Field(min_length=1)
    zone: ZoneType = ZoneType.NORMAL
    color: str | None = Field(default=None)
    coordinate: Coordinate
    max_drones: PositiveInt = 1
    hub_type: HubType = HubType.NORMAL
