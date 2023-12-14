import numpy as np

with open("input/day14", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
grid = np.array([list(s) for s in lines])


def move_round_rock(col: np.ndarray) -> np.ndarray:
    def find_new_location(i: int, arr: np.ndarray) -> int:
        if i == 0:
            return 0
        for j in range(i, 0, -1):
            if arr[j - 1] != ".":
                return j
        return 0

    new_col = np.copy(col)
    for i in range(len(new_col)):
        rock = new_col[i]
        if rock == "#":
            continue
        elif rock == ".":
            continue

        new_location = find_new_location(i, new_col)
        if new_location != i:
            new_col[new_location] = rock
            new_col[i] = "."
    return new_col


def tilt_north(grid: np.ndarray) -> np.ndarray:
    # tilt north, do transpose, and move column to left
    new_grid = np.copy(grid)
    for i in range(new_grid.T.shape[0]):
        new_grid.T[i] = move_round_rock(new_grid.T[i])
    return new_grid


def tilt_south(grid: np.ndarray) -> np.ndarray:
    # tilt south, do transpose, and move column to right = move reversed col to
    # left
    new_grid = np.copy(grid)
    for i in range(new_grid.T.shape[0]):
        new_grid.T[i] = np.flip(move_round_rock(np.flip(new_grid.T[i])))
    return new_grid


def tilt_east(grid: np.ndarray) -> np.ndarray:
    # tilt east, move row to right = move reversed row to left
    new_grid = np.copy(grid)
    for i in range(new_grid.shape[0]):
        new_grid[i] = np.flip(move_round_rock(np.flip(new_grid[i])))
    return new_grid


def tilt_west(grid: np.ndarray) -> np.ndarray:
    # tilt west, move row to left
    new_grid = np.copy(grid)
    for i in range(new_grid.shape[0]):
        new_grid[i] = move_round_rock(new_grid[i])
    return new_grid


def task_1(grid: np.ndarray) -> int:
    new_grid = tilt_north(grid)
    round_rocks_x, _ = np.where(new_grid == "O")
    return sum(len(new_grid) - x for x in round_rocks_x)


def task_2(grid: np.ndarray) -> int:
    def one_cycle(grid: np.ndarray) -> np.ndarray:
        new_grid = tilt_north(grid)
        new_grid = tilt_west(new_grid)
        new_grid = tilt_south(new_grid)
        new_grid = tilt_east(new_grid)
        return new_grid

    def grid_to_string(grid: np.ndarray) -> str:
        return "".join(grid.flatten())

    new_grid = np.copy(grid)

    unique_cycle_end_string = [grid_to_string(new_grid)]
    unique_grid = [new_grid]

    for i in range(1000000000):
        new_grid = one_cycle(new_grid)
        grid_string = grid_to_string(new_grid)
        if grid_string in unique_cycle_end_string:
            j = unique_cycle_end_string.index(grid_string)
            break
        unique_cycle_end_string.append(grid_string)
        unique_grid.append(new_grid)

    # Because the start grid pattern is also in  unique_cycle_end_string, there
    # is a difference of 1 between i index and j index
    cycle_length = i - j + 1  # type: ignore
    cycle_start = j - 1  # type: ignore
    offset = (1000000000 - cycle_start) % cycle_length
    final_grid = unique_grid[cycle_start + offset]
    round_rocks_x, _ = np.where(final_grid == "O")
    return sum(len(final_grid) - x for x in round_rocks_x)


print(task_1(grid))
print(task_2(grid))
