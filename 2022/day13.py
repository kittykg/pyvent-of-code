import copy
from enum import IntEnum
from functools import cmp_to_key


class Result(IntEnum):
    true = 1
    hold = 0
    false = -1


def in_right_order(l1: list, l2: list) -> int:
    l1_copy = copy.deepcopy(l1)
    l2_copy = copy.deepcopy(l2)

    while True:
        if len(l1_copy) == 0 and len(l2_copy) > 0:
            # l1 run out, right order
            return Result.true
        if len(l1_copy) > 0 and len(l2_copy) == 0:
            # l2 run out, not right order
            return Result.false
        if len(l1_copy) == 0 and len(l2_copy) == 0:
            # Reach end of list, all items equal
            return Result.hold

        # Both list has items left, continue the loop
        i1 = l1_copy.pop(0)
        i2 = l2_copy.pop(0)

        if type(i1) == int and type(i2) == int:
            if i1 < i2:
                return Result.true
            elif i1 == i2:
                continue
            else:
                return Result.false
        elif type(i1) == list and type(i2) == list:
            res = in_right_order(i1, i2)
            if res == Result.true:
                return Result.true
            elif res == Result.hold:
                continue
            else:
                return Result.false
        else:  # mixed type
            if type(i1) == int:
                i1 = [i1]
            else:
                i2 = [i2]
            res = in_right_order(i1, i2)
            if res == Result.true:
                return Result.true
            elif res == Result.hold:
                continue
            else:
                return Result.false


with open("input/day13", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def task_1():
    lists = [eval(l) for l in lines]
    res_list = [
        in_right_order(lists[i * 2], lists[i * 2 + 1])
        for i in range(len(lists) // 2)
    ]
    indices = [i + 1 for i, r in enumerate(res_list) if r == Result.true]
    print(sum(indices))


def task_2():
    DIVIDER_1 = [[2]]
    DIVIDER_2 = [[6]]
    lists = [eval(l) for l in lines]
    lists.append(DIVIDER_1)
    lists.append(DIVIDER_2)
    sorted_lists = sorted(lists, key=cmp_to_key(in_right_order), reverse=True)
    d1_index = sorted_lists.index(DIVIDER_1) + 1
    d2_index = sorted_lists.index(DIVIDER_2) + 1
    print(d1_index * d2_index)


task_1()
task_2()
