import math
from typing import List, Tuple

Position = Tuple[int, int]

# Get grid
with open("input/day12", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
grid = list(map(list, lines))

height = len(grid)
width = len(grid[0])

start_x, start_y = [
    (j, i) for i in range(height) for j in range(width) if grid[i][j] == "S"
][0]
end_x, end_y = [
    (j, i) for i in range(height) for j in range(width) if grid[i][j] == "E"
][0]

grid[start_y][start_x] = "a"
grid[end_y][end_x] = "z"
grid = [[ord(c) - ord("a") for c in row] for row in grid]


def update_priority_queue(
    pq: List[Tuple[int, Position]], item: Tuple[int, Position]
) -> None:
    positions = [p for _, p in pq]
    if item[1] in positions:
        i = positions.index(item[1])
        pq[i] = item
    else:
        pq.append(item)
    pq.sort(key=lambda x: x[0])


def get_min_distance(pq: List[Tuple[int, Position]]) -> float:
    dist = [[math.inf for _ in range(width)] for _ in range(height)]
    _, start_pos = pq[0]
    dist[start_pos[1]][start_pos[0]] = 0

    while pq:
        (_, (curr_x, curr_y)) = pq.pop(0)

        for diff_x, diff_y in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            neigh_x = curr_x + diff_x
            neigh_y = curr_y + diff_y

            if neigh_x not in range(width) or neigh_y not in range(height):
                continue

            if grid[neigh_y][neigh_x] - grid[curr_y][curr_x] <= 1:
                new_dist = dist[curr_y][curr_x] + 1
                if dist[neigh_y][neigh_x] > new_dist:
                    dist[neigh_y][neigh_x] = new_dist
                    update_priority_queue(
                        pq, (int(new_dist), (neigh_x, neigh_y))
                    )

    return dist[end_y][end_x]


def task_1():
    print(get_min_distance([(0, (start_x, start_y))]))


def task_2():
    all_as = [
        (j, i) for i in range(height) for j in range(width) if grid[i][j] == 0
    ]
    print(min([get_min_distance([(0, a)]) for a in all_as]))


task_1()
task_2()
