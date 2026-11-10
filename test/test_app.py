from src import FileParser
from src.model import SimulationConfig
import pytest
import subprocess

# maps/challenger:
# 01_the_impossible_dream.txt

# maps/easy:
# 01_linear_path.txt  02_simple_fork.txt  03_basic_capacity.txt

# maps/hard:
# 01_maze_nightmare.txt  02_capacity_hell.txt  03_ultimate_challenge.txt

# maps/medium:
# 01_dead_end_trap.txt  02_circular_loop.txt  03_priority_puzzle.txt

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
    assert lines == file[1]
