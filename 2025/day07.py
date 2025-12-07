# %%
import numpy as np

with open("input/day07", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

grid = np.array([list(line) for line in lines])
max_x, max_y = grid.shape
start_x, start_y = np.where(grid == "S")[0][0], np.where(grid == "S")[1][0]

# %%
beams = set([start_y])
split_count = 0
count_grid = np.zeros(grid.shape)
count_grid[start_x, start_y] = 1
coverage = set()  # for visualization

for i in range(1, max_x):
    new_beams = set()
    for curr_j in beams:
        if grid[i, curr_j] == "^":
            split_count += 1
            new_beams.update([curr_j - 1, curr_j + 1])
            count_grid[i, curr_j - 1] += count_grid[i - 1, curr_j]
            count_grid[i, curr_j + 1] += count_grid[i - 1, curr_j]
        else:
            new_beams.add(curr_j)
            count_grid[i, curr_j] += count_grid[i - 1, curr_j]
    for j in new_beams:
        coverage.add((i, j))
    beams = new_beams

print(split_count)
print(int(np.sum(count_grid[-1, :])))

# %%
# visualization for memes
for i, j in coverage:
    if i > max_x or j > max_y:
        continue
    grid[i, j] = "|"
for row in grid:
    print("".join(row))

print(count_grid)
