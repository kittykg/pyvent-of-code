with open("input/day09", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

disk_map = list(map(int, lines[0]))


def task_1():
    # Construct the disk
    disk, id, space = [], 0, False
    for i in disk_map:
        for _ in range(i):
            e = None if space else id
            disk.append(e)
        if not space:
            id += 1
        space = not space

    # Move the file
    left_pt, right_pt = 0, len(disk) - 1
    while left_pt < right_pt:
        left = disk[left_pt]
        if left is not None:
            left_pt += 1
            continue

        right = disk[right_pt]
        if right is None:
            right_pt -= 1
            continue

        # Swap the left (a None) and right (an ID)
        disk[left_pt], disk[right_pt] = disk[right_pt], disk[left_pt]
        left_pt += 1
        right_pt -= 1

    # Checksum
    cs = 0
    for i, j in enumerate(disk):
        if j is None:
            break
        cs += i * j
    print(cs)


class File:
    id: int
    start: int
    len: int
    afterwards_number_of_space: int

    def __init__(
        self, id: int, start: int, len: int, afterwards_number_of_space: int
    ):
        self.id = id
        self.start = start
        self.len = len
        self.afterwards_number_of_space = afterwards_number_of_space

    def clear_afterwards_space(self) -> int:
        og_afterwards_number_of_space = self.afterwards_number_of_space
        self.afterwards_number_of_space = 0

        return og_afterwards_number_of_space

    def get_next_free_location(self) -> int:
        return self.start + self.len + self.afterwards_number_of_space

    def get_occupied_space(self) -> int:
        return self.len + self.afterwards_number_of_space

    def get_disk_str(self) -> str:
        ret_str = ""
        for _ in range(self.len):
            ret_str += str(self.id)
        for _ in range(self.afterwards_number_of_space):
            ret_str += "."
        return ret_str

    def __repr__(self):
        return f"File(id={self.id}, start={self.start}, len={self.len}, afterwards_number_of_space={self.afterwards_number_of_space})"


def construct_disk(disk_map: list[int]) -> list[File]:
    disk, id, start = [], 0, 0
    for i in range(0, len(disk_map), 2):
        file_len = disk_map[i]
        afterwards_number_of_space = (
            disk_map[i + 1] if i + 1 < len(disk_map) else 0
        )
        disk.append(File(id, start, file_len, afterwards_number_of_space))
        id += 1
        start += file_len + afterwards_number_of_space

    return disk


def move_file(disk: list[File]):
    target_file_id = len(disk) - 1
    while True:
        for i in range(len(disk) - 1, -1, -1):
            if disk[i].id == target_file_id:
                break

        if i == 0:
            # The target file is the first file, we checked all files
            return

        target_file_idx = i
        target_file = disk[target_file_idx]
        previous_file = disk[target_file_idx - 1]

        can_swap = False

        for i, f in enumerate(disk):
            if i >= target_file_idx:
                break
            if f.afterwards_number_of_space >= target_file.len:
                can_swap = True
                break

        if can_swap:
            previous_file.afterwards_number_of_space += (
                target_file.get_occupied_space()
            )
            og_space = f.clear_afterwards_space()
            new_tf = File(
                id=target_file.id,
                start=f.get_next_free_location(),
                len=target_file.len,
                afterwards_number_of_space=og_space - target_file.len,
            )
            disk.insert(i + 1, new_tf)
            disk.pop(target_file_idx + 1)

        target_file_id -= 1


def task_2():
    from datetime import datetime

    start = datetime.now()
    disk = construct_disk(disk_map)
    move_file(disk)

    cs = 0
    for f in disk:
        for i in range(f.len):
            idx = f.start + i
            cs += idx * f.id
    print(cs)
    print(datetime.now() - start)


task_1()
task_2()
