from dataclasses import dataclass, field
from src.model import ConnectionKey, ZoneType, HubType

# type PlanElement = tuple[int, str | ConnectionKey]
type PlanElement = tuple[int, str]
"""
ターンと現在滞在しているハブについてのタプル型

時間を活用した探索のためのもの
"""

type PlanConnectionElement = tuple[int, ConnectionKey]
"""
ターンと現在滞在しているConnectionについてのタプル型

スケジュールと出力に利用する
"""

type ParentMap = dict[PlanElement | PlanConnectionElement,
                      PlanElement | PlanConnectionElement | None]
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
        id: ドローンの識別子
        position: ドローンの現在位置
        timeline: ドローンのTurnごとの位置の履歴、[0]に初期位置
    """
    id: int
    start_pos: str
    timeline: list[PlanElement | PlanConnectionElement] = field(
        default_factory=list)


@dataclass(frozen=True)
class SimulationResult:
    """シミュレーションの結果を表すデータクラス"""
    is_successful: bool
    drones: list[Drone]
