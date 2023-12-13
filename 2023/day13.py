import numpy as np

with open("input/day13", "r") as f:
    lines = list(f.read().split("\n"))

examples = []
e_start = 0
for i in range(len(lines)):
    if lines[i] == "":
        examples.append(np.array([list(s) for s in lines[e_start:i]]))
        e_start = i + 1


def match_head(s1: str, s2: str) -> bool:
    return s1.startswith(s2) if len(s1) >= len(s2) else s2.startswith(s1)


def find_reflection_str(s: str) -> list[int]:
    return [i for i in range(1, len(s)) if match_head(s[:i][::-1], s[i:])]


def find_reflection(example: np.ndarray) -> int:
    potential_row_reflections = find_reflection_str("".join(example[0]))
    potential_col_reflections = find_reflection_str("".join(example.T[0]))

    def valid_reflection(reflection: int, s: str) -> bool:
        return match_head(s[:reflection][::-1], s[reflection:])

    if len(potential_row_reflections) > 0:
        actual_row_reflections = [r for r in potential_row_reflections]
        for r in potential_row_reflections:
            for i in range(1, len(example)):
                if not valid_reflection(r, "".join(example[i])):
                    actual_row_reflections.remove(r)
                    break
        if len(actual_row_reflections) == 1:
            return actual_row_reflections[0]

    if len(potential_col_reflections) > 0:
        actual_col_reflections = [r for r in potential_col_reflections]
        for r in potential_col_reflections:
            for i in range(1, len(example[0])):
                if not valid_reflection(r, "".join(example.T[i])):
                    actual_col_reflections.remove(r)
                    break
        if len(actual_col_reflections) == 1:
            return actual_col_reflections[0] * 100

    return 0


def find_reflection_str_2(s: str, reflection: int) -> int:
    return sum(
        1 for a, b in zip(s[:reflection][::-1], s[reflection:]) if a != b
    )


def find_reflection_2(example: np.ndarray) -> int:
    def _find_reflection_2_(example: np.ndarray):
        for i in range(1, len(example[0])):
            reflection_diff = sum(
                find_reflection_str_2("".join(example[j]), i)
                for j in range(len(example))
            )
            if reflection_diff == 1:
                return i
        return -1

    r = _find_reflection_2_(example)
    c = _find_reflection_2_(example.T)

    if r > 0:
        return r
    if c > 0:
        return c * 100
    return 0


def task(find_reflection_fn):
    return sum([find_reflection_fn(e) for e in examples])


print(task(find_reflection))
print(task(find_reflection_2))
