"""fly-inのエントリーポイントとなるモジュール"""

import argparse
import sys

try:
    from fly_in import (
        FileParser,
        InvalidConfigError,
        RouteNotFoundError,
        Simulation,
        Visualizer,
    )
except (ImportError, ModuleNotFoundError) as e:
    print(f"Missing dependency: {e.name}\nPlease install it and try again.")
    sys.exit(2)

RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

EXIT_SUCCESS = 0
EXIT_INVALID = 1
EXIT_SYSTEM = 2
EXIT_UNEXPECTED = 3
EXIT_INTERRUPTED = 130


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
    parser.add_argument(
        "-s",
        "--max-file-size",
        type=int,
        help="Set the maximum file size in bytes. "
        + "If the file size exceeds this limit, "
        "the program will read the first max_file_size "
        + "bytes of the file. ",
        default=100_000_000,
        metavar="BYTES",
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
    status: str = "initializing"
    try:
        status = "parsing arguments"
        args = parse_args()
        color = args.color

        status = "reading configuration file"
        config = FileParser.parse_file(args.filename, args.max_file_size)

        status = "instantiating simulation class"
        fly_in = Simulation(config)

        status = "simulating"
        result = fly_in.simulate()

        status = "visualizing"
        Visualizer(result, color, config.hubs).show_result()
    except (InvalidConfigError, RouteNotFoundError) as e:
        print_colored_error(str(e), color)
        return 1
    except (ImportError, MemoryError, OSError) as e:
        err_msg: str = "Unknown error"
        if isinstance(e, (ImportError, ModuleNotFoundError)):
            err_msg = (
                f"Missing dependency: {e.name}\n"
                + "Please install it and try again."
            )
        elif isinstance(e, MemoryError):
            err_msg = (
                f"Out of memory while {status}\n"
                + f"Please check your computer.\n{e}"
            )
        elif isinstance(e, OSError):
            err_msg = f"{e}\n while {status}"

        print_colored_error(
            err_msg,
            color,
        )
        return 2
    except KeyboardInterrupt:
        print_colored_error(f"Interrupted while {status}", color)
        return 130
    except Exception as e:
        print_colored_error(
            f"UNEXPECTED ERROR while {status}: "
            + f"You should report this to the developer:\n{e}",
            color,
        )
        return 3

    return 0


if __name__ == "__main__":
    sys.exit(main())
