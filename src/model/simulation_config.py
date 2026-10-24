from pydantic import BaseModel, ConfigDict, PositiveInt, field_validator
from .hub import Hub
from .connection import Connection


# TODO: connectionsの型を検討する
class SimulationConfig(BaseModel):
    """シミュレーションの設定を表すモデル"""
    nb_drones: PositiveInt
    hubs: list[Hub]
    connections: list[Connection]
    model_config = ConfigDict({
        "extra": "forbid",
    })

    @classmethod
    @field_validator("hubs", mode="after")
    def validate_hubs(cls, value: list[Hub]) -> list[Hub]:
        """ハブの重複を検証するバリデータ"""
        hub_names = [hub.name for hub in value]
        if len(hub_names) != len(set(hub_names)):
            raise ValueError("Duplicate hub names are not allowed")
        return value

    # @classmethod
    # @field_validator("connections", mode="after")
    # def validate_connections(cls, value: list[Connection]) -> list[Connection]:
    #     """接続の重複を検証するバリデータ"""


class SimulationState(SimulationConfig):
    """シミュレーションの状態を表すモデル

    実際にシミュレーションを実行しているときに、その状態を管理するためのモデル

    オーバーライドによって値の属性を追加する

    TODO: ドローンの位置や状態を管理するための属性を追加する
    TODO: 解決をする場所まで移動する?
    """
    model_config = ConfigDict({
        "extra": "allow",
    })
