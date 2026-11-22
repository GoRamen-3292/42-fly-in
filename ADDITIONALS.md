# Additionals

このドキュメントでは、プロジェクトの実装において追加で参照したり、考慮した点、調べた仕様などについてまとめる。

---

## Enum

Enumのメンバーは慣習的に**大文字**で書かれる。

See also: [列挙型 HOWTO — Python 3.14.9 ドキュメント](https://docs.python.org/ja/3.14/howto/enum.html)

---

## グラフ理論について

### ノードとエッジについて

- node: 他とつながれるもののこと
- edge: 他との接続のことを指す

---

## argparse

argparseは、コマンドライン引数をパースするための標準ライブラリであり、終了時には自動的に`SystemExit` を送出する。

これはExceptionクラスの子クラスではないため、`except Exception` ではcatchできない。

### 終了時の挙動

`ArgumentParser` の `exit_on_error` によって、エラー時の挙動が変動する。

| 状況                                           | `exit_on_error=True`（デフォルト） | `exit_on_error=False` |
| ---------------------------------------------- | ---------------------------------- | --------------------- |
| 型変換の失敗・未知のオプション・必須引数の不足 | `SystemExit(2)`                    | `ArgumentError`       |
| `-h` / `--help`                                | `SystemExit(0)`                    | `SystemExit(0)`       |

- `-h` / `--help` は、`exit_on_error` の値にかかわらず `SystemExit(0)` を送出する。
- `add_argument` の定義自体に誤りがある場合には、`ArgumentError`、`ValueError`、`TypeError` のいずれかが発生する。

---

## pytest

基本的には、`test_` で始まる関数を定義することで、pytestはその関数をテストとして認識する。`assert` 文を使って条件をチェックし、失敗した場合はテストが失敗する。

### raises

pytest.raises() を使って、例外が発生することを確認するテストを作成できる。

`as exc_info` で受け取った `ExceptionInfo` オブジェクトからは、`.type`、`.value`、`.traceback` を参照できる。

```python
with pytest.raises(ValueError, match="invalid") as exc_info:
    parse("...")

print(exc_info.type)  # <class 'ValueError'>
print(exc_info.value)  # ValueError('invalid literal for int() with base 10: 'abc'')
print(str(exc_info.value))  # 'invalid literal for int() with base 10: 'abc''
```

- `exc_info` に対する `assert` は、`with` ブロックの**外**に書く。ブロックの中で例外が発生した時点で処理が終了するからである。
- メッセージの確認には `match=` を使う。例外の属性を確認したい場合には、pytest 8.4 以降で `check=` を使うことができる。

- [【Python3】pytestで例外を検出する方法 #メモ - Qiita](https://qiita.com/Jazuma/items/cb8dcd9ff01ed1c2d1f2)
- [API Reference - pytest documentation](https://docs.pytest.org/en/stable/reference/reference.html#pytest.raises)

---

## Pydantic

Pydanticのモデルの振る舞いなどについて

### Pydanticが値をvalidateするタイミング

- Pydanticはモデルのインスタンス化をしたときにvalidateする
- `model.test = 3` のように、モデルの属性に値を代入したときにはvalidateは発生しない
  - これはオプションで変更可能。 [Configuration | Pydantic Docs](https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_assignment)

### validator 内で発生させた例外の扱い

- validator の中で発生した `ValueError` / `AssertionError` などは、`ValidationError` にまとめられる。
  - 元の例外のインスタンスは、`e.errors()[i]["ctx"]["error"]` から取り出すことができる。

### model_post_init() の実行タイミング

| 呼び出し                                   | `model_post_init`                |
| ------------------------------------------ | -------------------------------- |
| `M(...)` / `model_validate` が成功したとき | 呼ばれる                         |
| バリデーションが失敗したとき               | 呼ばれない                       |
| `model_construct()`                        | 呼ばれる、ただし**値はvalidateされていない**） |
| `model_copy()`                             | 呼ばれない                       |

呼ばれる順番は、`field_validator` → `model_post_init` → `model_validator(mode="after")` である。

### 余分なキー

モデルに定義されていないキーの扱いは、`extra` の設定によって変わる。今回は、これを `forbid` に設定した。

- `"ignore"`（既定）: 無視される
- `"forbid"`: `ValidationError` になる
- `"allow"`: `model_extra` に格納される

---

## Ruff

Ruffは、Pythonのコードを静的に分析し品質を向上させるためのツールである。

flake8よりも高速である上、追加のルールの指定などをすることができるため、今回のプロジェクトではflake8とruffの両方を利用した。課題提出の際にflake8でのチェックがあるためである。

なお、mypyの持つ型チェッカーの機能はRuffにはない。このため、型のチェックにはmypyを併用した。

また、flake8のデフォルトの1行の最大文字数に合わせるため、`line-length = 79` を設定した。

---

## uv

### パッケージとして扱わない設定

`pyproject.toml` に `[build-system]` が定義されていると、`uv sync` や `uv run` を実行した際にプロジェクト自身もビルドされてインストールされる。

この課題ではルートディレクトリの `main.py` から実行する構成にするため、パッケージ化をしないように、`pyproject.toml` に以下を記述した。

```toml
[tool.uv]
package = false
```

新規にプロジェクトを作成する場合には、`uv init --no-package` を利用しても同様の構成になる。

なお、ビルドシステムが定義されているにもかかわらずパッケージのディレクトリが存在しない場合には、`Expected a Python module at: src/???/__init__.py` というエラーが発生する。

---

## Makefile

```makefile
example-rule:
    -uv run ruff check
    @echo "これは常に実行されます！"
```

### @から始まる行

コマンド先頭の `@` は `make example-rule` を実行した際に `echo "これは常に実行されます！"`というコマンドそのものの出力を表示しないオプションとなっています。

### -から始まる行

コマンド先頭の `-` は、終了コードが0でなくても続行するというオプションである。このため、末尾のechoは常に実行される。

- [makefile - Make: how to continue after a command fails? - Stack Overflow](https://stackoverflow.com/questions/2670130/make-how-to-continue-after-a-command-fails)
- [GNU make - 5.2 Recipe Echoing](https://www.gnu.org/software/make/manual/make.html#Echoing)
- [GNU make - 5.5 Errors in Recipes](https://www.gnu.org/software/make/manual/make.html#Errors)

### .PHONY

.PHONYは、makefileのターゲットがファイル名と同じ名前であっても、常にそのターゲットを実行するようにするための宣言です。

これにより、ターゲット名と同じ名前のファイルが存在しても、makeはそのターゲットを実行することが保証されます。

[GNU make - 4.9 Special Built-in Target Names](https://www.gnu.org/software/make/manual/make.html#Special-Targets)

---

## findコマンド

```txt
find: コマンド
. : cwd
-type d: ディレクトリに限定
\( condition \): 条件
-exec rm -rf {} +: ファイル削除、 {} はファイル名、 +は複数ファイルをまとめてrmで削除するオプション
```

---

## DocString

Googleスタイルを利用。なお言語についての規定はなかったため、日本語で書くことにした。なお、その際にDocStringの1行目の末尾にピリオドを要求するRuffのエラーが発生したため、`D415`ルールを無視するように設定した。
