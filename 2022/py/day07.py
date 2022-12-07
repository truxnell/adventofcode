from aocd import get_data

EXAMPLE = [
    "$ cd /",
    "$ ls",
    "dir a",
    "14848514 b.txt",
    "8504156 c.dat",
    "dir d",
    "$ cd a",
    "$ ls",
    "dir e",
    "29116 f",
    "2557 g",
    "62596 h.lst",
    "$ cd e",
    "$ ls",
    "584 i",
    "$ cd ..",
    "$ cd ..",
    "$ cd d",
    "$ ls",
    "4060174 j",
    "8033020 d.log",
    "5626152 d.ext",
    "7214296 k",
]

YEAR = 2022
DAY = 7


class Storage:
    def __init__(self):
        self.cwd = "/"
        self.dir = {"/": []}

    def cd(self, path: str):
        if path == "/":
            self.cwd = "/"
            return
        
        if path=="..":
            self.cwd=self.cwd[:self.cwd.rfind("/")] 
            return

        self.cwd+="/"
        self.cwd+=path



def solve_puzzle(puzzle: str, part_a=True) -> int:

    pass


def test_examples_pt_a():
    assert solve_puzzle(EXAMPLE) == 5


def test_pt_a():
    inp = get_data(day=DAY, year=YEAR)
    assert solve_puzzle(inp) == 0

"".rindex)
