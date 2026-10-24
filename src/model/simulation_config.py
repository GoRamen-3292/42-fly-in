from pydantic import BaseModel, ConfigDict, PositiveInt
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
