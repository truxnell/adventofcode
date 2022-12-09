from utils import AocdPuzzle

EXAMPLE = [
    "30373",
    "25512",
    "65332",
    "33549",
    "35390",
]

YEAR = 2022
DAY = 8


class Forest:
    def __init__(self, forest) -> None:

        self.forest = forest
        self.length = len(forest[0])
        self.height = len(forest)

    def is_visible(self, tree_x, tree_y) -> bool:

        tree_height = self.forest[tree_x][tree_y]
        count = 0
        for search_x in range(tree_x - 1, -1, -1):
            if self.forest[search_x][tree_y] >= tree_height:
                count += 1
                break
        for search_x in range(tree_x + 1, self.height):
            if self.forest[search_x][tree_y] >= tree_height:
                count += 1
                break

        for search_y in range(tree_y - 1, -1, -1):
            if self.forest[tree_x][search_y] >= tree_height:
                count += 1
                break

        for search_y in range(tree_y + 1, self.length):
            if self.forest[tree_x][search_y] >= tree_height:
                count += 1
                break
        if count == 4:
            return False
        return True

    def scenic_score(self, tree_x, tree_y) -> int:

        tree_height = self.forest[tree_x][tree_y]
        score = [0, 0, 0, 0]
        for search_x in range(tree_x - 1, -1, -1):
            score[0] += 1
            if self.forest[search_x][tree_y] >= tree_height:
                break
        for search_x in range(tree_x + 1, self.height):
            score[1] += 1
            if self.forest[search_x][tree_y] >= tree_height:
                break

        for search_y in range(tree_y - 1, -1, -1):
            score[2] += 1
            if self.forest[tree_x][search_y] >= tree_height:
                break

        for search_y in range(tree_y + 1, self.length):
            score[3] += 1
            if self.forest[tree_x][search_y] >= tree_height:
                break
        return score[0] * score[1] * score[2] * score[3]

    def visibility_grid(self):

        return [
            [self.is_visible(x, y) for y in range(self.length)]
            for x in range(self.length)
        ]

    def scenic_grid(self):

        return [
            [self.scenic_score(x, y) for y in range(self.length)]
            for x in range(self.length)
        ]

    def num_trees_visible(self):

        return sum([sum(x) for x in self.visibility_grid()])

    def max_scenic_score(self):

        return max([max(x) for x in self.scenic_grid()])


def solve_puzzle(puzzle: str, part_a=True) -> int:

    forest = Forest(puzzle)
    if part_a:
        return forest.num_trees_visible()
    return forest.max_scenic_score()


if __name__ == "__main__":

    print(solve_puzzle(EXAMPLE))


def test_examples_pt_a():
    assert solve_puzzle(EXAMPLE) == 21


def test_pt_a():
    assert solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines()) == 1703


def test_examples_pt_b():
    assert solve_puzzle(EXAMPLE, False) == 8


def test_pt_b():
    assert solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).lines(), False) == 1792222
