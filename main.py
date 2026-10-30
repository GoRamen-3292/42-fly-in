from src import FileParser, Simulation


def main() -> None:
    """メイン関数"""
    print("Hello, World!")
    try:
        config = FileParser.parse_file("test.txt")
        # print(config.model_dump(mode="Python"))
        fly_in = Simulation(config)
        for i in fly_in._drones:
            print(i)
            print(vars(i))
        fly_in.simulate()

    except FileNotFoundError:
        print("File not found")
    except ValueError as e:
        print(f"ValueError: {e}")
    except OSError as e:
        print(f"Unintended: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
