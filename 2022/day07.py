from enum import Enum
import re
from typing import Dict, List, Optional, Self


class TreeNodeType(Enum):
    DIR = "dir"
    FILE = "file"


class TreeNode:
    type: TreeNodeType
    name: str
    parent: Optional[Self]
    children: Dict[str, Self]
    size: int = 0

    def __init__(
        self,
        type: TreeNodeType,
        name: str,
        parent: Optional[Self],
        size: int = 0,
    ) -> None:
        self.type = type
        self.name = name
        self.parent = parent
        self.size = size

        self.children = dict()

    def calculate_size(self) -> int:
        if self.type == TreeNodeType.DIR and self.size == 0:
            # Need to calculate the size of dir recursively
            # This part of the calculation should be run only once at all
            for _, n in self.children.items():
                self.size += n.calculate_size()
        return self.size


def get_all_dir_size(root: TreeNode) -> List[int]:
    def _get_all_dir_size(node: TreeNode, dir_size_list: List[int]):
        for _, n in node.children.items():
            if n.type == TreeNodeType.DIR:
                dir_size_list.append(n.size)
                _get_all_dir_size(n, dir_size_list)

    dir_size_list = []
    _get_all_dir_size(root, dir_size_list)
    return dir_size_list


with open("input/day07", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

cd_p = re.compile(r"\$ cd (.+)")
dir_p = re.compile(r"dir (.+)")
file_p = re.compile(r"(\d+) (.+)")

# Construct tree
root = TreeNode(TreeNodeType.DIR, "/", None)
current_node: TreeNode = root
for l in lines[1:]:
    if cd_p.match(l):  # It's a cd command
        dir_name = cd_p.match(l)[1]
        if dir_name in current_node.children.keys():  # Go down a dir
            current_node = current_node.children[dir_name]
        elif dir_name == "..":  # Go up a dir
            current_node = current_node.parent
    if l == "$ ls":  # It's a ls command
        continue
    if dir_p.match(l):  # This line is a dir
        dir_name = dir_p.match(l)[1]
        child_node = TreeNode(TreeNodeType.DIR, dir_name, current_node)
        current_node.children[dir_name] = child_node
    if file_p.match(l):  # This line is a file
        file_size = file_p.match(l)[1]
        file_name = file_p.match(l)[2]
        child_node = TreeNode(
            TreeNodeType.FILE, file_name, current_node, size=int(file_size)
        )
        current_node.children[file_name] = child_node

# Update tree size for dir nodes
total_file_size = root.calculate_size()

# Task 1
all_dir_size = get_all_dir_size(root)
print(sum(list(filter(lambda i: i <= 100000, all_dir_size))))

# Task 2
free_size = total_file_size - (70000000 - 30000000)
print(min(list(filter(lambda i: i >= free_size, all_dir_size))))
