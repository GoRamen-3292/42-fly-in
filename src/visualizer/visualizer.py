from src.solver.types import ConnectionKey, PlanConnectionElement, PlanElement, SimulationResult
from collections import defaultdict


class Visualizer:
    @staticmethod
    def show_result(result: SimulationResult) -> None:
        output_dict: defaultdict[int, list[str]] = defaultdict(list)
        for drone in result.drones:
            for i, el in enumerate(drone.timeline):
                pos: str | ConnectionKey = el[1]
                if isinstance(pos, str):
                    pos_str = pos
                else:
                    pos_str = "-".join(pos)
                output_dict[i].append(
                    f"D{drone.id}-{pos_str}")

        sorted_keys = sorted(output_dict.keys())
        for key in sorted_keys:
            print(" ".join(output_dict[key]))
