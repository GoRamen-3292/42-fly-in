from dataclasses import dataclass
from src.model import ZoneType, HubType


@dataclass
class SolverHub:
    name: str
    connections: set[str]
    seen: bool = False
    shortest_path: list[str] | None = None
    min_cost: int | None = None
    # max_drones: int
    cost: int = 1
    zone: ZoneType = ZoneType.NORMAL
    hub_type: HubType = HubType.NORMAL_HUB


@dataclass
class Drone:
    """ドローンの状態を表すデータクラス"""
    id: int
    position: str


@dataclass(frozen=True)
class SimulationResult:
    """シミュレーションの結果を表すデータクラス"""
    is_successful: bool
    drones: list[Drone]
