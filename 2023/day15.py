from functools import reduce

with open("input/day15", "r") as f:
    line = list(filter(lambda x: x != "", f.read().split("\n")))
str_seq = line[0].split(",")


def hash_char(curr_val: int, c: str) -> int:
    return (curr_val + ord(c)) * 17 % 256


def hash_str(s: str) -> int:
    return reduce(hash_char, list(s), 0)


def task_2():
    boxes = [[] for _ in range(256)]

    def find_in_box_tuple(
        box: list[tuple[str, int]], label: str
    ) -> tuple[str, int] | None:
        for l, i in box:
            if l == label:
                return (l, i)
        return None

    def find_in_box_idx(box: list[tuple[str, int]], label: str) -> int:
        for i, (l, _) in enumerate(box):
            if l == label:
                return i
        return -1

    def operation_plus(s: str):
        label, focal_length_str = s.split("=")
        box_id = hash_str(label)
        focal_length = int(focal_length_str)

        idx = find_in_box_idx(boxes[box_id], label)
        if idx == -1:
            boxes[box_id].append((label, focal_length))
        else:
            boxes[box_id][idx] = (label, focal_length)

    def operation_minus(s: str):
        label, _ = s.split("-")
        box_id = hash_str(label)

        t = find_in_box_tuple(boxes[box_id], label)
        if t != None:
            boxes[box_id].remove(t)

    for s in str_seq:
        if "=" in s:
            operation_plus(s)
        else:
            operation_minus(s)

    acc_sum = 0
    for i, b in enumerate(boxes):
        for j, (_, f) in enumerate(b):
            acc_sum += (i + 1) * (j + 1) * f

    return acc_sum


# Task 1
print(sum(hash_str(s) for s in str_seq))
# Task 2
print(task_2())
