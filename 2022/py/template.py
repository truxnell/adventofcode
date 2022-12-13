import argparse
import sys
from typing import List

from utils import AocdPuzzle

YEAR = 2022
DAY = 11

EXAMPLE = []
ANS_1 = 0
ANS_2 = 0


def solve_puzzle(puzzle: List[str], part_a=True) -> int:

    return True


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=f"Advent of code for day {DAY}, December {YEAR}"
    )

    parser.add_argument(
        "-p", "--part", help="Part A or B", required=True, choices=["a", "b"]
    )
    parser.add_argument(
        "-s", "--solve", help="Submit solution", required=False, action="store_true"
    )
    args = vars(parser.parse_args())

    if not args["part"]:
        parser.print_usage()
        sys.exit()

    print(f"Advent of code for day {DAY}, December {YEAR}\n")
    if args["part"] == "a":
        print("Example 1")

        answer = solve_puzzle(EXAMPLE)
        print(f"Returned: {answer}, solution {ANS_1}, Equality {answer==ANS_1}")

        print("\n Part 1")
        answer_a = solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines())
        print(answer_a)

        if args["solve"]:
            AocdPuzzle.submit_answer("", answer_a, YEAR, DAY)

    if args["part"] == "b":
        print("Example 2")

        answer = solve_puzzle(EXAMPLE, part_a=False)
        print(f"Returned: {answer}, solution {ANS_2}, Equality {answer==ANS_2}")

        print("\n Part 2")
        answer_b = solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines(), part_a=False)
        print(answer_b)

        if args["solve"]:
            AocdPuzzle.submit_answer("", answer_b, YEAR, DAY)
