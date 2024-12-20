import numpy as np

with open("input/day20", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
char_grid = np.array([list(x) for x in lines])


def get_possible_next_step(curr_x: int, curr_y: int) -> list[tuple[int, int]]:
    possible_next_steps: list[tuple[int, int]] = []

    for direction in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        new_x = curr_x + direction[0]
        new_y = curr_y + direction[1]
        if (
            0 <= new_x < char_grid.shape[0]
            and 0 <= new_y < char_grid.shape[1]
            and char_grid[new_x, new_y] != "#"
        ):
            possible_next_steps.append((new_x, new_y))

    return possible_next_steps


curr = tuple(map(int, np.where(char_grid == "S")))
end = tuple(map(int, np.where(char_grid == "E")))
path: list[tuple[int, int]] = [curr]  # type: ignore
while curr != end:
    for next_node in get_possible_next_step(*curr):
        if next_node not in path:
            path.append(next_node)
            curr = next_node
            break


valid_tp = {i: 0 for i in range(2, 21)}
for i in range(len(path)):
    p1_x, p1_y = path[i]
    for j in range(i + 100, len(path)):
        p2_x, p2_y = path[j]
        distance = abs(p1_x - p2_x) + abs(p1_y - p2_y)
        if distance > 20:
            continue
        if j - i - distance >= 100:
            valid_tp[distance] += 1


print(f"Task 1: {valid_tp[2]}")
print(f"Task 2: {sum(valid_tp.values())}")
