from dataclasses import dataclass
from enum import Enum
import math
from typing import List, Tuple

Position = Tuple[int, int]


class Direction(Enum):
    U = "U"
    D = "D"
    L = "L"
    R = "R"


@dataclass
class Movement:
    direction: Direction
    step: int


def parse_line(s: str) -> Movement:
    l = s.split(" ")
    return Movement(direction=eval(f"Direction.{l[0]}"), step=int(l[1]))


def move_head_one(curr_head_pos: Position, direction: Direction) -> Position:
    x, y = curr_head_pos
    if direction == Direction.U:
        return (x, y + 1)
    if direction == Direction.D:
        return (x, y - 1)
    if direction == Direction.L:
        return (x - 1, y)
    if direction == Direction.R:
        return (x + 1, y)


def move_tail(new_head_pos: Position, curr_tail_pos: Position) -> Position:
    head_x, head_y = new_head_pos
    tail_x, tail_y = curr_tail_pos
    x_diff = head_x - tail_x
    y_diff = head_y - tail_y

    if abs(x_diff) <= 1 and abs(y_diff) <= 1:  # within limit, no need to move
        return curr_tail_pos

    def _get_move_dist_(diff: int) -> int:
        if diff == 0:
            return 0
        return int(math.copysign(1, diff))

    return (tail_x + _get_move_dist_(x_diff), tail_y + _get_move_dist_(y_diff))


with open("input/day09", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
head_movements = [parse_line(l) for l in lines]


def task_1(head_movements: List[Movement]) -> None:
    curr_head_pos = (0, 0)
    curr_tail_pos = (0, 0)
    tail_visited = set()
    tail_visited.add(curr_tail_pos)

    for m in head_movements:
        for _ in range(m.step):
            curr_head_pos = move_head_one(curr_head_pos, m.direction)
            curr_tail_pos = move_tail(curr_head_pos, curr_tail_pos)
            tail_visited.add(curr_tail_pos)

    print(len(tail_visited))


def task_2(head_movements: List[Movement]) -> None:
    knots_pos: List[Position] = [(0, 0)] * 10
    tail_visited = set()
    tail_visited.add(knots_pos[-1])

    for m in head_movements:
        for _ in range(m.step):
            knots_pos[0] = move_head_one(knots_pos[0], m.direction)
            for i in range(9):
                knots_pos[i + 1] = move_tail(knots_pos[i], knots_pos[i + 1])
            tail_visited.add(knots_pos[-1])

    print(len(tail_visited))


task_1(head_movements)
task_2(head_movements)
