from itertools import combinations
from typing import Dict, List, Set, Tuple

import networkx as nx


with open("input/day16", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def parse_line(l: str) -> Tuple[str, int, List[str]]:
    splitted = l.split(" ")
    valve = splitted[1]
    rate = int(splitted[4][5:-1])
    dest = "".join(splitted[9:]).split(",")
    return (valve, rate, dest)


# Let networkx calculate the pair wise distance for us hehe
G = nx.DiGraph()
valve_rate_dict: Dict[str, int] = dict()
for l in lines:
    valve, rate, dest = parse_line(l)
    valve_rate_dict[valve] = rate
    for d in dest:
        G.add_edge(valve, d)

useful_valves = [v for v, r in valve_rate_dict.items() if r > 0]

uv_dist_pair = dict()

for v1 in useful_valves + ["AA"]:
    for v2 in useful_valves + ["AA"]:
        uv_dist_pair[v1 + v2] = nx.shortest_path_length(G, v1, v2)


def search(
    time: int, curr_valve: str, useful_v: Set[str]
) -> Tuple[int, List[str]]:
    possibles = [(0, [])]

    for v in useful_v:
        if uv_dist_pair[curr_valve + v] < time:
            time_left = time - uv_dist_pair[curr_valve + v] - 1
            g = valve_rate_dict[v] * time_left
            o, path = search(time_left, v, useful_v - set([v]))
            possibles.append((g + o, [v] + path))
    return sorted(possibles, key=lambda x: x[0], reverse=True)[0]


def task_1():
    print(search(30, "AA", set(useful_valves))[0])


def task_2_cheat():
    # During the big fat input, one alone can't cover all valve in 26 min. Say
    # we let elephant go alone and it best covers a set EP, we just need to
    # cover the rest. This way we can together cover the most.
    # Only work for large input because example too small elephant can cover all
    # in 26 min. Runs a lot faster than none cheat way
    em, ep = search(26, "AA", set(useful_valves))
    mm, _ = search(26, "AA", set(useful_valves) - set(ep))
    print(em + mm)


def task_2():
    # None cheat way, but takes way longer
    def search_2(time: int, curr_valve: str, useful_v: Set[str]):
        possibles: List[Tuple[int, List[str]]] = [(0, [])]
        for i in range(1, len(useful_v) - 1):
            for ev in combinations(useful_v, i):
                eg, ep = search(time, curr_valve, set(ev))
                mg, mp = search(time, curr_valve, useful_v - set(ev))
                possibles.append((eg + mg, ep + mp))
        return sorted(possibles, key=lambda x: x[0], reverse=True)[0]

    print(search_2(26, "AA", set(useful_valves)))


task_1()
# task_2_cheat()
task_2()
