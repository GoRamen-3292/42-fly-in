"""ドローンの経路を計画するシミュレーションを定義するモジュール"""

import heapq
from typing import cast

from ..model import (
    Connection,
    Hub,
    HubType,
    SimulationConfig,
    ZoneType,
    normalize_connction_key,
)
from .types import (
    Drone,
    ParentMap,
    PlanConnectionElement,
    PlanElement,
    RouteNotFoundError,
    SimulationResult,
    SolverHub,
)


class Simulator:
    """与えられた設定から、ドローンの経路を計画するシミュレーションを提供するクラス

    ドローンを1台ずつ順番にダイクストラ法を用いて最短経路で計画し、
    各ターンにおけるハブと接続の
    使用状況を記録することで、後続のドローンが容量の制約を守れるようにする
    """

    def __init__(self, config: SimulationConfig) -> None:
        """シミュレーションを初期化するコンストラクタ

        Args:
            config: 検証済みのシミュレーションの設定

        Raises:
            RouteNotFoundError: 設定に開始ハブが存在しない場合
        """
        self._config = config
        self._result: SimulationResult | None = None
        self._drones: list[Drone] = []
        self._hubs: dict[str, SolverHub] = self.convert_hubs(
            config.hubs, config.connections
        )
        self._connections: list[Connection] = self.convert_connections(
            config.connections
        )

        self._max_turns = (len(self._hubs) - 1) * 2 + config.nb_drones - 1
        """最大ターンの設定

        直線上のハブで、すべてがrestrictedで
        一度に1台しか通れない場合の手数が考えうる最大ターン数
        """

        start_hub: SolverHub | None = next(
            (
                hub
                for hub in self._hubs.values()
                if hub.hub_type == HubType.START_HUB
            ),
            None,
        )
        if start_hub is None:
            raise RouteNotFoundError(
                "Cannot find a start hub in the configuration."
            )

        self._drones = [
            Drone(id=i + 1, start_pos=start_hub.name)
            for i in range(config.nb_drones)
        ]

        self._scheduler: dict[PlanElement, int] = {}
        self._connection_scheduler: dict[PlanConnectionElement, int] = {}
        """
        ドローンがどのターンにどの位置にいるのかを記録する辞書型

        キーはPlanElement型で、値はドローンの数
        """

    def get_result(self) -> SimulationResult | None:
        """シミュレーションの結果を取得するメソッド"""
        return self._result

    def simulate(self) -> SimulationResult:
        """シミュレーションを実行するメソッド

        Raises:
            RouteNotFoundError: 経路が見つからなかった場合に発生
            ValueError: 入力のconfigが不正な場合に発生
        Returns:
            SimulationResult: シミュレーションの結果
        """
        self._plan()
        self._result = SimulationResult(
            is_successful=True,
            drones=self._drones,
        )
        return self._result

    def _plan(self) -> None:
        # TODO: _plan_one_drone() 関数を作る
        for drone in self._drones:
            path: list[PlanElement | PlanConnectionElement] | None = (
                self.get_shortest_path(drone.start_pos)
            )
            if not path:
                raise RouteNotFoundError(
                    f"Cannot find a valid path for drone with ID: {drone.id}"
                )
            prev_hub: str = drone.start_pos
            for el in path:
                drone.timeline.append(el)
                if isinstance(el[1], str):
                    p_el: PlanElement = el[0], el[1]
                    self._scheduler[p_el] = self._scheduler.get(p_el, 0) + 1
                    pc_el: PlanConnectionElement = (
                        el[0],
                        normalize_connction_key((prev_hub, el[1])),
                    )
                    self._connection_scheduler[pc_el] = (
                        self._connection_scheduler.get(pc_el, 0) + 1
                    )
                    prev_hub = el[1]
                else:
                    pc_el = (el[0], normalize_connction_key(el[1]))
                    self._connection_scheduler[pc_el] = (
                        self._connection_scheduler.get(pc_el, 0) + 1
                    )
                    prev_hub = el[1][1]

    def _is_full_connection(self, plan: PlanConnectionElement) -> bool:
        plan = plan[0], normalize_connction_key(plan[1])
        connection: Connection = next(
            el for el in self._connections if el.hubs == plan[1]
        )
        max_con = connection.max_link_capacity
        cur_drones = self._connection_scheduler.get(plan, 0)
        return cur_drones >= max_con

    def _is_full_hub(self, plan: PlanElement) -> bool:
        """指定されたハブが満杯かどうかを判定するメソッド"""
        hub_name: str = plan[1]
        hub: SolverHub | None = self._hubs.get(hub_name)
        if not hub:
            raise ValueError(f"Cannot find hub with name: {hub_name}")
        if hub.hub_type in {HubType.START_HUB, HubType.END_HUB}:
            return False

        cur_drones: int = self._scheduler.get(plan, 0)
        return cur_drones >= hub.max_drones

    @staticmethod
    def trace_back_path(
        parent: ParentMap, end_hub: PlanElement
    ) -> list[PlanElement | PlanConnectionElement]:
        """最短経路を復元するメソッド"""
        current_hub: PlanElement | PlanConnectionElement | None = end_hub
        path: list[PlanElement | PlanConnectionElement] = []
        while current_hub is not None:
            path.append(current_hub)
            current_hub = parent[current_hub]
        path.reverse()
        return path

    def heappush_next_hubs(
        self,
        queue: list[PlanElement],
        current: PlanElement,
        next_name: str,
        parent: ParentMap,
    ) -> None:
        """次のハブをヒープに追加するメソッド"""
        new_turns = current[0] + 1

        next_hub = self._hubs[next_name]
        prev_turns, prev_hub = current

        conn_turn: PlanConnectionElement | None = None
        if next_hub.zone != ZoneType.RESTRICTED or prev_hub == next_hub.name:
            new_turns = prev_turns + 1
        else:
            new_turns = prev_turns + 2

        if prev_hub != next_hub.name:
            conn_turn = (prev_turns + 1, (prev_hub, next_name))
            if self._is_full_connection(conn_turn):
                return  # Connectionはいっぱいである
        new_el: PlanElement = (new_turns, next_name)

        if self._is_full_hub(new_el):
            return  # ドローンがいるハブはスキップする
        if new_turns > self._max_turns:
            # 最大ターン数を超えた場合は最短経路ではないのでスキップする
            return
        if new_el in parent:
            return

        if next_hub.zone == ZoneType.RESTRICTED and prev_hub != next_hub.name:
            conn_turn = cast(PlanConnectionElement, conn_turn)
            parent[conn_turn] = current
            parent[new_el] = conn_turn
        else:
            parent[new_el] = current
        heapq.heappush(queue, new_el)

    def get_shortest_path(
        self, start_hub: str
    ) -> list[PlanElement | PlanConnectionElement] | None:
        """開始ハブから終了ハブまでの最短経路を探索するメソッド

        ターン数をコストとし、計画済みのドローンによるハブと接続の
        使用状況を考慮しながら、その場での待機も含めて経路を探索する

        Args:
            start_hub: 探索を開始するハブの名前

        Returns:
            開始位置を先頭とし、ターンごとの位置を時系列に並べたリスト、
            経路が見つからない場合はNone

        Raises:
            ValueError: start_hubが存在しないハブの名前である場合
        """
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
            current_turns, current_pos = current
            current_hub: SolverHub = self._hubs[current_pos]
            # 来訪済みなら、return
            if current in visited:
                continue
            # 探索済みにする
            visited.add(current)

            # ゴール到達
            if current_hub.hub_type == HubType.END_HUB:
                return self.trace_back_path(
                    parent, (current_turns, current_pos)
                )

            # そのまま待機する場合も探索の候補に追加
            values = [(queue, current, current_pos, parent)]

            # すべての接続に対して...
            for next_name in current_hub.connections:
                next_node: SolverHub = self._hubs[next_name]
                if next_node.zone == ZoneType.BLOCKED:
                    continue  # 制限区域のハブはスキップする
                values.append((queue, current, next_name, parent))

            # 優先度の高いハブを先に探索する
            values = sorted(
                values,
                key=lambda x: self._hubs[x[2]].zone is ZoneType.PRIORITY,
                reverse=True,
            )
            for queue, current, next_name, parent in values:
                self.heappush_next_hubs(queue, current, next_name, parent)

        return None

    @staticmethod
    def convert_hubs(
        hubs: list[Hub], connections: list[Connection]
    ) -> dict[str, SolverHub]:
        """HubのリストをSimulation内で利用するSolverHubに変換するメソッド

        接続の情報をもとに、各ハブに隣接するハブの名前を設定する

        Returns:
            ハブ名をキーとするSolverHubの辞書
        """
        result: dict[str, SolverHub] = {}
        for hub in hubs:
            result[hub.name] = SolverHub(
                name=hub.name,
                connections=set(),
                zone=hub.zone,
                hub_type=hub.hub_type,
                max_drones=hub.max_drones,
            )
        for connection in connections:
            hub_1, hub_2 = connection.hubs
            result[hub_1].connections.add(hub_2)
            result[hub_2].connections.add(hub_1)
        return result

    @staticmethod
    def convert_connections(
        connections: list[Connection]
    ) -> list[Connection]:
        """接続のキーを正規化したConnectionのリストを作成するメソッド

        経路の計画に不要な行番号などの情報は取り除かれる
        """
        return [
            Connection.model_validate(
                obj={
                    "hubs": normalize_connction_key(conn.hubs),
                    "max_link_capacity": conn.max_link_capacity,
                }
            )
            for conn in connections
        ]
