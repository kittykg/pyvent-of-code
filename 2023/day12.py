from itertools import product


with open("input/day12", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def task_1():
    def check_match(pattern: str, expected_group: list[int]) -> bool:
        hash_groups_len = list(
            map(len, filter(lambda x: x != "", pattern.split(".")))
        )
        return hash_groups_len == expected_group

    def possible_arrangement(og_pattern: str, expected_group: list[int]):
        possible_arrangement_count = 0

        for fills in product(["#", "."], repeat=og_pattern.count("?")):
            pattern = ""
            j = 0
            for i in range(len(og_pattern)):
                if og_pattern[i] == "?":
                    pattern += fills[j]
                    j += 1
                else:
                    pattern += og_pattern[i]

            if check_match(pattern, expected_group):
                possible_arrangement_count += 1
        return possible_arrangement_count

    acc_sum = 0
    for l in lines:
        og_pattern, expected_group = l.split(" ")
        acc_sum += possible_arrangement(
            og_pattern, list(map(int, expected_group.split(",")))
        )
    return acc_sum


print(task_1())
