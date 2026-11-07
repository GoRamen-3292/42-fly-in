from src.solver.types import SimulationResult
from collections import defaultdict


class Visualizer:
    @staticmethod
    def show_result(result: SimulationResult) -> None:
        output_dict: defaultdict[int, list[str]] = defaultdict(list)
        for drone in result.drones:
            for i, el in enumerate(drone.timeline):
                output_dict[i].append(
                    f"D{drone.id}-{drone.timeline[i][1]}")

        sorted_keys = sorted(output_dict.keys())
        for key in sorted_keys:
            print(" ".join(output_dict[key]))
