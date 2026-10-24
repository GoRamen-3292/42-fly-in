import pytest
from src.model import SimulationConfig
from src.parser.read_line import parse_line
from src.model import Hub, HubType, ZoneType


@pytest.mark.parametrize("line", [
    "hub hub1 10 20",
    "     hub :: hub1 10 20",
    "     hub:      hub1 2 10\t20",
    "hub:      hub1 1 0 20",
    "hub:      hub1 1 0 20",
    "hub hub1 10 20:     ",
    "hub: hub1 10 20 fasf   ",
    "hub: hub1 asfd 20  ",
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
    "hub: invalid_drones 10 20 [max_drones=-1000 color=red]",
    "hub: invalid_drones 10 20 [max_drones=0 color=red]",
    "hub: invalid_drones 10.32 20.19 [max_drones=0 color=red]",
    "hub: unclosed_equal 10 20 [zone= max_drones=5 color=red]",
    " hub   :  double_equals  10\t 20 [    zone=priority=x   max_drones=5    color=red   ]   ",
    "hub    ::  two_columns  10\t 20 [    zone=priority=x   max_drones=5    color=red   ]   ",
    "hub   :   unclosed_metadata   10\t 20 [    zone=priority   max_drones=5    color=red      ",
    "   hub   : unstarted_metadata  hub1   10\t 20     zone=priority   max_drones=5    color=red ]     ",
    "hub   : empty_metadata_with_additional_arguments     10\t 20   []  zone=priority   max_drones=5    color=red ]     ",
    "hub:   too_many_brackets   10\t 20   [[[[  zone=priority   max_drones=5    color=red ]]]]     ",
    "hub:   too_many_brackets   10\t 20   [zone=p[rio]rity   max_drones=5    color=red ]]]]     ",
    "hub:   too_many_brackets   10\t 20   [color=p[rio]rity   max_drones=5    ]]]]     ",
    "hub:   too_many_brackets   10\t 20   [max_drones=2   max_drones=5    ]]]]     ",
    "hub:   too_many_brackets   10\t 20   [color=fasdf[adfa]   max_drones=5    ]]]]     ",
    "hub:   too_many_brackets   10\t 20   [color=fasdf[adfa]   max_drones=5    ]]     ",
])
def test_parse_line_with_options(line: str) -> None:
    config = SimulationConfig(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    with pytest.raises(ValueError):
        parse_line(line, config)
