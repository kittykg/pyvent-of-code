import re

with open("input/day03", "r") as f:
    instruction = "".join(list(filter(lambda x: x != "", f.read().split("\n"))))

p = re.compile(r"mul\((\d+),(\d+)\)")


def add_valid_mul(s):
    return sum([int(x) * int(y) for x, y in re.findall(p, s)])


def task_2():
    groups = re.split(r"don't\(\)", instruction)

    # Group 0 is guaranteed to be be executed
    total_sum = add_valid_mul(groups[0])

    # Group 1 onwards need to find do() first
    for g in groups[1:]:
        sub_g = re.split(r"do\(\)", g)
        if len(sub_g) == 1:
            # There is no do() in this group, nothing should be executed
            continue
        # Everything after the first do() should be executed
        total_sum += sum([add_valid_mul(g2) for g2 in sub_g[1:]])

    return total_sum


print(add_valid_mul(instruction))
print(task_2())
