from aocd import get_data


def day06(signal: str, length=4) -> int:

    return [
        i
        for i in range(0, len(signal) - length)
        if len(set(signal[i : i + length])) == length
    ][0] + length


ex = "bvwbjplbgvbhsrlpgdmjqwftvncz"
ex2 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"


def test_06_ex1a():
    assert day06(ex) == 5


def test_06_ex1b():
    inp = get_data(day=6, year=2022)
    assert day06(inp) == 1702


def test_06_ex2a():
    assert day06(ex2, length=14) == 19


def test_06_ex2b():
    inp = get_data(day=6, year=2022)
    assert day06(inp, length=14) == 3559
