import pytest
from src.visualizer import Visualizer
from src.solver.types import Drone, PlanElement, PlanConnectionElement, SimulationResult


@pytest.mark.parametrize("data", [
    SimulationResult(
        is_successful=True,
        drones=[
            Drone(
                id=0,
                start_pos="start",
                timeline=[
                    (0, "start"),
                    (0, ("start", "end")),
                    (1, "end")
                ]
            )
        ]
    )
])
def test_visualizer(data: SimulationResult) -> None:
    Visualizer.show_result(data)


@pytest.mark.parametrize("timeline", [
    [
        (0, "start"),
        (0, ("start", "end")),
        (1, "end")
    ],
    [
        (0, "start"),
        (0, ("start", "end")),
        (1, "end"),
        (1, ("end", "start")),
        (2, "start")]
])
def test_visualizer_timeline(timeline: list[PlanElement | PlanConnectionElement]) -> None:
    result = SimulationResult(
        is_successful=True,
        drones=[
            Drone(
                id=0,
                start_pos="start",
                timeline=timeline
            )
        ]
    )
    Visualizer.show_result(result)
