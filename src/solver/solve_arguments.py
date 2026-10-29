from src.model import SimulationConfig, Hub, Connection


type SimulationResult = None  # TODO: これを削除して実際の戻り値の型に変更する


class Simulation:
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.hubs: list[Hub] = config.hubs
        self.connections: list[Connection] = config.connections

    def simulate(self) -> SimulationResult:
        """シミュレーションを実行するメソッド"""
        raise NotImplementedError("Simulation logic is not implemented yet.")
