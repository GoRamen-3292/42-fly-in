from pydantic import BaseModel, ValidationError, field_validator


class InvalidConfigError(ValueError):
    """無効な設定ファイルのエラーを表すカスタムエラー"""


class TestModel(BaseModel):
    """テスト用のモデル"""

    name: str
    age: int

    @field_validator("age")
    def validate_age(cls, value: int) -> int:
        if value < 0:
            raise InvalidConfigError("Age must be a non-negative integer")
        return value


if __name__ == "__main__":
    # 正しいデータの例
    try:
        model = TestModel(name="Alice", age=30)
        print(model)
    except ValidationError as e:
        print(f"Validation error: {e}")

    # 無効なデータの例
    try:
        model = TestModel(name="Bob", age=-5)
    except ValidationError as e:
        print(e.errors())

        print()

        for error in e.errors():
            ctx = error.get("ctx")

            if not ctx:
                continue
            print(
                f"{ctx}",
                "",
                f"Error: {error}",
            )

            print()
