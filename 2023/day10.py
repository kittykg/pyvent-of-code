Coord = tuple[int, int]

with open("input/day10", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def get_start_coord() -> Coord:
    start_coord = (0, 0)
    for i, line in enumerate(lines):
        if "S" in line:
            start_coord = (i, line.index("S"))
            break
    return start_coord


def get_pipe(x: Coord) -> str:
    return lines[x[0]][x[1]]


def in_bounds(x: Coord) -> bool:
    return 0 <= x[0] < len(lines) and 0 <= x[1] < len(lines[0])


def connection(x: Coord) -> list[Coord]:
    x_p = get_pipe(x)

    if x_p == "|":
        # | is a vertical pipe connecting north and south.
        l = [(x[0] - 1, x[1]), (x[0] + 1, x[1])]
    elif x_p == "-":
        # - is a horizontal pipe connecting east and west.
        l = [(x[0], x[1] - 1), (x[0], x[1] + 1)]
    elif x_p == "L":
        # L is a 90-degree bend connecting north and east.
        l = [(x[0] - 1, x[1]), (x[0], x[1] + 1)]
    elif x_p == "J":
        # J is a 90-degree bend connecting north and west.
        l = [(x[0] - 1, x[1]), (x[0], x[1] - 1)]
    elif x_p == "7":
        # 7 is a 90-degree bend connecting south and west.
        l = [(x[0] + 1, x[1]), (x[0], x[1] - 1)]
    elif x_p == "F":
        # F is a 90-degree bend connecting south and east.
        l = [(x[0] + 1, x[1]), (x[0], x[1] + 1)]
    elif x_p == ".":
        # . is ground; there is no pipe in this tile.
        l = []
    else:
        # S is the starting position of the animal; there is a pipe on this
        # tile, but your sketch doesn't show what shape the pipe has.
        l = []

    return list(filter(in_bounds, l))


def connected_with_pipe(x: Coord, y: Coord) -> bool:
    x_p_l = connection(x)
    y_p_l = connection(y)

    if get_pipe(x) == "S":
        return x in y_p_l
    elif get_pipe(y) == "S":
        return y in x_p_l

    return y in x_p_l and x in y_p_l


def next_coord(x: Coord, come_from: Coord) -> Coord:
    x_p_l = connection(x)
    fl = list(filter(lambda y: y != come_from, x_p_l))
    assert len(fl) == 1, f"More than one next coord from {x}: {fl}."
    return fl[0]


def find_loop() -> tuple[list[Coord], list[Coord]]:
    start_coord = get_start_coord()

    # S is in a loop, there should be only two neighbours of S that are
    # connected to with a pipe.
    candidates = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            cx = start_coord[0] + i
            cy = start_coord[1] + j
            if not in_bounds((cx, cy)):
                continue
            if connected_with_pipe(start_coord, (cx, cy)):
                candidates.append((cx, cy))
    assert len(candidates) == 2, f"S doesn't have two candidates: {candidates}"

    # Find the loop
    loop_1 = [start_coord, candidates[0]]
    loop_2 = [start_coord, candidates[1]]

    l1_curr = loop_1[-1]
    l1_come_from = start_coord

    l2_curr = loop_2[-1]
    l2_come_from = start_coord

    while loop_1[-1] != loop_2[-1]:
        loop_1.append(next_coord(l1_curr, l1_come_from))
        loop_2.append(next_coord(l2_curr, l2_come_from))

        l1_come_from = l1_curr
        l1_curr = loop_1[-1]

        l2_come_from = l2_curr
        l2_curr = loop_2[-1]

    return loop_1, loop_2


def task_1() -> int:
    loop_1, loop_2 = find_loop()
    return max(len(loop_1), len(loop_2)) - 1


def task_2() -> float:
    loop_1, loop_2 = find_loop()
    full_loop = loop_1 + list(reversed(loop_2[1:-1]))

    # Shoelace formula to calculate the area of the polygon
    area = 0
    for c1, c2 in zip(full_loop, (full_loop[1:] + [full_loop[0]])):
        area += c1[0] * c2[1] - c1[1] * c2[0]
    area /= 2

    # Pick's theorem
    # A = i + b/2 - 1
    # i = A - b/2 + 1
    return abs(area) - len(full_loop) / 2 + 1


print(task_1())
print(task_2())


def prolog_input():
    with open("day10.out", "w") as f:
        start_coord = get_start_coord()
        f.write(f"start_coord(({start_coord[0]}, {start_coord[1]})).\n")
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                if c != ".":
                    f.write(f"pipe(({i}, {j}), '{c}').\n")
        f.write(f"x_bound(0, {len(lines) - 1}).\n")
        f.write(f"y_bound(0, {len(lines[0]) - 1}).\n")


prolog_input()
