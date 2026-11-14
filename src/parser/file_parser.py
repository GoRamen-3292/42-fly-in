from pydantic import ValidationError

from ..model import Connection, Hub, HubType, SimulationConfig


class InvalidConfigError(ValueError):
    """無効な設定ファイルのエラーを表す例外クラス"""

    def __init__(self, message: str, line_number: int | None = None) -> None:
        if line_number is not None:
            message = f"Line {line_number}: {message}"
        super().__init__(message)


class FileParser:
    @classmethod
    def parse_file(cls, file_path: str) -> SimulationConfig:
        """ファイルをパースする関数

        Args:
            file_path (str): パースするファイルのパス
        Raises:
            InvalidConfigError: 無効な設定ファイルの場合
            OSError: 各種ファイル操作に失敗した場合
        """
        config = SimulationConfig.model_construct(
            nb_drones=None,
            hubs=[],
            connections=[],
        )
        lineno = 0
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for lineno, line in enumerate(f, start=1):
                    cls.parse_line(line.strip(), config, lineno)
            return SimulationConfig.model_validate(config)
        except OSError as e:
            raise OSError(
                f"Error occurred while reading the file: {file_path}\n{e}"
            ) from e
        except InvalidConfigError as e:
            if lineno == 0:
                err_str = f"Unexpected error in the file: {file_path}\n{e}"
            else:
                err_str = (
                    f"Invalid configuration at line {lineno}: {file_path}\n{e}"
                )
            raise InvalidConfigError(err_str) from e
        except ValidationError as e:
            # TODO: Pydanticのエラーメッセージの抽出を行う
            raise InvalidConfigError(
                f"Validation error in the file: {file_path}\n{e}"
            ) from e

    @classmethod
    def parse_line(
        cls, line: str, config: SimulationConfig, lineno: int
    ) -> None:
        """1行のパースをする関数"""
        if line.startswith("#") or not line:
            return
        try:
            splits = line.partition(":")
            if splits[1] != ":":
                raise InvalidConfigError("Line must contain a ':' separator")
            key, value = (x.strip() for x in (splits[i] for i in (0, 2)))

            if key in HubType.__members__.values():
                config.hubs.append(cls._parse_hub_line(HubType(key), value))
            elif key == "connection":
                config.connections.append(cls._parse_connection_line(value))
            elif key == "nb_drones":
                if config.nb_drones is not None:
                    raise InvalidConfigError("nb_drones is already set")
                # validation前につき、config.nb_dronesの型はNoneである可能性がある
                config.nb_drones = int(value)
            else:
                raise InvalidConfigError(f"Unknown key: {key}")
        except ValidationError as e:
            # TODO: Pydanticのエラーメッセージの抽出を行う
            raise InvalidConfigError(str(e)) from e
        except InvalidConfigError as e:
            raise InvalidConfigError(str(e)) from e
        except ValueError as e:
            raise InvalidConfigError(str(e)) from e

    @classmethod
    def _parse_hub_line(cls, hub_type: HubType, value: str) -> Hub:
        """hubの行をパースする関数

        Raises:
            InvalidConfigError: 無効なhubの行の場合
        """
        values = value.split()
        if len(values) < 3:
            raise InvalidConfigError(
                "Hub line must contain at least 3 values: name, x, y"
            )
        name, x, y = values[:3]
        options = values[3:] if len(values) > 3 else []

        d: dict[str, str] = cls._parse_options(" ".join(options))

        return Hub.model_validate(
            {
                **d,
                "hub_type": hub_type,
                "name": name,
                "coordinate": (x, y),
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
            items = [x.strip() for x in option.split("=")]
            if len(items) != 2:
                raise InvalidConfigError(
                    f"Invalid option format: {option}. Expected: key=value"
                )
            key, value = items
            result[key] = value

        return result

    @classmethod
    def _parse_connection_line(cls, value: str) -> Connection:
        """connectionの行をパースする関数"""
        options: list[str] = value.split()

        connection: list[str] = options[0].split("-")
        if len(connection) != 2:
            raise InvalidConfigError(
                "Connection line must contain "
                + "exactly two hubs separated by '-'"
            )
        hub1, hub2 = connection

        if len(options) == 1:
            return Connection(
                hubs=(hub1, hub2),
            )
        else:
            options = options[1:]
            d: dict[str, str] = cls._parse_options(" ".join(options))

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
            raise InvalidConfigError("Options must be enclosed in brackets")
        return s[1:-1]
