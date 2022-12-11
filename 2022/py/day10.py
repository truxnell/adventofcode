import argparse
from typing import List

from utils import AocdPuzzle, chunks

EXAMPLE = [
    "addx 15",
    "addx -11",
    "addx 6",
    "addx -3",
    "addx 5",
    "addx -1",
    "addx -8",
    "addx 13",
    "addx 4",
    "noop",
    "addx -1",
    "addx 5",
    "addx -1",
    "addx 5",
    "addx -1",
    "addx 5",
    "addx -1",
    "addx 5",
    "addx -1",
    "addx -35",
    "addx 1",
    "addx 24",
    "addx -19",
    "addx 1",
    "addx 16",
    "addx -11",
    "noop",
    "noop",
    "addx 21",
    "addx -15",
    "noop",
    "noop",
    "addx -3",
    "addx 9",
    "addx 1",
    "addx -3",
    "addx 8",
    "addx 1",
    "addx 5",
    "noop",
    "noop",
    "noop",
    "noop",
    "noop",
    "addx -36",
    "noop",
    "addx 1",
    "addx 7",
    "noop",
    "noop",
    "noop",
    "addx 2",
    "addx 6",
    "noop",
    "noop",
    "noop",
    "noop",
    "noop",
    "addx 1",
    "noop",
    "noop",
    "addx 7",
    "addx 1",
    "noop",
    "addx -13",
    "addx 13",
    "addx 7",
    "noop",
    "addx 1",
    "addx -33",
    "noop",
    "noop",
    "noop",
    "addx 2",
    "noop",
    "noop",
    "noop",
    "addx 8",
    "noop",
    "addx -1",
    "addx 2",
    "addx 1",
    "noop",
    "addx 17",
    "addx -9",
    "addx 1",
    "addx 1",
    "addx -3",
    "addx 11",
    "noop",
    "noop",
    "addx 1",
    "noop",
    "addx 1",
    "noop",
    "noop",
    "addx -13",
    "addx -19",
    "addx 1",
    "addx 3",
    "addx 26",
    "addx -30",
    "addx 12",
    "addx -1",
    "addx 3",
    "addx 1",
    "noop",
    "noop",
    "noop",
    "addx -9",
    "addx 18",
    "addx 1",
    "addx 2",
    "noop",
    "noop",
    "addx 9",
    "noop",
    "noop",
    "noop",
    "addx -1",
    "addx 2",
    "addx -37",
    "addx 1",
    "addx 3",
    "noop",
    "addx 15",
    "addx -21",
    "addx 22",
    "addx -6",
    "addx 1",
    "noop",
    "addx 2",
    "addx 1",
    "noop",
    "addx -10",
    "noop",
    "noop",
    "addx 20",
    "addx 1",
    "addx 2",
    "addx 2",
    "addx -6",
    "addx -11",
    "noop",
    "noop",
    "noop",
]
EXAMPLE_2 = []
YEAR = 2022
DAY = 10


class Register:
    def __init__(self, cycle: int) -> None:

        self.value = 1
        self.cycle_speed = cycle
        self.ops = [0]

    def add_op(self, number: int) -> None:

        for _ in range(self.cycle_speed - 1):
            self.ops.append(0)
        self.ops.append(number)

    def cycle(self) -> None:
        if len(self.ops) > 0:
            self.value += self.ops.pop(0)


class CPU:
    def __init__(self) -> None:

        self.registers = {"x": Register(2)}
        self.clock = 0
        self.busy = 0
        self.program = []

    def __len__(self):
        return len(self.program)

    def load_program(self, program: List[str]) -> None:
        self.program = program
        self.cycle()

    def execute(self, op: str) -> None:

        if op == "noop":
            self.busy += 1

        operand = ""
        if " " in op:
            op, operand = op.split()

        if op[0:3].lower() == "add":
            self.registers[op[3]].add_op(int(operand))
            self.busy += 2

    def read_register(self, register: str):

        return self.registers[register].value

    def cycle(self) -> None:

        self.clock += 1
        if self.busy == 0:
            self.execute(self.program.pop(0))
        self.busy -= 1
        for register in self.registers.values():
            register.cycle()


def solve_puzzle(puzzle: str, part_a=True) -> int:
    """Solve an advent of code puzzle

    Args:
        puzzle (str): Puzzle input
        part_a (bool, optional): If we are solving part A or B. Defaults to True.

    Returns:
        int: Solution
    """
    cpu = CPU()
    cpu.load_program(puzzle)
    breaks = range(20, 2000, 40)

    total = 0
    lcd = ""
    while len(cpu):
        lcd_pos = cpu.clock - (40 * (cpu.clock // 40))
        if abs(cpu.read_register("x") - lcd_pos) <= 1:
            lcd += "#"
        else:
            lcd += "."
        if cpu.clock in breaks:
            total += cpu.clock * cpu.read_register("x")
        print(f"{cpu.clock} - {cpu.read_register('x')} - {total}")
        cpu.cycle()

    if part_a:
        return total
    return lcd


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=f"Advent of code for day {DAY}, December {YEAR}"
    )

    # lcd_disp = solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines(), part_a=False)
    lcd_disp = solve_puzzle(EXAMPLE, part_a=True)

    for chunk in chunks(lcd_disp, 40):
        print(chunk)

    solve_puzzle()


def test_examples_pt_a():
    assert solve_puzzle(EXAMPLE) == 13140


def test_pt_a():
    assert solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines()) == 13180

def test_a():
    assert solve_puzzle

#
#
# def test_examples_pt_b():
#     assert solve_puzzle(EXAMPLE, False) == 0
#
#
# def test_pt_b():
#     assert solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines(), False) == 0
