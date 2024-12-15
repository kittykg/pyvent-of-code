import numpy as np

TEST = False
GRID_FILE = "input/day15_grid" + ("_test" if TEST else "")
MOVE_FILE = "input/day15_move" + ("_test" if TEST else "")

CoordType = tuple[int, int]
movement_map = {"^": 0, ">": 1, "v": 2, "<": 3}

with open(MOVE_FILE, "r") as f:
    move_instructions = f.read()

with open(GRID_FILE, "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


# ============================================================================ #
#                                   Generic                                    #
# ============================================================================ #


def print_grid(char_grid: np.ndarray):
    for row in char_grid:
        print("".join(row))


def get_next_step(box_coord: CoordType, direction: int) -> CoordType:
    x, y = box_coord
    if direction == 0:  # up
        return (x - 1, y)
    elif direction == 1:  # right
        return (x, y + 1)
    elif direction == 2:  # down
        return (x + 1, y)
    # direction == 3, left
    return (x, y - 1)


def move_boxes_right(
    agent_next_step: CoordType, char_grid: np.ndarray, part: int = 1
) -> bool:
    x, y = agent_next_step
    for i in range(y, char_grid.shape[1]):
        if char_grid[x][i] == "#":
            # To the right of relevant boxes there is a wall, so moving them
            # won't be possible
            return False

        if char_grid[x][i] == ".":
            # The relevant boxes have a space to the right of it, so we can move
            # it
            if part == 1:
                char_grid[x, y + 1 : i + 1] = "O"
            else:
                boxes_str = char_grid[x, y:i]
                assert len(boxes_str) % 2 == 0
                char_grid[x, y + 1 : i + 1] = boxes_str

            char_grid[x, y] = "."
            return True
    return False


def move_boxes_left(
    agent_next_step: CoordType, char_grid: np.ndarray, part: int = 1
) -> bool:
    x, y = agent_next_step
    for i in range(y, -1, -1):
        if char_grid[x][i] == "#":
            # To the left of relevant boxes there is a wall, so moving them
            # won't be possible
            return False

        if char_grid[x][i] == ".":
            # The relevant boxes have a space to the left of it, so we can move
            # it
            if part == 1:
                char_grid[x, i:y] = "O"
            else:
                boxes_str = char_grid[x, i + 1 : y + 1]
                assert len(boxes_str) % 2 == 0
                char_grid[x, i:y] = boxes_str
            char_grid[x, y] = "."
            return True
    return False


# ============================================================================ #
#                                   Part 1                                     #
# ============================================================================ #


def move_boxes_up(agent_next_step: CoordType, char_grid: np.ndarray):
    x, y = agent_next_step
    for i in range(x, -1, -1):
        if char_grid[i][y] == "#":
            # Above the relevant boxes there is a wall, so moving them won't be
            # possible
            return False

        if char_grid[i][y] == ".":
            # The relevant boxes have a space above it, so we can move it
            char_grid[x, y] = "."
            char_grid[i:x, y] = "O"
            return True
    return False


def move_boxes_down(agent_next_step: CoordType, char_grid: np.ndarray):
    x, y = agent_next_step
    for i in range(x, len(char_grid)):
        if char_grid[i][y] == "#":
            # Below the relevant boxes there is a wall, so moving them won't be
            # possible
            return False

        if char_grid[i][y] == ".":
            # The relevant boxes have a space below it, so we can move it
            char_grid[x, y] = "."
            char_grid[x + 1 : i + 1, y] = "O"
            return True
    return False


def task_1():

    def move(
        curr_coord: CoordType, move_instr: str, char_grid: np.ndarray
    ) -> CoordType:
        direction = movement_map[move_instr]
        next_step = get_next_step(curr_coord, direction)
        if char_grid[next_step] == "#":
            # Next step is a wall, so we can't move there
            return curr_coord

        if char_grid[next_step] == ".":
            # Next step is empty, so we can move there
            char_grid[curr_coord] = "."
            char_grid[next_step] = "@"
            return next_step

        # Next step is a box
        if direction == 0:
            box_moved = move_boxes_up(next_step, char_grid)
        elif direction == 1:
            box_moved = move_boxes_right(next_step, char_grid)
        elif direction == 2:
            box_moved = move_boxes_down(next_step, char_grid)
        else:
            box_moved = move_boxes_left(next_step, char_grid)

        if box_moved:
            char_grid[curr_coord] = "."
            char_grid[next_step] = "@"
            return next_step

        return curr_coord

    char_grid = np.array([list(x) for x in lines], dtype=str)
    agent_curr: tuple[int, int] = tuple(map(int, np.where(char_grid == "@")))  # type: ignore

    for move_instr in move_instructions:
        if move_instr == "\n":
            continue
        agent_curr = move(agent_curr, move_instr, char_grid)

    boxes_x, boxes_y = np.where(char_grid == "O")
    return 100 * np.sum(boxes_x) + np.sum(boxes_y)


# ============================================================================ #
#                                   Part 2                                     #
# ============================================================================ #


def get_moveable_boxes_in_front(
    agent_next_step: CoordType, char_grid: np.ndarray, go_up: bool
) -> list[tuple[int, int, int]]:

    def box_blocked(box_key: tuple[int, int, int]) -> bool:
        x, y1, y2 = box_key
        x_2 = x - 1 if go_up else x + 1
        return char_grid[x_2][y1] == "#" or char_grid[x_2][y2] == "#"

    x, y = agent_next_step
    all_boxes, force_range = [], [y]

    x_range = range(x, -1, -1) if go_up else range(x, len(char_grid))
    for i in x_range:
        new_force_range = []
        for j in force_range:
            if char_grid[i][j] not in "[]":
                continue

            if char_grid[i][j] == "[":
                curr_c_key = (i, j, j + 1)
                new_force_range += [j, j + 1]
            else:
                curr_c_key = (i, j - 1, j)
                new_force_range += [j - 1, j]

            if box_blocked(curr_c_key):
                # If any box is blocked, the entire move is blocked
                return []

            all_boxes.append(curr_c_key)

        if len(new_force_range) == 0:
            # there are no boxes in the current row, so we can end the search
            break
        force_range = sorted(set(new_force_range))

    return all_boxes


def move_boxes_vertical(
    agent_next_step: CoordType, char_grid: np.ndarray, go_up: bool
) -> bool:
    movable_boxes = get_moveable_boxes_in_front(
        agent_next_step, char_grid, go_up
    )
    if len(movable_boxes) == 0:
        return False

    sorted_boxes = sorted(movable_boxes, key=lambda x: x[0], reverse=not go_up)
    for box in sorted_boxes:
        x, y1, y2 = box
        new_x = x - 1 if go_up else x + 1
        char_grid[x, y1] = "."
        char_grid[x, y2] = "."
        char_grid[new_x, y1] = "["
        char_grid[new_x, y2] = "]"
    return True


def task_2():

    def move(
        curr_coord: CoordType, move_instr: str, char_grid: np.ndarray
    ) -> CoordType:
        direction = movement_map[move_instr]
        next_step = get_next_step(curr_coord, direction)
        if char_grid[next_step] == "#":
            # Next step is a wall, so we can't move there
            return curr_coord

        if char_grid[next_step] == ".":
            # Next step is empty, so we can move there
            char_grid[curr_coord] = "."
            char_grid[next_step] = "@"
            return next_step

        # Next step is a box
        if direction == 1:
            box_moved = move_boxes_right(next_step, char_grid, part=2)
        elif direction == 3:
            box_moved = move_boxes_left(next_step, char_grid, part=2)
        else:
            box_moved = move_boxes_vertical(
                next_step, char_grid, direction == 0
            )

        if box_moved:
            char_grid[curr_coord] = "."
            char_grid[next_step] = "@"
            return next_step

        return curr_coord

    mod_lines = []
    for l in lines:
        mod_l = ""
        for c in l:
            if c == "O":
                mod_l += "[]"
            elif c == "#":
                mod_l += "##"
            elif c == ".":
                mod_l += ".."
            else:
                mod_l += "@."
        mod_lines.append(mod_l)

    char_grid = np.array([list(x) for x in mod_lines], dtype=str)
    agent_curr: tuple[int, int] = tuple(map(int, np.where(char_grid == "@")))  # type: ignore

    for move_instr in move_instructions:
        if move_instr == "\n":
            continue
        agent_curr = move(agent_curr, move_instr, char_grid)

    boxes_x, boxes_y = np.where(char_grid == "[")
    return 100 * np.sum(boxes_x) + np.sum(boxes_y)


# ============================================================================ #
#                                 Print results                                #
# ============================================================================ #

print(f"Task 1: {task_1()}")
print(f"Task 2: {task_2()}")
