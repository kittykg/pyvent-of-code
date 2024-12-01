from collections import Counter

with open("input/day01", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


number_list_1 = []
number_list_2 = []
for l in lines:
    n1, n2 = tuple(filter(lambda x: x != "", l.split(" ")))
    number_list_1.append(int(n1))
    number_list_2.append(int(n2))


def task_1():
    sorted_list_1 = sorted(number_list_1)
    sorted_list_2 = sorted(number_list_2)
    return sum(abs(x - y) for x, y in zip(sorted_list_1, sorted_list_2))


def task_2():
    counter_2 = Counter(number_list_2)

    total_diff = 0
    for n in number_list_1:
        if n not in counter_2:
            continue
        total_diff += n * counter_2[n]

    return total_diff


print(task_1())
print(task_2())
