from itertools import combinations
import numpy as np


with open("input/day08", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

char_grid = np.array([list(x) for x in lines], dtype=str)
max_row, max_col = char_grid.shape

location_dict: dict[str, list[tuple[int, int]]] = {}

for i in range(max_row):
    for j in range(max_col):
        c = char_grid[i, j]
        if not c.isalnum():
            continue
        if not c in location_dict:
            location_dict[c] = []
        location_dict[c].append((i, j))


def in_range(x: int, y: int) -> bool:
    return 0 <= x < max_row and 0 <= y < max_col


def compute_antinode(
    x: int, y: int, dx: int, dy: int, plus_flag: bool = True
) -> tuple[int, int] | None:
    if plus_flag:
        x1, y1 = x + dx, y + dy
    else:
        x1, y1 = x - dx, y - dy
    if not in_range(x1, y1):
        return None
    return x1, y1


def get_line(
    x1: int, y1: int, x2: int, y2: int, part_2: bool = False
) -> list[tuple[int, int] | None]:
    dy = y2 - y1
    dx = x2 - x1

    if not part_2:
        return [
            compute_antinode(x1, y1, dx, dy, False),
            compute_antinode(x2, y2, dx, dy, True),
        ]

    antinodes = []
    while True:
        new_point = compute_antinode(x1, y1, dx, dy, False)
        if new_point is None:
            break
        antinodes.append(new_point)
        x1, y1 = new_point

    while True:
        new_point = compute_antinode(x2, y2, dx, dy, True)
        if new_point is None:
            break
        antinodes.append(new_point)
        x2, y2 = new_point

    return antinodes


def task(part_2: bool = False):
    antinodes_loc = set()
    for locations in location_dict.values():
        for p1, p2 in combinations(locations, 2):
            p1x, p1y = p1
            p2x, p2y = p2

            for a in get_line(p1x, p1y, p2x, p2y, part_2):
                if a:
                    antinodes_loc.add(a)
            if part_2:
                antinodes_loc.add(p1)
                antinodes_loc.add(p2)

    print(f"Part {1 if not part_2 else 2}: {len(antinodes_loc)}")


task()
task(True)
