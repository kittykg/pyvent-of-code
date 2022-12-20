from typing import List, Optional, Self

with open("input/day20", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


class Node:
    val: int
    prev: Optional[Self]
    next: Optional[Self]

    def __init__(self, val, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


def get_nodes(key: int = 1):
    numbers = [int(l) * key for l in lines]
    nodes = [Node(i) for i in numbers]

    for n1, n2 in zip(nodes, nodes[1:]):
        n1.next = n2
        n2.prev = n1

    nodes[0].prev = nodes[-1]
    nodes[-1].next = nodes[0]

    return nodes


def move(nodes: List[Node]):
    for n in nodes:
        move_step = n.val % (len(nodes) - 1)

        # Remove the current node first
        n.prev.next = n.next  # type: ignore
        n.next.prev = n.prev  # type: ignore

        # Pair pointers
        p = n.prev
        q = n.next

        for _ in range(move_step):
            p = p.next  # type: ignore
            q = q.next  # type: ignore

        # Add back the current node
        p.next = n  # type: ignore
        n.prev = p
        q.prev = n  # type: ignore
        n.next = q


def get_output(nodes: List[Node]):
    for n in nodes:
        if n.val == 0:
            acc_val = 0
            c = n
            for _ in range(3):
                for _ in range(1000):
                    c = c.next  # type: ignore
                acc_val += c.val  # type: ignore
            print(acc_val)


def task_1():
    nodes = get_nodes()
    move(nodes)
    get_output(nodes)


def task_2():
    nodes = get_nodes(key=811589153)
    for _ in range(10):
        move(nodes)
    get_output(nodes)


task_1()
task_2()
