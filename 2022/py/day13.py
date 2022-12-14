import argparse
import ast
from functools import cmp_to_key
from itertools import zip_longest
from typing import List

from utils import AocdPuzzle, setup_logging

YEAR: int = 2022
DAY: int = 13

EXAMPLE = [
    "[1,1,3,1,1]",
    "[1,1,5,1,1]",
    "",
    "[[1],[2,3,4]]",
    "[[1],4]",
    "",
    "[9]",
    "[[8,7,6]]",
    "",
    "[[4,4],4,4]",
    "[[4,4],4,4,4]",
    "",
    "[7,7,7,7]",
    "[7,7,7]",
    "",
    "[]",
    "[3]",
    "",
    "[[[]]]",
    "[[]]",
    "",
    "[1,[2,[3,[4,[5,6,7]]]],8,9]",
    "[1,[2,[3,[4,[5,6,0]]]],8,9]",
]
ANS_1: int = 13
ANS_2: int = 140
PUZZLE = AocdPuzzle(year=YEAR, day=DAY)
PUZZLE_INPUT = PUZZLE.lines()

log = setup_logging("debug")


def check_order(left: List, right: List) -> int:
    """
    Returns:
        1: False
        0: True
        0: Even-no result, continue searching
    """
    if len(right) == 0 and len(left) > 0:
        return 1

    if len(right) > 0 and len(left) == 0:
        return -1

    for i in range(max(len(left), len(right))):
        if i == len(left) and i <= len(right):
            return -1

        if i == len(right) and i <= len(left):
            return 1
        if i == len(right) == len(left):
            return -1

        lft = left[i]
        rgt = right[i]

        if not type(lft) == type(rgt):
            if isinstance(rgt, list):
                lft = [lft]
            else:
                rgt = [rgt]
        if isinstance(lft, list):
            ret = check_order(lft, rgt)
            if ret == 1:
                return 1
            if ret == -1:
                return -1
            continue

        if lft < rgt:
            return -1

        if lft > rgt:
            return 1

    return 0


def solve_puzzle(puzzle_inp: List, part_a=True) -> int:

    sum_puzzle = 0
    index = 0
    log.debug("Parsing Puzzle Input")
    if part_a:
        for left, right, _ in zip_longest(
            puzzle_inp[::3], puzzle_inp[1::3], puzzle_inp[2::3]
        ):
            index += 1
            left = ast.literal_eval(left)
            right = ast.literal_eval(right)

            log.debug(f"{index}; Parsing L:{left}")
            log.debug(f"{index}; Parsing R:{right}")
            is_ordered = check_order(left, right)
            log.debug(f"{index}; Determined order status is {is_ordered}")
            if is_ordered == -1:
                sum_puzzle += index
                log.debug(f"{index}; Adding {index} to total, new total {sum_puzzle}")

        log.debug(f"Adding final answer of {sum_puzzle}")
        return sum_puzzle

    puzzle_inp = [ast.literal_eval(l) for l in puzzle_inp if l]

    puzzle_inp.append([[2]])
    puzzle_inp.append([[6]])

    puzzle_inp = sorted(puzzle_inp, key=cmp_to_key(check_order))

    return (puzzle_inp.index([[2]]) + 1) * (puzzle_inp.index([[6]]) + 1)


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
    assert solve_puzzle(PUZZLE_INPUT) == 4894


def test_examples_pt_b():
    assert solve_puzzle(EXAMPLE, False) == ANS_2


def test_pt_b():
    assert solve_puzzle(PUZZLE_INPUT, False) == 24180
