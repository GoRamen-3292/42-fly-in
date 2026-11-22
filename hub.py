"""ハブを表すモデルを定義するモジュール"""

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, field_validator

from model_types import Coordinate, HubType, ZoneType
from validate_args import validate_hub_name, validate_metadata


class Hub(BaseModel):
    """ハブを表すモデル"""

    model_config = ConfigDict(extra="forbid")

    hub_type: HubType = HubType.NORMAL_HUB
    name: str = Field(min_length=1)
    coordinate: Coordinate
    zone: ZoneType = ZoneType.NORMAL
    color: str | None = Field(default=None)
    max_drones: PositiveInt = 1
    line_no: int | None = None

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """ハブ名を検証するバリデータ

        ハブ名に'-'や空白文字が含まれていないことを確認する
        """
        validate_hub_name(value)
        return value

    @field_validator("color", mode="after")
    @classmethod
    def validate_color(cls, value: str | None) -> str | None:
        """色の指定を検証するバリデータ

        色が指定されている場合のみ、'='や空白文字が含まれていないことを確認する
        """
        if value:
            validate_metadata("color", value)
        return value
