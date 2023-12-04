with open("input/day04", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def parse_line(l: str) -> tuple[int, tuple[list[int], list[int]]]:
    sl = l.split(":")
    card_id = int(sl[0].split(" ")[-1])
    winning_numbers = [
        int(x)
        for x in filter(lambda x: x != "", sl[1].split("|")[0].split(" "))
    ]
    my_numbers = [
        int(x)
        for x in filter(lambda x: x != "", sl[1].split("|")[1].split(" "))
    ]
    return card_id, (winning_numbers, my_numbers)


def task_1() -> int:
    acc_sum = 0
    for l in lines:
        _, (winning_numbers, my_numbers) = parse_line(l)
        intersection = set(winning_numbers).intersection(set(my_numbers))
        if len(intersection) == 0:
            continue
        acc_sum += 2 ** (len(intersection) - 1)

    return acc_sum


def task_2() -> int:
    card_count = [1] * len(lines)
    for i, l in enumerate(lines):
        _, (winning_numbers, my_numbers) = parse_line(l)
        intersection = set(winning_numbers).intersection(set(my_numbers))
        if len(intersection) == 0:
            continue
        for j in range(len(intersection)):
            card_count[j + i + 1] += card_count[i]

    return sum(card_count)


print(task_1())
print(task_2())


def prolog_input() -> None:
    with open("day04.out", "w") as f:
        f.write("input([\n")
        pdl_str_list = []
        for l in lines:
            card_id, (winning_numbers, my_numbers) = parse_line(l)
            wns = f"[{','.join([str(x) for x in winning_numbers])}]"
            mns = f"[{','.join([str(x) for x in my_numbers])}]"
            pdl_str_list.append(f"({card_id},({wns},{mns}))")
        f.write(",\n".join(pdl_str_list))
        f.write("]).")


prolog_input()
