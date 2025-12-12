# %%
with open("input/day12", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

NUM_GIFTS, GIFT_SIZE = 6, 3
ConfigType = tuple[tuple[int, int], list[int]]


def parse_config(config: str) -> ConfigType:
    grid_size_str, targets_str = config.split(": ")
    grid_size = tuple(map(int, grid_size_str.split("x")))
    targets = list(map(int, targets_str.split(" ")))
    return grid_size, targets


def fit(config: ConfigType) -> bool:
    (Y, X), targets = config
    return Y // 3 * X // 3 >= sum(targets)


configs = [parse_config(l) for l in lines[NUM_GIFTS * (GIFT_SIZE + 1) :]]

print(sum(fit(c) for c in configs))

# %%
# Visualisation
import numpy as np

patterns = []
for i in range(NUM_GIFTS):
    pattern = np.array([["."] * GIFT_SIZE for _ in range(GIFT_SIZE)])
    for j in range(GIFT_SIZE):
        pattern[j, :] = list(lines[i * (GIFT_SIZE + 1) + 1 + j])
    patterns.append(pattern)


def fit_(config: ConfigType, do_print: bool = False) -> bool:
    def print_grid(grid: np.ndarray):
        for row in grid:
            print("".join(row))

    (Y, X), targets = config
    grid = np.array([["."] * X for _ in range(Y)])
    curr_x, curr_y = 0, 0
    for i, target in enumerate(targets):
        for _ in range(target):
            if curr_x + GIFT_SIZE > X:
                curr_x = 0
                curr_y += GIFT_SIZE
            if curr_y + GIFT_SIZE > Y:
                return False
            grid[curr_y : curr_y + GIFT_SIZE, curr_x : curr_x + GIFT_SIZE] = (
                patterns[i]
            )
            curr_x += GIFT_SIZE
    if do_print:
        print(f"Config: {config}")
        print_grid(grid)
        print()
    return True


for config in configs:
    assert fit_(config, do_print=True) == fit(config)

# %%
