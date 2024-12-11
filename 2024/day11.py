with open("input/day11", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
stones = list(map(int, lines[0].split(" ")))


def stone_split(stone: int) -> list[int]:
    if stone == 0:
        return [1]

    if len(str(stone)) % 2 == 0:
        stone_1 = int(str(stone)[: len(str(stone)) // 2])
        stone_2 = int(str(stone)[len(str(stone)) // 2 :])
        return [stone_1, stone_2]

    return [stone * 2024]


def blink(stone_count: dict[int, int]) -> dict[int, int]:
    new_stone_count = dict()
    for stone, count in stone_count.items():
        # print(stone, stone_split(stone))
        for ns in stone_split(stone):
            if ns not in new_stone_count:
                new_stone_count[ns] = 0
            new_stone_count[ns] += count
    return new_stone_count


def blink_n(stone_count: dict[int, int], n: int) -> int:
    for _ in range(n):
        stone_count = blink(stone_count)
    return sum(v for v in stone_count.values())


from datetime import datetime

start = datetime.now()
stone_count = dict()
for s in stones:
    if s not in stone_count:
        stone_count[s] = 0
    stone_count[s] += 1

print(blink_n(stone_count, 25))
print(blink_n(stone_count, 75))
print(f"Time: {datetime.now() - start}")
