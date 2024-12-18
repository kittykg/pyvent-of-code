from queue import PriorityQueue

import numpy as np

with open("input/day18", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

coords: list[tuple[int, int]] = [
    (int(l.split(",")[0]), int(l.split(",")[1])) for l in lines
]
grid_bound: int = 71


def create_char_grid(
    num_bytes_fallen: int = 1024, print_grid: bool = False
) -> np.ndarray:
    char_grid = np.array(
        [["." for _ in range(grid_bound)] for _ in range(grid_bound)]
    )
    for x, y in coords[:num_bytes_fallen]:
        char_grid[y, x] = "#"

    if print_grid:
        for row in char_grid:
            print("".join(row))

    return char_grid


def get_possible_next_step(
    curr_x: int, curr_y: int, char_grid: np.ndarray
) -> list[tuple[int, int]]:
    possible_next_steps: list[tuple[int, int]] = []

    for direction in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        new_x = curr_x + direction[0]
        new_y = curr_y + direction[1]
        if (
            0 <= new_y < char_grid.shape[0]
            and 0 <= new_x < char_grid.shape[1]
            and char_grid[new_y, new_x] != "#"
        ):
            # The coord must be in range and is not a wall '#'
            possible_next_steps.append((new_x, new_y))

    return possible_next_steps


def dijkstra(char_grid: np.ndarray) -> int:
    distance_grid = np.ndarray((grid_bound, grid_bound), dtype=int)
    distance_grid.fill(np.inf)
    distance_grid[0, 0] = 0

    queue = PriorityQueue()
    queue.put((0, (0, 0)))

    while not queue.empty():
        _, node = queue.get()
        x, y = node

        for next_node in get_possible_next_step(x, y, char_grid):
            alt_distance = distance_grid[y, x] + 1
            next_x, next_y = next_node
            if alt_distance < distance_grid[next_y, next_x]:
                distance_grid[next_y, next_x] = alt_distance
                queue.put((alt_distance, next_node))

    return distance_grid[grid_bound - 1, grid_bound - 1]


result = None
lower_bound, upper_bound = 2000, 3000  # Guessing the range, worked :P
# Do binary search to find the number of bytes fallen
while lower_bound < upper_bound:
    middle = (lower_bound + upper_bound) // 2
    dist = dijkstra(create_char_grid(middle))
    if dist > (grid_bound + 1) ** 2:  # bound^2 is the maximum possible distance
        upper_bound = middle
    else:
        lower_bound = middle + 1

print(f"Part 1: {dijkstra(create_char_grid())}")
print(f"Part 2: {coords[upper_bound - 1]}")
