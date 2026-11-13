import pytest

from src.model import Connection, normalize_connction_key


@pytest.mark.parametrize(
    "hubs",
    [
        ("hub1", "hub2"),
        ("hub1", "h"),
        ("hub2abcdefghijke", "hub3"),
        ("やっほー", "hub3"),
        ("hub=2", "hub3"),
        ("hub_2", "hub3"),
    ],
)
def test_valid_hubs_connection(hubs: tuple[str, str]) -> None:
    Connection(
        hubs=hubs,
        max_link_capacity=1,
    )


@pytest.mark.parametrize(
    "hubs",
    [
        ("hub1", "hub1"),  # 同じハブ名
        ("", "hub2"),  # 空のハブ名
        ("hub1", ""),  # 空のハブ名
        ("", ""),  # 空のハブ名
        ("hub-1", "hub-2"),  # ハブ名にハイフンが含まれる
        ("aaa", "bbb", "ccc"),  # ハブ名が3つ以上
        (),  # ハブ名が0個
        (" aaa "),  # 空白
        (" "),  # 空白
        (" \t"),  # 空白
        ("\t aaaa \t"),  # 空白
        (" aaaa "),  # 空白
        "fdasifa",
        4324431,
    ],
)
def test_invalid_hubs_connection(hubs: tuple[str, str]) -> None:
    with pytest.raises(ValueError):
        Connection(
            hubs=hubs,
            max_link_capacity=1,
        )


@pytest.mark.parametrize(
    "max_link_capacity",
    [
        1,
        10,
        100,
        4371809348157145981473597198543719878945980143509731089462093659143609135719857149375,
    ],
)
def test_valid_max_link_capacity(max_link_capacity: int) -> None:
    Connection(
        hubs=("hub1", "hub2"),
        max_link_capacity=max_link_capacity,
    )


@pytest.mark.parametrize(
    "max_link_capacity",
    [
        0,
        -1,
        -100,
        -4371809348157145981473597198543719878945980143509731089462093659143609135719857149375,
    ],
)
def test_invalid_max_link_capacity(max_link_capacity: int) -> None:
    with pytest.raises(ValueError):
        Connection(
            hubs=("hub1", "hub2"),
            max_link_capacity=max_link_capacity,
        )


@pytest.mark.parametrize(
    "hubs",
    [
        ("hub1", "hub2"),
        ("hub2", "hub1"),
        ("hub1", "hub3"),
        ("hub2", "hub3"),
        ("hub3", "hub1"),
    ],
)
def test_normalization_of_hubs(hubs: tuple[str, str]) -> None:
    connection = Connection(
        hubs=hubs,
        max_link_capacity=1,
    )
    assert connection.hubs == normalize_connction_key(hubs)
