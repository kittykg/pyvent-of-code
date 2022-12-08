import numpy as np


def is_visible(grid: np.ndarray, x: int, y: int) -> bool:
    # x, y shouldn't be on the edge of the grid
    def _is_visible_(trees: np.ndarray, curr_tree: int) -> bool:
        return bool(np.all(curr_tree > trees))

    left_visible = _is_visible_(grid[x, :y], grid[x, y])
    right_visible = _is_visible_(grid[x, y + 1 :], grid[x, y])
    top_visible = _is_visible_(grid[:x, y], grid[x, y])
    bottom_visible = _is_visible_(grid[x + 1 :, y], grid[x, y])

    return left_visible or right_visible or top_visible or bottom_visible


def scenic_score(grid: np.ndarray, x: int, y: int) -> int:
    # x, y shouldn't be on teh edge of the grid
    def _score_(trees: np.ndarray, curr_tree: int) -> int:
        # trees should be in the right order
        res = trees >= curr_tree
        if np.all(~res):  # all false, argmax would return 0
            return len(res)
        return int(np.argmax(res) + 1)

    left_score = _score_(np.flip(grid[x, :y]), grid[x, y])
    right_score = _score_(grid[x, y + 1 :], grid[x, y])
    top_score = _score_(np.flip(grid[:x, y]), grid[x, y])
    bottom_score = _score_(grid[x + 1 :, y], grid[x, y])

    return left_score * right_score * top_score * bottom_score


with open("input/day08", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
    grid = np.array([[int(c) for c in l] for l in lines])

# Task 1
print(
    (grid.shape[0] - 1) * 4
    + np.array(
        [
            [is_visible(grid, i, j) for j in range(1, grid.shape[1] - 1)]
            for i in range(1, grid.shape[0] - 1)
        ]
    ).sum()
)

# Task 1
print(
    np.array(
        [
            [scenic_score(grid, i, j) for j in range(1, grid.shape[1] - 1)]
            for i in range(1, grid.shape[0] - 1)
        ]
    ).max()
)
