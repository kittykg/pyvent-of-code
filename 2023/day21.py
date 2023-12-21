import numpy as np
from enum import IntEnum

Coord = tuple[int, int]

with open("input/day21", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
og_grid = np.array([list(s) for s in lines])


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def move_one_direction(coord: Coord, direction: Direction) -> Coord:
    if direction == Direction.UP:
        return (coord[0] - 1, coord[1])
    elif direction == Direction.RIGHT:
        return (coord[0], coord[1] + 1)
    elif direction == Direction.DOWN:
        return (coord[0] + 1, coord[1])
    else:
        return (coord[0], coord[1] - 1)


def task_1():
    start = (np.where(og_grid == "S")[0][0], np.where(og_grid == "S")[1][0])

    def in_bound(coord: Coord) -> bool:
        return (
            0 <= coord[0] < og_grid.shape[0]
            and 0 <= coord[1] < og_grid.shape[1]
        )

    def move_all_directions(coord: Coord) -> list[Coord]:
        return list(
            filter(
                lambda c: in_bound(c),
                [move_one_direction(coord, d) for d in Direction],
            )
        )

    def move_one_step(coord_list: list[Coord]) -> list[Coord]:
        new_coords = set()
        for i in range(len(coord_list)):
            for c in move_all_directions(coord_list[i]):
                if og_grid[c] != "#":
                    new_coords.add(c)
        return list(new_coords)

    coord_list = [start]
    for _ in range(64):
        coord_list = move_one_step(coord_list)
    return len(coord_list)


print(task_1())


# def print_grid(coords: list[Coord]):
#     new_grid = og_grid.copy()
#     for c in coords:
#         if 0 <= c[0] < og_grid.shape[0] and 0 <= c[1] < og_grid.shape[1]:
#             new_grid[c] = "O"

#     for l in new_grid:
#         print("".join(l))


# def print_grid_expand(coords: list[Coord]):
#     start = (np.where(og_grid == "S")[0][0], np.where(og_grid == "S")[1][0])

#     x_min = min([c[0] for c in coords])
#     x_max = max([c[0] for c in coords])
#     y_min = min([c[1] for c in coords])
#     y_max = max([c[1] for c in coords])

#     grid_x_count = (abs(x_min) // og_grid.shape[0] + 1) + (
#         x_max // og_grid.shape[0] + 1
#     )
#     grid_y_count = (abs(y_min) // og_grid.shape[1] + 1) + (
#         y_max // og_grid.shape[1] + 1
#     )

#     og_grid_location = (
#         abs(x_min) // og_grid.shape[0] + 1,
#         abs(y_min) // og_grid.shape[1] + 1,
#     )
#     og_start_location = (
#         start[0] + og_grid_location[0] * og_grid.shape[0],
#         start[1] + og_grid_location[1] * og_grid.shape[1],
#     )

#     new_grid = np.full(
#         (grid_x_count * og_grid.shape[0], grid_y_count * og_grid.shape[1]), "."
#     )
#     no_start_grid = og_grid.copy()
#     no_start_grid[start] = "."
#     for i in range(grid_x_count):
#         for j in range(grid_y_count):
#             if (i, j) == og_grid_location:
#                 copy_grid = og_grid
#             else:
#                 copy_grid = no_start_grid
#             new_grid[
#                 i * og_grid.shape[0] : (i + 1) * og_grid.shape[0],
#                 j * og_grid.shape[1] : (j + 1) * og_grid.shape[1],
#             ] = copy_grid

#     for c in coords:
#         c_x = c[0] - start[0] + og_start_location[0]
#         c_y = c[1] - start[1] + og_start_location[1]
#         new_grid[c_x, c_y] = "O"

#     for l in new_grid:
#         print("".join(l))


# def task_2():
#     start = (np.where(og_grid == "S")[0][0], np.where(og_grid == "S")[1][0])

#     def remap_coord(coord: Coord) -> Coord:
#         return (coord[0] % og_grid.shape[0], coord[1] % og_grid.shape[1])

#     def move_one_step(coord_list: list[Coord]) -> list[Coord]:
#         new_coords = set()
#         for i in range(len(coord_list)):
#             for c in [move_one_direction(coord_list[i], d) for d in Direction]:
#                 if og_grid[remap_coord(c)] != "#":
#                     new_coords.add(c)
#         return list(new_coords)

#     def edge_points(coord_list: list[Coord]) -> list[Coord]:
#         x_min = min([c[0] for c in coord_list])
#         x_max = max([c[0] for c in coord_list])

#         x_min_ys = [c[1] for c in coord_list if c[0] == x_min]
#         x_max_ys = [c[1] for c in coord_list if c[0] == x_max]

#         return [
#             (x_min, min(x_min_ys)),
#             (x_min, max(x_min_ys)),
#             (x_max, min(x_max_ys)),
#             (x_max, max(x_max_ys)),
#         ]

#     coord_list = [start]

#     for j in range(40):
#         coord_list = move_one_step(coord_list)
#         in_bound_coord = sorted(
#             [
#                 c
#                 for c in coord_list
#                 if 0 <= c[0] < og_grid.shape[0] and 0 <= c[1] < og_grid.shape[1]
#             ]
#         )

#         out_bound_coord = sorted(
#             [
#                 c
#                 for c in coord_list
#                 if not (0 <= c[0] < og_grid.shape[0])
#                 or not (0 <= c[1] < og_grid.shape[1])
#             ]
#         )

#         ep = sorted(edge_points(coord_list))
#         if j >= 10:
#             print(j)
#             print(in_bound_coord)
#             print(len(in_bound_coord))
#             print(ep)
#             print()

#         if (-5, -5) in out_bound_coord:
#             print(j)
#             print_grid_expand(coord_list)

#         if in_bound_coord in coord_list_history:
#             print(in_bound_coord)
#             print(coord_list_history.index(in_bound_coord))
#             print(out_bound_coord)
#             print(len(in_bound_coord))
#             break
#         else:
#             coord_list_history.append(in_bound_coord)

#         if j % 10 == 0:
#             print(j)
#             print_grid_expand(coord_list)
#             print()

#     return len(coord_list)


# print(task_2())
