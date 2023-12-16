import numpy as np
from enum import IntEnum

Coord = tuple[int, int]

with open("input/day16", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
grid = np.array([list(s) for s in lines])


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def in_bounds(coord: Coord) -> bool:
    return 0 <= coord[0] < grid.shape[0] and 0 <= coord[1] < grid.shape[1]


def reflect(direction: Direction, mirror: str) -> Direction:
    if mirror == "\\":
        if direction == Direction.UP:
            return Direction.LEFT
        elif direction == Direction.RIGHT:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.RIGHT
        else:  # direction == Direction.LEFT
            return Direction.UP
    else:  # mirror == "/"
        if direction == Direction.UP:
            return Direction.RIGHT
        elif direction == Direction.RIGHT:
            return Direction.UP
        elif direction == Direction.DOWN:
            return Direction.LEFT
        else:  # direction == Direction.LEFT
            return Direction.DOWN


def split(
    direction: Direction, splitter: str
) -> Direction | tuple[Direction, Direction]:
    if splitter == "|":
        if direction == Direction.UP or direction == Direction.DOWN:
            return direction
        else:  # direction == Direction.RIGHT or direction == Direction.LEFT
            return (Direction.UP, Direction.DOWN)
    else:  # mirror == "-"
        if direction == Direction.UP or direction == Direction.DOWN:
            return (Direction.RIGHT, Direction.LEFT)
        else:
            return direction


def move(direction: Direction, coord: Coord) -> Coord:
    if direction == Direction.UP:
        return (coord[0] - 1, coord[1])
    elif direction == Direction.RIGHT:
        return (coord[0], coord[1] + 1)
    elif direction == Direction.DOWN:
        return (coord[0] + 1, coord[1])
    else:  # direction == Direction.LEFT
        return (coord[0], coord[1] - 1)


def travel(start_coord: Coord, start_direction: Direction) -> set[Coord]:
    overall_travel_set = set()
    beam_queue = [(start_coord, start_direction)]
    visited_mirror_set = set()

    while len(beam_queue) > 0:
        curr_coord, curr_direction = beam_queue.pop(0)

        while in_bounds(curr_coord):
            if (curr_coord, curr_direction) in visited_mirror_set:
                break

            overall_travel_set.add(curr_coord)

            if grid[curr_coord] == ".":
                # grid[curr_coord] is empty
                curr_coord = move(curr_direction, curr_coord)
                continue

            visited_mirror_set.add((curr_coord, curr_direction))
            if grid[curr_coord] in ["\\", "/"]:
                # grid[curr_coord] is a mirror
                curr_direction = reflect(curr_direction, grid[curr_coord])
                curr_coord = move(curr_direction, curr_coord)
            else:
                # grid[curr_coord] is splitter (["|", "-"]):
                split_direction = split(curr_direction, grid[curr_coord])

                if isinstance(split_direction, Direction):
                    # visited_mirror_set.add((curr_coord, curr_direction))
                    curr_direction = split_direction
                    curr_coord = move(curr_direction, curr_coord)
                else:
                    dir1, dir2 = split_direction

                    # We continue in dir 1 and add dir 2 to the queue
                    beam_queue.append((move(dir2, curr_coord), dir2))

                    curr_direction = dir1
                    curr_coord = move(curr_direction, curr_coord)

    return overall_travel_set


travel_set_from_0_0 = travel((0, 0), Direction.RIGHT)


def task_1():
    return len(travel_set_from_0_0)


def task_2():
    start_pairs = []
    x_max, y_max = grid.shape
    for i in range(x_max):
        start_pairs.append(((i, 0), Direction.RIGHT))
        start_pairs.append(((i, y_max - 1), Direction.LEFT))
    for j in range(y_max):
        start_pairs.append(((0, j), Direction.DOWN))
        start_pairs.append(((x_max - 1, j), Direction.UP))

    start_pairs.remove(((0, 0), Direction.RIGHT))
    start_pairs.sort()

    energies = [len(travel_set_from_0_0)]
    for start_pair in start_pairs:
        energies.append(len(travel(*start_pair)))

    return max(energies)


print(task_1())
print(task_2())
