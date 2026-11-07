"""
ダイクストラ法（Dijkstra's Algorithm）をPythonで実装する #Python - Qiita
https://qiita.com/gomagoma000/items/edd3ff714e4d964c670c

このコードは、gomagoma000さんによって執筆されました。
Qiitaの利用規約に基づき、コードのフォーマットを変えてリポジトリ内に保存します。
"""

import heapq


def shortest_path(graph, start, end):
    queue = [(0, start, [])]
    seen = set()
    mins = {start: 0}
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node not in seen:
            seen.add(node)
            path = path + [node]
            if node == end:
                return cost, path

            for next_node, next_cost in graph[node].items():
                prev_cost = mins.get(next_node, None)
                next_cost += cost
                if prev_cost is None or next_cost < prev_cost:
                    heapq.heappush(queue, (next_cost, next_node, path))
                    mins[next_node] = next_cost

    return float("inf"), []


# define graph
graph = {
    'v0': {'v1': 8, 'v2': 3, 'v3': 1},
    'v1': {'v0': 8, 'v2': 3, 'v4': 1},
    'v2': {'v0': 3, 'v1': 3, 'v4': 4},
    'v3': {'v0': 1, 'v4': 2},
    'v4': {'v1': 1, 'v2': 4, 'v3': 2}
}

# Create a list of all vertices
vertices = ['v' + str(i) for i in range(0, 5)]

# Iterate over all pairs of vertices
for start in vertices:
    for end in vertices:
        # Skip if start and end are the same
        if start == end:
            cost, path = '-', '-'
        else:
            cost, path = shortest_path(graph, start, end)
        print(f"{start} to {end} : {cost}, {path}")
