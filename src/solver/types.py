from dataclasses import dataclass, field
from src.model import ZoneType, HubType


type PlanElement = tuple[int, str]
"""
ターンと現在の位置についてのタプル型

時間を活用した探索のためのもの
"""

type ParentMap = dict[PlanElement, PlanElement | None]
"""
直前にいたハブを記録し、最後に経路を復元するための辞書型
"""


@dataclass
class SolverHub:
    """
    Simulationクラス内でのHub

    Attributes:
        name (str): ハブの名前
        connections (set[str]): 接続されているハブの名前の集合
        max_drones (int): ハブに存在できる最大ドローン数
        zone (ZoneType): ハブのゾーンタイプ
        hub_type (HubType): ハブの種類
    """
    name: str
    connections: set[str]
    max_drones: int
    zone: ZoneType = ZoneType.NORMAL
    hub_type: HubType = HubType.NORMAL_HUB


@dataclass
class Drone:
    """ドローンの状態を表すデータクラス

    Attributes:
        id (int): ドローンの識別子
        position (str): ドローンの現在位置
        timeline (list[str]): ドローンのTurnごとの位置の履歴、[0]に初期位置
    """
    id: int
    position: str
    timeline: list[PlanElement] = field(default_factory=list)


@dataclass(frozen=True)
class SimulationResult:
    """シミュレーションの結果を表すデータクラス"""
    is_successful: bool
    drones: list[Drone]
