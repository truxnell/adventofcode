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
        self.dir = {"/": {}}

    def cd(self, path: str) -> None:
        if path == "/":
            self.cwd = "/"
            return

        if path == "..":
            self.cwd = self.cwd[: self.cwd.rfind("/")]
            return

        if self.cwd != "/":
            self.cwd += "/"
        self.cwd += path
        self.dir[self.cwd] = {}

    def add_file(self, file: str, size: int) -> None:
        if not self.cwd in self.dir:
            self.dir[self.cwd] = {}
        self.dir[self.cwd][file] = int(size)

    def dir_size(self, dir_path: str) -> int:

        if not dir_path in self.dir:
            return 0
        paths = []
        for path in self.dir.keys():
            if path[: len(dir_path)] == dir_path:
                paths.append(path)
        total = 0
        for path in paths:
            for file in self.dir[path].keys():
                size = self.dir[path][file]
                total += size
        return total

    def paths(self) -> str:

        for path in self.dir.keys():
            yield path


def solve_puzzle(puzzle: str, part_a=True) -> int:

    listing = Storage()
    for entry in puzzle:

        if entry[:4] == "$ cd":
            listing.cd(entry[5:])
        elif entry[:4] == "$ ls":
            pass
        elif entry[:3] == "dir":
            pass
        else:
            size, file = entry.split()
            listing.add_file(file, size)
    if part_a:

        total_size = 0
        for path in listing.paths():
            size = listing.dir_size(path)
            if size <= 100000:
                total_size += size

        return total_size

    total_space = 70000000
    required_space = 30000000
    need_delete = required_space - (total_space - listing.dir_size("/"))
    print(need_delete)
    dirs = [
        listing.dir_size(s)
        for s in listing.paths()
        if listing.dir_size(s) >= need_delete
    ]
    dirs.sort()
    print(dirs)
    return dirs[0]


if __name__ == "__main__":
    print(solve_puzzle(EXAMPLE))


def test_examples_pt_a():
    assert solve_puzzle(EXAMPLE) == 95437


def test_pt_a():
    inp = get_data(day=DAY, year=YEAR)
    inp = inp.splitlines()
    assert solve_puzzle(inp) == 1792222


def test_examples_pt_b():
    assert solve_puzzle(EXAMPLE, False) == 24933642


def test_pt_b():
    inp = get_data(day=DAY, year=YEAR)
    inp = inp.splitlines()
    assert solve_puzzle(inp, False) == 1112963
