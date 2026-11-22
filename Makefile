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
	echo "Not implemented yet (debug mode)"

clean:
	-uv run ruff clean
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf $(CACHE_DIRS)

fclean: clean
	rm -rf .venv

# TODO: ${CHECK_PATHS} を cwd `.` で置き換える
lint:
	uv run mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs .
	uv run flake8 .

lint-strict:
	uv run mypy --strict .
	uv run flake8 --disable-noqa .
	-uv run ruff check .
lint-fix:
	uv run ruff format .
	-uv run ruff check --fix .

check: lint-strict


.PHONY: all install run r color c visualize debug clean fclean \
        lint lint-strict lint-fix check
