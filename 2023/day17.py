# WIP: ?

import numpy as np
from enum import IntEnum


Coord = tuple[int, int]

with open("input/day17", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
grid = np.array([[int(i) for i in list(l)] for l in lines])

start_coord = (0, 0)
end_coord = (grid.shape[0] - 1, grid.shape[1] - 1)


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def turn_left(self) -> "Direction":
        return Direction((self - 1) % 4)

    def turn_right(self) -> "Direction":
        return Direction((self + 1) % 4)

    def is_vertical(self) -> bool:
        return self == Direction.UP or self == Direction.DOWN

    def is_horizontal(self) -> bool:
        return self == Direction.LEFT or self == Direction.RIGHT


class Axis(IntEnum):
    VERTICAL = 0
    HORIZONTAL = 1


def in_bounds(coord: Coord) -> bool:
    return 0 <= coord[0] < grid.shape[0] and 0 <= coord[1] < grid.shape[1]


def move(direction: Direction, coord: Coord, distance: int = 1) -> Coord:
    if direction == Direction.UP:
        return (coord[0] - distance, coord[1])
    elif direction == Direction.RIGHT:
        return (coord[0], coord[1] + distance)
    elif direction == Direction.DOWN:
        return (coord[0] + distance, coord[1])
    else:
        return (coord[0], coord[1] - distance)


def get_left_and_right_neighbours(
    coord: Coord, direction: Direction
) -> list[tuple[Coord, Direction]]:
    possible_candidates_left = [
        move(direction.turn_left(), coord, d) for d in range(1, 4)
    ]
    possible_candidates_right = [
        move(direction.turn_right(), coord, d) for d in range(1, 4)
    ]
    return [
        (c, direction.turn_left())
        for c in filter(in_bounds, possible_candidates_left)
    ] + [
        (c, direction.turn_right())
        for c in filter(in_bounds, possible_candidates_right)
    ]


def get_distance_between(c1: Coord, c2: Coord) -> int:
    x1, y1 = c1
    x2, y2 = c2

    distance = np.sum(
        grid[min(x1, x2) : max(x1, x2) + 1, min(y1, y2) : max(y1, y2) + 1]
    )
    return distance


distance_grid = np.full(grid.shape, 1000000000)
previous_coord: dict[Coord, set[tuple[Coord, Direction]]] = {}
distance_grid[start_coord] = grid[start_coord]

unvisited_coords: list[tuple[Coord, Axis]] = []

for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        unvisited_coords.append(((i, j), Axis.VERTICAL))
        unvisited_coords.append(((i, j), Axis.HORIZONTAL))

while len(unvisited_coords) > 0:
    min_tuple = min(
        [(distance_grid[t[0]], t) for t in unvisited_coords],
        key=lambda x: x[0],
    )[1]
    unvisited_coords.remove(min_tuple)

    u, axis = min_tuple
    if u == start_coord:
        neighbours = [
            (move(Direction.RIGHT, u, d), Direction.RIGHT) for d in range(1, 3)
        ] + [(move(Direction.DOWN, u, d), Direction.DOWN) for d in range(1, 3)]

        for v, d in neighbours:
            alt = distance_grid[u] + get_distance_between(u, v) - grid[u]

            if alt <= distance_grid[v]:
                distance_grid[v] = alt
                if v not in previous_coord:
                    previous_coord[v] = set()
                previous_coord[v].add((u, d))
    else:
        possible_come_from = previous_coord[u]
        for _, cd in possible_come_from:
            neighbours = get_left_and_right_neighbours(u, cd)

            for v, d in neighbours:
                # if v not in unvisited_coords:
                #     continue
                alt = distance_grid[u] + get_distance_between(u, v) - grid[u]

                if alt < distance_grid[v]:
                    distance_grid[v] = alt
                    previous_coord[v] = set()
                    previous_coord[v].add((u, d))

                if alt == distance_grid[v]:
                    distance_grid[v] = alt
                    previous_coord[v].add((u, d))


curr_coord = end_coord
path = []
while curr_coord != start_coord:
    path.append(curr_coord)
    possible_come_from = previous_coord[curr_coord]
    if len(possible_come_from) > 1:
        print("Multiple possible come from", curr_coord, possible_come_from)
        break
    curr_coord = list(possible_come_from)[0][0]
path.append(start_coord)
path.reverse()

path_grid = np.full(grid.shape, ".")
for c in path:
    path_grid[c] = "X"

for l in path_grid:
    print("".join([str(i) for i in l]))
