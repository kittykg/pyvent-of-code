with open("input/day17", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

og_reg_A = int(lines[0].split(": ")[1])
reg_A: int = int(lines[0].split(": ")[1])
reg_B: int = int(lines[1].split(": ")[1])
reg_C: int = int(lines[2].split(": ")[1])

program = list(map(int, lines[3].split(": ")[1].split(",")))


def print_all_registers():
    print(f"A: {reg_A}, B: {reg_B}, C: {reg_C}")


def get_combo_operant_value(operand: int) -> int:
    assert 0 <= operand <= 6, f"Invalid operand {operand}"
    if operand <= 3:
        return operand
    return {4: reg_A, 5: reg_B, 6: reg_C}[operand]


def adv(operand: int) -> int:
    global reg_A
    denominator = 2 ** get_combo_operant_value(operand)
    out = reg_A // denominator
    reg_A = out
    return out


def bxl(operand: int) -> int:
    global reg_B
    reg_B = reg_B ^ operand
    return reg_B


def bst(operand: int) -> int:
    global reg_B
    val = get_combo_operant_value(operand) % 8
    reg_B = val
    return reg_B


def jnz(operand: int) -> int:
    if reg_A == 0:
        return -1
    return operand


def bxc(operand: int) -> int:
    global reg_B
    reg_B = reg_B ^ reg_C
    return reg_B


def out(operand: int) -> int:
    return get_combo_operant_value(operand) % 8


def bdv(operand: int) -> int:
    global reg_B
    denominator = 2 ** get_combo_operant_value(operand)
    out = reg_A // denominator
    reg_B = out
    return out


def cdv(operand: int) -> int:
    global reg_C
    denominator = 2 ** get_combo_operant_value(operand)
    out = reg_A // denominator
    reg_C = out
    return out


opcode_to_instruction = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv,
}


def run_program():
    i = 0
    output_numbers = []

    while i < len(program):
        opcode = program[i]
        operand = program[i + 1]
        instr_fn = opcode_to_instruction[opcode]
        ret = instr_fn(operand)

        if opcode == 5:
            output_numbers.append(ret)
        if opcode == 3 and ret != -1:
            i = ret
        else:
            i += 2

    return ",".join(map(str, output_numbers))


print("Part 1:")
print(run_program())
