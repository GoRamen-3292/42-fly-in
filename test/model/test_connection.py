import pytest
from src.model import Connection


def test_valid_hubs_connection() -> None:

    HUB_CONNECTIONS = [
        ("hub1", "hub2"),
        ("hub1", "h"),
        ("hub2abcdefghijke", "hub3"),
        ("やっほー", "hub3"),
        ("hub=2", "hub3"),
        ("hub_2", "hub3"),
    ]
    for hubs in HUB_CONNECTIONS:
        Connection(
            hubs=hubs,
            max_link_capacity=1,
        )


def test_invalid_hubs_connection() -> None:
    from model import Connection

    INVALID_HUB_CONNECTIONS = [
        ("hub1", "hub1"),  # 同じハブ名
        ("", "hub2"),  # 空のハブ名
        ("hub1", ""),  # 空のハブ名
        ("", ""),  # 空のハブ名
        ("hub-1", "hub-2"),  # ハブ名にハイフンが含まれる
        ("aaa", "bbb", "ccc"),  # ハブ名が3つ以上
        (),  # ハブ名が0個
        "fdasifa",
        4324431,
    ]
    for hubs in INVALID_HUB_CONNECTIONS:
        with pytest.raises(ValueError):
            Connection(
                hubs=hubs,
                max_link_capacity=1,
            )
