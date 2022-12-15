from typing import Set, Tuple

Coordinate = Tuple[int, int]


def parse_line(l: str) -> Tuple[Coordinate, Coordinate]:
    splitted = l.split(" ")
    c_x = int(splitted[2][2:-1])
    c_y = int(splitted[3][2:-1])
    b_x = int(splitted[8][2:-1])
    b_y = int(splitted[9][2:])
    return (c_x, c_y), (b_x, b_y)


def manhattan_distance(c1: Coordinate, c2: Coordinate) -> int:
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def coverage(sensor: Coordinate, beacon: Coordinate) -> Set[Coordinate]:
    dist = manhattan_distance(sensor, beacon)
    covered = set()
    for i, y_diff in enumerate(range(dist, -1, -1)):
        for x_diff in range(i + 1):
            covered.add((sensor[0] + x_diff, sensor[1] + y_diff))
            covered.add((sensor[0] - x_diff, sensor[1] + y_diff))
            covered.add((sensor[0] + x_diff, sensor[1] - y_diff))
            covered.add((sensor[0] - x_diff, sensor[1] - y_diff))

    return covered


def print_grid(
    sensors: Set[Coordinate],
    beacons: Set[Coordinate],
    covered: Set[Coordinate],
) -> None:
    xs = (
        [s[0] for s in sensors]
        + [b[0] for b in beacons]
        + [c[0] for c in covered]
    )
    ys = (
        [s[1] for s in sensors]
        + [b[1] for b in beacons]
        + [c[1] for c in covered]
    )

    x_min = min(xs)
    x_max = max(xs)
    y_min = min(ys)
    y_max = max(ys)

    grid = [
        ["." for _ in range(x_max - x_min + 1)]
        for _ in range(y_max - y_min + 1)
    ]

    for s in sensors:
        grid[s[1] - y_min][s[0] - x_min] = "S"
    for b in beacons:
        grid[b[1] - y_min][b[0] - x_min] = "B"
    for c in covered:
        if grid[c[1] - y_min][c[0] - x_min] == ".":
            grid[c[1] - y_min][c[0] - x_min] = "#"

    for row in grid:
        print("".join(row))


with open("input/day15", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

parsed_lines = [parse_line(l) for l in lines]
sensors = set([s for s, _ in parsed_lines])
beacons = set([b for _, b in parsed_lines])

covered = set()
for s, b in parsed_lines:
    covered |= coverage(s, b)
