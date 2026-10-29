import pytest
from pydantic import ValidationError
from src.model import SimulationConfig
from src.parser import FileParser


parser = FileParser()


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
    config = SimulationConfig.model_construct(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    with pytest.raises(ValueError):
        parser.parse_line(line, config)


@pytest.mark.parametrize("line", [
    "hub: invalid_drones 10 20 [max_drones=-1000 color=red]",
    "hub: invalid_drones 10 20 [max_drones=0 color=red]",
    "hub: invalid_drones 10.32 20.19 [max_drones=0 color=red]",
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
])
def test_parse_line_with_options(line: str) -> None:
    config = SimulationConfig.model_construct(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    with pytest.raises(ValueError):
        parser.parse_line(line, config)


def test_multiple_start_hubs() -> None:
    config = SimulationConfig.model_construct(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    parser.parse_line("start_hub: start1 10 20", config)
    parser.parse_line("start_hub: start2 30 40", config)
    assert len(config.hubs) == 2
    with pytest.raises(ValidationError):
        SimulationConfig.model_validate(config)


def test_multiple_end_hubs() -> None:
    config = SimulationConfig.model_construct(
        nb_drones=10,
        hubs=[],
        connections=[],
    )

    # a
    parser.parse_line("end_hub: start1 10 20", config)
    parser.parse_line("end_hub: start2 30 40", config)
    with pytest.raises(ValidationError):
        SimulationConfig.model_validate(config)
