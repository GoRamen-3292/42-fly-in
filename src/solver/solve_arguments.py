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

        self._scheduler: dict[PlanElement, int] = {}
        """
        ドローンがどのターンにどの位置にいるのかを記録する辞書型

        キーはPlanElement型で、値はドローンの数
        """

    def get_result(self) -> SimulationResult:
        """シミュレーションの結果を取得するメソッド"""
        if self._result is None:
            raise RuntimeError("シミュレーションがまだ実行されていません。")
        return self._result

    def simulate(self) -> SimulationResult:
        """シミュレーションを実行するメソッド"""
        if self._result is not None:
            raise RuntimeError("シミュレーションはすでに実行されています。")
        self._plan()
        raise NotImplementedError(
            "visualizeの実装はまだ行われていません。")

    def _plan(self):
        for drone in self._drones:
            path = self.get_shortest_path(drone.position)
            if not path:
                raise Exception("合理的な手数の範囲内で経路が見つかりません")
            for el in path:
                self._scheduler[el] = self._scheduler.get(el, 0) + 1
            print("===", self._scheduler, sep="\n")

    def is_full_hub(self, plan: PlanElement) -> bool:
        """指定されたハブが満杯かどうかを判定するメソッド"""
        hub = self._hubs.get(plan[1])
        if not hub:
            raise Exception("Cannot find hub")
        elif hub.hub_type in (HubType.START_HUB, HubType.END_HUB):
            return False

        cur_hubs: int | None = self._scheduler.get(plan, None)
        return cur_hubs >= hub.max_drones if cur_hubs else False

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
        if self.is_full_hub(new_el):
            return  # ドローンがいるハブはスキップする
        elif new_turns > self._max_turns:
            return  # 最大ターン数を超えた場合は最短経路ではないのでスキップする
        elif new_el not in parent:
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
