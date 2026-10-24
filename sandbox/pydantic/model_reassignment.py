from pydantic import BaseModel, PositiveInt


class TestModel(BaseModel):
    a: PositiveInt
    b: PositiveInt


print("== TestModelをインスタンス化する ==")
model = TestModel(a=1, b=2)
print(model)

print("== aの値を負の数にする ==")
model.a = -1

print(model)

print("== aの値を負の数にする ==")
model.a = "str"  # type: ignore

print(model)
