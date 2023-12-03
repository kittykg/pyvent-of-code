with open("input/day03", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def task_1(lines: list[str]):
    pn_coords = []
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "." or lines[i][j].isnumeric():
                # Not a symbol
                continue

            for cx in range(i - 1, i + 2):
                for cy in range(j - 1, j + 2):
                    if (
                        cx < 0
                        or cy < 0
                        or cx >= len(lines)
                        or cy >= len(lines[i])
                    ):
                        # Out of bounds
                        continue

                    if cx == i and cy == j:
                        continue

                    if lines[cx][cy].isnumeric():
                        pn_coords.append((cx, cy))

    power_numbers = []
    power_number_coords_set = set()
    for cx, cy in pn_coords:
        if (cx, cy) in power_number_coords_set:
            continue

        power_number_coords_set.add((cx, cy))

        start_coord = -1
        end_coord = -1

        i = 0
        while True:
            if cy + i >= len(lines[cx]):
                end_coord = len(lines[cx])
                power_number_coords_set.add((cx, end_coord))
                break
            if not lines[cx][cy + i].isnumeric():
                end_coord = cy + i
                break
            i += 1
            power_number_coords_set.add((cx, cy + i))

        i = 0
        while True:
            if cy - i < 0:
                start_coord = 0
                power_number_coords_set.add((cx, start_coord))
                break
            if not lines[cx][cy - i].isnumeric():
                start_coord = cy - i + 1
                break
            i += 1
            power_number_coords_set.add((cx, cy - i))

        power_numbers.append(int(lines[cx][start_coord:end_coord]))

    return power_numbers


def task_2(lines: list[str]):
    gear_numbers = []
    gear_coords = set()

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] != "*":
                # Not a gear
                continue

            if (i, j) in gear_coords:
                continue

            gear_coords.add((i, j))

            pn_coords = []
            for cx in range(i - 1, i + 2):
                for cy in range(j - 1, j + 2):
                    if (
                        cx < 0
                        or cy < 0
                        or cx >= len(lines)
                        or cy >= len(lines[i])
                    ):
                        # Out of bounds
                        continue

                    if cx == i and cy == j:
                        continue

                    if lines[cx][cy].isnumeric():
                        pn_coords.append((cx, cy))

            power_numbers = []
            power_number_coords_set = set()

            for cx, cy in sorted(pn_coords):
                if (cx, cy) in power_number_coords_set:
                    continue

                power_number_coords_set.add((cx, cy))

                start_coord = -1
                end_coord = -1

                diff = 0
                while True:
                    if cy + diff >= len(lines[cx]):
                        end_coord = len(lines[cx])
                        power_number_coords_set.add((cx, end_coord))
                        break
                    if not lines[cx][cy + diff].isnumeric():
                        end_coord = cy + diff
                        power_number_coords_set.add((cx, end_coord))
                        break
                    diff += 1
                    power_number_coords_set.add((cx, cy + diff))

                diff = 0
                while True:
                    if cy - diff < 0:
                        start_coord = 0
                        power_number_coords_set.add((cx, start_coord))
                        break
                    if not lines[cx][cy - diff].isnumeric():
                        start_coord = cy - diff + 1
                        power_number_coords_set.add((cx, start_coord))
                        break
                    diff += 1
                    power_number_coords_set.add((cx, cy - diff))

                power_numbers.append(int(lines[cx][start_coord:end_coord]))

            if len(power_numbers) != 2:
                continue

            gear_numbers.append(power_numbers[0] * power_numbers[1])

    return gear_numbers


print(sum(task_1(lines)))
print(sum(task_2(lines)))
