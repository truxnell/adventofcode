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
            return [s.strip() for s in self.raw.split()]

        return list(s for s in self.raw.split())

    def numbers(self):
        """return a list of numbers."""
        return [int(s) for s in self.raw.split()]

    def grid(self):
        """return a grid"""
        return [s.split() for s in self.raw.split()]

    def number_grid(self):
        """return a grid of numbers."""
        return [[int(n) for n in row] for row in self.raw.split()]
