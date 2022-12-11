from day11 import DAY, EXAMPLE, YEAR, solve_puzzle
from utils import AocdPuzzle


def test_examples_pt_a():
    assert solve_puzzle(EXAMPLE) == 0


#
# def test_pt_a():
#     assert solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines()) == 0
#
#
# def test_examples_pt_b():
#     assert solve_puzzle(EXAMPLE, False) == 0
#
#
# def test_pt_b():
#     assert solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines(), False) == 0
