from utils import AocdPuzzle

EXAMPLE = [
    "R 4",
    "U 4",
    "L 3",
    "D 1",
    "R 4",
    "D 1",
    "L 5",
    "R 2",
]

YEAR = 2022
DAY = 8


class Rope:
    def __init__(self) -> None:

        self.head_x = 50
        self.head_y = 50
        self.tail_x = 50
        self.tail_y = 50

        self.visited = {f"{self.tail_x},{self.tail_y}": 1}

    def move(self, heading: str, count: int) -> None:

        for _ in range(0, count):
            if heading.upper() == "U":
                self.head_y -= 1

            if heading.upper() == "D":
                self.head_y += 1

            if heading.upper() == "L":
                self.head_x -= 1

            if heading.upper() == "R":
                self.head_x += 1

            self.update_tail()

    def update_tail(self) -> None:

        var_x = self.head_x - self.tail_x
        var_y = self.head_y - self.tail_y

        if abs(var_x) + abs(var_y) < 2:
            return
        if abs(var_x) == 2:
            var_x = var_x // 2
        elif abs(var_y) == 2:
            var_y = var_y // 2
        self.tail_x += var_x
        self.tail_y += var_y

        self.note_tail()

    def note_tail(self):

        self.visited[f"{self.tail_x},{self.tail_y}"] = 1

    def show_grid(self) -> None:

        print("Grid")
        lst = [["." for _ in range(0, 200)] for _ in range(0, 200)]

        lst[self.head_x][self.head_y] = "H"
        lst[self.tail_x][self.tail_y] = "T"

        for row in lst:
            print("".join(row))

    def count_visited(self) -> int:

        return len(self.visited)


def solve_puzzle(puzzle: str, part_a=True) -> int:

    rope = Rope()
    for move in puzzle:
        heading, count = move.split()
        rope.move(heading, int(count))
    return rope.count_visited()


if __name__ == "__main__":

    print(solve_puzzle(EXAMPLE))


def test_examples_pt_a():
    assert solve_puzzle(EXAMPLE) == 21


# def test_pt_a():
#     assert solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines()) == 1703
#
#
# def test_examples_pt_b():
#     assert solve_puzzle(EXAMPLE, False) == 8
#
#
# def test_pt_b():
#     assert solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines(), False) == 1792222
