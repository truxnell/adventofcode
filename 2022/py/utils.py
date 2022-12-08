from aocd import get_data


class AocdPuzzle:
    def __init__(self, year: int, day: int) -> None:
        if not year or not day:
            raise Exception("Missing day or year")
        self.raw = get_data(year=year, day=day)

    def text(self):
        """Yield stripped puzzle input for year, day"""
        yield [row.strip() for row in self.raw.split()]

    def lines(self, strip=False):
        """Yield a list of lines.  Stripped if strip=True"""
        if strip:
            yield [s.strip() for s in self.raw.split()]

        yield list(s for s in self.raw.split())

    def numbers(self):
        """Yield a list of numbers."""
        yield [int(s) for s in self.raw.split()]

    def grid(self):
        """Yield a grid of numbers."""
        yield [s.split() for s in self.raw.split()]

    def number_grid(self):
        """Yield a grid of numbers."""
        yield [[int(n) for n in row] for row in self.raw.split()]
