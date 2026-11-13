import subprocess
import warnings

import pytest

from src import FileParser
from src.model import SimulationConfig

type FileAndOptimalTurns = tuple[str, int]

FILES: list[FileAndOptimalTurns] = [
    ("maps/easy/01_linear_path.txt", 4),
    ("maps/easy/02_simple_fork.txt", 4),
    ("maps/easy/03_basic_capacity.txt", 4),
    ("maps/medium/01_dead_end_trap.txt", 8),
    ("maps/medium/02_circular_loop.txt", 10),
    ("maps/medium/03_priority_puzzle.txt", 6),
    ("maps/hard/01_maze_nightmare.txt", 13),
    ("maps/hard/02_capacity_hell.txt", 16),
    ("maps/hard/03_ultimate_challenge.txt", 26),
    ("maps/challenger/01_the_impossible_dream.txt", 43),
]


@pytest.mark.parametrize("file", FILES)
def test_parse_file(file: FileAndOptimalTurns) -> None:
    config: SimulationConfig = FileParser.parse_file(file[0])
    assert config is not None


@pytest.mark.parametrize("file", FILES)
def test_main_program_with_optimal_turns(file: FileAndOptimalTurns) -> None:
    result = subprocess.run(
        ["uv", "run", "python3", "main.py", file[0]], check=True, text=True, capture_output=True)
    lines = len(str(result.stdout).splitlines())
    if lines != file[1]:
        warnings.warn(
            f"File: {file[0]} | Optimal turns: {file[1]} | Actual turns: {lines}")
    assert file[1] <= lines <= file[1] * 1.25


@pytest.mark.parametrize("file", [
    "test/maps/no_path_b/01_simple_fork_priority.txt",
    "test/maps/no_path_b/02_simple_fork_priority.txt",
])
def test_priority_hub_preference(file: str) -> None:
    result = subprocess.run(
        ["uv", "run", "python3", "main.py", file], check=True, text=True, capture_output=True)
    lines = str(result.stdout).splitlines()
    # Check if the output contains the expected path that goes through the priority hub
    # Assuming HubB is the priority hub
    assert any("path_a" in line for line in lines)
    assert not any("path_b" in line for line in lines)
    assert any("goal" in line for line in lines)


@pytest.mark.parametrize("file", [
    "test/maps/restricted_max/01_simple_linear_all_restricted.txt",
    "test/maps/restricted_max/02_simple_linear_all_restricted.txt",
    "test/maps/restricted_max/03_simple_linear_all_restricted.txt",
])
def test_restricted_max(file: str) -> None:
    result = subprocess.run(
        ["uv", "run", "python3", "main.py", file], check=True, text=True, capture_output=True)
    lines = str(result.stdout).splitlines()
    # Check if the output contains the expected path that respects the restricted max capacity
    assert any("D1-start" in line for line in lines)
    assert any("D1-goal" in line for line in lines)
