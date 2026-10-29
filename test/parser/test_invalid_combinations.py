import pytest
from pydantic import ValidationError
from src.model import (Connection, Hub, HubType,
                       SimulationConfig, ZoneType)


def test_multiple_start_hubs() -> None:
    config = SimulationConfig.model_construct(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    config.hubs.append(Hub(
        name="start3",
        coordinate=(50, 60),
        hub_type=HubType.START_HUB,
        zone=ZoneType.NORMAL,
    ))
    config.hubs.append(Hub(
        name="start4",
        coordinate=(70, 80),
        hub_type=HubType.START_HUB,
        zone=ZoneType.NORMAL,
    ))
    with pytest.raises(ValidationError):
        SimulationConfig.model_validate(config.hubs)


def test_multiple_end_hubs() -> None:
    config = SimulationConfig.model_construct(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    config.hubs.append(Hub(
        name="end3",
        coordinate=(50, 60),
        hub_type=HubType.END_HUB,
        zone=ZoneType.NORMAL,
    ))
    config.hubs.append(Hub(
        name="end4",
        coordinate=(70, 80),
        hub_type=HubType.END_HUB,
        zone=ZoneType.NORMAL,
    ))


def test_duplicate_hub_names() -> None:
    config = SimulationConfig.model_construct(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    config.hubs.append(Hub(
        name="hub1",
        coordinate=(50, 60),
        hub_type=HubType.START_HUB,
        zone=ZoneType.NORMAL,
    ))
    config.hubs.append(Hub(
        name="hub1",
        coordinate=(70, 80),
        hub_type=HubType.END_HUB,
        zone=ZoneType.NORMAL,
    ))
    config.connections.append(Connection(
        hubs=("hub1", "hub2"),
        max_link_capacity=5,
    ))
    with pytest.raises(ValidationError):
        SimulationConfig.model_validate(config.hubs)


@pytest.mark.parametrize("hub_2_hubs", [
    ("hub1", "hub2"),
    ("hub2", "hub1"),
])
def test_duplicate_connections(hub_2_hubs: tuple[str, str]) -> None:
    config = SimulationConfig.model_construct(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    config.hubs.append(Hub(
        name="hub1",
        coordinate=(50, 60),
        hub_type=HubType.START_HUB,
        zone=ZoneType.NORMAL,
    ))
    config.hubs.append(Hub(
        name="hub2",
        coordinate=(70, 80),
        hub_type=HubType.END_HUB,
        zone=ZoneType.NORMAL,
    ))
    config.connections.append(Connection(
        hubs=("hub1", "hub2"),
        max_link_capacity=5,
    ))
    config.connections.append(Connection(
        hubs=hub_2_hubs,
        max_link_capacity=5,
    ))
    with pytest.raises(ValidationError):
        SimulationConfig.model_validate(config.connections)
