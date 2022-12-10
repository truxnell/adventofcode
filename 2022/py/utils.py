# pylint: disable=W1401
import re

from aocd import get_data


class AocdPuzzle:
    def __init__(self, year: int, day: int) -> None:
        if not year or not day:
            raise Exception("Missing day or year")
        self.raw = get_data(year=year, day=day)

    def text(self):
        """return stripped puzzle input for year, day"""
        return [row.strip() for row in self.raw.split()]

    def lines(self, strip=False):
        """return a list of lines.  Stripped if strip=True"""
        if strip:
            return [s.strip() for s in self.raw.splitlines()]

        return list(s for s in self.raw.splitlines())

    def numbers(self):
        """return a list of numbers."""
        return [int(s) for s in self.raw.split()]

    def grid(self):
        """return a grid"""
        return [s.split() for s in self.raw.split()]

    def number_grid(self):
        """Return a grid of numbers."""
        return [[int(n) for n in row] for row in self.raw.split()]


def num_from_string(inp: str):
    """Extract numbers from a string"""
    return re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", inp)


def chunks(string: str, num: int) -> str:
    """Produce `num`-character chunks from `string`."""
    for i in range(0, len(string), num):
        yield string[i : i + num]
