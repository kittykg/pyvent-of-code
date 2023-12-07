from functools import cmp_to_key

with open("input/day07", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))

cards = []
bids = []
for l in lines:
    cards.append(l.split(" ")[0])
    bids.append(int(l.split(" ")[1]))


def five_of_a_kind(hand: str) -> bool:
    # Five of a kind, where all five cards have the same label: AAAAA
    return len(set(hand)) == 1


def four_of_a_kind(hand: str) -> bool:
    # Four of a kind, where four cards have the same label and one card has a
    # different label: AA8AA
    if len(set(hand)) != 2:
        return False
    sorted_count = sorted([hand.count(card) for card in set(hand)])
    return sorted_count == [1, 4]


def full_house(hand: str) -> bool:
    # Full house, where three cards have the same label, and the remaining two
    # cards share a different label: 23332
    if len(set(hand)) != 2:
        return False
    sorted_count = sorted([hand.count(card) for card in set(hand)])
    return sorted_count == [2, 3]


def three_of_a_kind(hand: str) -> bool:
    # Three of a kind, where three cards have the same label, and the remaining
    # two cards are each different from any other card in the hand: TTT98
    if len(set(hand)) != 3:
        return False
    sorted_count = sorted([hand.count(card) for card in set(hand)])
    return sorted_count == [1, 1, 3]


def two_pair(hand: str) -> bool:
    # Two pair, where two cards share one label, two other cards share a second
    # label, and the remaining card has a third label: 23432
    if len(set(hand)) != 3:
        return False
    sorted_count = sorted([hand.count(card) for card in set(hand)])
    return sorted_count == [1, 2, 2]


def one_pair(hand: str) -> bool:
    # One pair, where two cards share one label, and the other three cards have
    # a different label from the pair and each other: A23A4
    if len(set(hand)) != 4:
        return False
    sorted_count = sorted([hand.count(card) for card in set(hand)])
    return sorted_count == [1, 1, 1, 2]


def high_card(hand: str) -> bool:
    # High card, where all cards' labels are distinct: 23456
    return len(set(hand)) == 5


def get_hand_type(hand: str) -> int:
    if five_of_a_kind(hand):
        return 10
    elif four_of_a_kind(hand):
        return 9
    elif full_house(hand):
        return 8
    elif three_of_a_kind(hand):
        return 7
    elif two_pair(hand):
        return 6
    elif one_pair(hand):
        return 5
    elif high_card(hand):
        return 4
    return 0


def comparison_function_1(hand1: str, hand2: str) -> int:
    # returns a negative number for less-than
    # zero for equality, or a positive number for greater-than
    hand1_type = get_hand_type(hand1)
    hand2_type = get_hand_type(hand2)

    if hand1_type > hand2_type:
        return 1
    elif hand1_type < hand2_type:
        return -1

    # same hand type, compare the cards
    card_strength = "23456789TJQKA"
    for c1, c2 in zip(hand1, hand2):
        if card_strength.index(c1) > card_strength.index(c2):
            return 1
        elif card_strength.index(c1) < card_strength.index(c2):
            return -1
    return 0


def task_1():
    cmp_fn = lambda x, y: comparison_function_1(x[0], y[0])
    sorted_cards = sorted(zip(cards, bids), key=cmp_to_key(cmp_fn))
    return sum([bid * (i + 1) for i, (_, bid) in enumerate(sorted_cards)])


def convert_card(hand: str) -> str:
    # J is a wild card now
    if "J" not in hand:
        return hand

    sorted_cards = sorted(
        [(hand.count(card), card) for card in set(hand) if card != "J"]
    )
    if len(sorted_cards) == 0:
        # All Js
        return hand

    _, max_card = sorted_cards[-1]
    return hand.replace("J", max_card)


def comparison_function_2(hand1: str, hand2: str) -> int:
    # returns a negative number for less-than
    # zero for equality, or a positive number for greater-than
    ch1 = convert_card(hand1)
    ch2 = convert_card(hand2)

    ch1_type = get_hand_type(ch1)
    ch2_type = get_hand_type(ch2)

    if ch1_type > ch2_type:
        return 1
    elif ch1_type < ch2_type:
        return -1

    # same hand type, compare the cards
    card_strength = "J23456789TQKA"
    for c1, c2 in zip(hand1, hand2):
        if card_strength.index(c1) > card_strength.index(c2):
            return 1
        elif card_strength.index(c1) < card_strength.index(c2):
            return -1
    return 0


def task_2():
    cmp_fn = lambda x, y: comparison_function_2(x[0], y[0])
    sorted_cards = sorted(zip(cards, bids), key=cmp_to_key(cmp_fn))
    print(sorted_cards)
    return sum([bid * (i + 1) for i, (_, bid) in enumerate(sorted_cards)])


print(task_1())
print(task_2())


def prolog_input():
    with open("day07.out", "w") as f:
        f.write("input([\n")
        f.write(",\n".join([f'   ("{c}", {b})' for c, b in zip(cards, bids)]))
        f.write("\n]).\n")


prolog_input()
