import pytest
from src.model import Hub, HubType, ZoneType, Coordinate


def test_hub_type() -> None:
    for hub_type in HubType.__members__.values():
        assert isinstance(hub_type, str)
        assert hub_type in ("hub", "start_hub", "end_hub")


def test_zone_type() -> None:
    for zone_type in ZoneType.__members__.values():
        assert isinstance(zone_type, str)
        assert zone_type in ("normal", "blocked", "restricted", "priority")


def test_correct_zonetype() -> None:
    # 最低限の引数でHubを作成
    for zone in ZoneType.__members__.values():
        Hub(
            name="Hub1",
            zone=zone,
            coordinate=(0, 0),
        )

    # 文字列からZoneTypeを作成する場合もテスト
    for zone in ZoneType.__members__.values():
        Hub(
            name="Hub1",
            zone=zone.value,  # type: ignore
            coordinate=(0, 0),
        )


def test_correct_hubtype() -> None:
    for hub_type in HubType.__members__.values():
        Hub(
            name="Hub1",
            coordinate=(0, 0),
            hub_type=hub_type
        )

    # 文字列からHubTypeを作成する場合もテスト
    for hub_type in HubType.__members__.values():
        Hub(
            name="Hub1",
            coordinate=(0, 0),
            hub_type=hub_type.value,  # type: ignore
        )


@pytest.mark.parametrize("coordinate", [
    (-10000, -10000),
    (-10000, 10000),
    (10000, -10000),
    (10000, 10000),
    ("1000", "2000"),
    ("0", 42),
    (42, "-42"),
    (0, 0),
])
def test_correct_coordinate(coordinate: Coordinate) -> None:
    """正しいHubのリストを持つSimulationConfigのテスト"""
    Hub(
        name="Hub1",
        coordinate=coordinate,
    )


@pytest.mark.parametrize("name", [
    "A",
    "Abcdefg",
    "あいうえお",
    "アイウエオ",
    "alpha_bet",
    "1234567890",
    "aaa=aaa",
    "#fjapdfasifjai",
    "#=[]",
    "[]",
])
def test_correct_name(name: str) -> None:
    Hub(
        name=name,
        coordinate=(0, 0),
    )


@pytest.mark.parametrize("color", [
    None,
    "",
    "red",
    "white",
    "#FFFFFF",
    "aaa-aaa",
    "]",
    "]]]",
    "[",
])
def test_correct_color(color: str | None) -> None:
    Hub(
        name="Hub1",
        coordinate=(0, 0),
        color=color
    )


def test_other_attributes() -> None:
    Hub(
        name="Hub1",
        zone=ZoneType.NORMAL,
        color="white",
        coordinate=(0, 0),
        max_drones=10,
        hub_type=HubType.START_HUB
    )
    Hub(
        name="Hub1",
        zone=ZoneType.BLOCKED,
        color="white",
        coordinate=(0, 0),
        max_drones=10,
        hub_type=HubType.START_HUB
    )
