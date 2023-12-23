from dataclasses import dataclass


Coord = tuple[int, int, int]
with open("input/day22", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


@dataclass
class Cube:
    start: Coord
    end: Coord

    def fall_one_step(self) -> "Cube":
        return Cube(
            (self.start[0], self.start[1], self.start[2] - 1),
            (self.end[0], self.end[1], self.end[2] - 1),
        )

    def get_orientation(self) -> int:
        """Return the axis that is flat on"""
        if self.start[0] == self.end[0] and self.start[1] != self.end[1]:
            # flat on y axis
            return 1
        elif self.start[0] != self.end[0] and self.start[1] == self.end[1]:
            # flat on 0 axis
            return 0
        # case of a single dot
        return -1

    def get_orientation_range(self) -> tuple[int, int]:
        """Return the range of the axis that is flat on"""
        if self.start[0] == self.end[0] and self.start[1] != self.end[1]:
            # flat on x axis, return the range of x
            return (self.start[1], self.end[1])
        elif self.start[0] != self.end[0] and self.start[1] == self.end[1]:
            # flat on y axis, return the range of y
            return (self.start[0], self.end[0])

        # case of a single dot, return its x and y coordinates
        return (self.start[0], self.start[1])


def parse_line(l: str) -> Cube:
    start_str, end_str = l.split("~")
    start = tuple(int(i) for i in start_str.split(","))
    end = tuple(int(i) for i in end_str.split(","))
    return Cube(min(start, end), max(start, end))  # type: ignore


cubes = [parse_line(l) for l in lines]

# sort the cubes based on their start z coordinate
sorted_cubes = sorted(cubes, key=lambda c: c.start[2])

# create a dict with the cube id as the key, this stores the original in air
# coordinates of each cube
cubes_with_id_dict = {i: c for i, c in enumerate(sorted_cubes)}


def support(c1: Cube, c2: Cube) -> bool:
    # Return True if c1 supports c2
    # there are 9 cases:
    c1_orientation = c1.get_orientation()
    c2_orientation = c2.get_orientation()

    if c1_orientation == -1 and c2_orientation == -1:
        # c1 and c2 are both single dots
        c1_or = c1.get_orientation_range()
        c2_or = c2.get_orientation_range()
        return c1_or == c2_or
    elif c1_orientation == -1 and c2_orientation == 0:
        # c1 is a single dot, c2 is flat on x axis
        c1_or = c1.get_orientation_range()
        c2_or = c2.get_orientation_range()  # c2's x range
        return (
            c2_or[0] <= c1_or[0] <= c2_or[1]  # check c1 is in c2's x range
            and c1_or[1] == c2.start[1]  # and c1's y is the same as c2's y
        )
    elif c1_orientation == -1 and c2_orientation == 1:
        # c1 is a single dot, c2 is flat on y axis
        c1_or = c1.get_orientation_range()
        c2_or = c2.get_orientation_range()  # c2's y range
        return (
            c2_or[0] <= c1_or[1] <= c2_or[1]  # check c1 is in c2's y range
            and c1_or[0] == c2.start[0]  # and c1's y is the same as c2's x
        )
    elif c1_orientation == 0 and c2_orientation == -1:
        # c1 is flat on x axis, c2 is a single dot
        c1_or = c1.get_orientation_range()  # c1's x range
        c2_or = c2.get_orientation_range()
        return (
            c1_or[0] <= c2_or[0] <= c1_or[1]  # check c2 is in c1's x range
            and c1.start[1] == c2_or[1]  # and c2's y is the same as c1's y
        )
    elif c1_orientation == 1 and c2_orientation == -1:
        # c1 is flat on y axis, c2 is a single dot
        c1_or = c1.get_orientation_range()  # c1's y range
        c2_or = c2.get_orientation_range()
        return (
            c1_or[0] <= c2_or[1] <= c1_or[1]  # check c2 is in c1's y range
            and c1.start[0] == c2_or[0]  # and c2's x is the same as c1's x
        )
    elif c1_orientation == c2_orientation == 0:
        # c1 and c2 both flat on x axis
        # check if there's an overlap on that axis
        c1_or = c1.get_orientation_range()
        c2_or = c2.get_orientation_range()
        if c1.start[1] != c2.start[1]:
            # if they don't have the same y coordinate, then they can't be
            # supporting each other
            return False
        return (
            len(
                set(range(c1_or[0], c1_or[1] + 1)).intersection(
                    set(range(c2_or[0], c2_or[1] + 1))
                )
            )
            > 0
        )
    elif c1_orientation == c2_orientation == 1:
        # c1 and c2 both flat on y axis
        # check if there's an overlap on that axis
        c1_or = c1.get_orientation_range()
        c2_or = c2.get_orientation_range()
        if c1.start[0] != c2.start[0]:
            # if they don't have the same x coordinate, then they can't be
            # supporting each other
            return False
        return (
            len(
                set(range(c1_or[0], c1_or[1] + 1)).intersection(
                    set(range(c2_or[0], c2_or[1] + 1))
                )
            )
            > 0
        )
    elif c1_orientation == 0 and c2_orientation == 1:
        # c1 flat on x axis, c2 flat on y axis
        # if they intersect, then c1 is supporting c2
        return (
            c1.start[0] <= c2.start[0] <= c1.end[0]
            and c2.start[1] <= c1.start[1] <= c2.end[1]
        )
    else:
        # c1 flat on y axis, c2 flat on x axis
        # if they intersect, then c1 is supporting c2
        return (
            c1.start[1] <= c2.start[1] <= c1.end[1]
            and c2.start[0] <= c1.start[0] <= c2.end[0]
        )


def fall():
    # create a dict with the cube id as the key, this stores the final fallen
    # coordinates of each cube
    fallen_cubes: dict[int, Cube] = {}
    fallen_bagged_based_on_z: dict[int, list[int]] = {1: []}

    for i, c in cubes_with_id_dict.items():
        if c.start[2] == 1:
            # The cube is already on the ground
            fallen_cubes[i] = c
            fallen_bagged_based_on_z[c.start[2]].append(i)
            continue

        while True:
            z_one_below = c.start[2] - 1

            if z_one_below == 0:
                # The cube is on the ground
                break

            if z_one_below not in fallen_bagged_based_on_z:
                # The cube is not on the ground, and there is no cube below it
                # so the cube will fall one step
                c = c.fall_one_step()
                continue

            # there is some cube below it
            cubes_below = fallen_bagged_based_on_z[z_one_below]

            # check if the cube is supported by any of the cubes below it
            support_cube_id: int | None = None
            for cb_id in cubes_below:
                if support(fallen_cubes[cb_id], c):
                    support_cube_id = cb_id
                    break
            if support_cube_id is not None:
                # the cube is supported by some cube below it
                # so the cube will stop falling
                break

            # the cube is not supported by any of the cubes below it
            c = c.fall_one_step()
            continue

        fallen_cubes[i] = c

        if c.get_orientation() == -1:
            # The block is in z orientation, add the end height of it to the bag
            key = c.end[2]

        else:
            # The block is in x or y orientation, add the start height of it to the
            # bag
            key = c.start[2]

        if key not in fallen_bagged_based_on_z:
            fallen_bagged_based_on_z[key] = []
        fallen_bagged_based_on_z[key].append(i)

    support_bagged_base_on_z = {}
    for z, cube_ids in fallen_bagged_based_on_z.items():
        for cid in cube_ids:
            cube = fallen_cubes[cid]
            if cube.get_orientation() == -1:
                actual_z = cube.start[2]
            else:
                actual_z = z

            if actual_z not in support_bagged_base_on_z:
                support_bagged_base_on_z[actual_z] = []
            support_bagged_base_on_z[actual_z].append(cid)

    # Create the dependence dictionaries
    support_dict = {}
    rely_on_dict = {}

    for z, cube_ids in support_bagged_base_on_z.items():
        if z == 1:
            # Ignore the cube on the ground
            continue

        for cid in cube_ids:
            cube = fallen_cubes[cid]
            z_below = z - 1

            if z_below == 0:
                break

            potential_cubes_below = fallen_bagged_based_on_z[z_below]
            for pc in potential_cubes_below:
                if support(fallen_cubes[pc], cube):
                    if pc not in support_dict:
                        support_dict[pc] = []
                    support_dict[pc].append(cid)

                    if cid not in rely_on_dict:
                        rely_on_dict[cid] = []
                    rely_on_dict[cid].append(pc)

    support_dict = {k: support_dict[k] for k in sorted(support_dict.keys())}
    rely_on_dict = {k: rely_on_dict[k] for k in sorted(rely_on_dict.keys())}

    return support_dict, rely_on_dict


support_dict, rely_on_dict = fall()


def task_1():
    disintegrate_count = 0

    for i in sorted(cubes_with_id_dict.keys()):
        if i not in support_dict:
            disintegrate_count += 1
            continue

        can_be_disintegrated = [False for _ in support_dict[i]]
        for k, supported_cid in enumerate(support_dict[i]):
            for j, sl in support_dict.items():
                if j == i:
                    continue
                if supported_cid in sl:
                    can_be_disintegrated[k] = True
                    break

        if all(can_be_disintegrated):
            disintegrate_count += 1
    return disintegrate_count


def task_2():
    def remove_one_block(
        cid: int,
        support_dict: dict[int, list[int]],
        rely_on_dict: dict[int, list[int]],
    ) -> int:
        if cid not in support_dict:
            return 0

        removal_list = [cid]

        for k, v in rely_on_dict.items():
            if set(v).issubset(removal_list):
                # All the blocks that this k relying on have been removed, k will be
                # gone too
                removal_list.append(k)

        return len(removal_list) - 1

    acc = 0
    for cid in cubes_with_id_dict.keys():
        acc += remove_one_block(cid, support_dict, rely_on_dict)
    return acc


print(task_1())
print(task_2())
