import numpy as np

with open("input/day10", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

grid = np.array([list(map(int, x)) for x in lines])
max_row, max_col = grid.shape
potential_trail_heads_loc = np.argwhere(grid == 0)


def in_range(x: int, y: int) -> bool:
    return 0 <= x < max_row and 0 <= y < max_col


CoordType = tuple[int, int]
RouteType = list[CoordType]


def get_steps(x: int, y: int) -> list[CoordType]:
    return list(
        filter(
            lambda x: in_range(*x),
            [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ],
        )
    )


def _hiking_trail(
    x: int,
    y: int,
    curr_height: int,
    history: RouteType,
    all_valid_route: list[RouteType],
) -> None:
    history.append((x, y))
    if grid[x, y] == 9:
        all_valid_route.append(history)
        return

    for s in get_steps(x, y):
        if grid[s] == curr_height + 1:
            _hiking_trail(*s, curr_height + 1, history.copy(), all_valid_route)

    return


def hiking_trail(x: int, y: int) -> list[RouteType]:
    valid_route = []
    _hiking_trail(x, y, 0, [], valid_route)
    return valid_route


from datetime import datetime

start = datetime.now()
all_hiking_trail: list[list[RouteType]] = [
    hiking_trail(*p) for p in potential_trail_heads_loc
]

print("Part 1: ", sum(len(set([r[-1] for r in ar])) for ar in all_hiking_trail))
print("Part 2: ", sum(len(ar) for ar in all_hiking_trail))
print(datetime.now() - start)
