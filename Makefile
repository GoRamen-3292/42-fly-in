# uvのデフォルトのsyncコマンド
install:
	uv sync

run:
	echo "Not implemented yet"

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
	flake8 src
	mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 src
	uv run mypy --strict src
