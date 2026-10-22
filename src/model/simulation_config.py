from pydantic import BaseModel, PositiveInt
from .hub import Hub
from .connection import Connection


# TODO: connectionsの型を検討する
class SimulationConfig(BaseModel):
    """シミュレーションの設定を表すモデル"""
    nb_drones: PositiveInt
    hubs: list[Hub]
    connections: list[Connection] = []
