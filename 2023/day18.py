import numpy as np
from enum import IntEnum
from typing import Callable


Coord = tuple[int, int]

with open("input/day18", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


class Direction(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


def parse_line(l: str) -> tuple[Direction, int, str]:
    dir_str, movement_str, hex_code = l.split(" ")
    if dir_str == "R":
        direction = Direction.RIGHT
    elif dir_str == "L":
        direction = Direction.LEFT
    elif dir_str == "U":
        direction = Direction.UP
    else:
        direction = Direction.DOWN
    movement = int(movement_str)
    hex_code = hex_code[1:-1]
    return (direction, movement, hex_code)


instructions = [parse_line(l) for l in lines]


def move(curr_coord: Coord, direction: Direction, movement: int) -> Coord:
    if direction == Direction.UP:
        return (curr_coord[0] - movement, curr_coord[1])
    elif direction == Direction.RIGHT:
        return (curr_coord[0], curr_coord[1] + movement)
    elif direction == Direction.DOWN:
        return (curr_coord[0] + movement, curr_coord[1])
    else:
        return (curr_coord[0], curr_coord[1] - movement)


def parse_hex_code_to_instructions(hex_code: str) -> tuple[Direction, int]:
    return (Direction(int(hex_code[-1])), int(hex_code[1:-1], 16))


def task(
    instruction_fn: Callable[
        [tuple[Direction, int, str]], tuple[Direction, int]
    ]
) -> int:
    curr_coord = (0, 0)
    points: list[Coord] = []
    lava_count = 0
    for instr in instructions:
        direction, movement = instruction_fn(instr)
        curr_coord = move(curr_coord, direction, movement)
        lava_count += movement
        points.append(curr_coord)

    # Shoelace formula to calculate the area of the polygon
    area = 0
    for c1, c2 in zip(points, (points[1:] + [points[0]])):
        area += c1[0] * c2[1] - c1[1] * c2[0]
    area /= 2

    # Pick's theorem + lava count
    return int(lava_count + abs(area) - lava_count / 2 + 1)


print(task(lambda x: (x[0], x[1])))
print(task(lambda x: parse_hex_code_to_instructions(x[2])))
