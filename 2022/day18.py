# THANKS TO MY HUBBY FOR THIS AMAZING SOLUTION

from typing import Tuple
import numpy as np
from scipy.ndimage import binary_fill_holes, convolve


def parse_line(l: str) -> Tuple[int, int, int]:
    cs = [int(c) for c in l.split(",")]
    return cs[0], cs[1], cs[2]


with open("input/day18", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


cubes = [parse_line(l) for l in lines]

max_x = max([x for x, _, _ in cubes])
max_y = max([y for _, y, _ in cubes])
max_z = max([z for _, _, z in cubes])
grid = np.zeros((max_x + 3, max_y + 3, max_z + 3))
for x, y, z in cubes:
    grid[x + 1, y + 1, z + 1] = 1


def task_1():
    sides = 0
    for d in range(3):
        shape = [1, 1, 1]
        shape[d] = 2
        kernel = np.array([1, -1]).reshape(shape)
        sides += np.count_nonzero(
            convolve(grid, kernel, mode="constant", cval=0.0)
        )
    print(sides)


def task_2():
    filled_grid = binary_fill_holes(grid).astype(int)  # type: ignore
    sides = 0
    for d in range(3):
        shape = [1, 1, 1]
        shape[d] = 2
        kernel = np.array([1, -1]).reshape(shape)
        sides += np.count_nonzero(
            convolve(filled_grid, kernel, mode="constant", cval=0.0)
        )
    print(sides)
