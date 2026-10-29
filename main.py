from src.parser import FileParser


def main() -> None:
    """メイン関数"""
    print("Hello, World!")
    try:
        config = FileParser.parse_file("test.txt")
        print(config.model_dump(mode="Python"))
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
