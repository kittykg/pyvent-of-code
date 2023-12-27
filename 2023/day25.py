import networkx as nx
from itertools import combinations
from dataclasses import dataclass

with open("input/day25", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def parse_line(l: str) -> tuple[str, list[str]]:
    head, tail = l.split(": ")
    connections = tail.split(" ")
    return head, connections


@dataclass
class Connection:
    start: str
    end: str

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Connection):
            return False
        return (self.start == __value.start and self.end == __value.end) or (
            self.start == __value.end and self.end == __value.start
        )


all_nodes = dict(parse_line(l) for l in lines)
G = nx.Graph()
for u, l in all_nodes.items():
    for v in l:
        G.add_edge(u, v, capacity=1)


def task_1():
    for s, t in combinations(all_nodes.keys(), 2):
        cut_value, partition = nx.flow.minimum_cut(G, s, t)
        if cut_value == 3:
            p1, p2 = partition
            return len(p1) * len(p2)


print(task_1())
