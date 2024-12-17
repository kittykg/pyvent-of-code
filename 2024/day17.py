with open("input/day17", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

og_reg_A: int = int(lines[0].split(": ")[1])
og_program: list[int] = list(map(int, lines[3].split(": ")[1].split(",")))


# 2,4     bst 4   # reg_B = reg_A % 8
# 1,5     bxl 5   # reg_B = reg_B ^ 5
# 7,5     cdv 5   # reg_C = reg_A // (2 ** reg_B)
# 1,6     bxl 6   # reg_B = reg_B ^ 6
# 0,3     adv 3   # reg_A = reg_A // 8
# 4,6     bxc 6   # reg_B = reg_B ^ reg_C
# 5,5     out 5   # print (reg_B % 8)
# 3,0     jnz 0   # if reg_A == 0 halt, otherwise start from beginning
def run_program(initial_reg_A: int = og_reg_A):
    A = initial_reg_A
    B, C = 0, 0

    output_numbers = []
    while A > 0:
        B, C = 0, 0
        B = A % 8
        B = B ^ 5
        C = A // (2**B)
        B = B ^ 6
        A = A // 8
        B = B ^ C
        output_numbers.append(B % 8)

    return output_numbers


print(f"Part 1:\n{','.join(map(str, run_program()))}")


# Part 2
final_As = []
A_acc: dict[int, list[int]] = {}

for i in range(1, len(og_program) + 1):
    # Check the last i elements of the og program
    t = og_program[-i:]
    if len(A_acc) == 0:
        # The first iteration is a special case, give [0] as the initial As list
        As = [0]
    else:
        # Find the output of last iteration, they are the possible starting
        # values of A that will give the same output for the last i elements of
        # the og
        As = A_acc[i - 1]

    for a in As:
        for j in range(8):
            # Since there's always A // 8 at the end of each loop, we can only
            # check a, a + 1, ... a + 7
            A = a + j
            out = run_program(A)
            if out == og_program:
                # This value of A works to have the program output to match with
                # the entire og program
                final_As.append(A)
            elif out == t:
                # This value of A works to have the program output to match with
                # the last i elements of the og program
                # Since there's always A // 8 at the end of each loop, the
                # possible start (used by the next iteration) will be A * 8
                if i not in A_acc:
                    A_acc[i] = []
                A_acc[i].append(A * 8)


print(f"Task 2: {min(final_As)}")
