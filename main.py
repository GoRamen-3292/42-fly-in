import argparse

from src import FileParser, InvalidConfigError, Simulation, Visualizer


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


def main() -> None:
    """メイン関数"""
    try:
        args = parse_args()
        config = FileParser.parse_file(args.filename)
        fly_in = Simulation(config)
        result = fly_in.simulate()
        Visualizer(result, args.color, config.hubs).show_result()
    except InvalidConfigError as e:
        print(str(e))
    except ValueError as e:
        print(f"ValueError: {e}")
    except OSError as e:
        print(f"Unintended: {e}")
    except Exception as e:  # noqa: BLE001
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
