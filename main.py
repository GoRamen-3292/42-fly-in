from src import FileParser, Simulation, Visualizer


def main() -> None:
    """メイン関数"""
    print("Hello, World!")
    try:
        config = FileParser.parse_file("maps/easy/01_linear_path.txt")
        # print(config.model_dump(mode="Python"))
        # config = FileParser.parse_file("02_simple_fork.txt")
        # config = FileParser.parse_file(
        #     "maps/hard/03_ultimate_challenge.txt")
        # config = FileParser.parse_file(
        #     "maps/challenger/01_the_impossible_dream.txt")
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
