"""シミュレーションの結果を標準出力に表示するモジュール"""

from collections import defaultdict

from .model import ConnectionKey, Hub
from .scheduler.types import SimulationResult

type OutputDict = defaultdict[int, list[str]]


def _fg256(n: int) -> str:
    """256色のANSIエスケープシーケンスを生成する関数

    Args:
        n: 256色のカラーパレットにおける0から255までの色番号
    """
    return f"\033[38;5;{n}m"


RESET_CODE = "\033[0m"
# TODO: 256色のANSIエスケープシーケンスについて調べる
COLOR_CODES: dict[str, str] = {
    # basic 8 colors
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    # bright colors
    "gray": "\033[90m",
    "grey": "\033[90m",
    "lightred": "\033[91m",
    "lime": "\033[92m",
    "lightgreen": "\033[92m",
    "lightyellow": "\033[93m",
    "lightblue": "\033[94m",
    "lightmagenta": "\033[95m",
    "lightcyan": "\033[96m",
    "brightwhite": "\033[97m",
    # extended colors (256-color mode)
    "orange": _fg256(208),
    "gold": _fg256(220),
    "brown": _fg256(94),
    "maroon": _fg256(88),
    "crimson": _fg256(160),
    "darkred": _fg256(88),
    "purple": _fg256(129),
    "violet": _fg256(177),
    "pink": _fg256(213),
    "teal": _fg256(30),
    "navy": _fg256(18),
    "olive": _fg256(100),
    "silver": _fg256(250),
    "indigo": _fg256(54),
    "turquoise": _fg256(80),
    "beige": _fg256(230),
}


class Visualizer:
    """シミュレーションの結果をターンごとに出力するクラス

    Attributes:
        result: 表示するシミュレーションの結果
        color: ハブ名を色付きで出力するかどうか
        hubs: ハブの色を参照するためのハブのリスト
    """

    def __init__(
        self,
        result: SimulationResult,
        color: bool = False,
        hubs: list[Hub] | None = None,
    ) -> None:
        """Visualizerを初期化するコンストラクタ

        Args:
            result: 表示するシミュレーションの結果
            color: ハブ名を色付きで出力するかどうか
            hubs: ハブの色を参照するためのハブのリスト、colorがTrueの場合は必須
        """
        self.result = result
        self.color = color
        self.hubs = hubs

    def show_result(self) -> None:
        """各ターンのドローンの移動を1行ずつ標準出力に表示するメソッド

        各行は「D<ドローンID>-<位置>」を空白区切りで並べた形式で、
        そのターンに移動しなかったドローンは出力しない

        Raises:
            ValueError: 色付きの出力が有効なのにハブの情報がない場合
        """
        output_dict = self._pre_process_args()
        sorted_keys = sorted(output_dict.keys())

        for i, key in enumerate(sorted_keys):
            if i == 0:
                continue
            print(" ".join(output_dict[key]))

    def _pre_process_args(self) -> OutputDict:
        output_dict: OutputDict = defaultdict(list)
        for drone in self.result.drones:
            for i, el in enumerate(drone.timeline):
                pos: str | ConnectionKey = el[1]
                pos_str = self._create_pos_str(pos)
                dpos_str = f"D{drone.id}-{pos_str}"
                if i > 0 and pos_str == drone.timeline[i - 1][1]:
                    continue
                output_dict[i].append(dpos_str)

        return output_dict

    def _create_pos_str(self, pos: str | ConnectionKey) -> str:
        if isinstance(pos, str):
            return self._create_formatted_name(pos)
        return "-".join([self._create_formatted_name(p) for p in pos])

    def _create_formatted_name(self, name: str) -> str:
        if not self.color:
            return name
        if not self.hubs:
            raise ValueError("Color output requires hub information.")

        color_name: str | None = next(
            (hub.color for hub in self.hubs if hub.name == name), None
        )
        if color_name is None:
            return name
        if color_name.lower() == "rainbow":
            return _create_rainbow_name(name)

        color_code: str | None = COLOR_CODES.get(color_name.lower())
        if color_code is None:
            return name
        return color_code + name + RESET_CODE


def _create_rainbow_name(name: str) -> str:
    rainbow_colors = [
        COLOR_CODES[key]
        for key in [
            "red",
            "orange",
            "yellow",
            "green",
            "blue",
            "indigo",
            "violet",
        ]
    ]
    rainbow_name = ""
    for i, char in enumerate(name):
        color_code = rainbow_colors[i % len(rainbow_colors)]
        rainbow_name += color_code + char
    return rainbow_name + RESET_CODE
