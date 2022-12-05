import re
import copy
from dataclasses import dataclass
from typing import List


@dataclass
class Instruction:
    num_crates: int
    source: int  # zero index
    dest: int  # zero index


def parse_instruction_string(s: str) -> Instruction:
    m = re.match(r"move (\d+) from (\d) to (\d)", s)
    assert m
    return Instruction(int(m[1]), int(m[2]) - 1, int(m[3]) - 1)


with open("input/day05", "r") as f:
    inst_lines = list(filter(lambda x: x != "", f.read().split("\n")))
instructions = [parse_instruction_string(l) for l in inst_lines]

with open('input_05', 'w') as f:
    for i in instructions:
        print(f'{i.num_crates},{i.source},{i.dest}', file=f)

with open("input/day05_crate", "r") as f:
    crate_lines = list(filter(lambda x: x != "", f.read().split("\n")))
crates = [l.split(",") for l in crate_lines]


def task(
    insts: List[Instruction], cs: List[List[str]], retain_order: bool
) -> None:
    for inst in insts:
        s = cs[inst.source][-inst.num_crates :]
        if not retain_order:
            s.reverse()
        cs[inst.dest] += s
        del cs[inst.source][-inst.num_crates :]
    print("".join([c[-1] for c in cs]))


task(copy.deepcopy(instructions), copy.deepcopy(crates), False)
task(copy.deepcopy(instructions), copy.deepcopy(crates), True)
