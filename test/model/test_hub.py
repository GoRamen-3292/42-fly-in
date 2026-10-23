import sys
from pathlib import Path

sys.path.append("../../src")
sys.path.append("src")


def test_correct_hubs() -> None:
    """正しいHubのリストを持つSimulationConfigのテスト"""
    from model import Hub, HubType, ZoneType

    # 最低限の引数でHubを作成
    for zone in ZoneType.__members__.values():
        Hub(
            name="Hub1",
            zone=zone,
            coordinate=(0, 0),
        )

    for hub_type in HubType.__members__.values():
        Hub(
            name="Hub1",
            coordinate=(0, 0),
            hub_type=hub_type
        )

    COORDINATES = [
        (-10000, -10000),
        (-10000, 10000),
        (10000, -10000),
        (10000, 10000),
        (0, 0),
    ]
    for coordinate in COORDINATES:
        Hub(
            name="Hub1",
            zone=ZoneType.NORMAL,
            coordinate=coordinate,
            hub_type=HubType.NORMAL
        )
