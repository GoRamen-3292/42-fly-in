from src.model import (Connection, Drone, Hub, HubType,
                       SimulationConfig, SimulationResult)
from src.model.types import ZoneType
from dataclasses import dataclass
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


class Simulation:
    def __init__(self, config: SimulationConfig):
        self._config = config
        self._connections: list[Connection] = config.connections
        self._result: SimulationResult | None = None
        self._drones: list[Drone] = []
        self._hubs: dict[str, SolverHub] = self.convert_hubs(
            config.hubs, config.connections)

        start_hub = next(
            (hub for hub in self._hubs.values()
             if hub.hub_type == HubType.START_HUB), None)
        if start_hub is None:
            raise ValueError("シミュレーションの開始ハブが見つかりません。")

        self._drones = [Drone(id=i, position=start_hub.name)
                        for i in range(config.nb_drones)]

    def get_result(self) -> SimulationResult:
        """シミュレーションの結果を取得するメソッド"""
        if self._result is None:
            raise RuntimeError("シミュレーションがまだ実行されていません。")
        return self._result

    def simulate(self) -> SimulationResult:
        """シミュレーションを実行するメソッド"""
        if self._result is not None:
            raise RuntimeError("シミュレーションはすでに実行されています。")
        i = 1
        while not all(self._hubs[drone.position].hub_type == HubType.END_HUB for drone in self._drones):
            print(f"=== Turn {i} ===")
            self._simulate_next_turn()
            i += 1
            # ここに出力処理を追加?

        raise NotImplementedError("シミュレーションの実装はまだ行われていません。")

    def _simulate_next_turn(self) -> None:
        """シミュレーションの次のターンを実行するメソッド"""
        next_candidates: dict[int, str] = {}
        for drone in self._drones:
            next_candidates[drone.id] = self._simulate_one_drone(drone)
        print()
        for drone in self._drones:
            id = drone.id
            next_hub = next_candidates[id]
            if self._hubs[next_hub].hub_type == HubType.END_HUB or \
                    all(drone.position != next_hub for drone in self._drones):
                drone.position = next_hub
                print(f"D{id}-{next_hub} ")
            else:
                print(f"Failed: D{id}-{next_hub}.")
                # ドローンが移動できない場合の処理を追加する
                # 例えば、ドローンが次のハブに移動できない場合の処理をここに追加する
                # 例: ドローンが次のハブに移動できない場合、現在の位置に留まるなど
                # drone.position = drone.position  # 現在の位置に留まる

    def _simulate_one_drone(self, drone: Drone) -> str:
        """1台のドローンのシミュレーションを実行するメソッド"""
        cur_hub = self._hubs[drone.position]

        path, distance = self.get_shortest_path(cur_hub.name)
        print(
            f"## Drone {drone.id}",
            f"- Current Hub: {cur_hub.name}",
            f"- Shortest Path: {path}",
            f"- Distance: {distance}",
            sep="\n",
        )
        return path[1] if path and len(path) > 1 else cur_hub.name

    def is_full_hub(self, hub_name: str) -> bool:
        """指定されたハブが満杯かどうかを判定するメソッド"""
        hub = self._hubs.get(hub_name)
        if hub and hub.hub_type == HubType.END_HUB:
            return False
        # if hub is None:
        #     raise ValueError(f"Hub '{hub_name}' not found.")
        return any(drone.position == hub_name for drone in self._drones)

    def get_shortest_path(self, start_hub: str) -> tuple[list[str] | None, int | None]:
        if start_hub not in self._hubs:
            raise ValueError(f"Start hub '{start_hub}' not found in hubs.")
        queue: list[tuple[int, str]] = [(0, start_hub)]
        for hub in self._hubs.values():
            hub.seen = False
            hub.shortest_path = None
            hub.min_cost = None
        self._hubs[start_hub].min_cost = 0

        if not queue:
            raise IndexError("No Start Hub found.")
        while queue:
            _, current_name = heapq.heappop(queue)  # TODO: heapqの意義について調べる
            current_hub = self._hubs[current_name]
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
                if self.is_full_hub(next_name):  # ドローンがいるハブはスキップする
                    continue  # ドローンがいるハブはスキップする
                next_node = self._hubs[next_name]
                prev_min_cost = next_node.min_cost
                if current_hub.min_cost is None:
                    raise Exception(
                        "min_cost is unset. Did you set when you push to the queue?")
                new_min_cost = next_node.cost + current_hub.min_cost
                if prev_min_cost is None or new_min_cost < prev_min_cost:
                    next_node.min_cost = new_min_cost
                    next_node.shortest_path = path
                    heapq.heappush(queue, (new_min_cost, next_name))
                    # print(f"Pushed {next_node.name}",
                    #       vars(next_node), sep="\n")

                # コストの比較をする

        return (None, None)

    def convert_hubs(self, hubs: list[Hub], connections: list[Connection]) -> dict[str, SolverHub]:
        result: dict[str, SolverHub] = {}
        for hub in hubs:
            result[hub.name] = (SolverHub(
                name=hub.name,
                connections=set(),
                zone=hub.zone,
                hub_type=hub.hub_type
            ))
        for connection in connections:
            hub_1, hub_2 = connection.hubs
            result[hub_1].connections.add(hub_2)
            result[hub_2].connections.add(hub_1)
        return result
