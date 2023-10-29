# pylint: disable=W1401
import logging
import math
import re
import sys
from math import copysign
from typing import Any, Generator, List, Union

import aocd
from PIL import Image, ImageDraw


class AocdPuzzle:
    def __init__(self, year: int, day: int) -> None:
        if not year or not day:
            raise Exception("Missing day or year")
        self.raw = aocd.get_data(year=year, day=day)

    def lines(self, strip=False):
        """return a list of lines.  Stripped if strip=True"""
        if strip:
            return [s.strip() for s in self.raw.splitlines()]

        return list(s for s in self.raw.splitlines())

    def numbers(self):
        """return a list of numbers."""
        return [int(s) for s in self.raw.split()]

    def grid(self) -> List[List[str]]:
        """return a grid"""
        return [list(s) for s in self.raw.split()]

    def grid_value_from_str(self, a_is_one=True) -> List[List[int]]:
        """return a grid"""
        return [[chr_to_value(c, a_is_one) for c in s] for s in self.raw.split()]

    def number_grid(self):
        """Return a grid of numbers."""
        return [[int(n) for n in row] for row in self.raw.split()]

    def submit_answer(self, answer, year: int, day: int) -> str:
        """Submit an answer for a year/day"""
        return aocd.submit(answer, day=day, year=year)

    def extracted_numbers(self) -> List[List[int]]:
        """Return a list of numbers extracted from string"""
        return [
            [
                int(i)
                for i in re.findall(
                    r"[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", l
                )
            ]
            for l in self.raw.splitlines()
        ]


def num_from_string(string: str):
    """
    Extract numbers from a string
    >>> num_from_string("200 units of 67")
    [200, 67]
    """
    return [
        int(i)
        for i in re.findall(
            r"[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", string
        )
    ]


def chunks(string: str, num: int) -> Generator:
    """
    Produce `num`-character chunks from `string`.
    >>> list(chunks("abcdefghi",3))
    ['abc', 'def', 'ghi']
    """
    for i in range(0, len(string), num):
        yield string[i : i + num]


def chr_to_value(string: str, a_is_one: bool = True) -> int:
    """
    Yield a list of values from a string
    [Aa]=1 - [zZ]=26 (a_is_one=True, default)
    [Aa]=0 - [zZ]=25 (a_is_on=False)

    >>> chr_to_value("a")
    1
    >>> chr_to_value("z")
    26
    """
    return ord(string) - ord("a") + a_is_one


def value_to_str(integer: int, a_is_one: bool = True) -> str:
    """
    Yield a list of strings from a List of numbers
    [Aa]=1 - [zZ]=26 (a_is_one=True, default)
    [Aa]=0 - [zZ]=25 (a_is_on=False)

    >>> value_to_str(1)
    'a'
    """
    return chr(integer + ord("a") - a_is_one)


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.formats = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logging(level: str):

    log = logging.getLogger(__name__)
    log.propagate = False

    fmt = "%(asctime)s | %(levelname)8s | %(message)s"

    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter(fmt))

    file_handler = logging.FileHandler(f"{sys.argv[0]}.log")
    file_handler.setLevel(logging.DEBUG)

    # logging.basicConfig(level=level)

    log.addHandler(stdout_handler)
    log.addHandler(file_handler)
    log.debug("Logging setup")

    levels: dict = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warn": logging.WARNING,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    }

    if level is None:
        raise ValueError(
            f"log level given: {level}"
            f" -- must be one of: {' | '.join(levels.keys())}"
        )

    log.setLevel(logging.DEBUG)

    return log


def irange(start: int, end: int, step=1):
    """
    Returns a range between start and end with step
    Intelligently deciding if step needs to be +ve/-ve
    >>> list(irange(10,0))
    [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    >>> list(irange(1,10))
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    return range(int(start), int(end), int(copysign(step, end - start)))


class DrawGrid:
    def __init__(
        self,
        matrix: List[List],
        cell_width: int,
        cell_height: int,
        bg_colour: int = 255,
        grid: bool = False,
        grid_colour: int = 128,
    ) -> None:

        self.matrix = matrix
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.bg_colour = bg_colour
        self.grid = grid
        self.grid_colour = grid_colour
        self.matrix_width = len(matrix[0])
        self.matrix_height = len(matrix)
        self.width = len(matrix[0]) * self.cell_width
        self.height = len(matrix) * self.cell_height

        self.image = Image.new(mode="L", size=(self.width, self.height), color=255)
        if grid:
            self.draw_grid()
        self.draw_cells()

    def draw_cells(self):

        draw = ImageDraw.Draw(self.image)
        for x in range(0, self.matrix_height):
            for y in range(0, self.matrix_width):
                if self.matrix[x][y] > 0:
                    cell = (
                        (
                            x * self.cell_height + self.grid,
                            y * self.cell_width + self.grid,
                        ),
                        (
                            (x + 1) * self.cell_height - self.grid,
                            (y + 1) * self.cell_width - self.grid,
                        ),
                    )
                    draw.rectangle(cell, fill=self.grid_colour)
                self.image.show()
                input()
        del draw

    def draw_grid(self):

        draw = ImageDraw.Draw(self.image)
        for x in range(0, self.height, self.cell_height):
            line = ((x, 0), (x, self.height))
            draw.line(line, fill=self.grid_colour)

        for y in range(0, self.width, self.cell_width):
            line = ((0, y), (self.width, y))
            draw.line(line, fill=self.grid_colour)

        del draw

    def show_image(self):
        self.image.show()


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def manhattan_distance(self, tuple_or_coord) -> int:
        """
        Calculate Manhattan distance between two points
        """
        if isinstance(tuple_or_coord, tuple):
            x, y = tuple_or_coord
        else:
            x, y = (tuple_or_coord.x, tuple_or_coord.y)
        return abs(self.x - x) + abs(self.y - y)

    def distance_to_origin(self):
        """Calculate the distance of the point from the origin (0, 0)."""
        return ((self.x**2) + (self.y**2)) ** 0.5

    def distance_to_point(self, other):
        """Calculate the distance between two points."""
        dx = other.x - self.x
        dy = other.y - self.y
        return ((dx**2) + (dy**2)) ** 0.5

    def midpoint(self, other):
        """Calculate the midpoint between two points."""
        x = (self.x + other.x) / 2
        y = (self.y + other.y) / 2
        return Point(x, y)

    def __str__(self):
        """Return a string representation of the point."""
        return f"({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        """Check if two Points are equal"""
        return self.x==other.x and self.y==other.y


class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def intersection(self, other):
        """Find the intersection of two lines."""
        x1, y1 = self.start.x, self.start.y
        x2, y2 = self.end.x, self.end.y
        x3, y3 = other.start.x, other.start.y
        x4, y4 = other.end.x, other.end.y

        # calculate the intersection using the line equation
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None  # the lines are parallel
        x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
        y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
        return Point(x, y)

    def length(self):
        """Calculate the length of the line."""
        dx = self.start.x - self.end.x
        dy = self.start.y - self.end.y
        return ((dx**2) + (dy**2)) ** 0.5

    def slope(self):
        """Calculate the slope of the line."""
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        return dy / dx

    def y_intercept(self):
        """Calculate the y-intercept of the line."""
        m = self.slope()
        b = self.start.y - m * self.start.x
        return b

    def is_horizontal(self):
        """Determine if the line is horizontal."""
        return self.start.y == self.end.y

    def is_vertical(self):
        """Determine if the line is vertical."""
        return self.start.x == self.end.x

    def __str__(self):
        """Return a string representation of the circle."""
        return (
            f"Line(start={self.start.x},{self.start.y}, end{self.end.x},{self.end.y})"
        )


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def area(self):
        """Calculate the area of the circle."""
        return math.pi * self.radius**2

    def circumference(self):
        """Calculate the circumference of the circle."""
        return 2 * math.pi * self.radius

    def is_inside(self, point):
        """Determine if a point is inside the circle."""
        return self.center.distance_to_point(point) < self.radius

    def __str__(self):
        """Return a string representation of the circle."""
        return f"Circle(center={self.center}, radius={self.radius})"


class Grid:
    def __init__(
        self, height: int, width: int, x: int = 0, y: int = 0, fill: int = 0
    ) -> None:
        self.height: int = height
        self.width: int = width
        self.fill: int = fill
        self.grid: List[List] = [
            [self.fill for _ in range(self.width)] for _ in range(self.height)
        ]

    def get(self, tuple_or_coord: Union[tuple, Point]) -> Any:
        if isinstance(tuple_or_coord, tuple):
            return self.grid[tuple_or_coord[0]][tuple_or_coord[1]]
        return self.grid[tuple_or_coord.x][tuple_or_coord.y]

    def set(self, tuple_or_coord: Union[tuple, Point], item: Any):
        if isinstance(tuple_or_coord, tuple):
            self.grid[tuple_or_coord[0]][tuple_or_coord[1]] = item
        else:
            self.grid[tuple_or_coord.x][tuple_or_coord.y] = item

    def draw_circle(
        self,
        x: int,
        y: int,
        radius: int,
        border_item: Any,
        filled=False,
        fill_item: Any = "",
    ):
        # Bresenham algorithm
        x_pos = -radius
        y_pos = 0
        err = 2 - 2 * radius
        if x >= self.width or y >= self.height:
            return
        while True:
            if filled:
                self.draw_horizontal_line(
                    x + x_pos, y + y_pos, 2 * (-x_pos) + 1, fill_item
                )
                self.draw_horizontal_line(
                    x + x_pos, y - y_pos, 2 * (-x_pos) + 1, fill_item
                )
            self.set((x - x_pos, y + y_pos), border_item)
            self.set((x + x_pos, y + y_pos), border_item)
            self.set((x + x_pos, y - y_pos), border_item)
            self.set((x - x_pos, y - y_pos), border_item)
            e2 = err
            if e2 <= y_pos:
                y_pos += 1
                err += y_pos * 2 + 1
                if -x_pos == y_pos and e2 <= x_pos:
                    e2 = 0
            if e2 > x_pos:
                x_pos += 1
                err += x_pos * 2 + 1
            if x_pos > 0:
                break

    def draw_line(self, x0, y0, x1, y1, item):
        if y0 == y1:
            self.draw_horizontal_line(x0, y0, y0 - y1, item)
        if x0 == x1:
            self.draw_vertical_line(x0, y0, x0 - x1, item)

        # Bresenham algorithm
        # TODO: determine if straight line, fallthrough to faster algo
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while (x0 != x1) and (y0 != y1):
            self.set((x0, y0), item)
            if 2 * err >= dy:
                err += dy
                x0 += sx
            if 2 * err <= dx:
                err += dx
                y0 += sy

    def draw_horizontal_line(self, x, y, width, item):
        for i in irange(x, x + width):
            self.set((i, y), item)

    def draw_vertical_line(self, x, y, height, item):
        for i in irange(y, y + height):
            self.set((x, i), item)

    def grid2d_to_str(
        self,
        x_slice: int = 0,
        x_num: int = 0,
        y_slice: int = 0,
        y_num: int = 0,
    ):
        """
        Returns a 2d grid for pretty printing
        >>> _=[[1,2,3],[4,5,6],[7,8,9]]
        >>> grid2d_to_str(_)
        ['123', '456', '789']
        """
        ret_grid = []

        if not x_slice and not x_num:
            x_slice = 0
            x_num = len(self.grid)

        if not y_slice and not y_num:
            y_slice = 0
            y_num = len(self.grid[0])

        for row in self.grid[x_slice : x_slice + x_num]:
            line = ""
            for char in row[y_slice : y_slice + y_num]:
                line += str(char)
            ret_grid.append(line)

        return ret_grid

    def print(
        self,
        x_slice: int = 0,
        x_num: int = 0,
        y_slice: int = 0,
        y_num: int = 0,
    ):

        for line in self.grid2d_to_str(x_slice, x_num, y_slice, y_num):
            print(line)


def grid2d_to_str(
    grid,
    x_slice: int = 0,
    x_num: int = 0,
    y_slice: int = 0,
    y_num: int = 0,
):
    """
    Returns a 2d grid for pretty printing
    >>> _=[[1,2,3],[4,5,6],[7,8,9]]
    >>> grid2d_to_str(_)
    ['123', '456', '789']
    """
    ret_grid = []

    if not x_slice and not x_num:
        x_slice = 0
        x_num = len(grid)

    if not y_slice and not y_num:
        y_slice = 0
        y_num = len(grid[0])

    for row in grid[x_slice : x_slice + x_num]:
        line = ""
        for char in row[y_slice : y_slice + y_num]:
            line += str(char)
        ret_grid.append(line)

    return ret_grid


class AOCTextUtils:
    @staticmethod
    def split_words(text: str) -> List[str]:
        """Splits a string into a list of words."""
        return text.split()

    @staticmethod
    def split_lines(text: str) -> List[str]:
        """Splits a string into a list of lines."""
        return text.strip().split("\n")

    @staticmethod
    def split_csv(text: str) -> List[List[str]]:
        """Splits a CSV string into a list of lists of strings."""
        lines = AOCTextUtils.split_lines(text)
        return [line.split(",") for line in lines]

    @staticmethod
    def split_tsv(text: str) -> List[List[str]]:
        """Splits a TSV string into a list of lists of strings."""
        lines = AOCTextUtils.split_lines(text)
        return [line.split("\t") for line in lines]

    @staticmethod
    def count_occurrences(text: str, substring: str) -> int:
        """Counts the number of occurrences of a substring in a string."""
        return text.count(substring)

    @staticmethod
    def find_all_occurrences(text: str, substring: str) -> List[int]:
        """Finds all occurrences of a substring in a string and returns a list of their indices."""
        return [
            i for i in range(len(text)) if text[i : i + len(substring)] == substring
        ]

    @staticmethod
    def is_palindrome(text: str) -> bool:
        """Returns True if a string is a palindrome, False otherwise."""
        return text == text[::-1]

    @staticmethod
    def reverse_string(text: str) -> str:
        """Reverses a string."""
        return text[::-1]

    @staticmethod
    def sort_string(text: str) -> str:
        """Sorts the characters in a string in alphabetical order."""
        return "".join(sorted(text))

    @staticmethod
    def get_anagrams(text: str, words: List[str]) -> List[str]:
        """Returns a list of words that are anagrams of the input string."""
        sorted_text = AOCTextUtils.sort_string(text)
        return [word for word in words if AOCTextUtils.sort_string(word) == sorted_text]


from typing import Tuple


class AOCCartesianUtils:
    @staticmethod
    def distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
        """Returns the Euclidean distance between two points."""
        x1, y1 = p1
        x2, y2 = p2
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    @staticmethod
    def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
        """Returns the Manhattan distance between two points."""
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def get_neighbors(point: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Returns the four neighboring points of a given point."""
        x, y = point
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    @staticmethod
    def get_diagonal_neighbors(point: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Returns the four diagonal neighboring points of a given point."""
        x, y = point
        return [(x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1), (x - 1, y - 1)]

    @staticmethod
    def get_points_in_radius(
        point: Tuple[int, int], radius: int
    ) -> List[Tuple[int, int]]:
        """Returns the points within a given radius of a given point."""
        points = []
        for x in range(point[0] - radius, point[0] + radius + 1):
            for y in range(point[1] - radius, point[1] + radius + 1):
                points.append((x, y))
        return points


from typing import List, Tuple


class AOCMathUtils:
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Returns the greatest common divisor of two numbers using the Euclidean algorithm."""
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Returns the least common multiple of two numbers."""
        return abs(a * b) // AOCMathUtils.gcd(a, b)

    @staticmethod
    def is_prime(n: int) -> bool:
        """Returns True if a number is prime, False otherwise."""
        if n in [2, 3]:
            return True
        if n == 1 or n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def get_factors(n: int) -> List[int]:
        """Returns the factors of a number."""
        return [i for i in range(1, n + 1) if n % i == 0]

    @staticmethod
    def get_divisors(n: int) -> List[int]:
        """Returns the divisors of a number."""
        factors = AOCMathUtils.get_factors(n)
        divisors = []
        for i in range(1, len(factors)):
            for j in range(i, len(factors)):
                divisors.append(factors[i] * factors[j])
        return divisors

    @staticmethod
    def is_square(n: int) -> bool:
        """Returns True if a number is a perfect square, False otherwise."""
        return int(n**0.5) ** 2 == n

    @staticmethod
    def prime_factorization(n: int) -> List[int]:
        """Returns the prime factorization of a number as a list of prime factors."""
        factors = []
        while n % 2 == 0:
            factors.append(2)
            n = n // 2
        for i in range(3, int(n**0.5) + 1, 2):
            while n % i == 0:
                factors.append(i)
                n = n // i
        if n > 2:
            factors.append(n)
        return factors

    @staticmethod
    def get_prime_numbers(n: int) -> List[int]:
        """Returns a list of the first n prime numbers."""
        primes = []
        i = 2
        while len(primes) < n:
            if AOCMathUtils.is_prime(i):
                primes.append(i)
            i += 1
        return primes

    @staticmethod
    def get_combinations(items: List[int], r: int) -> List[Tuple[int, ...]]:
        """Returns a list of all r-length combinations of elements in items."""
        items = list(items)
        combinations = []
        if r > len(items):
            return combinations
        items.sort()

        def _combinations(items, r, start, current):
            if r == 0:
                combinations.append(tuple(current))
                return
            for i in range(start, len(items)):
                current.append(items[i])
                _combinations(items, r - 1, i + 1, current)
                current.pop()

        _combinations(items, r, 0, [])
        return combinations


import hashlib
import zlib


class AOCStringUtils:
    @staticmethod
    def reverse_string(s: str) -> str:
        """Returns the reverse of a string."""
        return s[::-1]

    @staticmethod
    def is_palindrome(s: str) -> bool:
        """Returns True if a string is a palindrome, False otherwise."""
        return s == AOCStringUtils.reverse_string(s)

    @staticmethod
    def get_substrings(s: str) -> List[str]:
        """Returns a list of all substrings of a string."""
        substrings = []
        for i in range(len(s)):
            for j in range(i + 1, len(s) + 1):
                substrings.append(s[i:j])
        return substrings

    @staticmethod
    def get_anagrams(s: str) -> List[str]:
        """Returns a list of all anagrams of a string."""

        def _get_anagrams(s: str, current: str, used: List[bool]) -> None:
            if len(current) == len(s):
                anagrams.append(current)
                return
            for i in range(len(s)):
                if used[i]:
                    continue
                used[i] = True
                _get_anagrams(s, current + s[i], used)
                used[i] = False

        anagrams = []
        _get_anagrams(s, "", [False] * len(s))
        return anagrams

    @staticmethod
    def count_substring(s: str, sub: str) -> int:
        """Returns the number of occurrences of a substring in a string."""
        return s.count(sub)

    @staticmethod
    def get_hash(s: str, hash_type: str) -> str:
        """Returns the hash of a string using the specified hash function."""
        if hash_type == "md5":
            return hashlib.md5(s.encode()).hexdigest()
        elif hash_type == "sha1":
            return hashlib.sha1(s.encode()).hexdigest()
        elif hash_type == "sha256":
            return hashlib.sha256(s.encode()).hexdigest()
        elif hash_type == "sha512":
            return hashlib.sha512(s.encode()).hexdigest()
        else:
            raise ValueError(f"Invalid hash type: {hash_type}")

    @staticmethod
    def compress(s: str) -> bytes:
        """Compresses a string using zlib."""
        return zlib.compress(s.encode())

    @staticmethod
    def decompress(b: bytes) -> str:
        """Decompresses a string compressed using zlib."""
        return zlib.decompress(b).decode()
