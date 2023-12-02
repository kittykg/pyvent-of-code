with open("input/day02", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def parse_line(l: str) -> tuple[int, list[dict[str, int]]]:
    sl = l.split(":")
    game_id = int(sl[0].split(" ")[-1])
    parsed_dicts = []
    for b in sl[1].split(";"):
        d = {}
        for s in b.split(","):
            non_empty = list(filter(lambda x: x != "", s.split(" ")))
            d[non_empty[1]] = int(non_empty[0])
        parsed_dicts.append(d)
    return game_id, parsed_dicts


def satisfy(parsed_dict_list: list[dict[str, int]]) -> bool:
    for d in parsed_dict_list:
        # only 12 red cubes, 13 green cubes, and 14 blue cubes
        if "red" in d and d["red"] > 12:
            return False
        if "green" in d and d["green"] > 13:
            return False
        if "blue" in d and d["blue"] > 14:
            return False

    return True


def task_1() -> int:
    acc = 0
    for l in lines:
        game_id, parsed_dict_list = parse_line(l)
        if satisfy(parsed_dict_list):
            acc += game_id
    return acc


def power_of_bag(parsed_dict_list: list[dict[str, int]]) -> int:
    red_min = max([d["red"] for d in parsed_dict_list if "red" in d])
    green_min = max([d["green"] for d in parsed_dict_list if "green" in d])
    blue_min = max([d["blue"] for d in parsed_dict_list if "blue" in d])

    return red_min * green_min * blue_min


def task_2() -> int:
    acc = 0
    for l in lines:
        _, parsed_dict_list = parse_line(l)
        acc += power_of_bag(parsed_dict_list)
    return acc


print(task_1())
print(task_2())


def prolog_input() -> None:
    with open("day02.out", "w") as f:
        f.write("input([\n")
        pdl_str_list = []
        for l in lines:
            game_id, parsed_dict_list = parse_line(l)
            pdl_str = "["
            pdl_str += ",".join(
                [
                    ",".join([f"({k},{v})" for k, v in d.items()])
                    for d in parsed_dict_list
                ]
            )
            pdl_str += "]"
            pdl_str_list.append(f"({game_id},{pdl_str})")
        f.write(",\n".join(pdl_str_list))
        f.write("]).")


prolog_input()
