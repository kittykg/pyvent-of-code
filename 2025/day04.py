# %%
import numpy as np
import scipy

with open("input/day04", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

# %%
grid = np.array([list(map(lambda x: 1 if x == "@" else 0, x)) for x in lines])
kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
i = 0
acc = 0

while True:
    conv2d = scipy.signal.convolve2d(grid, kernel, mode="same")
    prod = conv2d * grid
    cond = (prod <= 4) & (prod >= 1)
    c = np.count_nonzero(cond)

    if c == 0:
        print(f"Task 2: {acc}")
        break

    if i == 0:
        print(f"Task 1: {c}")
        i += 1

    acc += c
    grid[np.where(cond)] = 0

# %%
