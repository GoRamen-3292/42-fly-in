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

#### ダイクストラ法

以下の記事内に掲載されていたコードを、実装した際の参考として利用した。 [コード](../sandbox/dijkstra/python_example.py) はリンク先にある。

- [ダイクストラ法（Dijkstra's Algorithm）をPythonで実装する #Python - Qiita](https://qiita.com/gomagoma000/items/edd3ff714e4d964c670c)

その他、ダイクストラ法の理解に以下の記事を利用した。

- [ダイクストラ法についてまとめてみた【経路探索アルゴリズム】｜らるす](https://note.com/rarusu/n/na7c9ca8ba1a0)
- [マップ上の最短距離を見つけるダイクストラ法を図解でわかりやすく説明 | python実装あり｜スイスのアボカド](https://note.com/avocado81230/n/n1a0e8a835d05)

#### A\* アルゴリズム

今回は採用しなかったが<ruby>A\*<rt>エースター</rt></ruby>アルゴリズムについて調べる際に以下の記事を参照した。

- [【C++日記】A\*アルゴリズム 編｜Frira](https://note.com/fgr_frira/n/n67c0b664140c)

#### DocString

- [GoogleスタイルのPython Docstringの入門 #新人プログラマ応援 - Qiita](https://qiita.com/11ohina017/items/118b3b42b612e527dc1d)
