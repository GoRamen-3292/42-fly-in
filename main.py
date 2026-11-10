import argparse
from src import FileParser, Simulation, Visualizer


def main() -> None:
    """メイン関数"""
    try:
        parser = argparse.ArgumentParser(
            prog='fly-in',
            description='A drone simulation program. Created as a part of the 42 curriculum.')
        parser.add_argument(
            'filename', help='The name of the file to parse')           # 位置引数
        parser.add_argument('-c', '--color', action='store_true',
                            default=False, help='Enable color output')
        args = parser.parse_args()
        print(args.filename, args.color)

        # config = FileParser.parse_file("01_linear_path.txt")
        # print(config.model_dump(mode="Python"))
        # config = FileParser.parse_file("02_simple_fork.txt")
        # config = FileParser.parse_file(
        #     "maps/hard/03_ultimate_challenge.txt")
        config = FileParser.parse_file(args.filename)
        # config = FileParser.parse_file(
        #     "maps/challenger/01_the_impossible_dream.txt")
        # print(config.model_dump(mode="Python"))
        fly_in = Simulation(config)
        # for i in fly_in._drones:
        #     print(i)
        #     print(vars(i))
        result = fly_in.simulate()
        Visualizer.show_result(result)
    except BaseException:
        raise
    # except FileNotFoundError:
    #     print("File not found")
    # except ValueError as e:
    #     print(f"ValueError: {e}")
    # except OSError as e:
    #     print(f"Unintended: {e}")
    # except Exception as e:
    #     print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
