import sys

sys.path.append("../../src")
sys.path.append("src")


def test_correct_zonetype() -> None:
    from model import Hub, ZoneType

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
            zone=zone.value,
            coordinate=(0, 0),
        )


def test_correct_hubtype() -> None:
    from model import Hub, HubType

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
            hub_type=hub_type.value
        )


def test_correct_coordinate() -> None:
    from model import Hub

    """正しいHubのリストを持つSimulationConfigのテスト"""
    COORDINATES = [
        (-10000, -10000),
        (-10000, 10000),
        (10000, -10000),
        (10000, 10000),
        ("1000", "2000"),
        ("0", 42),
        (42, "-42"),
        (0, 0),
    ]
    for coordinate in COORDINATES:
        Hub(
            name="Hub1",
            coordinate=coordinate,
        )


def test_correct_name() -> None:
    from model import Hub

    NAMES = [
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
    ]
    for name in NAMES:
        Hub(
            name=name,
            coordinate=(0, 0),
        )


def test_correct_color() -> None:
    from model import Hub

    COLORS = [
        None,
        "",
        "red",
        "white",
        "#FFFFFF",
        "aaa-aaa",
    ]
    for color in COLORS:
        Hub(
            name="Hub1",
            coordinate=(0, 0),
            color=color
        )


def test_other_attributes() -> None:
    from model import Hub, HubType, ZoneType

    Hub(
        name="Hub1",
        zone=ZoneType.NORMAL,
        color="white",
        coordinate=(0, 0),
        max_drones=10,
        hub_type=HubType.START
    )
    Hub(
        name="Hub1",
        zone=ZoneType.BLOCKED,
        color="white",
        coordinate=(0, 0),
        max_drones=10,
        hub_type=HubType.START
    )
