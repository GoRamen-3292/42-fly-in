_This project has been created as part of the 42 curriculum by ktomita._

# Fly-in

## Description

この課題は、与えられた制約下ですべてのドローンをスタートからゴールまでなるべく少ない手数で移動させるというシミュレーションをするプログラムを作成する問題である。
これらの課題は、マルチエージェント・パスファインディング問題(MAPF) という問題に一般化できます。

言語は Python 3.10以降で、既存のグラフ系のライブラリを利用することは禁じられています。

これらの課題を通して、以下のことを学習しました。

- A-maze-ingから引き続き学習していた、グラフ理論について
- ダイクストラ法、アルゴリズムについて
- オブジェクト指向プログラミング / Pythonでのプログラムの設計について
- Pydanticを用いたデータのバリデーションについて
- Ruffなどの静的解析ツールを用いたコードの品質向上について
- ...

### 与えられている制約

#### Hub - ハブ

- スタートのHubとゴールのHubが1つずつ与えられる
- それ以外のHubが0個以上与えられる
- Hubの座標は整数で与えられる
- Hubには最大1台、設定で指定された場合には複数台のドローンが同時に存在することができる

#### Drone - ドローン

- Droneの数は1以上の整数で与えられる
- DroneはHubとHubの間を原則1ターン、restrictedという属性を持つHubに移動する際には2ターンをかけて移動する
- ...

#### Connection - ハブ間の接続

- Connectionは、HubとHubの間の接続を表す
- この接続は、双方向である
- この接続には上限が存在する

---

## Prerequirements

このプログラムの実行には、以下のソフトウェアが必要である。

- uv: https://docs.astral.sh/uv/
- Python: バージョン 3.14 or 3.15、端末内で利用できない場合にはuvを用いて自動的にインストールされる

また、Makefileを利用するためには端末にGNU makeがインストールされている必要がある。(以降、本ソフトウェアについては make と表記する)

---

## Instructions

### 1. インストール・セットアップ

#### make

make が端末でインストールされている場合、以下のコマンドを利用することで
必要な依存関係をインストールすることができる。

```sh
make
```

実行後に、このコマンドについてヘルプ画面を出力する。`make install` を実行した場合には表示されない。

#### uv

make が利用できない場合、以下のコマンドを利用することでインストールを実行することができる。

```sh
uv sync
```

### 2. マップの作成

マップやドローンの数などの設定を含んだ設定ファイルを作成する。

`make run` や `make color` コマンドはデフォルトでは、config.txt を利用して実行される。

もし、example.txt を config.txt にコピーしたい場合には、以下のコマンドを実行する。

```sh
make config.txt  # make を利用する場合
cp example.txt config.txt  # make を利用しない場合
```

<!-- Input / output をリンクに -->

設定ファイルのフォーマットについては、[Input / Output](#input--output) セクションを参照すること。

### 3. 実行

#### make

make を利用して実行する場合、以下のコマンドを実行することができる。

```sh
# 色つき
make color MAP=/path/to/file
#  あるいはエイリアス: make c MAP=/path/to/file
#  あるいはエイリアス: make visualize MAP=/path/to/file

# 色なし
make run MAP=/path/to/file
#  あるいはエイリアス: make r MAP=/path/to/file
```

MAPの引数を利用しなかった場合、デフォルトのマップ `config.txt` を利用して実行します。

```sh
make color MAP=/path/to/file
# あるいはエイリアス: make c MAP=/path/to/file
```

#### uv

make を利用しない場合には、以下のコマンドを実行してください。

```sh
uv run main.py /path/to/file
```

---

## Input / Output

### 入力: 設定ファイル

#### 基本的な構文

以下について、`<0以上の数字>` のように`<` と `>` で挟まれた文字を `42` のように、`<` や `>` を含めずに置き換えてください。

```txt
キー: <値1> <値2> <...> [オプション1=値 オプション2=値]
```

`[]`

`str.isspace()` 関数でTrueを返す任意の文字を区切り文字として扱います。このため、値やオプションにこれらの文字を利用することはできません。

空行は無視され、`#`から始まる行はコメントとして扱われます。なお、文の途中の `#` についてはコメントとして扱われません。このため、ハブの名前に `#` を含めることは可能だ。

#### ドローンの数

```txt
nb_drones: <1以上の数字>
```

フォーマットの例については `example.txt` を参照してください。

#### ハブ

```txt
# 通常のハブ
hub: <ハブの名前> <x座標> <y座標>

# 開始地点
start_hub: <ハブの名前> <x座標> <y座標>

# 終了地点
end_hub: <ハブの名前> <x座標> <y座標>
```

#### ハブ間の接続

```txt
# ハブ間の接続
connection: <ハブの名前1> <ハブの名前2>
```

### 出力: ターミナル

以下のようなフォーマットで出力される。

<!-- TODO: 続きを書く -->

```txt
D1-hub
```

---

## Algorithm

このセクションでは、アルゴリズムについて解説する。

### 概要

このプログラムでは、ダイクストラ法を用いてそれぞれのドローンに対して最短の経路となるものを求めたあと、それをさらにPrioritized Planningと呼ばれる方法で貪欲に順番にすべてのドローンそれぞれに対して経路を求めた。

<!-- TODO: オーダーについて書く -->

### ダイクストラ法とは?

- 最短経路を算出するためのアルゴリズム
- それぞれのnodeに対して最短の距離を算出して保存する
- ゴールまでの経路を見つけた後、最短距離となる経路をスタートへとたどっていくことで最短経路を算出する

#### 具体的には?

スタート地点のノードとそこに到達するためのコスト(0) を優先度付きキューに追加したあと、以下のことを繰り返す。

1. キューの中から最小のコストとなるノードを取得し、キューからは削除する。
1. それを「訪れた」とマークする。
1. 現在のノードとエッジにより接続されている、まだ訪れていないノードに対して以下のことをする。

- それぞれ、そこまで現在のノードから到達した場合のコストを算出する。
- もし、そのコストが現時点とのその最小コストより低い場合、またはまだコストが未設定である場合には、現在のコストで置き換える。

その上で、ゴールのハブに到達した場合には、そこまでの最短経路を算出することができる。

### Prioritized Planningとは?

Prioritized Planning（優先順位付け計画）は、複数のタスクやアクションを優先順位に従って処理するための手法である。

### 今回の課題では

今回の課題では、1つのドローンではなく複数のドローンを用いて動かす。

そのため、今回は個別のドローンのルートの探索についてはダイクストラ法を用いたのだが。貪欲法と呼ばれるアルゴリズムを用いて最短経路を算出したあとに、それぞれのドローンが移動する際に、他のドローンと行動が重複しないようにしつつ、それぞれのドローンがその時点で最適な経路をたどるようにする。

#### 具体的には?

- まず、スタート地点とそのコストを優先度付きキューに追加

その上で、以下のことを繰り返す。

1. キューから最小のコストとなり、かつ同じコストである場合には優先度が高い移動パターンを1つ取り出す
1. 取り出したものと隣接するHubへ移動した場合、またはその場にとどまることの選択肢を取る行動パターンについて、それぞれ以下の操作をする

- 他のドローンの行動予定とそれが重複しないかどうか検証する
- もし、行動が重複しない場合にはその移動パターンをキューに追加する
- 移動パターンが他と一致しないなら、キューに追加する

これらのアルゴリズムは、ルートの種類によっては必ずしも最適な解を導き出すとは限らないが、今回の課題の付属のマップのにおいてはすべて最適解を導くことができた。

#### heapqの使い方について

今回は、これらのデータの取り出しや追加の操作を効率的に行うために、Pythonの標準ライブラリであるheapqを利用した。

heapqは、リストへの要素の取り出しや操作を効率的に行うことができるライブラリである。heapqを利用することで、リストの中から値が最小の要素を取り出す操作や、要素の追加を効率的に行うことができる。なお、heapq は既存の`list`型を用いる。

##### 利用方法

1. 要素が空である場合のみ、 `heapq.heaplify()` 関数を利用して、リストをヒープに変換する。
2. `heapq.heappush()` 関数を利用して、要素をヒープに追加する。
3. `heapq.heappop()` 関数を利用して、ヒープから最小の要素を取り出す。

---

## Schedule

| 時期         | PR       | 内容                                                    | 主に利用したこと・学んだこと                     |
| ------------ | -------- | ------------------------------------------------------- | ------------------------------------------------ |
| 10/21〜10/24 | #1       | 各種モデルの定義（Hub / Connection / SimulationConfig） | uv、Pydantic、Enum                               |
| 10/24〜10/29 | #2       | パーサー、ファイルの読み込み                            | pytest.parametrize、str.partition、str.isspace   |
| 10/29〜11/08 | #3       | Simulator、Dijkstra 法 + Scheduler                      | heapq、dataclass                                 |
| 11/09〜11/13 | #4〜#11  | restricted / priority への対応、argparse、Ruff の導入   | argparse の終了の仕方、Ruff                      |
| 11/14〜11/16 | #12〜#16 | color出力、例外処理、ディレクトリの再構成、docstring    | 終了コード、パッケージにしない構成、Google Style |
| 11/17〜11/20 | #18、#19 | パーサーのエラーに行番号を付与、Simulator の整理        | ValidationError の構造                           |
| 11/21 —      |          | ドキュメント、Makefileの微調整                          | Make の各種ルール                                |

---

## Resources

### AI Usage

今回のプロジェクトでは、AIを次のように利用しました。

- Pythonや各種ライブラリをDocumentationを調べること
- リスト内包表記など、より良いコードの書き方について
- DocStringの生成
- READMEの執筆の補助
- "Reduce repetitive or tedious tasks" の目的のためのGitHub CopilotのTab補完の利用
- メインとなるダイクストラ法のアルゴリズムの着想や、一度執筆したコードの修正の方針を考える際の補助

全てのコードを完全に理解した上で、部分的に用いたAIが生成したコードをレビューし必要に応じて修正を加えました。これらはすべて、AI Instructionsのガイドラインに従って行いました。

### Websites

#### Python 3.14.x / 3.15.x

Pythonのドキュメントの仕様について、常に公式のドキュメントを読むようにした。また、sandboxディレクトリ内で実際に実装をしてみて仕様を把握するようにもした。

なお、一部AIを活用して動作の検証やドキュメントの確認などを進めた箇所もあった。

- [Python 3.15.2 documentation](https://docs.python.org/3.15)
- [Python 3.14.10 documentation](https://docs.python.org/3.14/)

#### Pydantic

今回の実装では、Pydanticの仕様に大きく依存する形になっていた。そのため、Pydanticのドキュメントも大いに参照した。

- [Pydantic Validation | Pydantic Docs](https://pydantic.dev/docs/validation/2.14/get-started/)
- [Models | Pydantic Docs](https://pydantic.dev/docs/validation/2.14/usage/models/)
- [BaseModel | Pydantic Docs](https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/)

#### MAPF

MAPFと呼ばれる言葉については、主に以下の記事を参照した。

- [Multi-agent pathfinding](https://en.wikipedia.org/wiki/Multi-agent_pathfinding)
- [マルチエージェント経路計画の紹介 | Kei18's Note](https://kei18.github.io/note/posts/mapf-tutorial/#%e6%9c%80%e9%81%a9%e6%80%a7%e3%82%92%e7%8a%a0%e7%89%b2%e3%81%ab%e3%81%99%e3%82%8b-%e6%9c%89%e7%95%8c%e6%ba%96%e6%9c%80%e9%81%a9%e6%80%a7%e3%81%aa%e3%82%a2%e3%83%ab%e3%82%b4%e3%83%aa%e3%82%ba%e3%83%a0)

#### ダイクストラ法

以下の記事内に掲載されていたコードを、実装した際の参考として利用した。 [コード](./sandbox/dijkstra/python_example.py) はリンク先にある。

- [ダイクストラ法（Dijkstra's Algorithm）をPythonで実装する #Python - Qiita](https://qiita.com/gomagoma000/items/edd3ff714e4d964c670c)

その他、ダイクストラ法の理解に以下の記事を利用した。

- [ダイクストラ法についてまとめてみた【経路探索アルゴリズム】｜らるす](https://note.com/rarusu/n/na7c9ca8ba1a0)
- [マップ上の最短距離を見つけるダイクストラ法を図解でわかりやすく説明 | python実装あり｜スイスのアボカド](https://note.com/avocado81230/n/n1a0e8a835d05)
- [うさぎでもわかる離散数学（グラフ理論）　第14羽　ダイクストラ法による最短経路の求め方 - 工業大学生ももやまのうさぎ塾 (Momousagi Academy)](https://www.momoyama-usagi.com/entry/math-risan14#gsc.tab=0)
- [【これでわかる！】具体例を使ってダイクストラ法のアルゴリズムについてなるべくわかりやすく解説してみた](https://yukashun.com/shortest_path_dijkstra/)

#### A\* アルゴリズム

今回は採用しなかったが<ruby>A\*<rt>エースター</rt></ruby>アルゴリズムについて調べる際に以下の記事を参照した。

- [【C++日記】A\*アルゴリズム 編｜Frira](https://note.com/fgr_frira/n/n67c0b664140c)

#### DocString

- [GoogleスタイルのPython Docstringの入門 #新人プログラマ応援 - Qiita](https://qiita.com/11ohina017/items/118b3b42b612e527dc1d)

---

## Others

今回のこの作品を作るにあたってした判断や、細かな仕様については[ADDITIONALS.md](./ADDITIONALS.md), [DECISIONS.md](./DECISIONS.md) にまとめている。
