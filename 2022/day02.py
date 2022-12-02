from enum import IntEnum


class Choice(IntEnum):
    ROCK = -1
    PAPER = 0
    SCISSORS = 1

    def point(self) -> int:
        # 1 for Rock, 2 for Paper, and 3 for Scissors
        choice_point_map = {Choice.ROCK: 1, Choice.PAPER: 2, Choice.SCISSORS: 3}
        return choice_point_map[self]


class Result(IntEnum):
    # 0 if you lost, 3 if the round was a draw, and 6 if you won
    WIN = 6
    DRAW = 3
    LOSS = 0


def get_result(o: Choice, m: Choice) -> Result:
    diff_map = {
        -2: Result.WIN,
        -1: Result.LOSS,
        0: Result.DRAW,
        1: Result.WIN,
        2: Result.LOSS,
    }
    return diff_map[m - o]


def get_choice(r: Result, o: Choice) -> Choice:
    if r == Result.DRAW:
        return o
    if r == Result.LOSS:
        return Choice.SCISSORS if o - 1 == -2 else Choice(o - 1)
    return Choice.ROCK if o + 1 == 2 else Choice(o + 1)


# A for Rock, B for Paper, and C for Scissors
opponent_choice_map = {
    "A": Choice.ROCK,
    "B": Choice.PAPER,
    "C": Choice.SCISSORS,
}


# Task 1
# X for Rock, Y for Paper, and Z for Scissors.
def round_point_1(l: str) -> int:
    o, m = l.split(" ")
    my_choice_map = {"X": Choice.ROCK, "Y": Choice.PAPER, "Z": Choice.SCISSORS}
    oc = opponent_choice_map[o]
    mc = my_choice_map[m]
    return mc.point() + get_result(oc, mc)


# Task 2
# X means you need to lose, Y means you need to draw, Z means you need to win
def round_point_2(l: str) -> int:
    o, r = l.split(" ")
    result_map = {"X": Result.LOSS, "Y": Result.DRAW, "Z": Result.WIN}
    oc = opponent_choice_map[o]
    res = result_map[r]
    return res + get_choice(res, oc).point()


with open("input/day02", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))
print(sum([round_point_1(l) for l in lines]))
print(sum([round_point_2(l) for l in lines]))
