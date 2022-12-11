from day09 import DAY, EXAMPLE, EXAMPLE_2, YEAR, solve_puzzle
from utils import AocdPuzzle


def test_examples_pt_a():
    assert solve_puzzle(EXAMPLE) == 13


def test_pt_a():
    assert solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines()) == 6464


def test_examples_pt_b():
    assert solve_puzzle(EXAMPLE, False) == 1


def test_examples_pt_b_2():
    assert solve_puzzle(EXAMPLE_2, False) == 36
