from queue import PriorityQueue

import numpy as np


CoordType = tuple[int, int]

with open("input/day16", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
char_grid = np.array([list(x) for x in lines])

reindeer_start: CoordType = tuple(map(int, np.where(char_grid == "S")))  # type: ignore
goal: CoordType = tuple(map(int, np.where(char_grid == "E")))  # type: ignore


# Direction: 0 = up, 1 = right, 2 = down, 3 = left
def turn_left(direction: int) -> int:
    return (direction - 1) % 4


def turn_right(direction: int) -> int:
    return (direction + 1) % 4


def get_forward_coord(x: int, y: int, direction: int) -> CoordType:
    if direction == 0:  # up
        return (x - 1, y)
    elif direction == 1:  # right
        return (x, y + 1)
    elif direction == 2:  # down
        return (x + 1, y)
    # direction == 3, left
    return (x, y - 1)


def get_possible_next_step(
    curr_x: int, curr_y: int, direction: int, char_grid: np.ndarray
) -> list[tuple[int, int, int]]:
    possible_next_steps: list[tuple[int, int, int]] = []

    # Can move forward, left, or right
    for direction in [direction, turn_left(direction), turn_right(direction)]:
        forward_coord = get_forward_coord(curr_x, curr_y, direction)
        if (
            0 <= forward_coord[0] < char_grid.shape[0]
            and 0 <= forward_coord[1] < char_grid.shape[1]
            and char_grid[forward_coord] != "#"
        ):
            # The coord must be in range and is not a wall '#'
            possible_next_steps.append((*forward_coord, direction))

    return possible_next_steps


# Dijkstra's algorithm
x, y = reindeer_start
d = 1  # Start facing East (right)

distance_grid = np.ndarray(
    (char_grid.shape[0], char_grid.shape[1], 4), dtype=int
)
distance_grid.fill(np.inf)
distance_grid[x, y, d] = 0

queue = PriorityQueue()
queue.put((0, (x, y, d)))

path: dict[tuple[int, int, int], list] = dict()

while not queue.empty():
    _, node = queue.get()
    x, y, d = node

    for next_node in get_possible_next_step(x, y, d, char_grid):
        score = 1 if next_node[2] == d else 1001
        alt_dist = distance_grid[node] + score
        if alt_dist < distance_grid[next_node]:
            distance_grid[next_node] = alt_dist
            path[(next_node)] = [node]
            queue.put((alt_dist, (next_node)))
        elif alt_dist == distance_grid[next_node]:
            path[(next_node)].append(node)


# Part 1
print(f"Part 1: {np.min(distance_grid[goal])}")


# Part 2
seats = set()


def get_all_seats(curr_node: tuple[int, int, int]):
    x, y, _ = curr_node
    seats.add((x, y))
    if (x, y) == reindeer_start:
        return

    prev_nodes = path[curr_node]
    for next_coord in prev_nodes:
        get_all_seats(next_coord)


get_all_seats((goal[0], goal[1], int(np.argmin(distance_grid[goal]))))
print(f"Part 2: {len(seats)}")
