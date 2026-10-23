import pytest
from src.model import Hub, HubType, ZoneType
from pydantic import ValidationError


def test_incorrect_zonetype() -> None:
    # 最低限の引数でHubを作成
    for zone in (
        "undefined",
        None,
    ):
        with pytest.raises(ValidationError):
            Hub(
                name="Hub1",
                zone=zone,  # type: ignore
                coordinate=(0, 0),
            )

    with pytest.raises(AttributeError):
        Hub(
            name="Hub1",
            zone=ZoneType.UNDEF_ARG,  # type: ignore
            coordinate=(0, 0),
        )


def test_incorrect_hubtype() -> None:
    for hub_type in (
        "undefined",
        None,
    ):
        with pytest.raises(ValidationError):
            Hub(
                name="Hub1",
                coordinate=(0, 0),
                hub_type=hub_type,  # type: ignore
            )


def test_incorrect_coordinate() -> None:
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
                coordinate=coordinate,  # type: ignore
            )


def test_incorrect_name() -> None:
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
                name=name,  # type: ignore
                coordinate=(0, 0),
            )


def test_incorrect_color() -> None:
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
                color=color,  # type: ignore
            )


def test_other_attributes() -> None:
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
