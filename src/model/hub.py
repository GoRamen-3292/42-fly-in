from .types import Coordinate, ZoneType, HubType
from .validate_args import validate_hub_name, validate_metadata
from pydantic import (BaseModel, Field, PositiveInt, field_validator)


class Hub(BaseModel):
    name: str = Field(min_length=1)
    zone: ZoneType = ZoneType.NORMAL
    color: str | None = Field(default=None)
    coordinate: Coordinate
    max_drones: PositiveInt = 1
    hub_type: HubType = HubType.NORMAL

    @field_validator("name", mode="after")
    def validate_name(cls, value: str) -> str:
        validate_hub_name(value)
        return value

    @field_validator("color", mode="after")
    def validate_zone(cls, value: str | None) -> str | None:
        if value:
            validate_metadata("color", value)
        return value
