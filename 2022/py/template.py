import argparse

from utils import AocdPuzzle

EXAMPLE = []
EXAMPLE_2 = []
YEAR = 2022
DAY = 1


def solve_puzzle(puzzle: str, part_a=True) -> int:

    pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=f"Advent of code for day {DAY}, December {YEAR}"
    )

    parser.add_argument("-s", "--solve", help="Submit solution", required=True)
    args = vars(parser.parse_args())

    print(f"Advent of code for day {DAY}, December {YEAR}\n")

    print("Part 1")
    answer_a = solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines())
    print(answer_a)

    # print("\nPart 2")
    # answer_a=solve_puzzle(AocdPuzzle(year=YEAR, day=DAY,part_a=False).lines())
    # print(answer_a)

    if args["solve"].lower() == "a":
        AocdPuzzle.submit_answer(answer_a, YEAR, DAY)
