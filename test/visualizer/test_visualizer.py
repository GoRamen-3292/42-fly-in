import pytest

from fly_in.model.types import ConnectionKey
from fly_in.simulator.types import (
    Drone,
    SimulationResult,
)
from fly_in.visualizer import Visualizer


@pytest.mark.parametrize(
    "data",
    [
        SimulationResult(
            is_successful=True,
            drones=[
                Drone(
                    id=0,
                    start_pos="start",
                    timeline=["start", ("start", "end"), "end"],
                )
            ],
        )
    ],
)
def test_visualizer(data: SimulationResult) -> None:
    Visualizer(data).show_result()


@pytest.mark.parametrize(
    "timeline",
    [
        ["start", ("start", "end"), "end"],
        [
            "start",
            ("start", "end"),
            "end",
            ("end", "start"),
            "start",
        ],
    ],
)
def test_visualizer_timeline(
    timeline: list[str | ConnectionKey],
) -> None:
    result = SimulationResult(
        is_successful=True,
        drones=[Drone(id=0, start_pos="start", timeline=timeline)],
    )
    Visualizer(result).show_result()
