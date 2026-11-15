from typing import Any, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    PositiveInt,
    field_validator,
    model_validator,
)

from .connection import Connection
from .hub import Hub
from .types import HubType, InvalidConfigError


class SimulationConfig(BaseModel):
    """シミュレーションの設定を表すモデル"""

    model_config = ConfigDict(extra="forbid", revalidate_instances="always")

    nb_drones: PositiveInt
    hubs: list[Hub]
    connections: list[Connection]

    @field_validator("nb_drones", mode="after")
    @classmethod
    def validate_nb_drones(cls, value: int) -> int:
        """ドローンの数を検証するバリデータ"""
        if value is None:
            raise InvalidConfigError(
                "Invalid configuration:\n" + "The number of drones is unset"
            )
        elif value == 0:
            raise InvalidConfigError(
                "Invalid configuration:\n"
                + "The number of drones must be a positive integer"
            )
        return value

    @model_validator(mode="after")
    def validate_hubs(self) -> Self:
        """ハブの重複を検証するバリデータ"""
        hub_names = [hub.name for hub in self.hubs]
        if len(hub_names) != len(set(hub_names)):
            lines = tuple(
                hub.line_no
                for hub in self.hubs
                if hub_names.count(hub.name) > 1
            )

            raise InvalidConfigError(
                f"Invalid configuration at line {lines[0]} and {lines[1]}:\n"
                + "Duplicate hub names are not allowed"
            )

        start_hubs = [
            hub for hub in self.hubs if (hub.hub_type == HubType.START_HUB)
        ]
        end_hubs = [
            hub for hub in self.hubs if hub.hub_type == HubType.END_HUB
        ]
        if len(start_hubs) != 1 or len(end_hubs) != 1:
            raise InvalidConfigError(
                "Invalid configuration:\n"
                + "There must be exactly one start hub and one end hub"
            )

        for i, connection in enumerate(self.connections):
            for hub in connection.hubs:
                if hub not in hub_names:
                    raise InvalidConfigError(
                        f"Invalid configuration at line {connection.line_no}:\n"
                        + f"Connection {connection.hubs} references a hub that is not defined: {hub}"
                    )
            for j in range(i + 1, len(self.connections)):
                if (
                    connection.hubs == self.connections[j].hubs
                    or connection.hubs == self.connections[j].hubs[::-1]
                ):
                    line_1 = connection.line_no
                    line_2 = self.connections[j].line_no

                    raise InvalidConfigError(
                        f"Invalid configuration at line {line_1} and {line_2}:\n"
                        "Duplicate connections are not allowed: "
                        + str(connection.hubs)
                    )
        return self
