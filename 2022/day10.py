from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class InstructionType(Enum):
    NOOP = "noop"
    ADDX = "addx"


@dataclass
class Instruction:
    type: InstructionType
    val: Optional[int]


def parse_line(l: str) -> Instruction:
    sl = l.split(" ")
    if len(sl) == 1:
        return Instruction(InstructionType.NOOP, None)
    else:
        return Instruction(InstructionType.ADDX, int(sl[1]))


with open("input/day10", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
instructions = [parse_line(l) for l in lines]


def task_1(instructions: List[Instruction]) -> None:
    x_val = []
    curr_x = 1
    for i in instructions:
        if i.type == InstructionType.NOOP:
            x_val.append(curr_x)
        else:
            assert i.type == InstructionType.ADDX
            assert i.val
            x_val.append(curr_x)
            curr_x += i.val
            x_val.append(curr_x)

    def get_signal_strength(x_val: List[int], cycle: int) -> int:
        # cycle is 1 index
        return x_val[cycle - 2] * cycle

    print(
        sum(
            [
                get_signal_strength(x_val, c)
                for c in [20, 60, 100, 140, 180, 220]
            ]
        )
    )


def task_2(instructions: List[Instruction]) -> None:
    curr_x = 1
    pixel = []
    curr_crt_pos = 0

    def sprite_in_range(x: int, crt_pos: int) -> bool:
        return crt_pos in [x - 1, x, x + 1]

    for i in instructions:
        pixel.append("#" if sprite_in_range(curr_x, curr_crt_pos) else ".")
        curr_crt_pos += 1
        if curr_crt_pos == 40:
            curr_crt_pos = 0
        if i.type == InstructionType.ADDX:
            assert i.val
            pixel.append("#" if sprite_in_range(curr_x, curr_crt_pos) else ".")
            curr_crt_pos += 1
            curr_x += i.val
            if curr_crt_pos == 40:
                curr_crt_pos = 0

    for i in range(6):
        print("".join(pixel[i * 40 : (i + 1) * 40]))


task_1(instructions)
task_2(instructions)
