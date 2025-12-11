# %%
from functools import cache

import networkx as nx

with open("input/day11", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

G = nx.DiGraph()
for l in lines:
    u, vs = l.split(": ")
    for v in vs.split(" "):
        G.add_edge(u, v)


# %%
@cache
def count(curr: str, target: str) -> int:
    return 1 if curr == target else sum(count(next, target) for next in G[curr])


print(len(list(nx.all_simple_paths(G, source="you", target="out"))))
print(count("you", "out"))
print(count("svr", "fft") * count("fft", "dac") * count("dac", "out"))

# %%
