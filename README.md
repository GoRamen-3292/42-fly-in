_This project has been created as part of the 42 curriculum by ktomita._

# Fly-in

## Description

## Instructions

今回の開発環境は、以下の通りです。

- uv: 

## Resources

## Additional Notes

### Makefile

#### コマンド先頭のprefix

コマンド先頭の `-` は、終了コードが0でなくても続行するというオプションです

```sh
example-rule:
    -uv run ruff check
    @echo "これは常に実行されます！"
```

のように書けば、末尾のechoは常に実行されます！

(なお、コマンド先頭の `@` は `make example-rule` を実行した際に `echo "これは常に実行されます！"`を表示しないオプションとなっています。)

参考:

- [makefile - Make: how to continue after a command fails? - Stack Overflow](https://stackoverflow.com/questions/2670130/make-how-to-continue-after-a-command-fails)
- [Top (GNU make)](https://www.gnu.org/software/make/manual/html_node/index.html)

### findコマンド

```txt
find: コマンド
. : cwd
-type d: ディレクトリに限定
\( condition \): 条件
-exec rm -rf {} +: ファイル削除、 {} はファイル名、 +は複数ファイルをまとめてrmで削除するオプション
```

### argparse

すごく例外的なケースを除いて例外を発生させない

- TODO: 検証

### Others

- [ ] A detailed description of your algorithm choices and implementation strategy must 
  also be included.
- [ ] Documentation of the visual representation features and how they enhance the user
  experience.
- [ ] Example input and expected output demonstrating the program’s functionality.

## スケジュール

- 2026-10-21: リポジトリ作成
- 2026-11-04: DEADLINE
