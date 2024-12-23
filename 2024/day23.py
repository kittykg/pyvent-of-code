import networkx as nx

with open("input/day23", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

G = nx.Graph()
for l in lines:
    n1, n2 = l.split("-")
    G.add_nodes_from([n1, n2])
    G.add_edge(n1, n2)

all_cliques = list(nx.enumerate_all_cliques(G))

# Part 1
three_sets = set()
for c in all_cliques:
    if len(c) != 3:
        continue
    if not any(x.startswith("t") for x in c):
        continue
    three_sets.add(tuple(sorted(c)))
print(len(three_sets))

# Part 2
print(",".join(sorted(all_cliques[-1])))
