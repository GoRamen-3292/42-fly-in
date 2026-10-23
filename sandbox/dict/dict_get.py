d: dict[str, str] = {
    "aaa": "bbb",
    "ccc": "ddd",
}

print(d.get("aaa"))  # 出力: bbb
print(d.get("eee"))  # 出力: None
print(d.get("eee", "No value"))  # 出力: No value
