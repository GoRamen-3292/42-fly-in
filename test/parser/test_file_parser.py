import pytest
from pydantic import ValidationError

from src.model import SimulationConfig
from src.parser import FileParser

parser = FileParser()


@pytest.mark.parametrize(
    "lines",
    [
        [
            "start_hub: start1 10 20",
            "start_hub: start2 30 40",
        ],
        [
            "end_hub: end1 10 20",
            "end_hub: end2 30 40",
        ],
    ],
)
def test_multiple_start_end_hubs(lines: list[str]) -> None:
    config = SimulationConfig.model_construct(
        nb_drones=10,
        hubs=[],
        connections=[],
    )
    for line in lines:
        parser.parse_line(line, config, 42)
    assert len(config.hubs) == 2
    with pytest.raises(ValidationError):
        SimulationConfig.model_validate(config)
