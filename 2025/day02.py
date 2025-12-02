# %%
with open("input/day02", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


# %%
def parse_line(l: str) -> list[tuple[int, int]]:
    return [parse_range(r) for r in l.split(",")]


def parse_range(r: str) -> tuple[int, int]:
    return tuple(map(int, r.split("-")))


ranges = [parse_line(l) for l in lines][0]


# %%
def invalid_number_task_1(n: int) -> bool:
    num_digits = len(str(n))
    if num_digits % 2:  # odd number of digits, valid
        return False
    return str(n)[: num_digits // 2] == str(n)[num_digits // 2 :]


# %%
def invalid_number_task_2(n: int) -> bool:
    num_digits = len(str(n))
    for size in range(1, num_digits // 2 + 1):
        if num_digits % size > 0:
            continue
        parts = [
            str(n)[j * size : (j + 1) * size] for j in range(num_digits // size)
        ]
        if all(part == parts[0] for part in parts):
            return True
    return False


# %%
acc_1, acc_2 = 0, 0
for n1, n2 in ranges:
    for n in range(n1, n2 + 1):
        if invalid_number_task_1(n):
            acc_1 += n
        if invalid_number_task_2(n):
            acc_2 += n


print(f"Task 1: {acc_1}")
print(f"Task 2: {acc_2}")

# %%
