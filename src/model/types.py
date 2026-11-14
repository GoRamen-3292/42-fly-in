from enum import Enum

type Coordinate = tuple[int, int]
"""座標を表す型

[0]: x座標
[1]: y座標
"""


type ConnectionKey = tuple[str, str]
"""
接続へのキー
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


class InvalidConfigError(ValueError):
    """無効な設定ファイルのエラーを表す例外クラス"""

    def __init__(self, message: str, line_number: int | None = None) -> None:
        if line_number is not None:
            message = f"Line {line_number}: {message}"
        super().__init__(message)
