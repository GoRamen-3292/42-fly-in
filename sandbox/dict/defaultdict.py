from collections import defaultdict

result: defaultdict[int, list[str]] = defaultdict(list)

for i in range(10):
    for j in range(26):
        c = chr(ord('A') + j)
        result[i].append(c)

print(result)
