from pydantic import BaseModel, ConfigDict, PositiveInt, field_validator

from .connection import Connection
from .hub import Hub
from .types import HubType, InvalidConfigError


class SimulationConfig(BaseModel):
    """シミュレーションの設定を表すモデル"""

    model_config = ConfigDict(extra="forbid", revalidate_instances="always")

    nb_drones: PositiveInt
    hubs: list[Hub]
    connections: list[Connection]

    @field_validator("hubs", mode="after")
    @classmethod
    def validate_hubs(cls, value: list[Hub]) -> list[Hub]:
        """ハブの重複を検証するバリデータ"""
        hub_names = [hub.name for hub in value]
        if len(hub_names) != len(set(hub_names)):
            lines = tuple(
                hub.line_no for hub in value if hub_names.count(hub.name) > 1
            )

            raise InvalidConfigError(
                f"Invalid configuration at line {lines[0]} and {lines[1]}:\n" +
                "Duplicate hub names are not allowed"
            )

        start_hubs = [
            hub for hub in value if (hub.hub_type == HubType.START_HUB)
        ]
        end_hubs = [hub for hub in value if hub.hub_type == HubType.END_HUB]
        if len(start_hubs) != 1 or len(end_hubs) != 1:
            raise InvalidConfigError(
                "Invalid configuration:\n"
                + "There must be exactly one start hub and one end hub"
            )

        return value

    @field_validator("connections", mode="after")
    @classmethod
    def validate_connections(cls, value: list[Connection]) -> list[Connection]:
        """接続の重複を検証するバリデータ"""
        for i, connection in enumerate(value):
            for j in range(i + 1, len(value)):
                if (
                    connection.hubs == value[j].hubs
                    or connection.hubs == value[j].hubs[::-1]
                ):
                    line_1 = connection.line_no
                    line_2 = value[j].line_no

                    raise InvalidConfigError(
                        f"Invalid configuration at line {line_1} and {line_2}:\n"
                        "Duplicate connections are not allowed: "
                        + str(connection.hubs)
                    )
        return value
