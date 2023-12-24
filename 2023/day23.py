import numpy as np
from enum import IntEnum


Coord = tuple[int, int]


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


arrow_to_direction = {
    "^": Direction.UP,
    ">": Direction.RIGHT,
    "v": Direction.DOWN,
    "<": Direction.LEFT,
}


with open("input/day23", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

grid = np.array([list(s) for s in lines])
start_coord = (0, 1)
end_coord = (grid.shape[0] - 1, grid.shape[1] - 2)


def in_bound(coord: Coord) -> bool:
    return 0 <= coord[0] < grid.shape[0] and 0 <= coord[1] < grid.shape[1]


def move(coord: Coord, direction: Direction) -> Coord:
    if direction == Direction.UP:
        return (coord[0] - 1, coord[1])
    elif direction == Direction.RIGHT:
        return (coord[0], coord[1] + 1)
    elif direction == Direction.DOWN:
        return (coord[0] + 1, coord[1])
    else:
        return (coord[0], coord[1] - 1)


def possible_next_step(
    coord: Coord, visited_coords: set[Coord], allow_climbing_slope: bool
) -> list[Coord]:
    curr = grid[coord]
    if not allow_climbing_slope and curr in arrow_to_direction:
        moveable_directions = [arrow_to_direction[curr]]
    else:
        moveable_directions = list(Direction)

    next_step = []
    for d in moveable_directions:
        next_coord = move(coord, d)
        if (
            in_bound(next_coord)
            and grid[next_coord] != "#"
            and next_coord not in visited_coords
        ):
            next_step.append(next_coord)

    return next_step


def travel(
    curr_coord: Coord,
    past_history: set[Coord],
    allow_climbing_slope: bool = False,
) -> tuple[bool, set[Coord]]:
    def travel_without_split(
        start_coord: Coord,
        past_history: set[Coord],
    ) -> set[Coord] | tuple[Coord, set[Coord]]:
        curr_coord = start_coord
        visited_coords = past_history.copy()

        while True:
            visited_coords.add(curr_coord)

            if curr_coord == end_coord:
                return visited_coords

            next_steps = possible_next_step(
                curr_coord, visited_coords, allow_climbing_slope
            )

            if len(next_steps) == 0:
                return visited_coords
            if len(next_steps) == 1:
                curr_coord = next_steps[0]
            else:
                return curr_coord, visited_coords

    if curr_coord == end_coord:
        return True, past_history

    ret = travel_without_split(curr_coord, past_history)
    if isinstance(ret, tuple):
        # we reached a junction, recurse on this junction
        junction, visited_coords = ret
        next_steps = possible_next_step(
            junction, visited_coords, allow_climbing_slope
        )
        candidates = []
        for next_step in next_steps:
            res, route = travel(
                next_step, visited_coords.copy(), allow_climbing_slope
            )
            if res:
                candidates.append((res, route))
        if len(candidates) == 0:
            return False, visited_coords
        return True, max(candidates, key=lambda x: len(x[1]))[1]
    else:
        # we either reach the true end or a dead end
        if end_coord in ret:
            return True, ret
        else:
            return False, ret


def task_1():
    _, ret = travel(start_coord, set())
    # -1 because we don't count the start
    return len(ret) - 1


def task_2():
    _, ret = travel(start_coord, set(), allow_climbing_slope=True)
    # -1 because we don't count the start
    return len(ret) - 1


import time

start = time.time()
print(task_1())
print(task_2())
end = time.time()
print(end - start)
