from dataclasses import dataclass
from src.model.types import HubType, ZoneType
import heapq


@dataclass
class SolverHub:
    name: str
    connections: set[str]
    seen: bool = False
    shortest_path: list[str] | None = None
    min_cost: int | None = None
    cost: int = 1
    zone: ZoneType = ZoneType.NORMAL
    hub_type: HubType = HubType.NORMAL_HUB


def search_hub(name: str, queue: list[SolverHub]) -> SolverHub:
    return next(
        (node for node in queue if node.name == name)
    )


def get_shortest_path() -> tuple[list[str] | None, int | None]:
    hubs: list[SolverHub] = [
        SolverHub(
            hub_type=HubType.START_HUB,
            name="start",
            connections={"h2", "h4"},
        ),
        SolverHub(
            name="h4",
            connections={"start", "goal"},
        ),
        SolverHub(
            name="h2",
            connections={"start", "h3"},
        ),
        SolverHub(
            name="h3",
            connections={"h2", "goal"}
        ),
        SolverHub(
            name="goal",
            connections={"h4", "h3"},
            hub_type=HubType.END_HUB,
        ),
    ]
    queue: list[tuple[int, str]] = []
    for hub in hubs:
        if hub.hub_type == HubType.START_HUB:
            hub.min_cost = 0
            queue.append((0, hub.name))

    if not queue:
        raise IndexError("No Start Hub found.")
    while queue:
        _, current_name = heapq.heappop(queue)  # TODO: heapqの意義について調べる
        current_hub = search_hub(current_name, hubs)
        # 来訪済みなら、return
        if current_hub.seen:
            continue
        # 探索済みにする
        current_hub.seen = True

        # 最短経路の置き換え
        if current_hub.shortest_path is None:
            path = [current_hub.name]
        else:
            path = current_hub.shortest_path + [current_hub.name]

        # ゴール到達
        if current_hub.hub_type == HubType.END_HUB:
            return (path, current_hub.min_cost)

        # すべての接続に対して...
        for next_name in current_hub.connections:
            next_node = search_hub(next_name, hubs)
            prev_min_cost = next_node.min_cost
            if current_hub.min_cost is None:
                raise Exception(
                    "min_cost is unset. Did you set when you push to the queue?")
            new_min_cost = next_node.cost + current_hub.min_cost
            if prev_min_cost is None or new_min_cost < prev_min_cost:
                next_node.min_cost = new_min_cost
                next_node.shortest_path = path
                heapq.heappush(queue, (new_min_cost, next_name))
                print(f"Pushed {next_node.name}", vars(next_node), sep="\n")

            # コストの比較をする

    return (None, None)


print(get_shortest_path())
