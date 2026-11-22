_This project has been created as part of the 42 curriculum by ktomita._

# Fly-in

## Description

This project is a program that simulates moving every drone from the start to the goal in as few turns as possible under the given constraints.
This kind of problem can be generalized as the Multi-Agent Path Finding problem (MAPF).

In this project, the subject specifies the use of Python 3.10 or later, and the use of existing graph libraries is forbidden.

Through this project, I learned the following:

- Graph theory, which I had continued studying since A-maze-ing
- Dijkstra's algorithm and algorithms in general
- Object-oriented programming / program design in Python
- Data validation with Pydantic
- Improving code quality with static analysis tools such as Ruff
- ...

### Given constraints

#### Hub

- Exactly one start hub and one end hub are given
- Zero or more other hubs are given
- Hub coordinates are given as integers
- A hub can hold at most one drone at a time, or multiple drones if specified in the configuration
- `priority` and `restricted` are attributes that can be assigned to a hub

#### Drone

- The number of drones is given as an integer of 1 or more
- A drone moves between hubs in 1 turn as a rule, and takes 2 turns when moving to a hub with the `restricted` attribute
- ...

#### Connection

- A connection represents a link between two hubs
- Connections are bidirectional
- Connections have a capacity limit

---

## Prerequirements

The following software is required to run this program.

- uv: https://docs.astral.sh/uv/
- Python: version 3.14 or 3.15; if it is not available on your machine, it is installed automatically by uv

In addition, GNU make must be installed to use the Makefile. (Hereafter, this software is referred to as make.)

---

## Instructions

### 1. Installation / Setup

#### make

If make is installed on your machine, you can install the required dependencies with the following command.

```sh
make
```

After it runs, a help screen for the commands is printed. It is not shown when you run `make install`.

#### uv

If make is not available, you can install with the following command.

```sh
uv sync
```

### 2. Creating a map

Create a configuration file containing the map, the number of drones, and other settings.

By default, the `make run` and `make color` commands use config.txt.

If you want to copy example.txt to config.txt, run the following command.

```sh
make config.txt  # when using make
cp example.txt config.txt  # when not using make
```

For the configuration file format, see the [Input / Output](#input--output) section.

### 3. Running

#### make

To run with make, you can use the following commands.

```sh
# With color
make color MAP=/path/to/file
#  or alias: make c MAP=/path/to/file
#  or alias: make visualize MAP=/path/to/file

# Without color
make run MAP=/path/to/file
#  or alias: make r MAP=/path/to/file
```

If the MAP argument is omitted, the default map `config.txt` is used.

```sh
make color
make run
# or alias: make c
# or alias: make r
```

#### uv

If you do not use make, run the following command.

```sh
uv run main.py /path/to/file
```

---

## Input / Output

### Input: configuration file

#### Basic syntax

In the following, replace text enclosed in `<` and `>`, such as `<a number of 0 or more>`, with a value such as `42`, without including the `<` and `>`.

```txt
key: <value1> <value2> <...> [<option1>=<value> <option2>=<value>]
```

The part enclosed in `[]` is optional and may be omitted.

Any character for which `str.isspace()` returns True is treated as a delimiter. Therefore, these characters cannot be used in values or options.

Empty lines are ignored, and lines starting with `#` are treated as comments. Note that a `#` in the middle of a line is not treated as a comment, so a hub name may contain `#`.

#### Number of drones

```txt
nb_drones: <a number of 1 or more>
```

See `example.txt` for an example of the format.

#### Hubs

```txt
# Regular hub
hub: <hub name> <x coordinate> <y coordinate>

# Start point
start_hub: <hub name> <x coordinate> <y coordinate>

# End point
end_hub: <hub name> <x coordinate> <y coordinate>
```

#### Connections between hubs

```txt
# Connection between hubs
connection: <hub name 1> <hub name 2>
```

### Output: terminal

The output is printed in the following format.

```
$ make run
D1-loop_a D2-loop_a
D1-loop_b D3-loop_a
D1-loop_b-exit_point D2-loop_b D4-loop_a
...
```

The first line shows each drone's action in turn 1, the second line shows each drone's action in turn 2, and so on.

---

## Algorithm

This section explains the algorithm.

### Overview

This program uses a method called Prioritized Planning: for each drone in turn, it repeatedly finds the shortest path currently available, records it once the order is decided, and then finds a path for the next drone. Each shortest path is computed with Dijkstra's algorithm.

By greedily finding a path for every drone one after another in this way, the program does not always finish in the optimal number of turns, but it always produces a valid solution as long as there is at least one route from the start to the goal. In addition, for all the maps provided with the subject, it produced solutions with the optimal number of turns required by the subject.

### Time complexity

Let V be the number of hubs, E the number of connections, D the number of drones, and T the upper bound on the number of turns (`2(V − 1) + D − 1`).

For each drone, a Dijkstra search is run with "(turn, hub)" as the state, and this is repeated for every drone.

The complexity is obtained by multiplying the following:

- **D**: the search is repeated once per drone
- **T · (V + E)**: the number of moves tried in one search. There are at most T·V states, and from each one we try "wait" and "move to an adjacent hub"
- **E + log(T·V)**: the cost per move. Checking connection capacity takes O(E), and pushing the next hub to explore onto heapq takes O(log(T·V))

Therefore, the complexity is
`O(D · T · (V + E) · (E + log(T·V)))`

### What is Dijkstra's algorithm?

- An algorithm for computing shortest paths
- It computes and stores the shortest distance to each node
- After finding a path to the goal, it computes the shortest path by tracing back from the goal to the start along the minimum-distance route

#### More specifically?

After adding the start node and the cost to reach it (0) to a priority queue, repeat the following:

1. Take the node with the lowest cost from the queue and remove it from the queue.
1. Mark it as "visited".
1. For each unvisited node connected to the current node by an edge, do the following:
    - Compute the cost of reaching it from the current node.
    - If that cost is lower than its current minimum cost, or if its cost has not been set yet, replace it with this cost.

Then, once the goal hub is reached, the shortest path to it can be computed.

### In this project?

The shortest path for each drone was computed with the following flow.

- First, add the start point and its cost to the priority queue

Then, repeat the following:

1. Take one movement pattern from the queue that has the lowest cost and, among those with the same cost, the highest priority, taking into account whether the hub has the `priority` attribute
1. For each action pattern derived from it — moving to an adjacent hub or staying in place — do the following:
    - Check whether it conflicts with the planned actions of other drones
    - If the action does not conflict, add that movement pattern to the queue

#### How heapq is used

To perform these retrieval and insertion operations efficiently, I used heapq from Python's standard library.

heapq is a library that allows efficient retrieval and manipulation of list elements. With heapq, you can efficiently take the smallest element from a list and add elements to it. Note that heapq works on the existing `list` type.

To determine which value is the smallest, heapq internally compares elements with the `<` operator.

A heap is a data structure: a tree in which each parent node's value is smaller (or larger) than its children's values. It is used in algorithms such as heap sort, and here it was used to make the priority queue implementation efficient.

##### Usage

1. Use an empty list, or, only if it is not empty, initialize the list as a heap with the `heapq.heapify()` function.
1. Add elements to the heap with the `heapq.heappush()` function.
1. Take the smallest element from the heap with the `heapq.heappop()` function.

---

## Schedule

| Period        | PR         | Content                                                         | Main things used / learned                          |
| ------------- | ---------- | --------------------------------------------------------------- | --------------------------------------------------- |
| 10/21–10/24   | #1         | Defining models (Hub / Connection / SimulationConfig)           | uv, Pydantic, Enum                                  |
| 10/24–10/29   | #2         | Parser, file loading                                            | pytest.parametrize, str.partition, str.isspace      |
| 10/29–11/08   | #3         | Simulator, Dijkstra's algorithm + Scheduler                     | heapq, dataclass                                    |
| 11/09–11/13   | #4–#11     | Support for restricted / priority, argparse, introducing Ruff   | How argparse exits, Ruff                            |
| 11/14–11/16   | #12–#16    | Color output, exception handling, directory restructure, docstrings | Exit codes, non-package layout, Google Style    |
| 11/17–11/20   | #18, #19   | Line numbers in parser errors, cleaning up the Simulator        | Structure of ValidationError                        |
| 11/21 —       |            | Documentation, minor Makefile adjustments                       | Various Make rules                                  |

---

## Resources

### AI Usage

In this project, I used AI in the following ways:

- Looking up documentation for Python and various libraries
- Better ways to write code, such as list comprehensions
- Generating docstrings
- Assisting with writing the README
- Using GitHub Copilot's Tab completion for the purpose of "Reduce repetitive or tedious tasks"
- Assisting with the idea for the main Dijkstra-based algorithm and with deciding how to revise code I had already written

I fully understood all of the code, reviewed the AI-generated code that I partially used, and modified it as needed. All of this was done in accordance with the AI Instructions guidelines.

### Websites

#### Python 3.14.x / 3.15.x

For the specification of Python, I always made a point of reading the official documentation. I also implemented things in the sandbox directory to understand the behavior.

In some places, I also used AI to help verify behavior and check documentation.

- [Python 3.15.2 documentation](https://docs.python.org/3.15)
- [Python 3.14.10 documentation](https://docs.python.org/3.14/)

#### Pydantic

The implementation relies heavily on Pydantic's behavior, so I referred to the Pydantic documentation extensively.

- [Pydantic Validation | Pydantic Docs](https://pydantic.dev/docs/validation/2.14/get-started/)
- [Models | Pydantic Docs](https://pydantic.dev/docs/validation/2.14/usage/models/)
- [BaseModel | Pydantic Docs](https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/)

#### MAPF

For the term MAPF, I mainly referred to the following articles.

- [Multi-agent pathfinding](https://en.wikipedia.org/wiki/Multi-agent_pathfinding)
- [マルチエージェント経路計画の紹介 | Kei18's Note](https://kei18.github.io/note/posts/mapf-tutorial/#%e6%9c%80%e9%81%a9%e6%80%a7%e3%82%92%e7%8a%a0%e7%89%b2%e3%81%ab%e3%81%99%e3%82%8b-%e6%9c%89%e7%95%8c%e6%ba%96%e6%9c%80%e9%81%a9%e6%80%a7%e3%81%aa%e3%82%a2%e3%83%ab%e3%82%b4%e3%83%aa%e3%82%ba%e3%83%a0) (Introduction to Multi-Agent Path Planning, in Japanese)

#### Dijkstra's algorithm

I used the code published in the following article as a reference for my implementation. The [code](./sandbox/dijkstra/python_example.py) is available at the link.

- [ダイクストラ法（Dijkstra's Algorithm）をPythonで実装する #Python - Qiita](https://qiita.com/gomagoma000/items/edd3ff714e4d964c670c) (Implementing Dijkstra's Algorithm in Python, in Japanese)

I also used the following articles to understand Dijkstra's algorithm (all in Japanese).

- [ダイクストラ法についてまとめてみた【経路探索アルゴリズム】｜らるす](https://note.com/rarusu/n/na7c9ca8ba1a0)
- [マップ上の最短距離を見つけるダイクストラ法を図解でわかりやすく説明 | python実装あり｜スイスのアボカド](https://note.com/avocado81230/n/n1a0e8a835d05)
- [うさぎでもわかる離散数学（グラフ理論）　第14羽　ダイクストラ法による最短経路の求め方 - 工業大学生ももやまのうさぎ塾 (Momousagi Academy)](https://www.momoyama-usagi.com/entry/math-risan14#gsc.tab=0)
- [【これでわかる！】具体例を使ってダイクストラ法のアルゴリズムについてなるべくわかりやすく解説してみた](https://yukashun.com/shortest_path_dijkstra/)

#### A\* algorithm

Although I did not adopt it this time, I referred to the following article when researching the A\* (A-star) algorithm.

- [【C++日記】A\*アルゴリズム 編｜Frira](https://note.com/fgr_frira/n/n67c0b664140c) (in Japanese)

#### Docstrings

- [GoogleスタイルのPython Docstringの入門 #新人プログラマ応援 - Qiita](https://qiita.com/11ohina017/items/118b3b42b612e527dc1d) (Introduction to Google-style Python docstrings, in Japanese)
- [Google Style Guides | Style guides for Google-originated open-source projects](https://google.github.io/styleguide/pyguide.html)

---

## Others

The decisions I made while building this project and the detailed specifications are summarized in [ADDITIONALS.md](./ADDITIONALS.md) and [DECISIONS.md](./DECISIONS.md). (Japanese only)
