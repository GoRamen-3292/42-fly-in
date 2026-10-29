from ..model import Connection, Hub, HubType, SimulationConfig
from pydantic import ValidationError


class FileParser:
    @classmethod
    def parse_file(cls, file_path: str) -> SimulationConfig:
        """ファイルをパースする関数

        Args:
            file_path (str): パースするファイルのパス
        Raises:
            ValueError: ファイルのパースに失敗した場合
            FileNotFoundError: ファイルが存在しない場合
        """
        config = SimulationConfig.model_construct(
            nb_drones=None,
            hubs=[],
            connections=[],
        )
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                cls.parse_line(line.strip(), config)
        return SimulationConfig.model_validate(config)

    @classmethod
    def parse_line(cls, line: str, config: SimulationConfig) -> None:
        """1行のパースをする関数"""
        if line.startswith("#") or not line:
            return
        try:
            splits = line.split(":", maxsplit=1)
            if len(splits) <= 1:
                raise ValueError(f"Invalid number of ':' in line: {line}")
            key, value = (x.strip() for x in splits)

            if key in HubType.__members__.values():
                config.hubs.append(cls._parse_hub_line(
                    HubType(key), value, config))
            elif key == "connection":
                config.connections.append(
                    cls._parse_connection_line(value, config))
            elif key == "nb_drones":
                if config.nb_drones is not None:
                    raise ValueError("nb_drones is already set")
                config.nb_drones = int(value)
            else:
                raise ValueError(f"Unknown key: {key}")
        except (ValueError, ValidationError, IndexError) as e:
            raise ValueError(f"Invalid line format: {line}" + "\n" + str(e))

    @classmethod
    def _parse_hub_line(cls, hub_type: HubType, value: str,
                        config: SimulationConfig) -> Hub:
        """hubの行をパースする関数"""
        values = value.split()

        name, x, y = values[:3]
        options = values[3:] if len(values) > 3 else []

        d: dict[str, str] = cls._parse_options(" ".join(options))

        return Hub.model_validate(
            {
                **d,
                "hub_type": hub_type,
                "name": name,
                "coordinate": (int(x), int(y)),
                "color": d.get("color"),
            }
        )

    @classmethod
    def _parse_options(cls, options: str) -> dict[str, str]:
        """オプションのパースをする関数"""
        options = options.strip()
        if not options:
            return {}

        result: dict[str, str] = {}
        for option in cls.extract_brackets(options).split():
            key, value = (x.strip() for x in option.split("="))
            result[key] = value

        return result

    @classmethod
    def _parse_connection_line(cls, value: str,
                               config: SimulationConfig) -> Connection:
        """connectionの行をパースする関数"""
        # ここでvalueを解析してConnectionを作成し、configに追加する処理を書く
        options = value.split()
        hub1, hub2 = options[0].split("-")
        if len(options) == 1:
            return Connection(
                hubs=(hub1, hub2),
            )
        else:
            options = options[1:]
            d = cls._parse_options(" ".join(options))

            return Connection.model_validate(
                {
                    **d,
                    "hubs": (hub1, hub2),
                }
            )

    @staticmethod
    def extract_brackets(s: str) -> str:
        """文字列から角括弧で囲まれた部分を抽出する"""
        s = s.strip()
        if s[0] != "[" or s[-1] != "]":
            raise ValueError("Options must be enclosed in brackets")
        return s[1:-1]
