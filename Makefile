# ディレクトリ
CHECK_PATHS = src sandbox main.py
TEST_PATHS = test
CACHE_DIRS = .mypy_cache .pytest_cache
MAP = test.txt

install:
	uv sync

run:
	@uv run main.py $(MAP)

debug:
	echo "Not implemented yet (debug mode)"

# DOCS:
clean:
	-uv run ruff clean
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf $(CACHE_DIRS)

fclean: clean
	rm -rf .venv

# TODO: ${CHECK_PATHS} を cwd `.` で置き換える
lint:
	uv run mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs $(CHECK_PATHS)
	uv run flake8 $(CHECK_PATHS)

# TODO: $(TEST_PATHS) のルールの見直し、先頭の `-` の条件の見直し
lint-strict:
	uv run mypy --strict $(CHECK_PATHS) $(TEST_PATHS)
	uv run flake8 --disable-noqa $(CHECK_PATHS)
	uv run flake8 --max-line-length 200 --disable-noqa $(TEST_PATHS)
	-uv run ruff check $(CHECK_PATHS) $(TEST_PATHS)

# TODO: 先頭の `-`の条件の見直し
lint-fix:
	uv run ruff format $(CHECK_PATHS) $(TEST_PATHS)
	-uv run ruff check --fix $(CHECK_PATHS) $(TEST_PATHS)

check: lint-strict test

test:
	uv run pytest

.PHONY: install run debug clean lint lint-strict lint-fix check test
