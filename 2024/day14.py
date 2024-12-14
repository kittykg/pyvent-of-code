import re
from collections import Counter

with open("input/day14", "r") as f:
    lines = f.read()

RobotType = tuple[int, int, int, int]
RobotCoordType = tuple[int, int]

p = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")
robots: list[RobotType] = [tuple(map(int, s)) for s in re.findall(p, lines)]  # type: ignore
grid_x, grid_y = 101, 103


def move(robot: RobotType, time: int) -> RobotType:
    x, y, vx, vy = robot
    new_x = (x + vx * time) % grid_x
    new_y = (y + vy * time) % grid_y
    return (new_x, new_y, vx, vy)


def get_robot_coords(robots: list[RobotType]) -> list[RobotCoordType]:
    return [(x, y) for x, y, _, _ in robots]


def count_quadrants(robot_coords: list[RobotCoordType]) -> int:
    midline_x, midline_y = grid_x // 2, grid_y // 2

    def locate_quadrant(x: int, y: int) -> int:
        if x == midline_x or y == midline_y:
            return -1
        if x < midline_x and y < midline_y:
            return 0
        if x > midline_x and y < midline_y:
            return 1
        if x < midline_x and y > midline_y:
            return 2
        return 3

    quadrants = Counter([locate_quadrant(x, y) for x, y in robot_coords])
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def is_a_christmas_tree_(
    x: int, y: int, robot_coords: list[RobotCoordType]
) -> bool:
    # Christmas tree with 5 layers
    #                   #
    #                  ###
    #                 #####
    #                #######
    #               #########
    #                 #####
    #                #######
    #               #########
    #              ###########
    #             #############
    #               #########
    #              ###########
    #             #############
    #            ###############
    #           #################
    #             #############
    #            ###############
    #           #################
    #          ###################
    #         #####################
    #                  ###
    #                  ###
    #                  ###

    tree_height = 23
    if y + tree_height > grid_y or x + 10 > grid_x or x - 10 < 0:
        return False

    middle_x, curr_y = x, y
    for i in range(4):
        for j in range(5):
            for new_x in range(middle_x - j - i * 2, middle_x + j + i * 2 + 1):
                if (new_x, curr_y) not in robot_coords:
                    return False
            curr_y += 1

    for _ in range(3):
        for x in range(middle_x - 1, middle_x + 1 + 1):
            if (x, curr_y) not in robot_coords:
                return False
        curr_y += 1
    return True


def is_a_christmas_tree(coords: list[RobotCoordType]) -> bool:
    for c in coords:
        if is_a_christmas_tree_(*c, coords):
            return True
    return False


def task_1() -> int:
    return count_quadrants(
        get_robot_coords([move(robot, 100) for robot in robots])
    )


def task_2():
    moved_robot = robots.copy()
    t = 0
    while True:
        moved_robot = [move(robot, 1) for robot in moved_robot]
        t += 1
        robot_coords = get_robot_coords(moved_robot)
        if is_a_christmas_tree(robot_coords):
            for j in range(grid_y):
                for i in range(grid_x):
                    if (i, j) in [(x, y) for x, y in robot_coords]:
                        print("#", end="")
                    else:
                        print(".", end="")
                print()
            return t


print(f"Task 1: {task_1()}")
print(f"Task 2: {task_2()}")
