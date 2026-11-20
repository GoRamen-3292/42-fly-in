import pytest
from pydantic import ValidationError

from fly_in import InvalidConfigError, SimulationConfig
from fly_in.parser import FileParser, SimulationParserConfig

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
    config = SimulationParserConfig()
    for line in lines:
        parser.parse_line(line, config, 42)
    assert len(config.hubs) == 2
    with pytest.raises(ValidationError):
        SimulationConfig.model_validate(
            {
                "nb_drones": 10,
                "hubs": config.hubs,
                "connections": config.connections,
            }
        )


@pytest.mark.parametrize(
    "nb_drones",
    [
        "nb_drones: 0",
        "nb_drones: -1",
        "nb_drones: -10",
        "nb_drones: -4.2",
        "nb_drones: 1.5",
        "nb_drones: 0.9",
        "nb_drones: １",
    ],
)
def test_parse_line_with_invalid_nb_drones(nb_drones: str) -> None:
    config = SimulationParserConfig()
    parser.parse_line(nb_drones, config, 42)
    with pytest.raises(InvalidConfigError):
        parser.parse_text(
            "\n".join(
                [nb_drones, "start_hub: start1 10 20", "end_hub: end1 30 40"]
            )
        )
