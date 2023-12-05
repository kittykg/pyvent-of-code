import time


with open("input/day05_seed", "r") as f:
    seeds = list(filter(lambda x: x != "", f.read().split("\n")))[0]
    seeds = [int(s) for s in seeds.split(" ")]

with open("input/day05_map", "r") as f:
    map_lists = list(filter(lambda x: x != "", f.read().split("\n")))

name_locations = [i for i, l in enumerate(map_lists) if l[-1] == ":"]
maps = []
for i in range(len(name_locations)):
    start = name_locations[i] + 1
    if i == len(name_locations) - 1:
        end = len(map_lists)
    else:
        end = name_locations[i + 1]
    maps.append(
        list(
            map(lambda x: [int(s) for s in x.split(" ")], map_lists[start:end])
        )
    )


def task_1():
    task_1_seeds = seeds.copy()
    for mapping in maps:
        ranges = [(m[1], m[1] + m[2] - 1) for m in mapping]

        for i in range(len(task_1_seeds)):
            s = task_1_seeds[i]
            for j, r in enumerate(ranges):
                if r[0] <= s <= r[1]:
                    task_1_seeds[i] = s - r[0] + mapping[j][0]
                    break

    return min(task_1_seeds)


def range_overlap(r1, r2) -> bool:
    start = max(r1[0], r2[0])
    end = min(r1[1], r2[1])
    return start <= end


def uncovered_range(r1, r2) -> list:
    overlap_start = max(r1[0], r2[0])
    overlap_end = min(r1[1], r2[1])

    if overlap_start == r1[0] and overlap_end == r1[1]:
        # r1 is completely covered by r2
        return []

    if overlap_start > r1[0] and overlap_end == r1[1]:
        # r1 has a bit on the left not covered by r2
        return [(r1[0], overlap_start - 1)]

    if overlap_start == r1[0] and overlap_end < r2[1]:
        # r1 has a bit on the right not covered by r2
        return [(overlap_end + 1, r1[1])]

    # r1 has both on the left and right not covered by r2
    return [(r1[0], overlap_start - 1), (overlap_end + 1, r1[1])]


def map_seeds_from_range(sr, ranges, new_mapping_starts):
    seed_range = [sr]
    mapped_seed_range = []
    while len(seed_range) > 0:
        sr = seed_range.pop()
        mapping_found = False
        for j, r in enumerate(ranges):
            if not range_overlap(sr, r):
                continue

            # There is overlap
            mapped_seeds_start = max(sr[0], r[0])
            mapped_seeds_end = min(sr[1], r[1])
            mapped_seed_range.append(
                (
                    mapped_seeds_start - r[0] + new_mapping_starts[j],
                    mapped_seeds_end - r[0] + new_mapping_starts[j],
                )
            )

            # Calculate the seed that are not mapped
            ur = uncovered_range(sr, r)
            seed_range.extend(ur)
            mapping_found = True
            break

        if not mapping_found:
            mapped_seed_range.append(sr)

    return mapped_seed_range


def task_2():
    task_2_seeds = []
    i = 0
    while i < len(seeds):
        task_2_seeds.append((seeds[i], seeds[i] + seeds[i + 1] - 1))
        i += 2

    for mapping in maps:
        ranges = [(m[1], m[1] + m[2] - 1) for m in mapping]
        new_seeds = []
        for s in task_2_seeds:
            new_mapping = map_seeds_from_range(
                s, ranges, [m[0] for m in mapping]
            )
            new_seeds += new_mapping
        task_2_seeds = new_seeds

    return min([s[0] for s in task_2_seeds])


print(task_1())

start = time.time()
print(task_2())
print(time.time() - start)


def prolog_input():
    with open("day05.out", "w") as f:
        # Write the seeds
        f.write("seeds([")
        f.write(",".join([str(s) for s in seeds]))
        f.write("]).\n")

        f.write("maps([\n")
        all_mapping_str = []
        for mapping in maps:
            mapping_str = "["
            mapping_str += ",".join(
                [f"({m[0]},{m[1]},{m[2]})" for m in mapping]
            )
            mapping_str += "]"
            all_mapping_str.append(mapping_str)
        f.write(",\n".join(all_mapping_str))
        f.write("]).")


# prolog_input()
