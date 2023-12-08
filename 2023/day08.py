from dataclasses import dataclass
import math


@dataclass
class Connection:
    start: str
    left: str
    right: str


def parse_line_to_connection(l: str) -> Connection:
    start = l.split(" = ")[0]
    l_and_r = l.split(" = ")[1].split(", ")
    left = l_and_r[0][1:]
    right = l_and_r[1][:-1]
    return Connection(start, left, right)


with open("input/day08", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

instructions = lines[0]
connections = [parse_line_to_connection(l) for l in lines[1:]]
connections_dict = {c.start: c for c in connections}


def task_1():
    instruction_queue = [*instructions]
    curr_node = "AAA"
    steps_count = 0
    while curr_node != "ZZZ":
        conn = connections_dict[curr_node]
        instr = instruction_queue.pop(0)
        if instr == "L":
            curr_node = conn.left
        else:
            curr_node = conn.right
        steps_count += 1
        if len(instruction_queue) == 0:
            instruction_queue = [*instructions]
    return steps_count


def travel_2(start_node: str) -> int:
    def is_end_node(node: str) -> bool:
        return node[-1] == "Z"

    instruction_queue = [*instructions]
    curr_node = start_node
    steps_count = 0
    while not is_end_node(curr_node):
        conn = connections_dict[curr_node]
        instr = instruction_queue.pop(0)
        if instr == "L":
            curr_node = conn.left
        else:
            curr_node = conn.right
        steps_count += 1
        if len(instruction_queue) == 0:
            instruction_queue = [*instructions]
    return steps_count


def task_2():
    all_a_nodes = [c.start for c in connections if c.start[-1] == "A"]
    all_a_steps = [travel_2(a) for a in all_a_nodes]
    return math.lcm(*all_a_steps)


print(task_1())
print(task_2())


def prolog_input():
    with open("day08.out", "w") as f:
        f.write(f'instruction_str("{instructions}").\n')
        for c in connections:
            f.write(
                f"connection({c.start.lower()}, {c.left.lower()}, {c.right.lower()}).\n"
            )


prolog_input()
