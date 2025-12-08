# %%
with open("input/day08", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

coords = [tuple(map(int, line.split(","))) for line in lines]


# %%
def euclidean_distance(
    x1: int, y1: int, z1: int, x2: int, y2: int, z2: int
) -> float:
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5


# %%
distance_dict = {}
for i in range(len(coords)):
    for j in range(i + 1, len(coords)):
        distance_dict[(i, j)] = euclidean_distance(*coords[i], *coords[j])
sorted_distance_dict = sorted(distance_dict.items(), key=lambda x: x[1])

circuits = {p: set([p]) for p in coords}
TARGET = 1000
for i, ((ip1, ip2), _) in enumerate(sorted_distance_dict):
    p1, p2, c1, c2 = coords[ip1], coords[ip2], None, None
    for c in circuits:
        if p1 in circuits[c]:
            c1 = c
        if p2 in circuits[c]:
            c2 = c
    if c1 != c2:
        circuits[c1] |= circuits[c2]
        del circuits[c2]

    if i + 1 == TARGET:
        circuits_lengths = sorted(
            [len(c) for c in circuits.values()], reverse=True
        )
        print(circuits_lengths[0] * circuits_lengths[1] * circuits_lengths[2])

    if len(circuits) == 1:
        print(p1[0] * p2[0])
        break

# %%
