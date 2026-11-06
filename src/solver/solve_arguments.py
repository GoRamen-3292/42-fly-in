from src.model import Connection, Hub, HubType, SimulationConfig
from src.model.types import ZoneType
from .types import Drone, PlanElement, ParentMap, SolverHub, SimulationResult
import heapq


class Simulation:
    def __init__(self, config: SimulationConfig):
        self._config = config
        self._connections: list[Connection] = config.connections
        self._result: SimulationResult | None = None
        self._drones: list[Drone] = []
        self._hubs: dict[str, SolverHub] = self.convert_hubs(
            config.hubs, config.connections)

        # 最大ターンの設定
        # どれだけかかっても、すべてのハブの数 + ドローンの数の2倍以内で終わるはず
        # 理由は、すべてのハブが同じ経路ですべてrestrictedだった場合であるため
        # TODO: この場合についてのテストケースを作る
        self._max_turns = (len(self._hubs) + config.nb_drones) * 2

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
        return path[1][1] if path and len(path) > 1 else cur_hub.name

    def is_full_hub(self, hub_name: str) -> bool:
        """指定されたハブが満杯かどうかを判定するメソッド"""
        hub = self._hubs.get(hub_name)
        if hub and hub.hub_type == HubType.END_HUB:
            return False

        return any(drone.position == hub_name for drone in self._drones)

    def trace_back_path(self, parent: ParentMap,
                        end_hub: PlanElement) -> list[PlanElement]:
        """最短経路を復元するメソッド"""
        current_hub: PlanElement | None = end_hub
        path: list[PlanElement] = []
        while current_hub is not None:
            path.append(current_hub)
            current_hub = parent[current_hub]
        path.reverse()
        return path

    def heappush_next_hubs(self, queue: list[PlanElement],
                           current: PlanElement, next_name: str,
                           parent: ParentMap) -> None:
        """次のハブをヒープに追加するメソッド"""

        # TODO: ここのコストを1以外にHubTypeに応じて分岐する
        new_turns = current[0] + 1

        new_el = (new_turns, next_name)
        if new_el not in parent:
            if new_turns > self._max_turns:
                # 最大ターン数を超えた場合は最短経路ではないのでスキップする
                return
            heapq.heappush(queue, new_el)
            parent[new_el] = current

    def get_shortest_path(
            self, start_hub: str) -> list[PlanElement] | None:
        if start_hub not in self._hubs:
            raise ValueError(f"Start hub '{start_hub}' not found in hubs.")

        queue: list[PlanElement] = [(0, start_hub)]
        """
        キューを用いて、次に探索するハブを管理する

        tuple型で、コストとハブ名を格納
        """

        visited: set[PlanElement] = set()
        """
        「来訪済み」のハブ、除外に利用
        """

        parent: ParentMap = {(0, start_hub): None}
        """
        直前のハブを記録する
        """

        while queue:
            current: PlanElement = heapq.heappop(queue)
            current_turns, current_name = current
            current_hub = self._hubs[current_name]
            # 来訪済みなら、return
            if current in visited:
                continue
            # 探索済みにする
            visited.add(current)

            # ゴール到達
            if current_hub.hub_type == HubType.END_HUB:
                return self.trace_back_path(
                    parent, (current_turns, current_name))

            # そのまま待機する場合も探索の候補に追加
            self.heappush_next_hubs(queue, current, current_name, parent)

            # すべての接続に対して...
            for next_name in current_hub.connections:
                if self.is_full_hub(next_name):
                    continue  # ドローンがいるハブはスキップする
                next_node: SolverHub = self._hubs[next_name]
                if next_node.zone == ZoneType.BLOCKED:
                    continue  # 制限区域のハブはスキップする
                self.heappush_next_hubs(queue, current, next_name, parent)

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
