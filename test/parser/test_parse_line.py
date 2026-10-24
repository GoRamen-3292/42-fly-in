from src.model import SimulationConfig
from src.parser.read_line import parse_line
from src.model import Hub, HubType, ZoneType


def test_parse_line() -> None:
    config = SimulationConfig(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    for line in [
        "hub: hub1 10 20",
        "     hub     : hub1 10 20",
        "     hub     : hub1 10\t20",
        "hub: hub1 10 20     ",
        "hub :hub1  10    20",
    ]:
        parse_line(line, config)
        assert len(config.hubs) == 1
        assert config.hubs[0].name == "hub1"
        assert config.hubs[0].coordinate == (10, 20)
        assert config.hubs[0].hub_type == HubType.NORMAL_HUB
        assert config.hubs[0].zone == ZoneType.NORMAL
        config.hubs.clear()


def test_parse_line_with_options() -> None:
    config = SimulationConfig(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    for line in [
        "hub: hub1 10 20 [zone=priority max_drones=5 color=red]",
        "    hub: hub1   10\t 20 [    zone=priority   max_drones=5    color=red   ]   ",
        "   hub   :   hub1   10\t 20 [    zone=priority   max_drones=5    color=red   ]   ",

    ]:
        parse_line(line, config)
        assert len(config.hubs) == 1
        assert config.hubs[0].name == "hub1"
        assert config.hubs[0].coordinate == (10, 20)
        assert config.hubs[0].hub_type == HubType.NORMAL_HUB
        assert config.hubs[0].zone == ZoneType.PRIORITY
        config.hubs.clear()
    # parse_line(
    #     , config)
