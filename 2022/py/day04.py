from typing import List


def day04a(jobs: List, alternate=False):

    count = 0
    for job in jobs:

        job1, job2 = job.split(",")
        job1 = set(mixrange(job1))
        job2 = set(mixrange(job2))

        if not alternate:
            if job1.issubset(job2) or job2.issubset(job1):
                count += 1
        else:
            if list(job1&job2):
                count += 1

    return count


def char_find_in_strings(char: str, strings: List) -> bool:

    if len(strings) == 1:

        return char in strings[0]

    if char in strings[0]:
        return char_find_in_strings(char, strings[1:])

    return False


def string_split_half(string: str) -> str:

    string1, string2 = string[: len(string) // 2], string[len(string) // 2 :]

    return string1, string2


def mixrange(string: str) -> List:
    """Decode number ranges into a range() object"""
    rng = []
    for i in string.split(","):
        if "-" not in i:
            rng.append(int(i))
        else:
            lll, hhh = map(int, i.split("-"))
            rng += range(lll, hhh + 1)
    return rng


ex = [
    "2-4,6-8",
    "2-3,4-5",
    "5-7,7-9",
    "2-8,3-7",
    "6-6,4-6",
    "2-6,4-8",
]


def test_04_ex1a():
    assert day04a(ex) == 2


def test_04_ex1b():
    assert day04a(ex,True) == 4

def test_04a(day04_lines):
    assert day04a(day04_lines) == 576


def test_04b(day04_lines):
    assert day04a(day04_lines,True) == 905
