import numpy as np


def mark_card(cards, draw_number):
    for card in cards:
        card[np.where(card == draw_number)] = 0
        if min(card.sum(axis=0)) == 0 or min(card.sum(axis=1)) == 0:
            return card
    return True


def day04a(lines):
    day04_input = lines.copy()
    day04_input = [x for x in day04_input if x]
    cards = []
    draw = [int(x) for x in day04_input[0].split(",")]

    for i in range(1, len(day04_input), 5):
        cards.append(np.array([x.split() for x in day04_input[i : i + 5]], dtype=int))

    for i in draw:
        ret = mark_card(cards, i)
        if type(ret) == np.ndarray:
            break

    return ret.sum() * int(i)


ex = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1
22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19
 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6
14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7""".split(
    "\n"
)


def test_04_ex1a():
    assert day04a(ex) == 4512


# def test_04_ex1b():
#     assert day04b(*parse(ex)) == 1924


def test_04(day04_lines):
    assert day04a(day04_lines) == 60368
