def is_marker(input_str: str, num_char: int, i: int) -> bool:
    s = input_str[i : i + num_char]
    return len(set(s)) == num_char


with open("input/day06", "r") as f:
    input_str = list(filter(lambda x: x != "", f.read().split("\n")))[0]

i_range = range(len(input_str))
print(list(filter(lambda i: is_marker(input_str, 4, i), i_range))[0] + 4)
print(list(filter(lambda i: is_marker(input_str, 14, i), i_range))[0] + 14)
