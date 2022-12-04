from typing import Tuple, Set


def parse_string(l: str) -> Tuple[Set[int], Set[int]]:
    a_string, b_string = l.split(",")
    a = set(range(int(a_string.split("-")[0]), int(a_string.split("-")[1]) + 1))
    b = set(range(int(b_string.split("-")[0]), int(b_string.split("-")[1]) + 1))
    return a, b


def is_subset(l: str) -> bool:
    a, b = parse_string(l)
    return a.issubset(b) or b.issubset(a)


def has_intersection(l: str) -> bool:
    a, b = parse_string(l)
    return len(a.intersection(b)) > 0


with open("input/day04", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
# Task 1
print(len(list(filter(is_subset, lines))))
# Task 2
print(len(list(filter(has_intersection, lines))))
