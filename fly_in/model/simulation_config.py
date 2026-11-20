"""シミュレーション全体の設定を表すモデルを定義するモジュール"""

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

    @field_validator("nb_drones", mode="before")
    @classmethod
    def validate_nb_drones(cls, value: Any) -> Any:
        """ドローンの数を検証するバリデータ"""
        if value is None:
            raise InvalidConfigError(
                "nb_drones: The number of drones is unset",
            )
        return value

    @model_validator(mode="after")
    def validate_duplicates(self) -> Self:
        """ハブと接続の整合性を検証するバリデータ

        - ハブ名が重複していないことを確認する
        - 開始ハブと終了ハブがそれぞれ1つずつ存在することを確認する
        - 接続が定義済みのハブのみを参照していることを確認する
        - 同じハブの組み合わせの接続が重複していないことを確認する

        Raises:
            InvalidConfigError: いずれかの条件を満たさない場合、
                PydanticによってValidationErrorに包まれて送出される
        """
        self._validate_hubs()
        self._validate_connections()
        return self

    def _validate_hubs(self) -> None:
        hub_names = [hub.name for hub in self.hubs]

        if len(hub_names) != len(set(hub_names)):
            for hub in self.hubs:
                if hub_names.count(hub.name) <= 1:
                    continue
                lines: list[int] = [
                    h.line_no
                    for h in self.hubs
                    if h.name == hub.name and h.line_no is not None
                ]
                raise InvalidConfigError(
                    f"Duplicate hub name: {hub.name}",
                    lines if lines else None,
                )

        for hubtype in (HubType.START_HUB, HubType.END_HUB):
            self._check_hub_type(hubtype)

    def _check_hub_type(self, hub_type: HubType) -> None:
        matches = [hub for hub in self.hubs if hub.hub_type == hub_type]
        if len(matches) != 1:
            raise InvalidConfigError(
                f"hubs: There must be exactly one {hub_type} hub",
                [hub.line_no for hub in matches if hub.line_no is not None],
            )

    def _validate_connections(self) -> None:
        hub_names = [hub.name for hub in self.hubs]

        for i, connection in enumerate(self.connections):
            for hub in connection.hubs:
                if hub not in hub_names:
                    raise InvalidConfigError(
                        f"connection: Connection {connection.hubs}"
                        + f" references a hub that is not defined: {hub}",
                        [connection.line_no] if connection.line_no else None,
                    )
            for j in range(i + 1, len(self.connections)):
                if (
                    connection.hubs == self.connections[j].hubs
                    or connection.hubs == self.connections[j].hubs[::-1]
                ):
                    line_1 = connection.line_no
                    line_2 = self.connections[j].line_no
                    lines: list[int] | None = (
                        [line_1, line_2] if line_1 and line_2 else None
                    )

                    raise InvalidConfigError(
                        "connection: Duplicate connections are not allowed: "
                        + str(connection.hubs),
                        lines,
                    )
