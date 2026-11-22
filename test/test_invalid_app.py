import subprocess
import sys

import pytest

from fly_in import FileParser, InvalidConfigError

CASES: list[tuple[str, list[int] | None]] = [
    ("test/maps/errors/dupe_connection.txt", [10, 11]),
    ("test/maps/errors/dupe_hub.txt", [5, 6]),
    ("test/maps/errors/dupe_nb_drones.txt", [3]),
    ("test/maps/errors/invalid_connection_format.txt", [10]),
    ("test/maps/errors/invalid_coordinate.txt", [5]),
    ("test/maps/errors/invalid_nb_drones.txt", [2]),
    ("test/maps/errors/invalid_option_format.txt", [5]),
    ("test/maps/errors/no_brackets.txt", [6]),
    ("test/maps/errors/no_separator.txt", [5]),
    ("test/maps/errors/nonexist_hubs.txt", [8]),
    ("test/maps/errors/unknown_key.txt", [5]),
    ("test/maps/errors/empty.txt", None),
    ("test/maps/errors/no_nb_drones.txt", None),
    ("test/maps/errors/no_start_hub.txt", None),
]


@pytest.mark.parametrize(("file", "lines"), CASES)
def test_invalid_parse_file(file: str, lines: list[int] | None) -> None:
    with pytest.raises(InvalidConfigError) as exc_info:
        FileParser.parse_file(file)

    if lines:
        assert exc_info.value.line_numbers == lines
    else:
        assert not exc_info.value.line_numbers
    message = str(exc_info.value)
    if lines:
        expected = ", ".join(str(n) for n in lines)
        assert f"at line {expected}:" in message
    else:
        assert "at line" not in message


@pytest.mark.parametrize("color", [False, True])
@pytest.mark.parametrize(("file", "lines"), CASES)
def test_invalid_main_program(
    file: str, lines: list[int] | None, color: bool
) -> None:
    opts = ["--color"] if color else []
    args = [sys.executable, "main.py", *opts, file]
    result = subprocess.run(args, check=False, text=True, capture_output=True)
    print(result.stderr)

    assert result.returncode == 1
    assert "Invalid configuration" in result.stderr
    if lines:
        expected = ", ".join(str(n) for n in lines)
        assert f"at line {expected}:" in result.stderr
    else:
        assert "at line" not in result.stderr


@pytest.mark.parametrize("color", [False, True])
def test_no_goal_path_not_found(color: bool) -> None:
    opts = ["--color"] if color else []
    args = [sys.executable, "main.py", *opts, "test/maps/errors/no_goal.txt"]
    result = subprocess.run(args, check=False, text=True, capture_output=True)

    assert result.returncode == 1
    assert "Cannot find a valid path for drone with ID: 1" in result.stderr
