from typing import List

with open("input/day03", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def shared_item(s: str) -> int:
    first = s[: int(len(s) / 2)]
    second = s[int(len(s) / 2) :]
    char = set(first).intersection(set(second)).pop()
    return ord(char) - (38 if char.isupper() else 96)


def shared_item_group(l: List[str]) -> int:
    char = set(l[0]).intersection(set(l[1])).intersection(set(l[2])).pop()
    return ord(char) - (38 if char.isupper() else 96)


print(sum([shared_item(l) for l in lines]))
print(
    sum([shared_item_group(lines[i : i + 3]) for i in range(0, len(lines), 3)])
)
