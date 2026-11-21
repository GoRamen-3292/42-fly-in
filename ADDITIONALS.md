# Additionals

このドキュメントでは、プロジェクトの実装において追加で参照したり、考慮した点、調べた仕様などについてまとめる。

---

## Words

#### キュー

データ構造について。LIFO(Last in first out)という、最後に追加したものが最後に取り出されるという特性を持つ。

#### ノード

グラフ理論における、接続を表すもの。

#### エッジ

グラフ理論における、

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

## heapq

<!-- TODO:  -->

---

## argparse

argparseは、コマンドライン引数をパースするための標準ライブラリであり、終了時には自動的に`SystemExit` を送出する。

これはExceptionクラスの子クラスではないため、`except Exception` でcatchすることはしなかった。

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
- `model.test = 3` のような、モデルの属性に値を代入したときにはvalidateしない
  - オプションで変更可能。 See also: [Configuration | Pydantic Docs](https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_assignment)

---

## Ruff

Ruffは、Pythonのコードを静的に分析し品質を向上させるためのツールである。

flake8よりも高速である上、追加のルールの指定などをすることができるため、今回のプロジェクトではflake8とruffの両方を利用した。

しかしながら、課題提出の際にflake8でのチェックがあるため、今回はflake8も依存関係に追加し、またチェックをするようにした。

---

## Makefile

## @から始まる行

- コマンドの通常のオプションには表示されない

[GNU make](https://www.gnu.org/software/make/manual/make.html#Echoing)

## -から始まる行

- 終了コードが0以外で失敗しても、makeはそのエラーを無視して次のコマンドを実行する

[GNU make](https://www.gnu.org/software/make/manual/make.html#Errors)

