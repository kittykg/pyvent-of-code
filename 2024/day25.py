import numpy as np

with open("input/day25", "r") as f:
    groups = f.read().split("\n\n")

keys = []
locks = []

for g in groups:
    char_grid = np.array(
        [list(row) for row in g.split("\n") if row != ""], dtype=str
    )
    heights = np.sum(char_grid == "#", axis=0) - 1
    if np.all(char_grid[0] == "#"):
        locks.append(heights)
    else:
        keys.append(heights)

fit = 0
for k in keys:
    for l in locks:
        if np.all((k + l) <= 5):
            fit += 1

print(fit)
