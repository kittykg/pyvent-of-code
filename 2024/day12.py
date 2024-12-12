import numpy as np


with open("input/day12", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


# ============================================================================ #
#                                   General                                    #
# ============================================================================ #


# Fill '.' around the grid to avoid out of bounds errors
temp_char_grid = np.array([[c for c in line] for line in lines], dtype=str)
max_row, max_col = temp_char_grid.shape
char_grid = np.zeros((max_row + 2, max_col + 2), dtype=str)
char_grid.fill(".")
char_grid[1 : max_row + 1, 1 : max_col + 1] = temp_char_grid
actual_grid_start, actual_grid_end = 1, max_row


def get_neighbours(x: int, y: int) -> list[tuple[int, int]]:
    return [(x, y) for x, y in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]]


# ============================================================================ #
#                                    Part 1                                    #
# ============================================================================ #


fence_grid = np.zeros(char_grid.shape)
for i in range(1, actual_grid_end + 1):
    for j in range(1, actual_grid_end + 1):
        curr_plant = char_grid[i, j]
        for nx, ny in get_neighbours(i, j):
            if char_grid[nx, ny] != curr_plant:
                fence_grid[i, j] += 1


def get_perimeter(region: set[tuple[int, int]]) -> int:
    return int(sum(fence_grid[x, y] for x, y in region))


# ============================================================================ #
#                                    Part 2                                    #
# ============================================================================ #


def count_corner(x: int, y: int) -> int:
    curr_plant = char_grid[x, y]

    top_plant = char_grid[x - 1, y]
    right_plant = char_grid[x, y + 1]
    left_plant = char_grid[x, y - 1]
    bot_plant = char_grid[x + 1, y]

    top_left_plant = char_grid[x - 1, y - 1]
    top_right_plant = char_grid[x - 1, y + 1]
    bot_left_plant = char_grid[x + 1, y - 1]
    bot_right_plant = char_grid[x + 1, y + 1]

    def is_corner(plant_1: str, plant_2: str, plant_3: str):
        # Corner can happen only like these:
        # .O.   OX.
        # OX.   XX.
        # ...   ...
        if plant_1 != curr_plant and plant_2 != curr_plant:
            return True
        return (
            plant_1 == curr_plant
            and plant_2 == curr_plant
            and plant_3 != curr_plant
        )

    return sum(
        1
        for p1, p2, p3 in [
            (left_plant, top_plant, top_left_plant),
            (right_plant, top_plant, top_right_plant),
            (left_plant, bot_plant, bot_left_plant),
            (right_plant, bot_plant, bot_right_plant),
        ]
        if is_corner(p1, p2, p3)
    )


# ============================================================================ #
#                                 Overall task                                 #
# ============================================================================ #


visited = np.zeros(char_grid.shape, dtype=bool)


def get_region(x: int, y: int, plant_type: str, region: set[tuple[int, int]]):
    if char_grid[x, y] != plant_type:
        return

    visited[x, y] = True
    region.add((x, y))
    for nx, ny in get_neighbours(x, y):
        if not visited[nx, ny]:
            get_region(nx, ny, plant_type, region)


price_dict: dict[tuple[int, int, str], tuple[int, int, int]] = {}
for i in range(1, actual_grid_end + 1):
    for j in range(1, actual_grid_end + 1):
        if visited[i, j]:
            continue

        plant_type = char_grid[i, j]
        region = set()
        get_region(i, j, plant_type, region)

        perimeter = get_perimeter(region)
        corners = sum(count_corner(x, y) for x, y in region)
        area = len(region)

        price_dict[(i, j, plant_type)] = (area, perimeter, corners)

print(sum(a * p for a, p, _ in price_dict.values()))
print(sum(a * c for a, _, c in price_dict.values()))
