# Pydantic

Pydanticのモデルの振る舞いなどについてまとめる・

## Pydanticが値をvalidateするタイミング

- Pydanticはモデルのインスタンス化をしたときにvalidateする
- `model.test = 3` のような、モデルの属性に値を代入したときにはvalidateしない
  - オプションで変更可能。 See also: [Configuration | Pydantic Docs](https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_assignment)
