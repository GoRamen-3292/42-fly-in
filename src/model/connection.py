from .hub import Hub
from pydantic import BaseModel, PositiveInt, Field


class Connection(BaseModel):
    """
    2つのハブ間の接続を表すモデル
    """
    name: str = Field(min_length=1)
    nodes: tuple[Hub, Hub]
    max_link_capacity: PositiveInt = 1
