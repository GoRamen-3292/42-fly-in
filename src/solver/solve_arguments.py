from src.model import (Connection, Drone, Hub, HubType,
                       SimulationConfig, SimulationResult)


class Simulation:
    def __init__(self, config: SimulationConfig):
        self._config = config
        self._hubs: list[Hub] = config.hubs
        self._connections: list[Connection] = config.connections
        self._result: SimulationResult | None = None
        self._drones: list[Drone] = []

        start_hub = next(
            (hub for hub in self._hubs
             if hub.hub_type == HubType.START_HUB), None)
        if start_hub is None:
            raise ValueError("シミュレーションの開始ハブが見つかりません。")

        self._drones = [Drone(id=i, position=start_hub)
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
        self._simulate_next_turn()
        raise NotImplementedError("シミュレーションの実装はまだ行われていません。")

    def _simulate_next_turn(self) -> None:
        """シミュレーションの次のターンを実行するメソッド"""
        for drone in self._drones:
            # ドローンの移動ロジックを実装する
            self._simulate_one_drone(drone)

    def _simulate_one_drone(self, drone: Drone) -> None:
        """1台のドローンのシミュレーションを実行するメソッド"""
        cur_hub = drone.position

        if cur_hub.hub_type == HubType.END_HUB:
            print("End Hub")
            return
        next_hubs = []
        for connection in self._connections:
            hubs = connection.hubs
            if hubs[0] == cur_hub.name:
                next_hubs.append(hubs[1])
            elif hubs[1] == cur_hub.name:
                next_hubs.append(hubs[0])

        print("===")
        print(next_hubs)
