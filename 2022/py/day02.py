from typing import List


def rate_round(opponent: str, myself: str, alternate=False) -> int:

    opp = ord(opponent) - 65
    me = ord(myself) - 88

    rating = me - opp
    if rating < 0:
        rating += 3

    match rating:
        case 0:
            return 3
        case 1:
            return 6
        case 2:
            return 0
        case _:
            print(f"{opp} - {me}")
            raise Exception


def lookup_shape(opponent: str, myself: str):

    answers = {
        "AX": "Z",
        "AY": "X",
        "AZ": "Y",
        "BX": "X",
        "BY": "Y",
        "BZ": "Z",
        "CX": "Y",
        "CY": "Z",
        "CZ": "X",
    }

    return answers[opponent + myself]


def day02a(guide: List, alternate=False):

    score = 0

    for round in guide:

        opp, me = round.split(" ")
        if alternate:
            me = lookup_shape(opp, me)
        score += ord(me) - 87
        score += rate_round(opp, me, alternate)

    return score


ex = ["A Y", "B X", "C Z"]


def test_02_ex1a():
    assert day02a(ex) == 15


def test_02_ex1b():
    assert day02a(ex, True) == 12


def test_02a(day02_lines):
    assert day02a(day02_lines) == 15691


def test_02b(day02_lines):
    assert day02a(day02_lines, True) == 12989
