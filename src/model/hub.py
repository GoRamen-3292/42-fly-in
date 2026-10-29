from .types import Coordinate, ZoneType, HubType
from .validate_args import validate_hub_name, validate_metadata
from pydantic import (BaseModel, ConfigDict,
                      Field, PositiveInt, field_validator)


class Hub(BaseModel):
    hub_type: HubType = HubType.NORMAL_HUB
    name: str = Field(min_length=1)
    coordinate: Coordinate
    zone: ZoneType = ZoneType.NORMAL
    color: str | None = Field(default=None)
    max_drones: PositiveInt = 1
    model_config = ConfigDict(extra="forbid")

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, value: str) -> str:
        validate_hub_name(value)
        return value

    @field_validator("color", mode="after")
    @classmethod
    def validate_zone(cls, value: str | None) -> str | None:
        if value:
            validate_metadata("color", value)
        return value
