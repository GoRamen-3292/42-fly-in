## Instructions

### 1. インストール・セットアップ

#### make

make が端末でインストールされている場合、以下のコマンドを利用することで
必要な依存関係をインストールすることができます。

```sh
make
```

実行後に、このコマンドについてヘルプ画面を出力します。`make install` を実行した場合には表示されません。

#### uv

make が利用できない場合、以下のコマンドを利用することでインストールを実行することができます。

```sh
uv sync
```

### 2. マップの作成

マップを含んだファイルを作成します。

マップのフォーマットについては、Input / Output セクションを参照してください。

<!-- TODO: Input / Output セクション -->

### 3. 実行

#### make

make を利用して実行する場合、以下のコマンドを実行することができます。

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
