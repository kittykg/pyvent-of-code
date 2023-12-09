from functools import reduce


with open("input/day09", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
num_lists = [list(map(int, line.split(" "))) for line in lines]


def sequence_diff(sequence: list[int]) -> list[int]:
    return [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]


def sequence_diff_r(nl: list[int]) -> list[list[int]]:
    diff = sequence_diff(nl)
    if set(diff) == set([0]):
        return [diff]
    other_diffs = sequence_diff_r(diff)
    return [diff] + other_diffs


def extrapolate_sequence_1(prev_diff: int, sequence: list[int]) -> int:
    return sequence[-1] + prev_diff


def extrapolate_sequence_2(prev_diff: int, sequence: list[int]) -> int:
    return sequence[0] - prev_diff


def task(extrapolate_fn) -> int:
    acc_sum = 0
    for nl in num_lists:
        pyramid = [nl] + sequence_diff_r(nl)
        pyramid.reverse()
        acc_sum += reduce(lambda d, l: extrapolate_fn(d, l), pyramid[1:], 0)

    return acc_sum


print(task(extrapolate_sequence_1))  # task 1
print(task(extrapolate_sequence_2))  # task 2


def prolog_input():
    with open("day09.out", "w") as f:
        f.write("input([")
        f.write(",\n".join([f"[{','.join(map(str, nl))}]" for nl in num_lists]))
        f.write(f"]).\n")


prolog_input()
