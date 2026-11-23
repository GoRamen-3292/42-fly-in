CHECK_PATHS = fly_in sandbox main.py
TEST_PATHS = test
CACHE_DIRS = .mypy_cache .pytest_cache
MAP = config.txt

all: install
	@uv run main.py --help

install: $(MAP)
	uv sync

$(MAP):
	@echo "Creating $(MAP) from example.txt"
	cp example.txt $(MAP)

run:
	@uv run main.py $(MAP)

r: run

color:
	@uv run main.py $(MAP) --color

c: color

visualize: color

debug:
	@uv run python3 -m pdb main.py $(MAP)

clean:
	-uv run ruff clean
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf $(CACHE_DIRS)

fclean: clean
	rm -rf .venv

lint:
	uv run mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs $(CHECK_PATHS)
	uv run flake8 $(CHECK_PATHS)

lint-strict:
	uv run mypy --strict $(CHECK_PATHS) $(TEST_PATHS)
	uv run flake8 --disable-noqa $(CHECK_PATHS)
	uv run flake8 --max-line-length 200 --disable-noqa $(TEST_PATHS)
	-uv run ruff check $(CHECK_PATHS) $(TEST_PATHS)

lint-fix:
	uv run ruff format $(CHECK_PATHS) $(TEST_PATHS)
	-uv run ruff check --fix $(CHECK_PATHS) $(TEST_PATHS)

check: lint-strict test

test:
	uv run pytest

.PHONY: all install run r color c visualize debug clean fclean \
        lint lint-strict lint-fix check test
