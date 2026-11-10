from src.solver.types import ConnectionKey, Drone, PlanConnectionElement, PlanElement, SimulationResult
from collections import defaultdict


class Visualizer:
    @classmethod
    def show_result(cls, result: SimulationResult) -> None:
        output_dict: defaultdict[int, list[str]] = defaultdict(list)
        for drone in result.drones:
            for i, el in enumerate(drone.timeline):
                pos: str | ConnectionKey = el[1]
                pos_str = el[1] if isinstance(pos, str) else "-".join(pos)
                dpos_str = f"D{drone.id}-{pos_str}"
                if dpos_str in output_dict.get(i - 1, []):
                    continue
                output_dict[i].append(dpos_str)

        sorted_keys = sorted(output_dict.keys())
        for i, key in enumerate(sorted_keys):
            if i == 0:
                continue
            print(" ".join(output_dict[key]))
