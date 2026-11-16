import argparse
import sys

from src import FileParser, InvalidConfigError, Simulation, Visualizer
from src.solver.types import RouteNotFoundError

RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def parse_args() -> argparse.Namespace:
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
    args = parser.parse_args()
    return args


def print_colored_error(message: str, color: bool = False) -> None:
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
    # 予期せずExceptionクラスおよびその子クラスをraiseすることのない関数
    args = parse_args()
    try:
        config = FileParser.parse_file(args.filename)
        fly_in = Simulation(config)
        result = fly_in.simulate()
        Visualizer(result, args.color, config.hubs).show_result()
        return 0
    except (InvalidConfigError, RouteNotFoundError) as e:
        print_colored_error(str(e), args.color)
        return 1
    except MemoryError as e:
        print_colored_error(
            f"Out of memory\nPlease check your computer. {e}", args.color
        )
        return 2
    except OSError as e:
        print_colored_error(f"Error while processing:\n{e}", args.color)
        return 2
    except KeyboardInterrupt:
        print_colored_error("Interrupted", args.color)
        return 130
    except Exception as e:  # noqa: BLE001
        print_colored_error(
            f"UNEXPECTED ERROR: You should report this to the developer:\n{e}",
            args.color,
        )
        return 3


if __name__ == "__main__":
    sys.exit(main())
