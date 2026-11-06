from src.model import Connection, Hub, HubType, SimulationConfig
from src.model.types import ZoneType
from .model import Drone, SolverHub, SimulationResult
import heapq


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
        while not all(
            self._hubs[drone.position].hub_type == HubType.END_HUB
                for drone in self._drones):
            print(f"=== Turn {i} ===")
            self._simulate_next_turn()
            i += 1
            if i > 1000:
                # TODO: この処理を消去する
                raise RuntimeError(
                    "シミュレーションが終了しませんでした。"
                    "無限ループの可能性があります。")

        raise NotImplementedError(
            f"シミュレーションは{i}手で終了しました。"
            "visualizeの実装はまだ行われていません。")

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

    def _simulate_one_drone(self, drone: Drone) -> str:
        """1台のドローンのシミュレーションを実行するメソッド"""
        cur_hub = self._hubs[drone.position]

        path = self.get_shortest_path(cur_hub.name)
        print(
            f"## Drone {drone.id}",
            f"- Current Hub: {cur_hub.name}",
            f"- Shortest Path: {path}",
            sep="\n",
        )
        return path[1] if path and len(path) > 1 else cur_hub.name

    def is_full_hub(self, hub_name: str) -> bool:
        """指定されたハブが満杯かどうかを判定するメソッド"""
        hub = self._hubs.get(hub_name)
        if hub and hub.hub_type == HubType.END_HUB:
            return False

        return any(drone.position == hub_name for drone in self._drones)

    def trace_back_path(self, parent: dict[str, str | None],
                        end_hub: str) -> list[str]:
        """最短経路を復元するメソッド"""
        current_hub: str | None = end_hub
        path: list[str] = []
        while current_hub is not None:
            path.append(current_hub)
            current_hub = parent[current_hub]
        path.reverse()
        return path

    def get_shortest_path(
            self, start_hub: str) -> list[str] | None:
        if start_hub not in self._hubs:
            raise ValueError(f"Start hub '{start_hub}' not found in hubs.")

        queue: list[tuple[int, str]] = [(0, start_hub)]
        """
        キューを用いて、次に探索するハブを管理する

        tuple型で、コストとハブ名を格納
        """
        visited: set[str] = set()
        """
        「来訪済み」のハブ、除外に利用
        """
        min_cost: dict[str, int] = {start_hub: 0}
        """
        それぞれのハブごとにかかる最小のコストを記録する辞書
        """
        parent: dict[str, str | None] = {start_hub: None}
        """
        直前のハブを記録する
        """

        while queue:
            _, current_name = heapq.heappop(queue)  # TODO: heapqの意義について調べる
            current_hub = self._hubs[current_name]
            # 来訪済みなら、return
            if current_name in visited:
                continue
            # 探索済みにする
            visited.add(current_hub.name)

            # ゴール到達
            if current_hub.hub_type == HubType.END_HUB:
                return self.trace_back_path(parent, current_name)

            # すべての接続に対して...
            for next_name in current_hub.connections:
                if min_cost[current_name] is None:
                    raise Exception(
                        "min_cost is unset. "
                        "Did you set when you push to the queue?"
                    )
                elif self.is_full_hub(next_name):
                    continue  # ドローンがいるハブはスキップする
                next_node = self._hubs[next_name]
                if next_node.zone == ZoneType.BLOCKED:
                    continue  # 制限区域のハブはスキップする

                # コストを算出する
                # 見つからなかったらNone、つまり「無限大」にする
                prev_min_cost = min_cost[next_name] if next_name in min_cost else None
                # TODO: ここのコストを1以外にHubTypeに応じて分岐する
                new_min_cost = 1 + min_cost[current_name]
                if prev_min_cost is None or new_min_cost < prev_min_cost:
                    min_cost[next_name] = new_min_cost
                    heapq.heappush(queue, (new_min_cost, next_name))
                    parent[next_name] = current_name

                # コストの比較をする

        return None

    def convert_hubs(self, hubs: list[Hub],
                     connections: list[Connection]) -> dict[str, SolverHub]:
        result: dict[str, SolverHub] = {}
        for hub in hubs:
            result[hub.name] = (SolverHub(
                name=hub.name,
                connections=set(),
                zone=hub.zone,
                hub_type=hub.hub_type,
                max_drones=hub.max_drones,
            ))
        for connection in connections:
            hub_1, hub_2 = connection.hubs
            result[hub_1].connections.add(hub_2)
            result[hub_2].connections.add(hub_1)
        return result
