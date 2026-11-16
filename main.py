"""fly-inのエントリーポイントとなるモジュール"""

import argparse
import sys

from fly_in import (
    FileParser,
    InvalidConfigError,
    RouteNotFoundError,
    Simulation,
    Visualizer,
)

RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def parse_args() -> argparse.Namespace:
    """コマンドライン引数をパースする関数"""
    parser = argparse.ArgumentParser(
        prog="fly-in",
        description="A drone simulation program."
        + " Created as a part of the 42 curriculum.",
    )
    parser.add_argument("filename", help="The name of the file to parse")
    parser.add_argument(
        "-c",
        "--color",
        action="store_true",
        default=False,
        help="Enable color output",
    )
    return parser.parse_args()


def print_colored_error(message: str, color: bool = False) -> None:
    """エラーメッセージを標準エラー出力に表示する関数

    colorがTrueの場合は、メッセージの1行目を赤色の太字で、
    2行目以降を太文字で強調して表示する
    """
    lines = message.splitlines()

    if color and lines:
        print(
            f"{BOLD}{RED}ERROR:{RESET}",
            f"{BOLD}{lines[0]}{RESET}",
            *lines[1:],
            sep="\n",
            file=sys.stderr,
        )
    else:
        print("ERROR:", message, sep="\n", file=sys.stderr)


def main() -> int:
    """メイン関数"""
    color: bool = False
    try:
        args = parse_args()
        color = args.color

        config = FileParser.parse_file(args.filename)
        fly_in = Simulation(config)
        result = fly_in.simulate()
        Visualizer(result, color, config.hubs).show_result()
    except (InvalidConfigError, RouteNotFoundError) as e:
        print_colored_error(str(e), color)
        return 1
    except MemoryError as e:
        print_colored_error(
            f"Out of memory\nPlease check your computer. {e}", color
        )
        return 2
    except OSError as e:
        print_colored_error(f"Error while processing:\n{e}", color)
        return 2
    except KeyboardInterrupt:
        print_colored_error("Interrupted", color)
        return 130
    except Exception as e:
        print_colored_error(
            f"UNEXPECTED ERROR: You should report this to the developer:\n{e}",
            color,
        )
        return 3

    return 0


if __name__ == "__main__":
    sys.exit(main())
