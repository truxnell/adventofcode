from aocd import get_data

EXAMPLE = []
YEAR = 2022
DAY = 7


def solve_puzzle(puzzle: str, part_a=True) -> int:

    pass


def test_examples_pt_a():
    assert solve_puzzle(EXAMPLE) == 5


def test_pt_a():
    inp = get_data(day=DAY, year=YEAR)
    assert solve_puzzle(inp) == 0
