from pydantic import (BaseModel, Field, PositiveInt)
from .types import Coordinate, ZoneType, HubType


class Hub(BaseModel):
    name: str = Field(min_length=1)
    zone: ZoneType = ZoneType.normal
    color: str | None = Field(default=None)
    coordinate: Coordinate
    max_drones: PositiveInt = 1
    hub_type: HubType
