# %%
with open("input/day05", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

# %%
fresh_ranges: list[tuple[int, int]] = []
products = []

for l in lines:
    if "-" in l:
        fresh_ranges.append(tuple(map(int, l.split("-"))))
    else:
        products.append(int(l))

fresh_ranges.sort(key=lambda x: x[0])

while True:
    for i in range(len(fresh_ranges) - 1):
        r1, r2 = fresh_ranges[i][0], fresh_ranges[i][1]
        r3, r4 = fresh_ranges[i + 1][0], fresh_ranges[i + 1][1]
        if r2 < r3:
            continue
        # merge the two ranges
        fresh_ranges[i] = (min(r1, r3), max(r2, r4))
        fresh_ranges.pop(i + 1)
        break
    if i == len(fresh_ranges) - 1:
        break


acc_1 = 0
for p in products:
    for r in fresh_ranges:
        if r[0] <= p <= r[1]:
            acc_1 += 1
            break
print(acc_1)


acc_2 = 0
for r in fresh_ranges:
    acc_2 += r[1] - r[0] + 1
print(acc_2)

# %%
