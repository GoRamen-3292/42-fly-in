from typing import Any

from pydantic import BaseModel, ConfigDict, PositiveInt, field_validator

from .types import ConnectionKey
from .validate_args import validate_hub_name


def normalize_connction_key(conn: ConnectionKey) -> ConnectionKey:
    """Connectionの正規化を実行する関数

    全てのモデルのインスタンス時や比較時に違うキーの組み合わせ
    """
    if conn[0] <= conn[1]:
        return conn
    else:
        return conn[1], conn[0]


class Connection(BaseModel):
    """2つのハブ間の接続を表すクラス"""

    model_config = ConfigDict(extra="forbid")

    hubs: tuple[str, str]
    max_link_capacity: PositiveInt = 1
    line_no: int | None = None

    @field_validator("hubs", mode="after")
    @classmethod
    def validate_hubs(cls, value: tuple[str, str]) -> tuple[str, str]:
        """ハブの接続を検証するバリデータ

        - 2つのハブが同じでないことを確認する
        - ハブ名が空でないことを確認する
        """
        for hub_name in value:
            if not hub_name:
                raise ValueError("hub names must not be empty")
            validate_hub_name(hub_name)
        if value[0] == value[1]:
            raise ValueError("hubs must contain two different hub names")
        return value

    def model_post_init(self, context: Any) -> None:
        """モデルの初期化と

        _
        """
        if isinstance(self.hubs, tuple) and len(self.hubs) == 2:
            self.hubs = normalize_connction_key(self.hubs)
        else:
            raise ValueError("hubs must be a tuple of two hub names")
