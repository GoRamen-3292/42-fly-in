from src.visualizer.visualizer import COLOR_CODES, RESET_CODE

if __name__ == "__main__":
    for color_name, color_code in COLOR_CODES.items():
        print(f"{color_code}{color_name}{RESET_CODE}")
