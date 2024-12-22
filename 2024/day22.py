with open("input/day22", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

initial_secret_numbers = list(map(int, lines))


def fn(i: int) -> int:
    i = ((i * 64) ^ i) % 16777216
    i = ((i // 32) ^ i) % 16777216
    i = ((i * 2048) ^ i) % 16777216
    return i


def get_secret_number_sequence(i: int) -> list[int]:
    sequence = [i]
    for _ in range(2000):
        i = fn(i)
        sequence.append(i)
    return sequence


def get_changes(sequence: list[int]) -> list[int]:
    changes = []
    for i in range(1, len(sequence)):
        changes.append(sequence[i] - sequence[i - 1])
    return changes


all_secrete_number_sequences = [
    get_secret_number_sequence(i) for i in initial_secret_numbers
]
all_prices = [
    list(map(lambda x: x % 10, s)) for s in all_secrete_number_sequences
]
all_changes = [get_changes(s) for s in all_prices]

print(f"Part 1: {sum(s[-1] for s in all_secrete_number_sequences)}")


seq_to_price_map = {}

for i in range(len(all_changes)):
    prices = all_prices[i]
    changes = all_changes[i]

    seen = set()

    for j in range(len(changes) - 3):
        seq = (
            changes[j],
            changes[j + 1],
            changes[j + 2],
            changes[j + 3],
        )
        if seq in seen:
            continue

        seen.add(seq)
        if seq not in seq_to_price_map:
            seq_to_price_map[seq] = 0
        seq_to_price_map[seq] += prices[j + 4]


print(f"Part 2: {sorted(seq_to_price_map.items(), key=lambda x: x[1])[-1][1]}")
