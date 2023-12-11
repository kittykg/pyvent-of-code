Coord = tuple[int, int]

with open("input/day11", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

og_coords = []
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c != ".":
            og_coords.append((i, j))

row_set = set([coord[0] for coord in og_coords])
full_row = set(range(len(lines)))
expanding_rows = full_row - row_set

col_set = set([coord[1] for coord in og_coords])
full_col = set(range(len(lines[0])))
expanding_cols = full_col - col_set


def expand(distance: int) -> list[Coord]:
    def expand_coord(expand_set: set[int], c: int, distance: int) -> int:
        return c + len([x for x in expand_set if x < c]) * distance

    return [
        (
            expand_coord(expanding_rows, x, distance),
            expand_coord(expanding_cols, y, distance),
        )
        for x, y in og_coords
    ]


def manhattan_distance(c1: Coord, c2: Coord) -> int:
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def task(distance: int = 1) -> float:
    coords = expand(distance)
    acc_sum = 0
    for c1 in coords:
        for c2 in coords:
            if c1 != c2:
                acc_sum += manhattan_distance(c1, c2)
    return acc_sum / 2


print(task(1))
print(task(1000000 - 1))


def prolog_input():
    with open("day11.out", "w") as f:
        for x, y in og_coords:
            f.write(f"coord({x},{y}).\n")
        f.write(f"x_len({len(lines)}).\n")
        f.write(f"y_len({len(lines[0])}).\n")


# prolog_input()
