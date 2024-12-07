from itertools import product

with open("input/day07", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def parse_line(line: str) -> tuple[int, list[int]]:
    expected_sum = int(line.split(": ")[0])
    numbers = list(map(int, line.split(": ")[1].split(" ")))
    return expected_sum, numbers


equations = list(map(parse_line, lines))


def possible_computation(
    expected_sum: int, numbers: list[int], operators: str = "+*"
) -> bool:
    for possible_ops in product(operators, repeat=len(numbers) - 1):
        result = numbers[0]
        for i in range(len(possible_ops)):
            if possible_ops[i] == "+":
                result += numbers[i + 1]
            elif possible_ops[i] == "*":
                result *= numbers[i + 1]
            else:
                # Part 2 -- '|', concat operator
                result = int(str(result) + str(numbers[i + 1]))
        if result == expected_sum:
            return True

    return False


print(sum(es for es, ns in equations if possible_computation(es, ns)))
print(sum(es for es, ns in equations if possible_computation(es, ns, "+*|")))
