with open("input/day02", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


levels = list(map(lambda l: list(map(int, l.split())), lines))


def safe(level: list[int]):
    diff = level[1] - level[0]
    if diff == 0 or abs(diff) > 3:
        return False
    sign = diff > 0
    for i in range(1, len(level) - 1):
        diff = level[i + 1] - level[i]
        if diff == 0 or (diff > 0) != sign or abs(diff) > 3:
            return False
    return True


# def safe_np(level: list[int]):
#     import numpy as np

#     diffs = np.diff(np.array(level))
#     if not all(diffs):
#         return False
#     if np.any(np.sign(diffs[0]) != np.sign(diffs)):
#         return False
#     if not all(np.abs(diffs) <= 3):
#         return False
#     return True


def safe_2(level: list[int]):
    if safe(level):
        return True

    for i in range(len(level)):
        mod_level = level[:i] + level[i + 1 :]
        if safe(mod_level):
            return True

    return False


print(len(list(filter(safe, levels))))
print(len(list(filter(safe_2, levels))))
