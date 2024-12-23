from collections import deque, defaultdict
from enum import IntEnum
from functools import cache

with open("input/day21", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

A_num = 10
codes = [[A_num if s == "A" else int(s) for s in l] for l in lines]


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def to_char(self) -> str:
        return {
            Direction.UP: "^",
            Direction.RIGHT: ">",
            Direction.DOWN: "v",
            Direction.LEFT: "<",
        }[self]


def bfs_with_all_options(start, goal, mapping: dict) -> list[list[Direction]]:
    queue = deque([start])
    distances = {start: 0}
    parents = defaultdict(list)

    # Perform BFS
    while queue:
        node = queue.popleft()
        for next, dir in mapping[node]:
            if next not in distances:
                distances[next] = distances[node] + 1
                parents[next].append((node, dir))
                queue.append(next)
            elif distances[next] == distances[node] + 1:
                parents[next].append((node, dir))

    # Reconstruct all paths
    def backtrack_paths(node):
        if node == start:
            return [[]]

        paths = []
        for parent_node, dir in parents[node]:
            for path in backtrack_paths(parent_node):
                paths.append(path + [dir])
        return paths

    return backtrack_paths(goal)


@cache
def bfs_number_pad(start: int, goal: int) -> list[list[Direction]]:
    next_possible_mapping: dict[int, list[tuple[int, Direction]]] = {
        0: [(2, Direction.UP), (A_num, Direction.RIGHT)],
        1: [(2, Direction.RIGHT), (4, Direction.UP)],
        2: [
            (0, Direction.DOWN),
            (1, Direction.LEFT),
            (3, Direction.RIGHT),
            (5, Direction.UP),
        ],
        3: [(2, Direction.LEFT), (6, Direction.UP), (A_num, Direction.DOWN)],
        4: [(1, Direction.DOWN), (5, Direction.RIGHT), (7, Direction.UP)],
        5: [
            (2, Direction.DOWN),
            (4, Direction.LEFT),
            (6, Direction.RIGHT),
            (8, Direction.UP),
        ],
        6: [(3, Direction.DOWN), (5, Direction.LEFT), (9, Direction.UP)],
        7: [(4, Direction.DOWN), (8, Direction.RIGHT)],
        8: [(5, Direction.DOWN), (7, Direction.LEFT), (9, Direction.RIGHT)],
        9: [(6, Direction.DOWN), (8, Direction.LEFT)],
        A_num: [(0, Direction.LEFT), (3, Direction.UP)],
    }
    return bfs_with_all_options(start, goal, next_possible_mapping)


@cache
def bfs_direction_pad(start: str, goal: str) -> list[list[Direction]]:
    next_possible_mapping: dict[str, list[tuple[str, Direction]]] = {
        "<": [("v", Direction.RIGHT)],
        "v": [
            ("<", Direction.LEFT),
            ("^", Direction.UP),
            (">", Direction.RIGHT),
        ],
        ">": [("v", Direction.LEFT), ("A", Direction.UP)],
        "^": [("v", Direction.DOWN), ("A", Direction.RIGHT)],
        "A": [(">", Direction.DOWN), ("^", Direction.LEFT)],
    }
    return bfs_with_all_options(start, goal, next_possible_mapping)


@cache
def compute_min_direction_l(x1, x2, recursion_depth: int) -> int:
    all_l = bfs_direction_pad(x1, x2)

    if recursion_depth == 0:
        return min(len(l) for l in all_l) + 1

    all_len_l = []
    for l in all_l:
        l_translated: list[str] = [d.to_char() for d in l] + ["A"]
        len_l = 0

        for i, e in enumerate(l_translated):
            x_sub_1 = "A" if i == 0 else l_translated[i - 1]
            len_l += compute_min_direction_l(x_sub_1, e, recursion_depth - 1)

        all_len_l.append(len_l)

    return min(all_len_l)


def task(recursion_depth: int = 1):
    out = 0
    for code in codes:
        x0: int = A_num
        len_l_a = 0

        for a in code:

            all_l_b = bfs_number_pad(x0, a)

            all_len_l_b = []

            for l_b in all_l_b:

                l_b_translated: list[str] = [d.to_char() for d in l_b] + ["A"]
                len_l_b = 0

                for i, b in enumerate(l_b_translated):

                    x1 = "A" if i == 0 else l_b_translated[i - 1]

                    len_l_b += compute_min_direction_l(x1, b, recursion_depth)

                all_len_l_b.append(len_l_b)

            len_l_a += min(all_len_l_b)
            x0 = a

        k2 = int("".join(str(x) for x in code[:3]))

        out += len_l_a * k2

    return out


print(f"Task 1: {task()}")
print(f"Task 2: {task(24)}")
