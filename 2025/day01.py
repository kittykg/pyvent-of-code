# %%
with open("input/day01", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

# %%

n, count_1, count_2 = 50, 0, 0
for l in lines:
    direction, movement = l[0], int(l[1:])
    tmp = n - movement if direction == "L" else n + movement
    count_2 += abs(tmp) // 100 + int(n != 0 and tmp <= 0)
    n = tmp % 100
    count_1 += 1 if n == 0 else 0

print(count_1)
print(count_2)
