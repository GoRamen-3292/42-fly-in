import pytest
from src.model import Hub, HubType, ZoneType
from typing import Any
from pydantic import ValidationError


@pytest.mark.parametrize("zone", [
    "undefined",
    None,
])
def test_incorrect_zonetype(zone: Any) -> None:
    with pytest.raises(ValidationError):
        Hub(
            name="Hub1",
            zone=zone,
            coordinate=(0, 0),
        )


@pytest.mark.parametrize("hub_type", [
    "undefined",
    None,
])
def test_incorrect_hubtype(hub_type: Any) -> None:
    with pytest.raises(ValidationError):
        Hub(
            name="Hub1",
            coordinate=(0, 0),
            hub_type=hub_type,
        )


@pytest.mark.parametrize("coordinate", [
    "aaa",
    "1000, 2000",
    "100, 200",
    (100, 200, 300),
    (),
])
def test_incorrect_coordinate(coordinate: Any) -> None:
    with pytest.raises(ValidationError):
        Hub(
            name="Hub1",
            coordinate=coordinate,
        )


@pytest.mark.parametrize("name", [
    32482094,
    None,
    123.43,
    "",
    "aaaa aaaa",
    "aaaa-aaaa",
    "       ",
    "aaa-aaa",
    "aaa aaa",
])
def test_incorrect_name(name: str) -> None:
    with pytest.raises(ValidationError):
        Hub(
            name=name,
            coordinate=(0, 0),
        )


@pytest.mark.parametrize("color", [
    4932,
    123.43,
    "red=",
    "red ",
    "[=]"
    "aaa=aaaaa"
])
def test_incorrect_color(color: Any) -> None:
    with pytest.raises(ValidationError):
        Hub(
            name="Hub1",
            coordinate=(0, 0),
            color=color,
        )


def test_other_attributes() -> None:
    with pytest.raises(ValidationError):
        Hub(
            name="Hub1",
            zone=ZoneType.NORMAL,
            color="white",
            coordinate=(0, 0),
            max_drones=0,
            hub_type=HubType.START_HUB
        )

    with pytest.raises(ValidationError):
        Hub(
            name="Hub1",
            zone=ZoneType.BLOCKED,
            color="white",
            coordinate=(0, 0),
            max_drones=0,
            hub_type=HubType.START_HUB
        )
