# %%
import numpy as np


# %%

with open("input/day06", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

operators = list(filter(lambda x: x != "", lines.pop().split()))
num_arrays = np.array([(list[int](map(int, line.split()))) for line in lines])

acc_1 = 0
for i, o in enumerate(operators):
    if o == "*":
        acc_1 += np.prod(num_arrays[:, i])
    else:
        acc_1 += np.sum(num_arrays[:, i])
print(acc_1)


# %%

with open("input/day06", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
operators = list(filter(lambda x: x != "", lines.pop().split()))

max_len = max(len(l) for l in lines)
for i in range(len(lines)):
    if len(lines[i]) != max_len:
        lines[i] += " " * (max_len - len(lines[i]))
char_arrays = np.array([list(line) for line in lines])

_, y = char_arrays.shape
acc_2 = 0
prev = None
for i in range(y - 1, -1, -1):
    if np.all(char_arrays[:, i] == " "):
        if prev is None:
            c = char_arrays[:, i + 1 :].T
        else:
            c = char_arrays[:, i + 1 : prev].T
        nums = [int("".join(map(str, row.flatten()))) for row in c]
        op = operators.pop()
        if op == "+":
            acc_2 += sum(nums)
        elif op == "*":
            acc_2 += np.prod(nums)
        prev = i

c = char_arrays[:, 0:prev].T
nums = [int("".join(map(str, row.flatten()))) for row in c]
op = operators.pop(0)
if op == "+":
    acc_2 += sum(nums)
elif op == "*":
    acc_2 += np.prod(nums)

print(acc_2)
# %%
