from copy import deepcopy
import functools
import operator
import re
from typing import List, Optional


class Monkey:
    id: int
    items: List[int]
    op: str
    op_num: Optional[int]
    test_num: int
    true_action: int
    false_action: int
    inspect_items_times: int

    def __init__(
        self,
        id: int,
        items: List[int],
        op: str,
        op_num: Optional[int],
        test_num: int,
        true_action: int,
        false_action: int,
    ) -> None:
        self.id = id
        self.items = items
        self.op = op
        self.op_num = op_num
        self.test_num = test_num
        self.true_action = true_action
        self.false_action = false_action
        self.inspect_items_times = 0

    def inspect(self, item: int) -> int:
        if self.op_num is None and self.op == "*":
            new_item = item * item
        elif self.op_num is None and self.op == "+":
            new_item = item + item
        elif self.op == "*":
            assert self.op_num
            new_item = item * self.op_num
        else:
            assert self.op_num
            new_item = item + self.op_num

        self.inspect_items_times += 1
        return new_item

    def test_item(self, item: int) -> int:
        if item % self.test_num == 0:
            return self.true_action
        else:
            return self.false_action

    def __str__(self) -> str:
        if self.op_num is None and self.op == "*":
            operation_str = f"old * old"
        elif self.op_num is None and self.op == "+":
            operation_str = f"old + old"
        elif self.op == "*":
            assert self.op_num
            operation_str = f"old * {self.op_num}"
        else:
            assert self.op_num
            operation_str = f"old + {self.op_num}"
        return "\n".join(
            [
                f"Monkey {self.id}:",
                f"  Items {self.items}",
                f"  Operation: {operation_str}",
                f"  Test: % {self.test_num}",
                f"    True: {self.true_action}",
                f"    False: {self.false_action}",
            ]
        )


with open("input/day11", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def parse_monkey(line_group: List[str]) -> Monkey:
    id = int(re.findall(r"\d", line_group[0])[0])
    items = [int(i) for i in line_group[1][18:].split(", ")]
    op_num_candidate = re.findall(r"\d", line_group[2])
    op_sign = re.findall(r"[+*]", line_group[2])[0]
    test_num = int("".join(re.findall(r"\d", line_group[3])))
    true_action = int(re.findall(r"\d", line_group[4])[0])
    false_action = int(re.findall(r"\d", line_group[5])[0])

    return Monkey(
        id=id,
        items=items,
        op=op_sign,
        op_num=int("".join(op_num_candidate)) if op_num_candidate else None,
        test_num=test_num,
        true_action=true_action,
        false_action=false_action,
    )


monkeys: List[Monkey] = [
    parse_monkey(lines[i * 6 : (i + 1) * 6]) for i in range(8)
]


def round(
    monkeys: List[Monkey], divide_by_3: bool = True, prime_product: int = 1
) -> None:
    for m in monkeys:
        while len(m.items) > 0:
            worry = m.items.pop(0)
            new_worry = m.inspect(worry)
            if divide_by_3:
                new_worry = new_worry // 3
            else:
                new_worry = new_worry % prime_product
            monkeys[m.test_item(new_worry)].items.append(new_worry)


def task_1(monkeys: List[Monkey]) -> None:
    for _ in range(20):
        round(monkeys)
    t1, t2 = sorted([m.inspect_items_times for m in monkeys], reverse=True)[:2]
    print(t1 * t2)


def task_2(monkeys: List[Monkey]) -> None:
    prime_product = functools.reduce(
        operator.mul, [m.test_num for m in monkeys]
    )
    for _ in range(10000):
        round(monkeys, divide_by_3=False, prime_product=prime_product)
    t1, t2 = sorted([m.inspect_items_times for m in monkeys], reverse=True)[:2]
    print(t1 * t2)


task_1(deepcopy(monkeys))
task_2(deepcopy(monkeys))
