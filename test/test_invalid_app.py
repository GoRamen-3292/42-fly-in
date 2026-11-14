import subprocess

import pytest

from src import FileParser
from src.model import SimulationConfig

FILES: list[str] = [
    "maps/errors/dupe_connection.txt",
]


@pytest.mark.parametrize("file", FILES)
def test_invalid_parse_file(file: str) -> None:
    config: SimulationConfig = FileParser.parse_file(file)
    assert config is not None


@pytest.mark.parametrize("file", FILES)
def test_invalid_main_program(file: str) -> None:
    result = subprocess.run(
        ["uv", "run", "python3", "main.py", file],
        check=False,
        text=True,
        capture_output=True,
    )
    print(result.stdout)
    assert False


@pytest.mark.parametrize("file", FILES)
def test_main_program_with_colors_and_optimal_turns(
    file: str,
) -> None:
    result = subprocess.run(
        ["uv", "run", "python3", "main.py", "-c", file],
        check=False,
        text=True,
        capture_output=True,
    )
    print(result.stdout)

    assert False
