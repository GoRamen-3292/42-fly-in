from enum import Enum

type Coordinate = tuple[int, int]
"""座標を表す型

[0]: x座標
[1]: y座標
"""


class ZoneType(str, Enum):
    """ゾーンの種類を表す列挙型

    - normal: ドローンが1ターンで通行できる通常のゾーン
    - blocked: ドローンが通行できないゾーン
    - restricted: ドローンが2ターンを通過に要するゾーン
    - priority: 経路探索において優先されるゾーン、1ターンを通過に要する
    """
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class HubType(str, Enum):
    NORMAL_HUB = "hub"
    START_HUB = "start_hub"
    END_HUB = "end_hub"
