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

---

## pytest

基本的には、`test_` で始まる関数を定義することで、pytestはその関数をテストとして認識する。`assert` 文を使って条件をチェックし、失敗した場合はテストが失敗する。

### raises

pytest.raises() を使って、例外が発生することを確認するテストを作成できる。

- [【Python3】pytestで例外を検出する方法 #メモ - Qiita](https://qiita.com/Jazuma/items/cb8dcd9ff01ed1c2d1f2)
- [API Reference - pytest documentation](https://docs.pytest.org/en/stable/reference/reference.html#pytest.raises)

---

## Pydantic

Pydanticのモデルの振る舞いなどについてまとめる・

### Pydanticが値をvalidateするタイミング

- Pydanticはモデルのインスタンス化をしたときにvalidateする
- `model.test = 3` のように、モデルの属性に値を代入したときにはvalidateは発生しない
  - これはオプションで変更可能。 [Configuration | Pydantic Docs](https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_assignment)

---

## Ruff

Ruffは、Pythonのコードを静的に分析し品質を向上させるためのツールである。

flake8よりも高速である上、追加のルールの指定などをすることができるため、今回のプロジェクトではflake8とruffの両方を利用した。課題提出の際にflake8でのチェックがあるためである。

なお、mypyの持つ型チェッカーの機能はRuffにはない。

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

