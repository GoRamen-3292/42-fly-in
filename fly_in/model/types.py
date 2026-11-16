"""共通して利用する型や例外を定義するモジュール"""

from enum import StrEnum

type Coordinate = tuple[int, int]
"""座標を表す型

[0]: x座標
[1]: y座標
"""


type ConnectionKey = tuple[str, str]
"""
接続へのキー
"""


class ZoneType(StrEnum):
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


class HubType(StrEnum):
    """ハブの種類を表す列挙型

    - hub: 経由地となる通常のハブ
    - start_hub: すべてのドローンの出発地点となるハブ
    - end_hub: すべてのドローンの目的地となるハブ
    """

    NORMAL_HUB = "hub"
    START_HUB = "start_hub"
    END_HUB = "end_hub"


class InvalidConfigError(ValueError):
    """無効な設定ファイルのエラーを表す例外クラス

    Attributes:
        line_numbers: エラーの原因となった設定ファイルの行番号のリスト、
            特定できない場合はNone
    """

    def __str__(self) -> str:
        """行番号を含めたエラーメッセージを返すメソッド"""
        if self.line_numbers:
            lines_str = ", ".join(str(line) for line in self.line_numbers)
            return (
                f"Invalid configuration at line {lines_str}:\n"
                + super().__str__()
            )
        return "Invalid configuration:\n" + super().__str__()

    def __init__(
        self, message: str, line_numbers: list[int] | None = None
    ) -> None:
        """InvalidConfigErrorを初期化するコンストラクタ

        Args:
            message: エラーの内容を表すメッセージ
            line_numbers: エラーの原因となった設定ファイルの行番号のリスト
        """
        super().__init__(message)
        self.line_numbers = line_numbers
