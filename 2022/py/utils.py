# pylint: disable=W1401
import logging
import re
import sys
from typing import Generator, List

import aocd


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
