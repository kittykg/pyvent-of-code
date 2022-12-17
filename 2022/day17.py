from typing import List, Set, Tuple

with open("input/day17", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

jet_pattern = lines[0]

Coordinate = Tuple[int, int]
rock_1 = [(0, 0), (1, 0), (2, 0), (3, 0)]
rock_2 = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
rock_3 = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
rock_4 = [(0, 0), (0, 1), (0, 2), (0, 3)]
rock_5 = [(0, 0), (1, 0), (0, 1), (1, 1)]
rock_list = [rock_1, rock_2, rock_3, rock_4, rock_5]

TUNNEL_WIDTH = 7


def print_grid(rock: List[Coordinate], occupied: Set[Coordinate]) -> None:
    y_max = max([y for _, y in rock] + [y for _, y in occupied])
    grid = [["." for _ in range(TUNNEL_WIDTH)] for _ in range(y_max + 1)]
    for x, y in rock:
        grid[y_max - y][x] = "@"
    for x, y in occupied:
        grid[y_max - y][x] = "#"

    for r in grid:
        print("|" + "".join(r) + "|")
    print("+-------+")


def pattern(occupied: Set[Coordinate]) -> str:
    # Cheat way of a pattern, does work some how
    h = tunnel_height(occupied)
    p = []
    for x in range(TUNNEL_WIDTH):
        for y in range(h, 0, -1):
            if (x, y) in occupied:
                p.append(h - y)
                break
    return ",".join([str(i) for i in p])


def moveable(
    rock: List[Coordinate],
    occupied: Set[Coordinate],
    movement: Coordinate,
    is_jet: bool = False,
) -> bool:
    move_x, move_y = movement
    rx = [x for x, _ in rock]
    ry = [y for _, y in rock]

    if max(rx) + move_x >= TUNNEL_WIDTH:
        return False
    if min(rx) + move_x < 0:
        return False
    if not is_jet and min(ry) == 0:
        return False
    if set([(x + move_x, y + move_y) for x, y in rock]).intersection(occupied):
        return False
    return True


def tunnel_height(occupied: Set[Coordinate]) -> int:
    return max([y for _, y in occupied]) + 1


def update_pointer(ptr: int, len: int) -> int:
    return 0 if ptr + 1 >= len else ptr + 1


def rock_fall(
    rock_ptr: int, jp_ptr: int, occupied: Set[Coordinate]
) -> Tuple[int, int]:
    spawn_point_x = 2
    spawn_point_y = 3 + (tunnel_height(occupied) if occupied else 0)
    rock = [
        (x + spawn_point_x, y + spawn_point_y) for x, y in rock_list[rock_ptr]
    ]

    while True:
        # Jet movement
        movement = (1, 0) if jet_pattern[jp_ptr] == ">" else (-1, 0)
        if moveable(rock, occupied, movement, is_jet=True):
            rock = [(x + movement[0], y + movement[1]) for x, y in rock]
        jp_ptr = update_pointer(jp_ptr, len(jet_pattern))

        # Down movement
        movement = (0, -1)
        if moveable(rock, occupied, movement):
            rock = [(x + movement[0], y + movement[1]) for x, y in rock]
        else:
            for r in rock:
                occupied.add(r)
            break

    return update_pointer(rock_ptr, len(rock_list)), jp_ptr


def task_1():
    rock_ptr = 0
    jp_ptr = 0
    occupied = set()

    for _ in range(2022):
        rock_ptr, jp_ptr = rock_fall(rock_ptr, jp_ptr, occupied)
    print(tunnel_height(occupied))


def task_2():
    rock_ptr = 0
    jp_ptr = 0
    occupied = set()
    seen_pattern = dict()

    BIG_NUMBER = 1000000000000

    for i in range(BIG_NUMBER):
        rock_ptr, jp_ptr = rock_fall(rock_ptr, jp_ptr, occupied)
        ps = f"{rock_ptr}.{jp_ptr}.{pattern(occupied)}"
        h = tunnel_height(occupied)
        if ps in seen_pattern:
            old_i, old_h = seen_pattern[ps]
            checkpoint_i = i
            delta_i = i - old_i
            delta_h = h - old_h
            break
        else:
            seen_pattern[ps] = (i, h)

    repeat = (BIG_NUMBER - checkpoint_i) // delta_i  # type: ignore
    new_i = checkpoint_i + repeat * delta_i + 1  # type: ignore

    while new_i < BIG_NUMBER:
        rock_ptr, jp_ptr = rock_fall(rock_ptr, jp_ptr, occupied)
        new_i += 1

    print(tunnel_height(occupied) + repeat * delta_h)  # type: ignore


task_1()
task_2()
