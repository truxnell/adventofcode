import argparse
import ast
from functools import cmp_to_key
from itertools import zip_longest
from typing import List

from utils import AocdPuzzle, setup_logging

YEAR: int = 2022
DAY: int = 14

EXAMPLE = []
ANS_1: int = 0
ANS_2: int = 0
PUZZLE = AocdPuzzle(year=YEAR, day=DAY)
PUZZLE_INPUT = PUZZLE.lines()

log = setup_logging("debug")


def solve_puzzle(puzzle_inp: List, part_a=True) -> int:

    return 0


if __name__ == "__main__":

    # Available types
    # lines() list of lines, stripped if strip=True
    # text() list of lines
    # numbers() list(s) of numbers from string
    # grid() grid of inpt
    # grid_value_from_str() grid of numbers, converting a-z to 1-25
    # number_grid() number grid of input

    parser = argparse.ArgumentParser(
        description=f"Advent of code for day {DAY}, December {YEAR}"
    )
    parser.add_argument(
        "-p", "--part", help="Part A or B", required=False, choices=["a", "b"]
    )
    parser.add_argument(
        "-s", "--solve", help="Submit solution", required=False, action="store_true"
    )
    args = vars(parser.parse_args())
    # if not args["parse"]:
    #     parser.print_help()
    #     sys.exit()

    print(f"Advent of code for day {DAY}, December {YEAR}\n")
    if args["part"] == "a" or not args["part"]:
        print("Example 1")

        answer = solve_puzzle(EXAMPLE)
        print(f"Returned: {answer}, solution {ANS_1}, Equality {answer==ANS_1}")

        print("\nPart 1")
        answer_a = solve_puzzle(PUZZLE_INPUT)
        print(answer_a)

        if args["solve"]:
            PUZZLE.submit_answer(answer_a, YEAR, DAY)

    if args["part"] == "b" or not args["part"]:
        print("Example 2")

        answer = solve_puzzle(EXAMPLE, part_a=False)
        print(f"Returned: {answer}, solution {ANS_2}, Equality {answer==ANS_2}")

        print("\nPart 2")
        answer_b = solve_puzzle(PUZZLE_INPUT, part_a=False)
        print(answer_b)

        if args["solve"]:
            PUZZLE.submit_answer(answer_b, YEAR, DAY)


def test_examples_pt_a():
    assert solve_puzzle(EXAMPLE) == ANS_1


def test_pt_a():
    assert solve_puzzle(PUZZLE_INPUT) == 0


def test_examples_pt_b():
    assert solve_puzzle(EXAMPLE, False) == ANS_2


def test_pt_b():
    assert solve_puzzle(PUZZLE_INPUT, False) == 0
           AocdPuzzle.submit_answer("", answer_b, YEAR, DAY)
