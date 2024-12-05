with open("input/day05", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

orders = [tuple(map(int, l.split("|"))) for l in lines if "|" in l]
updates = [list(map(int, l.split(","))) for l in lines if "," in l]
assert len(orders) + len(updates) == len(lines)

orders_dict = {}
for n1, n2 in orders:
    if n1 not in orders_dict:
        orders_dict[n1] = []
    orders_dict[n1].append(n2)


def safe_update(update: list[int]) -> bool:
    for i in range(len(update) - 1):
        n1 = update[i]
        for j in range(i + 1, len(update)):
            n2 = update[j]
            n2_order = orders_dict.get(n2, [])
            if n2_order == []:
                continue
            if n1 in n2_order:
                return False
    return True


def change_unsafe_update(update: list[int]) -> int:
    safe = False
    while not safe:
        safe = True
        for i in range(len(update) - 1):
            n1 = update[i]
            swapped = False
            for j in range(i + 1, len(update)):
                n2 = update[j]
                n2_order = orders_dict.get(n2, [])
                if n2_order == []:
                    continue
                if n1 in n2_order:
                    temp = update[i]
                    update[i] = update[j]
                    update[j] = temp
                    safe = False
                    break
            if swapped:
                break

    return update[len(update) // 2]


safe_updates, unsafe_updates = [], []
for update in updates:
    if safe_update(update):
        safe_updates.append(update)
    else:
        unsafe_updates.append(update)

print(sum(update[len(update) // 2] for update in safe_updates))
print(sum(change_unsafe_update(update) for update in unsafe_updates))
