with open("input/day19", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

towels = lines[0].split(", ")
goals = lines[1:]


def match(goal: str, mem: dict[str, int]) -> int:
    if goal == "":
        return 1

    number_of_ways = 0
    for t in towels:
        if goal.endswith(t):
            new_goal = goal[: len(goal) - len(t)]
            if new_goal in mem:
                new_goal_match = mem[new_goal]
            else:
                new_goal_match = match(new_goal, mem)
                mem[new_goal] = new_goal_match

            number_of_ways += new_goal_match

    return number_of_ways


mem = {}
l = [match(g, mem) for g in goals]
print(f"Part 1: {len([x for x in l if x > 0])}")
print(f"Part 2: {sum(l)}")
