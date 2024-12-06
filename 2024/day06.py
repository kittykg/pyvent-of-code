import numpy as np
import numpy.typing as npt

with open("input/day06", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

char_grid = np.array([list(x) for x in lines], dtype=str)
max_row, max_col = char_grid.shape


start_x, start_y = -1, -1
start_dir = ""
for i in range(max_row):
    for j in range(max_col):
        if char_grid[i, j] in ["v", "^", "<", ">"]:
            start_x, start_y = i, j
            start_dir = char_grid[i, j]
            break


assert start_x != -1 and start_y != -1, "No starting point found"
assert start_dir in ["v", "^", "<", ">"], "Invalid starting direction"


# Part 1 (with visualization)
def travel_with_trace(grid: npt.NDArray[np.str_]) -> npt.NDArray[np.int_]:
    # To note what direction the agent has passed through, we use 2 bits
    # 00 -> no direction
    # 01 -> horizontal
    # 10 -> vertical
    coverage_grid = np.zeros((max_row, max_col), dtype=int)
    curr_x, curr_y, curr_dir = start_x, start_y, start_dir

    while True:
        if curr_dir == "v":
            # Go down
            coverage_grid[curr_x, curr_y] = np.bitwise_or(
                coverage_grid[curr_x, curr_y], 0b10
            )
            slice = grid[curr_x + 1 :, curr_y]
            slice_indices = np.arange(curr_x + 1, max_row)
        elif curr_dir == "^":
            # Go up
            coverage_grid[curr_x, curr_y] = np.bitwise_or(
                coverage_grid[curr_x, curr_y], 0b10
            )
            slice = grid[:curr_x, curr_y]
            slice_indices = np.arange(0, curr_x)
        elif curr_dir == "<":
            # Go left
            coverage_grid[curr_x, curr_y] = np.bitwise_or(
                coverage_grid[curr_x, curr_y], 0b01
            )
            slice = grid[curr_x, :curr_y]
            slice_indices = np.arange(0, curr_y)
        else:
            # Go right
            coverage_grid[curr_x, curr_y] = np.bitwise_or(
                coverage_grid[curr_x, curr_y], 0b01
            )
            slice = grid[curr_x, curr_y + 1 :]
            slice_indices = np.arange(curr_y + 1, max_col)

        where_to_stop = np.where(slice == "#")[0]

        if len(where_to_stop) == 0:
            if curr_dir in ["v", "^"]:
                coverage_grid[slice_indices, curr_y] = np.bitwise_or(
                    coverage_grid[slice_indices, curr_y], 0b10
                )
            else:
                coverage_grid[curr_x, slice_indices] = np.bitwise_or(
                    coverage_grid[curr_x, slice_indices], 0b01
                )
            break

        if curr_dir == "v":
            stop_index = where_to_stop[0]
            coverage_grid[slice_indices[:stop_index], curr_y] = np.bitwise_or(
                coverage_grid[slice_indices[:stop_index], curr_y],
                0b10,
            )
            curr_dir = "<"
            curr_x = slice_indices[stop_index] - 1
        elif curr_dir == "^":
            stop_index = where_to_stop[-1]
            coverage_grid[slice_indices[stop_index + 1 :], curr_y] = (
                np.bitwise_or(
                    coverage_grid[slice_indices[stop_index + 1 :], curr_y],
                    0b10,
                )
            )
            curr_dir = ">"
            curr_x = slice_indices[stop_index] + 1
        elif curr_dir == "<":
            stop_index = where_to_stop[-1]
            coverage_grid[curr_x, slice_indices[stop_index + 1 :]] = (
                np.bitwise_or(
                    coverage_grid[curr_x, slice_indices[stop_index + 1 :]], 0b01
                )
            )
            curr_dir = "^"
            curr_y = slice_indices[stop_index] + 1
        else:
            stop_index = where_to_stop[0]
            coverage_grid[curr_x, slice_indices[:stop_index]] = np.bitwise_or(
                coverage_grid[curr_x, slice_indices[:stop_index]], 0b01
            )
            curr_dir = "v"
            curr_y = slice_indices[stop_index] - 1

    return coverage_grid


# Part 2
def travel_check_loop(grid: npt.NDArray[np.str_]) -> bool:
    history: set[tuple[int, int, int]] = set()
    # 3rd "bit" represents direction. North: 0, East: 1, South: 2, West: 3

    curr_x, curr_y = start_x, start_y
    curr_dir: int = {"^": 0, ">": 1, "v": 2, "<": 3}[start_dir]

    def get_next_x_y(
        curr_x: int, curr_y: int, curr_dir: int
    ) -> tuple[int, int]:
        if curr_dir == 0:
            return curr_x - 1, curr_y
        if curr_dir == 1:
            return curr_x, curr_y + 1
        if curr_dir == 2:
            return curr_x + 1, curr_y
        return curr_x, curr_y - 1

    while True:
        if (curr_x, curr_y, curr_dir) in history:
            # Been here before with the same heading direction, gonna loop
            return True

        history.add((curr_x, curr_y, curr_dir))
        next_x, next_y = get_next_x_y(curr_x, curr_y, curr_dir)

        if next_x < 0 or next_x >= max_row or next_y < 0 or next_y >= max_col:
            break

        next_square = grid[next_x, next_y]
        if next_square == "#":
            curr_dir = (curr_dir + 1) % 4
        else:
            curr_x, curr_y = next_x, next_y

    return False


def task_1():
    coverage_grid = travel_with_trace(char_grid)
    print(f"Part 1: {np.count_nonzero(coverage_grid)}")
    # Visualization
    # for i in range(max_row):
    #     print_str = ""
    #     for j in range(max_col):
    #         if coverage_grid[i, j] == 0:
    #             print_str += char_grid[i, j]
    #         else:
    #             if coverage_grid[i, j] == 0b11:
    #                 print_str += "+"
    #             elif coverage_grid[i, j] == 0b01:
    #                 print_str += "-"
    #             else:
    #                 print_str += "|"
    #     print(print_str)


def task_2():
    from datetime import datetime

    start = datetime.now()
    count = 0
    for i in range(max_row):
        for j in range(max_col):
            mod_grid = char_grid.copy()
            mod_grid[i, j] = "#"
            if travel_check_loop(mod_grid):
                count += 1
    end = datetime.now()
    print(f"Part 2: {count}\tTime: {end - start}")


task_1()
task_2()
