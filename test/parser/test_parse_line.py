import pytest
from src.model import SimulationConfig
from src.parser import FileParser
from src.model import HubType, ZoneType


parse_line = FileParser().parse_line


@pytest.mark.parametrize("line", [
    "hub: hub1 10 20",
    "     hub     : hub1 10 20",
    "     hub     : hub1 10\t20",
    "hub: hub1 10 20     ",
    "      hub   : hub1 10 20     ",
    "      hub   : hub1 10 20     ",
    "hub :hub1  10    20",
])
def test_parse_line_with_values(line: str) -> None:
    config = SimulationConfig.model_construct(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    parse_line(line, config)
    assert len(config.hubs) == 1
    assert config.hubs[0].name == "hub1"
    assert config.hubs[0].coordinate == (10, 20)
    assert config.hubs[0].hub_type == HubType.NORMAL_HUB
    assert config.hubs[0].zone == ZoneType.NORMAL


@pytest.mark.parametrize("line", [
    "hub: test=hub 10 20",
    "hub: test/hub 10 20 [zone=priority]",
    "start_hub: test_hub 10 20 [zone=priority]",
    "start_hub: test:hub 10 20 [zone=priority]",
    "start_hub: :::: 10 20 [zone=priority]",
    "end_hub: test_hub 10 20 [zone=priority]",
])
def test_parse_line(line: str) -> None:
    config = SimulationConfig.model_construct(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    parse_line(line, config)


@pytest.mark.parametrize("line", [
    "hub: hub1 10 20 [color=red zone=priority max_drones=5]",
    "hub: hub1 10 20 [zone=priority color=red max_drones=5]",
    "hub: hub1 10 20 [zone=priority max_drones=5 color=red]",
    "hub: hub1 10 20 [zone=priority max_drones=5 color=r:::::ed]",
    "hub: hub1 10 20 [zone=priority max_drones=5 color=r:::::ed:]",
    "    hub: hub1   10\t 20 [    zone=priority   max_drones=5    color=red   ]   ",
    "   hub   :   hub1   10\t 20 [    zone=priority   max_drones=5    color=red   ]   ",
    "   hub   :   hub1   10\t 20 [    zone=priority   max_drones=5    color=red]]   ",
])
def test_parse_line_with_options_with_values(line: str) -> None:
    config = SimulationConfig.model_construct(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    parse_line(line, config)
    assert len(config.hubs) == 1
    assert config.hubs[0].name == "hub1"
    assert config.hubs[0].coordinate == (10, 20)
    assert config.hubs[0].hub_type == HubType.NORMAL_HUB
    assert config.hubs[0].zone == ZoneType.PRIORITY


@pytest.mark.parametrize("line", [
    "hub: hub1 10 20 []",
    "hub: hub1 10 20 [color=or-ange]",
    "hub: hub1 10 20 [zone=normal]",
    "hub: hub1 10 20 [max_drones=6]",
    "hub: hub1 10 20 [color=or-ange zone=normal max_drones=5]",
    "hub: hub1 10 20 [zone=blocked color=red max_drones=1]",
    "hub: hub1 -100 -304 [zone=priority color=red max_drones=1]",
    "hub: hub1 10 20 [zone=priority max_drones=5 color=red]",
    "    hub: hub1   10\t 20 [    zone=restricted   max_drones=5    color=red   ]   ",
    "   hub   :   hub1   10\t 20 [    zone=blocked   max_drones=5    color=red   ]   ",
    "   hub   :   hub1   10\t 20 [    zone=normal   max_drones=5    color=red   ]   ",
])
def test_parse_line_with_options(line: str) -> None:
    config = SimulationConfig.model_construct(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    parse_line(line, config)
    assert len(config.hubs) == 1
