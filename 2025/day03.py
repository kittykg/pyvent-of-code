# %%
with open("input/day03", "r") as f:
    banks = list(filter(lambda x: x != "", f.read().split("\n")))


def f(bank: str, length: int) -> str:
    acc = ""
    for remain in range(length - 1, -1, -1):
        j = bank.index(max(bank[: len(bank) - remain]))
        acc += bank[j]
        bank = bank[j + 1 :]
    return int(acc)


print(sum(f(b, 2) for b in banks))
print(sum(f(b, 12) for b in banks))

# %%
