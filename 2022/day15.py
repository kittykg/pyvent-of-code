from typing import List, Optional, Tuple

Coordinate = Tuple[int, int]
MB_Pair = Tuple[int, int]
X_Range = Tuple[int, int]


def parse_line(l: str) -> Tuple[Coordinate, Coordinate]:
    splitted = l.split(" ")
    c_x = int(splitted[2][2:-1])
    c_y = int(splitted[3][2:-1])
    b_x = int(splitted[8][2:-1])
    b_y = int(splitted[9][2:])
    return (c_x, c_y), (b_x, b_y)


with open("input/day15", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
parsed_lines = [parse_line(l) for l in lines]


def manhattan_distance(c1: Coordinate, c2: Coordinate) -> int:
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def task_1(target_y: int = 2000000) -> None:
    def covered_x(y: int, sensors: Coordinate, dist: int) -> Optional[X_Range]:
        y_diff = abs(y - sensors[1])
        if y_diff > dist:
            return None
        spare_dist = dist - y_diff
        return ((sensors[0] - spare_dist), (sensors[0] + spare_dist))

    TARGET_Y = target_y

    covered = []
    for s, b in parsed_lines:
        c = covered_x(TARGET_Y, s, manhattan_distance(s, b))
        if c:
            covered += list(range(c[0], c[1] + 1))

    covered = set(covered)

    sensors_x = set([s[0] for s, _ in parsed_lines if s[1] == TARGET_Y])
    beacons_x = set([b[0] for _, b in parsed_lines if b[1] == TARGET_Y])

    print(len(covered - sensors_x - beacons_x))


def task_2(bound: int = 4000000) -> None:
    BOUND = bound

    def get_boundary_function(sensor: Coordinate, dist: int) -> List[MB_Pair]:
        # This give the m and b for a line that just about outside the square
        # of the sensor
        b1 = (sensor[0] - dist - 1, sensor[1])
        i1 = b1[1] - b1[0]  # y = x + i1 --> i1 = y - x
        i2 = b1[1] + b1[0]  # y = -x + i2 --> i2 = y + x
        b2 = (sensor[0] + dist + 1, sensor[1])
        i3 = b2[1] - b2[0]  # y = x + i3 --> i3 = y - x
        i4 = b2[1] + b2[0]  # y = -x + i4 --> i4 = y + x

        return [(1, i1), (-1, i2), (1, i3), (-1, i4)]

    def line_intersection(b1: int, b2: int) -> Coordinate:
        # Line intersection of y1 = x + b1 and y2 = -x + b2
        return ((b2 - b1) // 2, (b1 + b2) // 2)

    def in_bound(point: Coordinate) -> bool:
        return point[0] in range(BOUND) and point[1] in range(BOUND)

    lines = []
    scanner_tuple = []
    for s, b in parsed_lines:
        dist = manhattan_distance(s, b)
        lines += get_boundary_function(s, dist)
        scanner_tuple.append((s, dist))

    m1_lines_b = [b for m, b in lines if m == 1]
    m_m1_lines_b = [b for m, b in lines if m == -1]

    for b1 in m1_lines_b:
        for b2 in m_m1_lines_b:
            intersect = line_intersection(b1, b2)
            if not in_bound(intersect):
                continue

            in_range = False
            for s, dist in scanner_tuple:
                if manhattan_distance(intersect, s) <= dist:
                    in_range = True
                    continue
            if not in_range:
                print(intersect[0] * 4000000 + intersect[1])
                return


task_1()
task_2()
