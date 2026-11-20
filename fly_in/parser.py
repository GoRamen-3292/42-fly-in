"""設定ファイルからSimulationConfigを生成するパーサーを含むモジュール"""

from dataclasses import dataclass, field

from pydantic import ValidationError

from .model import Connection, Hub, HubType, SimulationConfig
from .model.types import InvalidConfigError


@dataclass
class _SimulationParserConfig:
    """設定ファイルの読み込み状態を表すクラス"""

    nb_drones_line: int | None = None
    nb_drones: str | None = None
    hubs: list[Hub] = field(default_factory=list)
    connections: list[Connection] = field(default_factory=list)


class FileParser:
    """設定ファイルを読み込み、SimulationConfigとして返すクラス"""

    @classmethod
    def parse_file(
        cls, file_path: str, max_size: int = 100_000_000
    ) -> SimulationConfig:
        """ファイルをパースする関数

        Args:
            file_path: パースするファイルのパス
            max_size: ファイルから読み込む最大の文字数

        Returns:
            検証済みのシミュレーションの設定

        Raises:
            InvalidConfigError: 無効な設定ファイルの場合
            OSError: 各種ファイル操作に失敗した場合
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                file_txt: str = f.read(max_size + 1)

            if len(file_txt) > max_size:
                raise InvalidConfigError(
                    f"File size exceeds the limit of {max_size} bytes", None
                )

            return cls.parse_text(file_txt)

        except (OSError, UnicodeDecodeError) as e:
            raise OSError(
                f"Error occurred while reading the file: {file_path}\n{e}"
            ) from e

    @classmethod
    def parse_text(cls, text: str) -> SimulationConfig:
        """Configをテキストから読み込み、処理をする

        Args:
            text: パースするテキスト

        Returns:
            検証済みのシミュレーションの設定

        Raises:
            InvalidConfigError: 無効な設定ファイルの場合
        """
        config = _SimulationParserConfig()
        lineno: int | None = None

        try:
            lines = text.splitlines()
            for lineno, line in enumerate(lines, start=1):
                cls.parse_line(line.strip(), config, lineno)
            lineno = None
            return SimulationConfig.model_validate(
                {
                    "nb_drones": config.nb_drones,
                    "hubs": config.hubs,
                    "connections": config.connections,
                }
            )
        except InvalidConfigError:
            raise
        except ValidationError as e:
            if not e.errors():
                raise InvalidConfigError(
                    "Unknown validation error occurred"
                ) from e
            err_lines: list[int] | None = _lines_from_loc(
                e.errors()[0]["loc"], config
            )
            found_err: InvalidConfigError | None = _find_config_error(e)
            if found_err is not None:
                if found_err.line_numbers is None:
                    found_err.line_numbers = err_lines
                raise found_err from e

            raise InvalidConfigError(
                _parse_validation_error(e), err_lines
            ) from e

    @classmethod
    def parse_line(
        cls, line: str, config: _SimulationParserConfig, lineno: int
    ) -> None:
        """1行のパースをする関数"""
        if line.startswith("#") or not line:
            return
        splits = line.partition(":")
        if splits[1] != ":":
            raise InvalidConfigError(
                "Line must contain a ':' separator", [lineno]
            )
        key, value = (x.strip() for x in (splits[i] for i in (0, 2)))
        if not key or not value:
            raise InvalidConfigError(
                "Line must contain a key and a value", [lineno]
            )
        try:
            if key in HubType.__members__.values():
                config.hubs.append(
                    cls._parse_hub_line(HubType(key), value, lineno)
                )
            elif key == "connection":
                config.connections.append(
                    cls._parse_connection_line(value, lineno)
                )
            elif key == "nb_drones":
                cls._parse_nb_drones_line(config, value, lineno)
            else:
                raise InvalidConfigError(f"Unknown key {key}", [lineno])
        except InvalidConfigError as e:
            e.args = (f"{key}: {e.args[0]}",)
            if e.line_numbers is None:
                e.line_numbers = [lineno]
            raise
        except ValidationError as e:
            pyd_err = e.errors()[0]
            err_type: str = pyd_err.get("type")
            if err_type == "model_type":
                raise InvalidConfigError(
                    "Extra configuration fields found in the file",
                    [lineno] if lineno else None,
                ) from e
            raise _find_config_error(e, lineno) or InvalidConfigError(
                _parse_validation_error(e), [lineno]
            ) from e

    @classmethod
    def _parse_nb_drones_line(
        cls, config: _SimulationParserConfig, value: str, lineno: int
    ) -> None:
        """nb_dronesの行をパースする関数

        Raises:
            InvalidConfigError: 無効なnb_dronesの行の場合
        """
        if config.nb_drones is not None:
            raise InvalidConfigError(
                "Cannot set the number of drones multiple times", [lineno]
            )
        config.nb_drones = value
        config.nb_drones_line = lineno

    @classmethod
    def _parse_hub_line(
        cls, hub_type: HubType, value: str, lineno: int
    ) -> Hub:
        """hubの行をパースする関数

        Raises:
            InvalidConfigError: 無効なhubの行の場合
        """
        values = value.split()
        if len(values) < 3:
            raise InvalidConfigError(
                "Hub line must contain at least 3 values: name, x, y", [lineno]
            )
        name, x, y = values[:3]
        options = values[3:] if len(values) > 3 else []

        d: dict[str, str] = cls._parse_options(" ".join(options))

        if any(k in d for k in ["hub_type", "name", "coordinate", "line_no"]):
            raise InvalidConfigError("Invalid option key")
        return Hub.model_validate(
            {
                **d,
                "hub_type": hub_type,
                "name": name,
                "coordinate": (x, y),
                "line_no": lineno,
            }
        )

    @staticmethod
    def _parse_options(options: str) -> dict[str, str]:
        """オプションのパースをする関数"""
        options = options.strip()
        if not options:
            return {}

        result: dict[str, str] = {}
        for option in extract_brackets(options).split():
            items = [x.strip() for x in option.split("=")]
            if len(items) != 2:
                raise InvalidConfigError(
                    f"Invalid option format: {option}. Expected: key=value"
                )
            key, value = items

            if not key or not value:
                raise InvalidConfigError(
                    f"Invalid option format: {option}. "
                    + "Key and value must be non-empty"
                )
            if key in result:
                raise InvalidConfigError(f"Duplicate option key: {key}")
            result[key] = value

        return result

    @classmethod
    def _parse_connection_line(cls, value: str, lineno: int) -> Connection:
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
                line_no=lineno,
            )
        options = options[1:]
        d: dict[str, str] = cls._parse_options(" ".join(options))

        if any(k in d for k in ["hubs", "line_no"]):
            raise InvalidConfigError(
                "Cannot set 'hubs' or 'line_no' in connection options"
            )
        return Connection.model_validate(
            {
                **d,
                "hubs": (hub1, hub2),
                "line_no": lineno,
            }
        )


def extract_brackets(s: str) -> str:
    """文字列から角括弧で囲まれた部分を抽出する"""
    s = s.strip()
    if s[0] != "[" or s[-1] != "]":
        raise InvalidConfigError("Options must be enclosed in brackets")
    return s[1:-1]


def _parse_validation_error(e: ValidationError) -> str:
    """PydanticのValidationErrorをパースして、エラーメッセージを返す関数"""
    err_list: list[str] = []
    for err in e.errors():
        err_loc: tuple[int | str, ...] = err.get("loc", ("unknown",))
        err_loc_str: str = f"{err_loc[0]}: " if err_loc else ""
        if err["msg"] is None:
            err_list.append(f"Unknown error at {err_loc_str}")
        else:
            err_list.append(err_loc_str + err["msg"])
    return "\n".join(err_list)


def _lines_from_loc(
    loc: tuple[int | str, ...], config: _SimulationParserConfig
) -> list[int] | None:
    """Pydanticのエラー位置(loc)から設定ファイルの行番号を求める関数

    locの先頭はエラーが発生したフィールド名、リストの要素であれば
    その次にインデックスが続く (例: ('hubs', 3, 'name'))

    Args:
        loc: ValidationError.errors()の各要素に含まれるエラー位置
        config: 行番号の情報を持つ読み込み状態

    Returns:
        対応する行番号のリスト、特定できない場合はNone
    """
    if not loc:
        return None
    field = loc[0]
    if field == "nb_drones":
        return [config.nb_drones_line] if config.nb_drones_line else None
    if field in ("hubs", "connections") and len(loc) > 1:
        index = loc[1]
        items: list[Hub] | list[Connection] = (
            config.hubs if field == "hubs" else config.connections
        )
        if isinstance(index, int) and 0 <= index < len(items):
            line_no = items[index].line_no
            return [line_no] if line_no else None
    return None


def _find_config_error(
    e: ValidationError, lineno: int | None = None
) -> InvalidConfigError | None:
    """ValidationErrorに含まれるInvalidConfigErrorを取り出す関数

    Pydanticのバリデータ内で送出されたInvalidConfigErrorは
    ValidationErrorに包まれるため、元の例外を取り出して返す
    取り出した例外に行番号が設定されていない場合は、linenoを補う

    Args:
        e: 探索対象のValidationError
        lineno: 例外に行番号が設定されていない場合に補う行番号

    Returns:
        見つかったInvalidConfigError、見つからなかった場合はNone
    """
    for err in e.errors():
        if err["type"] == "model_type":
            return InvalidConfigError(
                "Extra configuration fields found in the file",
                [lineno] if lineno else None,
            )
        ctx = err.get("ctx", {}).get("error")
        if isinstance(ctx, InvalidConfigError):
            if ctx.line_numbers is None:
                ctx.line_numbers = [lineno] if lineno else None
            return ctx
    return None
