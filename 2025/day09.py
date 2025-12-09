# %%
from itertools import combinations
from shapely.geometry import Polygon, box

with open("input/day09", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

coords = list(map(eval, lines))
pairs = list(combinations(coords, 2))


def area(p1, p2):
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)


big_polygon = Polygon(coords)

areas_1 = []
areas_2 = []
for p1, p2 in pairs:
    areas_1.append(area(p1, p2))
    rect = box(p1[0], p1[1], p2[0], p2[1])
    if big_polygon.contains(rect):
        areas_2.append(area(p1, p2))

print(max(areas_1))
print(max(areas_2))


# %%
# Part 2 attempt: find if any polygon boundary intersects with the rectangle
# Didn't work lol so I gave up and used the shapely


def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def intersect(A, B, C, D):
    # Return true if line segments AB and CD intersect
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


areas_2 = []
for p1, p2 in pairs:
    if p1[0] == p2[0] or p1[1] == p2[1]:
        continue

    valid = True
    rect_corners = [p1, (p1[0], p2[1]), p2, (p2[0], p1[1])]
    for i in range(len(coords)):
        p3, p4 = coords[i - 1], coords[i]
        if (
            intersect(p3, p4, rect_corners[0], rect_corners[1])
            or intersect(p3, p4, rect_corners[1], rect_corners[2])
            or intersect(p3, p4, rect_corners[2], rect_corners[3])
            or intersect(p3, p4, rect_corners[3], rect_corners[0])
        ):
            valid = False
            break
    if valid:
        areas_2.append(area(p1, p2))

print(max(areas_2))

# %%
