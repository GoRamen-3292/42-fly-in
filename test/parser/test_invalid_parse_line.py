import pytest

from fly_in.model import InvalidConfigError, SimulationConfig
from fly_in.parser import FileParser

parser = FileParser()


@pytest.mark.parametrize(
    "line",
    [
        "nb-drones: 10",
        "nb_drones: 0",
        "nb_drones: 1.3",
        "nb_drones: 4.2",
        "nb_drones: ",
        "nb_drones: -1.2",
        "nb_drones: -6.2",
        "nb: -6.2",
        "hub:",
        "start-hub:",
        "start_hub:",
        "end-hub:",
        "end_hub:",
        "hub:       ",
        "hub hub1 10 20",
        "hub: hub1 １０ ２０",
        "hub:hub1 10.0 ２０ ",
        ":hub hub1 10 20",
        "::hub1 10 20",
        "     hub :: hub1 10 20",
        "     hub:      hub1 2 10\t20",
        "hub:hub1 1 0 20",
        "hub:      hub1 1 0 20",
        "hub hub1 10 20:     ",
        "hub: hub1 10 20 fasf   ",
        "hub: hub1 asfd 20  ",
        "hub :hub1  1 0    2 0 3 3 43",
    ],
)
def test_parse_line(line: str) -> None:
    config = SimulationConfig.model_construct(
        nb_drones=None,
        hubs=[],
        connections=[],
    )
    with pytest.raises(InvalidConfigError, match="at line 42:"):
        parser.parse_line(line, config, 42)


@pytest.mark.parametrize(
    "line",
    [
        "hub: invalid_drones 10 20 [max_drones=-1000 color=red]",
        "hub: invalid_drones 10 20 [max_drones=0 color=red]",
        "hub: invalid_drones 10.32 20.19 [max_drones=0 color=red]",
        "hub: duplicate_options 10 20 [max_drones=10 max_drones=6]",
        "hub: duplicate_options 10 20 [max_drones=1 max_drones=6]",
        "hub: invalid_zone 10 20 [zone=adjdasjfa]",
        "hub: invalid_zone 10 20 [zone=]",
        "hub: unclosed_equal 10 20 [zone= max_drones=5 color=red]",
        " hub   :  double_equals  10\t 20 [    zone=priority=x   max_drones=5    color=red   ]   ",
        " hub   :  double_equals  10\t 20 [    ==x   max_drones=5    color=red   ]   ",
        " hub   :  value_only  10\t 20 [    =x   max_drones=5    color=red   ]   ",
        "hub   :   unclosed_metadata   10\t 20 [    zone=priority   max_drones=5    color=red      ",
        "   hub   : unstarted_metadata  hub1   10\t 20     zone=priority   max_drones=5    color=red ]     ",
        "hub   : empty_metadata_with_additional_arguments     10\t 20   []  zone=priority   max_drones=5    color=red ]     ",
        "hub:   too_many_brackets   10\t 20   [[[[  zone=priority   max_drones=5    color=red ]]]]     ",
        "hub:   too_many_brackets   10\t 20   [zone=p[rio]rity   max_drones=5    color=red ]]]]     ",
        "hub:   too_many_brackets   10\t 20   [color=p[rio]rity   max_drones=5    ]]]]     ",
        "hub:   too_many_brackets   10\t 20   [max_drones=2   max_drones=5    ]]]]     ",
        "hub:   too_many_brackets   10\t 20   [color=fasdf[adfa]   max_drones=5    ]]]]     ",
        "hub:   too_many_brackets   10\t 20   [color=fasdf[adfa]   max_drones=5    ]]     ",
        "hub:   too_many_args   10 20   [color=fasdf[adfa]   max_drones=5  test=non_existent  ]     ",
        "hub:   too_many_args   10 20   [color=fasdf[adfa] ==  max_drones=5  test=non_existent  ]     ",
        "hub:   double_args   10 20   [color=fasdf[adfa]  color=color  test=non_existent  ]     ",
        "hub    ::  two_columns  10 20 [    zone=priority   max_drones=5    color=red   ]   ",
        "hub    ::  two_columns  10 [    zone=priority   max_drones=5    color=red   ]   ",
    ],
)
def test_parse_line_with_options(line: str) -> None:
    config = SimulationConfig.model_construct(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    with pytest.raises(InvalidConfigError, match="at line 42:"):
        parser.parse_line(line, config, 42)
