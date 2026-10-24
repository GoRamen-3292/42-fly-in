import pytest
from src.model import SimulationConfig
from src.parser.read_line import parse_line
from src.model import Hub, HubType, ZoneType


@pytest.mark.parametrize("line", [
    "hub hub1 10 20",
    "     hub :: hub1 10 20",
    "     hub     : hub1 10\t20",
    "hub hub1 10 20:     ",
    "hub :hub1  1 0    2 0 3 3 43",
])
def test_parse_line(line: str) -> None:
    config = SimulationConfig(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    with pytest.raises(ValueError):
        parse_line(line, config)


@pytest.mark.parametrize("line", [
    "unclosed_equal: hub1 10 20 [zone= max_drones=5 color=red]",
    "    double_equals: hub1   10\t 20 [    zone=priority=x   max_drones=5    color=red   ]   ",
    "    two_columns:: hub1   10\t 20 [    zone=priority=x   max_drones=5    color=red   ]   ",
    "unclosed_metadata   :   hub1   10\t 20 [    zone=priority   max_drones=5    color=red      ",
    "unstarted_metadata   hub   :   hub1   10\t 20     zone=priority   max_drones=5    color=red ]     ",
    "empty_metadata_with_additional_arguments   :   hub1   10\t 20   []  zone=priority   max_drones=5    color=red ]     ",
])
def test_parse_line_with_options(line: str) -> None:
    config = SimulationConfig(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    with pytest.raises(ValueError):
        parse_line(line, config)
