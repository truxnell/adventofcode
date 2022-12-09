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
EXAMPLE_2 = [
    "R 5",
    "U 8",
    "L 8",
    "D 3",
    "R 17",
    "D 10",
    "L 25",
    "U 20",
]
YEAR = 2022
DAY = 9


class Rope:
    def __init__(self, num_tails: int) -> None:

        self.head_x = 50
        self.head_y = 50
        self.num_tails = num_tails - 1
        self.tails = {}
        for tail in range(num_tails):
            self.tails[tail] = {"x": 50, "y": 50}
        self.visited = {
            f"{self.tails[self.num_tails]['x']},{self.tails[self.num_tails]['y']}": 1
        }

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
        # self.show_grid()

    def update_tail(self) -> None:

        for tail in range(self.num_tails + 1):
            if tail == 0:

                var_x = self.head_x - self.tails[tail]["x"]
                var_y = self.head_y - self.tails[tail]["y"]
            else:

                var_x = self.tails[tail - 1]["x"] - self.tails[tail]["x"]
                var_y = self.tails[tail - 1]["y"] - self.tails[tail]["y"]

            if abs(var_x) <= 1 and abs(var_y) <= 1:
                continue
            if abs(var_x) == 2:
                var_x = var_x // 2
            if abs(var_y) == 2:
                var_y = var_y // 2
            self.tails[tail]["x"] += var_x
            self.tails[tail]["y"] += var_y

        self.note_tail()
        # self.show_grid()

    def note_tail(self):

        self.visited[
            f"{self.tails[self.num_tails]['x']},{self.tails[self.num_tails]['y']}"
        ] = 1

    def show_grid(self) -> None:

        print("Grid")
        lst = [["." for _ in range(0, 100)] for _ in range(0, 100)]

        for key in self.visited:
            x, y = key.split(",")
            lst[int(y)][int(x)] = "#"
        lst[self.head_y][self.head_x] = "H"

        for tail in range(self.num_tails + 1):
            lst[self.tails[tail]["y"]][self.tails[tail]["x"]] = str(tail)

        for row in lst:
            print("".join(row))
        input()

    def count_visited(self) -> int:

        return len(self.visited)


def solve_puzzle(puzzle: str, part_a=True) -> int:

    if part_a:
        rope = Rope(num_tails=1)
    else:
        rope = Rope(num_tails=9)

    for move in puzzle:
        heading, count = move.split()
        rope.move(heading, int(count))
    return rope.count_visited()


if __name__ == "__main__":

    print(solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines(), part_a=False))


def test_examples_pt_a():
    assert solve_puzzle(EXAMPLE) == 13


def test_pt_a():
    assert solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines()) == 6464


def test_examples_pt_b():
    assert solve_puzzle(EXAMPLE, False) == 1


def test_examples_pt_b_2():
    assert solve_puzzle(EXAMPLE_2, False) == 36


#
#
# def test_pt_b():
#     assert solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines(), False) == 1792222
