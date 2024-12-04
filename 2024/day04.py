import numpy as np


with open("input/day04", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

char_grid = np.array([list(x) for x in lines], dtype=str)
max_row, max_col = char_grid.shape


def in_bounds_x(i: int) -> bool:
    return 0 <= i < max_row


def in_bounds_y(j: int) -> bool:
    return 0 <= j < max_col


# Part 1


def get_adjacent(i: int, j: int) -> tuple[list[list[int]], list[list[int]]]:
    xs = []
    ys = []

    for x_diff, y_diff in [
        (-1, 0),  # Go north (-1, 0)
        (0, 1),  # Go east (0, 1)
        (1, 0),  # Go south (1, 0)
        (0, -1),  # Go west (0, -1)
        (-1, -1),  # Go north-west (-1, -1)
        (-1, 1),  # Go north-east (-1, 1)
        (1, -1),  # Go south-west (1, -1)
        (1, 1),  # Go south-east (1, 1)
    ]:
        potentials_x = [i, i + x_diff, i + x_diff * 2, i + x_diff * 3]
        potentials_y = [j, j + y_diff, j + y_diff * 2, j + y_diff * 3]

        if np.all(
            [
                in_bounds_x(x) and in_bounds_y(y)
                for x, y in zip(potentials_x, potentials_y)
            ]
        ):
            xs.append(potentials_x)
            ys.append(potentials_y)

    return xs, ys


def count_xmas():
    count = 0
    for i in range(max_row):
        for j in range(max_col):
            if char_grid[i, j] != "X":
                continue

            xs, ys = get_adjacent(i, j)
            for xl, yl in zip(xs, ys):
                word = "".join(char_grid[xl, yl])
                if word == "XMAS":
                    count += 1

    return count


# Part 2


def get_x_shape(i: int, j: int) -> list[tuple[list[int], list[int]]] | None:
    # North east -> South west / North west -> South east
    xs = [i - 1, i, i + 1]
    ys = [j - 1, j, j + 1]

    if np.all([in_bounds_x(x) and in_bounds_y(y) for x, y in zip(xs, ys)]):
        return [
            (xs, ys),
            (xs, list(reversed(ys))),
        ]

    return None


def count_x_shape_mas():
    count = 0

    for i in range(max_row):
        for j in range(max_col):
            if char_grid[i, j] != "A":
                continue

            x_shape = get_x_shape(i, j)
            if x_shape is None:
                continue

            word_1 = "".join(char_grid[x_shape[0][0], x_shape[0][1]])
            word_2 = "".join(char_grid[x_shape[1][0], x_shape[1][1]])

            if word_1 != "MAS" and word_1 != "SAM":
                continue
            if word_2 != "MAS" and word_2 != "SAM":
                continue
            count += 1

    return count
