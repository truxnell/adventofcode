import argparse
import os
from re import A
from typing import List, Optional, Tuple

from utils import AocdPuzzle, grid2d_to_str, irange, setup_logging

YEAR: int = 2022
DAY: int = 14

EXAMPLE = [
    "498,4 -> 498,6 -> 496,6",
    "503,4 -> 502,4 -> 502,9 -> 494,9",
]
ANS_1: int = 24
ANS_2: int = 93
PUZZLE = AocdPuzzle(year=YEAR, day=DAY)
PUZZLE_INPUT = PUZZLE.lines()

log = setup_logging("debug")


class SandSpawner:
    def __init__(self, x: int, y: int, grid: List[List]) -> None:
        self.x: int = x
        self.y: int = y
        self.repr: str = "$"


class Sand:
    def __init__(self, grid: List[List], x: int, y: int) -> None:

        self.x = x
        self.y = y
        self.repr = "O"
        grid[x][y] = self.repr

    def update(self, grid: List[List]) -> bool:

        if not self.check_cell_occupied(grid, self.x + 1, self.y):
            self.move(grid, self.x, self.y, self.x + 1, self.y)
            return True

        if not self.check_cell_occupied(grid, self.x + 1, self.y - 1):
            self.move(grid, self.x, self.y, self.x + 1, self.y - 1)
            return True

        if not self.check_cell_occupied(grid, self.x + 1, self.y + 1):
            self.move(grid, self.x, self.y, self.x + 1, self.y + 1)
            return True

        return False

    def move(self, grid: List[List], x1: int, y1: int, x2: int, y2: int) -> None:
        grid[x1][y1] = "."
        grid[x2][y2] = self.repr
        self.x = x2
        self.y = y2

    def check_cell_occupied(self, grid: List[List], x: int, y: int) -> bool:
        if grid[x][y] == ".":
            return False
        return True


class FallingSand:
    def __init__(self) -> None:
        self.wall_repr: str = "#"
        self.air_repr: str = "."
        self.grid: List[List] = [
            [self.air_repr for _ in range(1000)] for _ in range(500)
        ]
        self.lowest_x: int = 0

    def parse_puzzle(self, puzzle: List[str]) -> None:
        for line in puzzle:
            current: Optional[Tuple] = None

            for coord in line.split(" -> "):
                ytmp, xtmp = coord.split(",")
                x: int = int(xtmp)
                y: int = int(ytmp)
                if x > self.lowest_x:
                    self.lowest_x = x
                self.grid[x][y] = self.wall_repr
                if not current:
                    current = (int(x), int(y))
                    continue

                if x == current[0]:
                    for y_new in irange(y, current[1]):
                        self.grid[x][y_new] = self.wall_repr

                else:
                    for x_new in irange(current[0], x):
                        self.grid[x_new][y] = self.wall_repr
                current = (int(x), int(y))

            self.lowest_x += 1

    def simulate(self) -> int:

        sand_spawner = (0, 500)
        sand_spawned = 0
        sand_inbounds = True

        while sand_inbounds:
            sand = Sand(self.grid, sand_spawner[0], sand_spawner[1])
            sand_spawned += 1
            sand_moving = True
            while sand_moving:
                sand_moving = sand.update(self.grid)
                if sand.x > self.lowest_x:
                    sand_inbounds = False
                    sand_moving = False
                # self.print(True)
                # input()
            if (sand.x, sand.y) == sand_spawner:
                sand_inbounds = False
                sand_moving = False
                sand_spawned += 1

        return sand_spawned - 1

    def print(self, clear: bool = False) -> None:
        if clear:
            os.system("cls" if os.name == "nt" else "clear")
        for line in grid2d_to_str(self.grid, 0, min(self.lowest_x, 150), 400, 200):
            print(line)


def solve_puzzle(puzzle_inp: List, part_a=True) -> int:

    if part_a:
        model = FallingSand()
        model.parse_puzzle(puzzle_inp)
        ret = model.simulate()
        model.print()

        return ret

    lowest_x: int = 0
    for line in puzzle_inp:
        for coord in line.split("->"):
            ytmp, xtmp = coord.split(",")
            x: int = int(xtmp)
            y: int = int(ytmp)
            if x > lowest_x:
                lowest_x = x

    puzzle_inp.append(f"0,{lowest_x+2} -> 900,{lowest_x+2}")

    model = FallingSand()

    model.parse_puzzle(puzzle_inp)
    ret = model.simulate()
    model.print()

    return ret


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
    assert solve_puzzle(PUZZLE_INPUT) == 838


def test_examples_pt_b():
    assert solve_puzzle(EXAMPLE, False) == ANS_2


def test_pt_b():
    assert solve_puzzle(PUZZLE_INPUT, False) == 0
