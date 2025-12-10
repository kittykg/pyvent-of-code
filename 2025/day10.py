# %%
import numpy as np
from scipy.optimize import milp, LinearConstraint

with open("input/day10", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


def parse_line(line: str) -> tuple[list[int], list[tuple[int]], set[int]]:
    buttons: list[tuple[int]] = []
    for p in line.split(" "):
        if p.startswith("["):
            target = [1 if p[i] == "#" else 0 for i in range(1, len(p) - 1)]
        elif p.startswith("("):
            buttons.append(
                eval(p) if isinstance(eval(p), tuple) else (eval(p),)
            )
        elif p.startswith("{"):
            joltages = list(map(int, p.strip("{").strip("}").split(",")))
    return target, buttons, joltages


# %%
def task(
    target: list[int], buttons: list[tuple[int]], joltages: list[int]
) -> list[int]:
    def task_1() -> int:
        initial_state = [0] * len(target)
        history = [(initial_state, [])]
        while len(history) > 0:
            curr_state, path = history.pop(0)
            for button in buttons:
                if path and button == path[-1]:
                    continue
                new_path = path.copy()
                new_path.append(button)
                new_state = curr_state.copy()
                for i in button:
                    new_state[i] ^= 1
                if new_state == target:
                    return len(new_path)
                history.append((new_state, new_path))
        return 0

    def task_2() -> int:
        N = len(buttons)
        button_matrix = np.zeros((N, len(joltages)))
        for i, button in enumerate(buttons):
            for j in button:
                button_matrix[i, j] = 1
        res = milp(
            c=np.ones(N),
            integrality=np.ones(N),
            constraints=LinearConstraint(
                A=button_matrix.T, ub=np.array(joltages), lb=np.array(joltages)
            ),
        )  # min_x c.T @ x = sum(x_i)  s.t. A @ x == b, x >= 0, x integer
        return int(np.sum(res.x))

    return [task_1(), task_2()]


print(np.array([task(*parse_line(l)) for l in lines]).sum(axis=0))


# %%
