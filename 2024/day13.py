import re

with open("input/day13", "r") as f:
    lines = f.read()

p = re.compile(
    r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\n"
    r"Prize: X=(\d+), Y=(\d+)"
)
claw_machines: list[tuple[int, int, int, int, int, int]] = [
    tuple(map(int, x)) for x in p.findall(lines)  # type: ignore
]


def solve(
    a: int, b: int, c: int, d: int, e: int, f: int, flag: bool = False
) -> tuple[int, int] | None:
    # |a c| * |m| = |e|
    # |b d|   |n|   |f|
    #   A   *  p  =  t
    # p = A^-1 * t
    # A^-1 = 1/(ad - bc) * |d -c|
    #                      |-b a|
    if flag:
        e += 10000000000000
        f += 10000000000000

    det = a * d - b * c
    if det == 0:
        return None
    m = (d * e - c * f) / det
    n = (a * f - b * e) / det

    if not m.is_integer() or not n.is_integer():
        return None
    if not flag and (m > 100 or n > 100):
        return None

    return int(m), int(n)


def task(flag: bool = False) -> int:
    solved = [solve(*x, flag) for x in claw_machines]
    return sum(x[0] * 3 + x[1] for x in solved if x is not None)


print(task())
print(task(True))
