from dataclasses import dataclass
from .hub import Hub


class Drone:
    """ドローンの状態を表すデータクラス"""

    def __init__(self, id: int, position: Hub):
        self.id = id
        self.position = position


@dataclass(frozen=True)
class SimulationResult:
    """シミュレーションの結果を表すデータクラス"""
    is_successful: bool
    drones: list[Drone]
