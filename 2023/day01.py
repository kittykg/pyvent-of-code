with open("input/day01", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def parse_line_1(l: str) -> int:
    d = list(filter(lambda x: x.isnumeric(), l))
    return int(f"{d[0]}{d[-1]}")


def parse_line_2(l: str) -> int:
    digits_in_str = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    digits_str = [str(i) for i in range(10)]

    front_ptr = 0
    back_ptr = -1

    first_digit = None
    last_digit = None

    while first_digit is None or last_digit is None:
        front_str = l[:front_ptr]
        back_str = l[back_ptr:]
        for i, ds in enumerate(digits_in_str):
            if ds in front_str and first_digit is None:
                first_digit = i
            elif ds in back_str and last_digit is None:
                last_digit = i
        for i, d in enumerate(digits_str):
            if d in front_str and first_digit is None:
                first_digit = i
            elif d in back_str and last_digit is None:
                last_digit = i

        front_ptr += 1
        back_ptr -= 1

    return int(f"{first_digit}{last_digit}")


nums = [parse_line_1(l) for l in lines]
print(sum(nums))
nums = [parse_line_2(l) for l in lines]
print(sum(nums))
