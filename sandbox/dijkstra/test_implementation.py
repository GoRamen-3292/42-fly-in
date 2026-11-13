import heapq
from dataclasses import dataclass

from src.model import Connection, Hub
from src.model.types import HubType, ZoneType


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


def get_shortest_path(
    hubs_arg: list[Hub], connections_arg: list[Connection]
) -> tuple[list[str] | None, int | None]:
    hubs: dict[str, SolverHub] = convert_hubs(hubs_arg, connections_arg)

    queue: list[tuple[int, str]] = []
    for name, hub in hubs.items():
        if hub.hub_type == HubType.START_HUB:
            hub.min_cost = 0
            queue.append((0, name))

    if not queue:
        raise IndexError("No Start Hub found.")
    while queue:
        _, current_name = heapq.heappop(queue)  # TODO: heapqの意義について調べる
        current_hub = hubs[current_name]
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
            next_node = hubs[next_name]
            prev_min_cost = next_node.min_cost
            if current_hub.min_cost is None:
                raise Exception(
                    "min_cost is unset." + "Did you set when you push to the queue?"
                )
            new_min_cost = next_node.cost + current_hub.min_cost
            if prev_min_cost is None or new_min_cost < prev_min_cost:
                next_node.min_cost = new_min_cost
                next_node.shortest_path = path
                heapq.heappush(queue, (new_min_cost, next_name))
                print(f"Pushed {next_node.name}", vars(next_node), sep="\n")

            # コストの比較をする

    return (None, None)


def convert_hubs(
    hubs: list[Hub], connections: list[Connection]
) -> dict[str, SolverHub]:
    result: dict[str, SolverHub] = {}
    for hub in hubs:
        result[hub.name] = SolverHub(
            name=hub.name, connections=set(), zone=hub.zone, hub_type=hub.hub_type
        )
    for connection in connections:
        hub_1, hub_2 = connection.hubs
        result[hub_1].connections.add(hub_2)
        result[hub_2].connections.add(hub_1)
    return result


result = get_shortest_path(
    [
        Hub(
            hub_type=HubType.START_HUB,
            name="start",
            coordinate=(0, 0),
        ),
        Hub(
            name="h4",
            coordinate=(0, 1),
        ),
        Hub(name="h2", coordinate=(1, 0)),
        Hub(name="h3", coordinate=(1, 1)),
        Hub(name="goal", hub_type=HubType.END_HUB, coordinate=(1, 2)),
    ],
    [
        Connection(hubs=("start", "h4"), max_link_capacity=1),
        Connection(hubs=("start", "h2"), max_link_capacity=1),
        Connection(hubs=("h4", "goal"), max_link_capacity=1),
        Connection(hubs=("h2", "h3"), max_link_capacity=1),
        Connection(hubs=("h3", "goal"), max_link_capacity=1),
    ],
)

print(result)
