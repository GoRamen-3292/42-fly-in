from .hub import Hub
from pydantic import BaseModel, PositiveInt, Field


class Connection(BaseModel):
    """
    2つのハブ間の接続を表すモデル
    """
    name: str = Field(min_length=1)
    hubs: tuple[str, str]
    max_link_capacity: PositiveInt = 1
