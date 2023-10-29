import argparse
from itertools import combinations

from tqdm import tqdm
from utils import AocdPuzzle, Line, Point, num_from_string, setup_logging
from typing import List

YEAR: int = 2022
DAY: int = 15

EXAMPLE = [
    "Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
    "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
    "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
    "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
    "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
    "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
    "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
    "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
    "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
    "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
    "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
    "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
    "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
    "Sensor at x=20, y=1: closest beacon is at x=15, y=3",
]
ANS_1: int = 26
ANS_1_ROW: int = 10
PT_A_ROW: int = 2000000
ANS_2: int = 56000011
PUZZLE = AocdPuzzle(year=YEAR, day=DAY)
PUZZLE_INPUT = PUZZLE.extracted_numbers()
EXAMPLE = [num_from_string(l) for l in EXAMPLE]

log = setup_logging("debug")


def solve_puzzle(puzzle_inp: List, search_row: int, part_a=True) -> int:

    if part_a:
        for line in puzzle_inp:
            dist = Point(line[0], line[1]).manhattan_distance((line[2], line[3]))
            line.append(dist)
            # log.debug(f"{line[0]},{line[1]} distance to {line[2]},{line[3]} is {dist}")

        lowest_y = 0
        highest_y = 0

        for line in puzzle_inp:
            dist = line[1] + line[4] + 1
            if dist > highest_y:
                highest_y = dist
            dist = line[1] - line[4] - 1
            if dist < lowest_y:
                lowest_y = dist

        count = 0
        brk = False
        log.debug(f"Searching y={search_row}")
        for col in tqdm(range(lowest_y, highest_y)):
            for beacons in puzzle_inp:
                if search_row == beacons[3] and col == beacons[2]:
                    brk = True
                    break
            if brk:
                brk = False
                continue
            for sensors in puzzle_inp:
                dist = Point(col, search_row).manhattan_distance(
                    ((sensors[0], sensors[1]))
                )
                if dist <= sensors[4]:
                    count += 1
                    break
        return count

    log.info("Searching for distress beacon")
    for line in puzzle_inp:
        dist = Point(line[0], line[1]).manhattan_distance((line[2], line[3]))
        line.append(dist)
    alines = []
    blines = []
    max_x = 0
    max_y = 0
    for x, y, _, _, d in tqdm(puzzle_inp):
        alines.append(Line(Point(x + d + 1, y), Point(x, y + d + 1)))  # /
        blines.append(Line(Point(x + d + 1, y), Point(x, y - d - 1)))  # \
        blines.append(Line(Point(x - d - 1, y), Point(x, y + d + 1)))  # \
        alines.append(Line(Point(x - d - 1, y), Point(x, y - d - 1)))  # /

        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

        point = []
        for line1, line2 in [(a, b) for a in alines for b in blines]:
            intersect = line1.intersection(line2)
            if intersect:
                if (
                    intersect.x.is_integer()
                    and intersect.y.is_integer()
                    and intersect.x <= max_x
                    and intersect.x >= 0
                    and intersect.y <= max_y
                    and intersect.y >= 0
                ):
                    if not intersect in point:
                        point.append(intersect)

    for pt in point:
        inside_range = False
        for sensors in puzzle_inp:
            dist = Point(pt.x, pt.y).manhattan_distance((sensors[0], sensors[1]))
            if dist <= sensors[4]:
                inside_range = True
        if not inside_range:
            return int(pt.x * 4_000_000 + pt.y)

    log.error("Failed to find beacon :(.  RIP Elves")
    return -1


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

        answer = solve_puzzle(EXAMPLE, ANS_1_ROW)
        print(f"Returned: {answer}, solution {ANS_1}, Equality {answer==ANS_1}")

        print("\nPart 1")
        answer_a = solve_puzzle(PUZZLE_INPUT, PT_A_ROW)
        print(answer_a)

        if args["solve"]:
            PUZZLE.submit_answer(answer_a, YEAR, DAY)

    if args["part"] == "b" or not args["part"]:
        print("Example 2")

        answer = solve_puzzle(EXAMPLE, 0, part_a=False)
        print(f"Returned: {answer}, solution {ANS_2}, Equality {answer==ANS_2}")

        print("\nPart 2")
        answer_b = solve_puzzle(PUZZLE_INPUT, 0, part_a=False)
        print(answer_b)

        if args["solve"]:
            PUZZLE.submit_answer(answer_b, YEAR, DAY)


def test_examples_pt_a():
    assert solve_puzzle(EXAMPLE, ANS_1_ROW) == ANS_1


def test_pt_a():
    assert solve_puzzle(PUZZLE_INPUT, PT_A_ROW) == 5846122


def test_examples_pt_b():
    assert solve_puzzle(EXAMPLE, 0, False) == ANS_2


def test_pt_b():
    assert solve_puzzle(PUZZLE_INPUT, 0, False) == 0
