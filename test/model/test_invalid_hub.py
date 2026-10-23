import sys
import pytest
from pydantic import ValidationError
from pathlib import Path

sys.path.append("../../src")
sys.path.append("src")


def test_incorrect_zonetype() -> None:
    from model import Hub, HubType, ZoneType

    # 最低限の引数でHubを作成
    for zone in (
        "undefined",
        None,
    ):
        with pytest.raises(ValidationError):
            Hub(
                name="Hub1",
                zone=zone,
                coordinate=(0, 0),
            )

    with pytest.raises(AttributeError):
        Hub(
            name="Hub1",
            zone=ZoneType.UNDEF_ARG,
            coordinate=(0, 0),
        )


def test_incorrect_hubtype() -> None:
    from model import Hub, HubType, ZoneType

    for hub_type in (
        "undefined",
        None,
    ):
        with pytest.raises(ValidationError):
            Hub(
                name="Hub1",
                coordinate=(0, 0),
                hub_type=hub_type
            )


def test_incorrect_coordinate() -> None:
    from model import Hub, HubType, ZoneType

    COORDINATES = (
        "aaa",
        "1000, 2000",
        "100, 200",
        (100, 200, 300),
        (),

    )
    for coordinate in COORDINATES:
        with pytest.raises(ValidationError):
            Hub(
                name="Hub1",
                coordinate=coordinate,
            )


def test_incorrect_name() -> None:
    from model import Hub, HubType, ZoneType

    NAMES = [
        32482094,
        None,
        123.43,
        "",
        "aaaa aaaa",
        "aaaa-aaaa",
        "       ",
        "aaa-aaa",
        "aaa aaa",
    ]
    for name in NAMES:
        with pytest.raises(ValidationError):
            Hub(
                name=name,
                coordinate=(0, 0),
            )


def test_incorrect_color() -> None:
    from model import Hub, HubType, ZoneType

    COLORS = [
        4932,
        123.43,
        "]",
        "]]]",
        "red=",
        "red ",
        "[",
        "[=]"
        "aaa=aaaaa"
    ]
    for color in COLORS:
        with pytest.raises(ValidationError):
            Hub(
                name="Hub1",
                coordinate=(0, 0),
                color=color
            )


def test_other_attributes() -> None:
    from model import Hub, HubType, ZoneType

    with pytest.raises(ValidationError):
        Hub(
            name="Hub1",
            zone=ZoneType.NORMAL,
            color="white",
            coordinate=(0, 0),
            max_drones=0,
            hub_type=HubType.START
        )

    with pytest.raises(ValidationError):
        Hub(
            name="Hub1",
            zone=ZoneType.BLOCKED,
            color="white",
            coordinate=(0, 0),
            max_drones=0,
            hub_type=HubType.START
        )
