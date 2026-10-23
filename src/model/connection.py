from .validate_args import validate_hub_name
from pydantic import BaseModel, PositiveInt, field_validator


class Connection(BaseModel):
    """
    2つのハブ間の接続を表すモデル
    """
    hubs: tuple[str, str]
    max_link_capacity: PositiveInt = 1

    @field_validator("hubs", mode="after")
    @classmethod
    def validate_hubs(cls, value: tuple[str, str]) -> tuple[str, str]:
        """
        ハブの接続を検証するバリデータ

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
