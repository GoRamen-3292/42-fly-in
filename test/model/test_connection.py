import pytest
from src.model import Connection


@pytest.mark.parametrize("hubs", [
    ("hub1", "hub2"),
    ("hub1", "h"),
    ("hub2abcdefghijke", "hub3"),
    ("やっほー", "hub3"),
    ("hub=2", "hub3"),
    ("hub_2", "hub3"),
])
def test_valid_hubs_connection(hubs: tuple[str, str]) -> None:
    Connection(
        hubs=hubs,
        max_link_capacity=1,
    )


@pytest.mark.parametrize("hubs", [
    ("hub1", "hub1"),  # 同じハブ名
    ("", "hub2"),  # 空のハブ名
    ("hub1", ""),  # 空のハブ名
    ("", ""),  # 空のハブ名
    ("hub-1", "hub-2"),  # ハブ名にハイフンが含まれる
    ("aaa", "bbb", "ccc"),  # ハブ名が3つ以上
    (),  # ハブ名が0個
    "fdasifa",
    4324431,
])
def test_invalid_hubs_connection(hubs: tuple[str, str]) -> None:
    with pytest.raises(ValueError):
        Connection(
            hubs=hubs,
            max_link_capacity=1,
        )
