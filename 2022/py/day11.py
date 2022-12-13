import argparse
import operator
import sys
from typing import List

from utils import AocdPuzzle, num_from_string

YEAR = 2022
DAY = 11
EXAMPLE = [
    "Monkey 0:",
    "  Starting items: 79, 98",
    "  Operation: new = old * 19",
    "  Test: divisible by 23",
    "    If true: throw to monkey 2",
    "    If false: throw to monkey 3",
    " ",
    "Monkey 1:",
    "  Starting items: 54, 65, 75, 74",
    "  Operation: new = old + 6",
    "  Test: divisible by 19",
    "    If true: throw to monkey 2",
    "    If false: throw to monkey 0",
    " ",
    "Monkey 2:",
    "  Starting items: 79, 60, 97",
    "  Operation: new = old * old",
    "  Test: divisible by 13",
    "    If true: throw to monkey 1",
    "    If false: throw to monkey 3",
    " ",
    "Monkey 3:",
    "  Starting items: 74",
    "  Operation: new = old + 3",
    "  Test: divisible by 17",
    "    If true: throw to monkey 0",
    "    If false: throw to monkey 1",
]
ANS_1 = 10605
ANS_2 = 2713310158


class Monkey:
    def __init__(
        self,
        starting_items: List[int],
        op: str,
        op_num: int,
        test_num: int,
        if_true: int,
        if_false: int,
        worry: int,
    ) -> None:
        ops = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
        }
        self.items = starting_items
        self.op = ops[op]  # Store the py math function call as the op
        self.op_num = op_num
        self.test_num = test_num
        self.if_true = if_true
        self.if_false = if_false
        self.inspect_count = 0
        self.worry = worry

    def inspect(self):

        self.items = [
            self.op(item, item) // self.worry
            if self.op_num == "old"
            else self.op(item, int(self.op_num)) // self.worry
            for item in self.items
        ]
        self.inspect_count += len(self.items)

    def yeet(self):
        return self.items.pop(0)


class MonkeyBusiness:
    def __init__(self) -> None:
        self.monkeys = []

    def load_puzzle(self, puzzle: List[str], worry) -> None:

        self.supermod = 1
        while len(puzzle) > 5:
            puzzle.pop(0)
            starting_items = num_from_string(puzzle.pop(0))
            _, _, _, _, op, op_num = puzzle.pop(0).split()
            test_num = num_from_string(puzzle.pop(0))[0]
            if_true = num_from_string(puzzle.pop(0))[0]
            if_false = num_from_string(puzzle.pop(0))[0]
            self.monkeys.append(
                Monkey(starting_items, op, op_num, test_num, if_true, if_false, worry)
            )
            if len(puzzle) > 0:
                puzzle.pop(0)
            self.supermod *= test_num

    def cycle(self):

        for monkey in self.monkeys:
            if len(monkey.items):
                monkey.inspect()
                for _ in range(len(monkey.items)):
                    item = monkey.yeet()
                    item %= self.supermod
                    if item % monkey.test_num:
                        # not divisible
                        self.monkeys[monkey.if_false].items.append(item)
                    else:
                        # divisible
                        self.monkeys[monkey.if_true].items.append(item)

    def mul_top_two(self) -> int:
        lst = []
        for monkey in self.monkeys:
            lst.append(monkey.inspect_count)
        lst.sort(reverse=True)
        return lst[0] * lst[1]


def solve_puzzle(puzzle: str, part_a=True) -> int:

    monkey_business = MonkeyBusiness()
    monkey_business.load_puzzle(puzzle, (3 if part_a else 1))

    cycles = 20 if part_a else 10000
    for i in range(cycles):
        monkey_business.cycle()

    return monkey_business.mul_top_two()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=f"Advent of code for day {DAY}, December {YEAR}"
    )

    parser.add_argument(
        "-p", "--part", help="Part A or B", required=True, choices=["a", "b"]
    )
    parser.add_argument(
        "-s", "--solve", help="Submit solution", required=False, action="store_true"
    )
    args = vars(parser.parse_args())

    if not args["part"]:
        parser.print_usage()
        sys.exit()

    print(f"Advent of code for day {DAY}, December {YEAR}\n")
    if args["part"] == "a":
        print("Example 1")

        answer = solve_puzzle(EXAMPLE)
        print(f"Returned: {answer}, solution {ANS_1}, Equality {answer==ANS_1}")

        print("\n Part 1")
        answer_a = solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines())
        print(answer_a)

        if args["solve"]:
            AocdPuzzle.submit_answer("", answer_a, YEAR, DAY)

    if args["part"] == "b":
        print("Example 2")

        answer = solve_puzzle(EXAMPLE, part_a=False)
        print(f"Returned: {answer}, solution {ANS_2}, Equality {answer==ANS_2}")

        print("\n Part 2")
        answer_b = solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines(), part_a=False)
        print(answer_b)

        if args["solve"]:
            AocdPuzzle.submit_answer("", answer_b, YEAR, DAY)


def test_examples_pt_a():
    assert solve_puzzle(EXAMPLE) == 10605


def test_pt_a():
    assert solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines()) == 55930


def test_examples_pt_b():
    assert solve_puzzle(EXAMPLE, False) == 0


def test_pt_b():
    assert solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines(), False) == 14636993466
