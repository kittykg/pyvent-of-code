import math

with open("input/day06", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

time = [int(s) for s in lines[0].split(":")[1].split(" ") if s != ""]
distance = [int(s) for s in lines[1].split(":")[1].split(" ") if s != ""]


def strategy(t, d) -> int:
    # solve x^2 - tx + d < 0
    # x = (t +- sqrt(t^2 - 4d)) / 2
    sqrt = math.sqrt(t**2 - 4 * d)
    x1 = math.floor((t + sqrt) / 2)
    x2 = math.ceil((t - sqrt) / 2)
    return x1 - x2 + 1


def task_1() -> int:
    acc_prod = 1
    for t, d in zip(time, distance):
        acc_prod *= strategy(t, d)
    return acc_prod


def task_2() -> int:
    t = int("".join([str(i) for i in time]))
    d = int("".join([str(i) for i in distance]))
    return strategy(t, d)


print(task_1())
print(task_2())
