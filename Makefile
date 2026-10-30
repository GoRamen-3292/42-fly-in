# ディレクトリ
CHECK_PATHS = src sandbox main.py
TEST_PATHS = test

install:
	uv sync

run:
	uv run main.py

debug:
	echo "Not implemented yet (debug mode)"

# DOCS:
# find: ディレクトリ名
# . : cwd
# -type d: ディレクトリに限定
# \( condition \): 条件一覧
# -exec rm -rf {} +: ファイル削除、 {} はファイル名、 +は複数ファイルをまとめてrmで削除するオプション
clean:
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +

lint:
	flake8 $(CHECK_PATHS)
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs $(CHECK_PATHS)

# TODO: test/のルールの見直し
lint-strict:
	uv run flake8 $(CHECK_PATHS)
	uv run mypy --strict $(CHECK_PATHS)
	uv run flake8 --max-line-length 200 $(TEST_PATHS)
	uv run mypy --strict $(TEST_PATHS)

check: lint-strict test
	@echo ">> All checks passed! :D"

test:
	uv run pytest

.PHONY: install run debug clean lint lint-strict test
