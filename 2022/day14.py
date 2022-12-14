from copy import deepcopy
from typing import List, Set, Tuple

Grid = List[List[str]]
Coordinate = Tuple[int, int]


with open("input/day14", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def parse_line(l: str) -> List[Coordinate]:
    coords = set()
    line_coord = [
        (int(coord.split(",")[0]), int(coord.split(",")[1]))
        for coord in l.split(" -> ")
    ]
    for i in range(len(line_coord) - 1):
        p1_x, p1_y = line_coord[i]
        p2_x, p2_y = line_coord[i + 1]
        if p1_x == p2_x:  # Vertical line
            start = min(p1_y, p2_y)
            end = max(p1_y, p2_y)
            for j in range(start, end + 1):
                coords.add((p1_x, j))
        elif p1_y == p2_y:  # Horizontal line
            start = min(p1_x, p2_x)
            end = max(p1_x, p2_x)
            for j in range(start, end + 1):
                coords.add((j, p1_y))

    return [(x, y) for x, y in coords]


def task_1():
    rocks = [c for l in lines for c in parse_line(l)]
    xs = [r[0] for r in rocks] + [500]
    ys = [r[1] for r in rocks]
    x_min = min(xs)
    x_max = max(xs)
    x_len = x_max - x_min + 1
    y_len = max(ys) + 1

    grid = [["." for _ in range(x_len)] for _ in range(y_len)]
    for r in [(r[0] - x_min, r[1]) for r in rocks]:
        grid[r[1]][r[0]] = "#"
    grid[0][500 - x_min] = "+"

    def _is_blocked(coord: Coordinate) -> bool:
        c_x, c_y = coord
        c = grid[c_y][c_x]
        return c == "o" or c == "#"

    def _in_grid(coord: Coordinate) -> bool:
        c_x, c_y = coord
        return c_y in range(len(grid)) and c_x in range(len(grid[0]))

    count = 0
    while True:
        curr_coord = (500 - x_min, 0)
        new_sand = False
        while _in_grid(curr_coord):
            down = (curr_coord[0], curr_coord[1] + 1)
            down_left = (curr_coord[0] - 1, curr_coord[1] + 1)
            down_right = (curr_coord[0] + 1, curr_coord[1] + 1)
            if (
                not _in_grid(down)
                or not _in_grid(down_left)
                or not _in_grid(down_right)
            ):
                break
            if not _is_blocked(down):  # Move down
                curr_coord = down
            elif not _is_blocked(down_left):  # Move diagonally down and left
                curr_coord = down_left
            elif not _is_blocked(down_right):  # Move diagonally down and right\
                curr_coord = down_right
            else:  # rest
                grid[curr_coord[1]][curr_coord[0]] = "o"
                count += 1
                new_sand = True
                break
        if not new_sand:
            break
    print(count)


# For visualising part 2
def print_grid(rocks: Set[Coordinate], occupied: Set[Coordinate]) -> None:
    xs = [r[0] for r in occupied] + [500]
    ys = [r[1] for r in rocks]
    x_min = min(xs) - 1
    x_max = max(xs) + 1
    x_len = x_max - x_min + 1
    y_len = max(ys) + 2 + 1

    grid = [["." for _ in range(x_len)] for _ in range(y_len)]
    for i in range(x_len):
        grid[-1][i] = "#"
    for r in [(r[0] - x_min, r[1]) for r in rocks]:
        grid[r[1]][r[0]] = "#"
    grid[0][500 - x_min] = "+"

    for o in [(o[0] - x_min, o[1]) for o in occupied]:
        if grid[o[1]][o[0]] != "#":
            grid[o[1]][o[0]] = "o"

    for i, row in enumerate(grid):
        print("".join(row))


def task_2():
    rocks = set([c for l in lines for c in parse_line(l)])
    occupied = deepcopy(rocks)
    floor_y = max([r[1] for r in rocks]) + 2
    count = 0
    while (500, 0) not in occupied:
        curr_coord = (500, 0)
        while True:
            if curr_coord[1] + 1 == floor_y:  # Rest
                occupied.add(curr_coord)
                break
            down = (curr_coord[0], curr_coord[1] + 1)
            down_left = (curr_coord[0] - 1, curr_coord[1] + 1)
            down_right = (curr_coord[0] + 1, curr_coord[1] + 1)
            if down not in occupied:  # Move down
                curr_coord = down
            elif down_left not in occupied:  # Move diagonally down and left
                curr_coord = down_left
            elif down_right not in occupied:  # Move diagonally down and right\
                curr_coord = down_right
            else:  # Rest
                occupied.add(curr_coord)
                break
        count += 1
    print(count)


task_1()
task_2()
