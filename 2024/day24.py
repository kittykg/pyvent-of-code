from collections import deque


with open("input/day24", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


wires: dict[str, int] = {}
instruction_list: list[tuple[str, str, str, str]] = []

for l in lines:
    if ": " in l:
        key, value = l.split(": ")
        wires[key] = int(value)

    else:
        x1, gate_type, x2, _, out = l.split(" ")
        instruction_list.append((x1, x2, gate_type, out))


queue = deque(instruction_list)

while queue:
    x1, x2, gate_type, out = queue.popleft()
    if x1 not in wires or x2 not in wires:
        queue.append((x1, x2, gate_type, out))
        continue

    x1_value = wires[x1]
    x2_value = wires[x2]
    if gate_type == "AND":
        wires[out] = x1_value & x2_value
    elif gate_type == "OR":
        wires[out] = x1_value | x2_value
    else:  # XOR
        wires[out] = x1_value ^ x2_value


z_str = "".join(
    [
        str(wires[z])
        for z in sorted(
            [k for k in wires.keys() if k.startswith("z")], reverse=True
        )
    ]
)
print(f"Task 1: {int(z_str, 2)}")


wrong = set()
for x1, x2, gate_type, out in instruction_list:
    if (
        out.startswith("z")
        and gate_type != "XOR"
        and out != f"z{len(z_str) - 1}"
    ):
        wrong.add(out)
    if (
        gate_type == "XOR"
        and out[0] not in ["x", "y", "z"]
        and x1[0] not in ["x", "y", "z"]
        and x2[0] not in ["x", "y", "z"]
    ):
        wrong.add(out)
    if gate_type == "AND" and "x00" not in [x1, x2]:
        for xx1, xx2, sub_gate, sub_out in instruction_list:
            if (out == xx1 or out == xx2) and sub_gate != "OR":
                wrong.add(out)
    if gate_type == "XOR":
        for xx1, xx2, sub_gate, sub_out in instruction_list:
            if (out == xx1 or out == xx2) and sub_gate == "OR":
                wrong.add(out)

print(f"Task 2: {','.join(sorted(wrong))}")
