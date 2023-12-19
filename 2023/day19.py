from functools import reduce


Part = tuple[int, int, int, int]

with open("input/day19_condition", "r") as f:
    conditions_lines = list(filter(lambda x: x != "", f.read().split("\n")))

with open("input/day19_parts", "r") as f:
    parts_lines = list(filter(lambda x: x != "", f.read().split("\n")))


class DecisionNode:
    condition: str
    true_node: str
    false_node: "DecisionNode | str"

    def __init__(
        self,
        condition: str,
        true_node: str,
        false_node: "DecisionNode | str",
    ):
        self.condition = condition
        self.true_node = true_node
        self.false_node = false_node

    def decide(self, part: Part) -> str:
        x, m, a, s = part
        if eval(self.condition):
            return self.true_node

        if isinstance(self.false_node, str):
            return self.false_node
        return self.false_node.decide(part)

    def __repr__(self) -> str:
        return f"DecisionNode({self.condition}, {self.true_node}, {self.false_node})"


def parse_condition_line(l: str) -> tuple[str, DecisionNode]:
    workflow_name, l_split = l.split("{")
    cond_list = l_split[:-1].split(",")

    node = cond_list[-1]
    for i in range(len(cond_list) - 2, -1, -1):
        condition, true_node = cond_list[i].split(":")
        node = DecisionNode(condition, true_node, node)

    return workflow_name, node  # type: ignore


def parse_part_line(l: str) -> Part:
    x, m, a, s = l[1:-1].split(",")

    def _part(p: str) -> int:
        return int(p.split("=")[1])

    return (_part(x), _part(m), _part(a), _part(s))


condition_dict: dict[str, DecisionNode] = {}
for l in conditions_lines:
    workflow, decision = parse_condition_line(l)
    condition_dict[workflow] = decision

parts = [parse_part_line(l) for l in parts_lines]


def task_1():
    def decide_part(part: Part) -> int:
        node = condition_dict["in"]
        while True:
            decision = node.decide(part)
            if decision == "A":
                return sum(part)
            elif decision == "R":
                return 0
            node = condition_dict[decision]

    return sum(decide_part(part) for part in parts)


print(task_1())


def flatten():
    all_accept_condition_str_list: list[list[str]] = []

    def _flatten(node: DecisionNode | str, curr_path: list[str]):
        if isinstance(node, str):
            if node == "A":
                all_accept_condition_str_list.append(curr_path.copy())
                return
            elif node == "R":
                return
            else:
                node = condition_dict[node]

        assert isinstance(node, DecisionNode)

        left_new_curr_path = curr_path.copy()
        left_new_curr_path.append(node.condition)
        _flatten(node.true_node, left_new_curr_path)

        right_new_curr_path = curr_path.copy()
        right_new_curr_path.append(f"not {node.condition}")
        _flatten(node.false_node, right_new_curr_path)

    _flatten(condition_dict["in"], [])
    return all_accept_condition_str_list


def convert_to_group(cond_list: list[str]) -> dict[str, dict[str, int]]:
    def reverse_sign(sign: str) -> str:
        if sign == ">":
            return "<="
        else:
            return ">="

    grouped_by_head_cond: dict[str, list[str]] = {
        "x": [],
        "m": [],
        "a": [],
        "s": [],
    }
    for cond in cond_list:
        if "not" not in cond:
            head = cond[0]
            sign = cond[1]
            body = cond[2:]
        else:
            cond = cond[4:]
            head = cond[0]
            sign = reverse_sign(cond[1])
            body = cond[2:]
        cond = " ".join([head, sign, body])
        grouped_by_head_cond[head].append(cond)

    def group_by_sign(conditions: list[str]) -> dict[str, list[int]]:
        if len(conditions) == 0:
            return {}

        grouped_by_sign: dict[str, list[int]] = {
            "<=": [],
            ">=": [],
            ">": [],
            "<": [],
        }
        for cond in conditions:
            _, sign, body = cond.split()
            grouped_by_sign[sign].append(int(body))
        return grouped_by_sign

    grouped_by_head_and_sign: dict[str, dict[str, int]] = {}
    for head, cond_list in grouped_by_head_cond.items():
        sign_group = group_by_sign(cond_list)
        if len(sign_group) > 0:
            grouped_by_head_and_sign[head] = {}
            for s, b in sign_group.items():
                if len(b) > 0:
                    if s in ["<=", "<"]:
                        grouped_by_head_and_sign[head][s] = min(b)
                    else:
                        grouped_by_head_and_sign[head][s] = max(b)
        else:
            grouped_by_head_and_sign[head] = {}

    return grouped_by_head_and_sign


def convert_to_interval(group: dict[str, int]) -> tuple[int, int]:
    INTERVAL_START = 1
    INTERVAL_END = 4000

    if len(group) == 0:
        return (INTERVAL_START, INTERVAL_END)

    if "<=" not in group and "<" not in group:
        upper_bound = INTERVAL_END
    elif "<=" in group and "<" not in group:
        upper_bound = group["<="]
    elif "<=" not in group and "<" in group:
        upper_bound = group["<"] - 1
    else:
        upper_bound = min(group["<="], group["<"] - 1)

    if ">=" not in group and ">" not in group:
        lower_bound = INTERVAL_START
    elif ">=" in group and ">" not in group:
        lower_bound = group[">="]
    elif ">=" not in group and ">" in group:
        lower_bound = group[">"] + 1
    else:
        lower_bound = max(group[">="], group[">"] + 1)

    return (lower_bound, upper_bound)


def task_2():
    all_accept_condition_str_list = flatten()
    cond_group_list = [
        convert_to_group(cond_list)
        for cond_list in all_accept_condition_str_list
    ]

    return sum(
        reduce(
            lambda prod, interval: prod * (interval[1] - interval[0] + 1),
            [convert_to_interval(sign_group) for sign_group in group.values()],
            1,
        )
        for group in cond_group_list
    )


print(task_2())
