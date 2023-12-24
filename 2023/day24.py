import itertools

Coord = tuple[int, int, int]
Velocity = tuple[int, int, int]

with open("input/day24", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def parse_line(l: str) -> tuple[Coord, Velocity]:
    c_str, v_str = l.split(" @ ")
    c = tuple(map(int, c_str.split(", ")))
    v = tuple(map(int, v_str.split(", ")))
    return c, v  # type: ignore


cv_pairs = list(map(parse_line, lines))


def get_2d_line(c: Coord, v: Velocity) -> tuple[float, float]:
    # y = mx + b
    # m = delta y / delta x = v[1] / v[0]
    # b = y - mx = c[1] - (v[1] / v[0]) * c[0]
    m = v[1] / v[0]
    b = c[1] - m * c[0]
    return m, b


def check_in_the_same_direction_2d(
    x: float, y: float, cv_pair: tuple[Coord, Velocity]
) -> bool:
    x_change = cv_pair[1][0]
    y_change = cv_pair[1][1]

    if x_change < 0:
        # x is decreasing
        if x > cv_pair[0][0]:
            return False
    if x_change > 0:
        # x is increasing
        if x < cv_pair[0][0]:
            return False
    if y_change < 0:
        # y is decreasing
        if y > cv_pair[0][1]:
            return False
    if y_change > 0:
        # y is increasing
        if y < cv_pair[0][1]:
            return False
    return True


def intersect_2d(
    cv_pair1: tuple[Coord, Velocity], cv_pair2: tuple[Coord, Velocity]
) -> tuple[float, float] | None:
    m1, b1 = get_2d_line(*cv_pair1)
    m2, b2 = get_2d_line(*cv_pair2)

    if m1 == m2:
        # parallel lines
        return None

    # y = m1x + b1
    # y = m2x + b2
    # m1x + b1 = m2x + b2
    # x(m1 - m2) = b2 - b1
    # x = (b2 - b1) / (m1 - m2)
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1

    # need to check if x is in the range of both lines since the lines are
    # actually vector (going in one direction)
    if not check_in_the_same_direction_2d(
        x, y, cv_pair1
    ) or not check_in_the_same_direction_2d(x, y, cv_pair2):
        return None

    return x, y


def task_1(x_bounds: tuple[float, float], y_bounds: tuple[float, float]):
    acc_cross = 0
    all_pairs = list(itertools.combinations(cv_pairs, 2))
    for cv1, cv2 in all_pairs:
        intersection = intersect_2d(cv1, cv2)
        if intersection is not None:
            x, y = intersection
            if (
                x_bounds[0] <= x <= x_bounds[1]
                and y_bounds[0] <= y <= y_bounds[1]
            ):
                acc_cross += 1
    return acc_cross


# test
# print(task_1((7, 27), (7, 27)))
print(
    task_1(
        (200000000000000, 400000000000000), (200000000000000, 400000000000000)
    )
)


def task_2():
    from sympy import symbols, solve

    x = symbols("x")
    y = symbols("y")
    z = symbols("z")
    dx = symbols("dx")
    dy = symbols("dy")
    dz = symbols("dz")
    t1 = symbols("t1")
    t2 = symbols("t2")
    t3 = symbols("t3")

    cv1, cv2, cv3 = cv_pairs[:3]
    res = solve(
        [
            x + dx * t1 - cv1[0][0] - cv1[1][0] * t1,
            y + dy * t1 - cv1[0][1] - cv1[1][1] * t1,
            z + dz * t1 - cv1[0][2] - cv1[1][2] * t1,
            x + dx * t2 - cv2[0][0] - cv2[1][0] * t2,
            y + dy * t2 - cv2[0][1] - cv2[1][1] * t2,
            z + dz * t2 - cv2[0][2] - cv2[1][2] * t2,
            x + dx * t3 - cv3[0][0] - cv3[1][0] * t3,
            y + dy * t3 - cv3[0][1] - cv3[1][1] * t3,
            z + dz * t3 - cv3[0][2] - cv3[1][2] * t3,
        ],
        [x, y, z, dx, dy, dz, t1, t2, t3],
        dict=True,
    )

    return res[0][x] + res[0][y] + res[0][z]


print(task_2())
