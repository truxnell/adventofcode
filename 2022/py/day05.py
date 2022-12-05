from typing import List


def day05a(jobs: List, alternate=False):

    brk = 0
    for i, line in enumerate(jobs):

        if not line.strip():
            brk = i
            break
    columns = int(jobs[brk - 1].strip()[-1])
    stack = [["" for _ in range(0, columns)] for _ in range(0, 45)]
    for line in range(0, brk - 1):
        print(jobs[line])
        stack.append([jobs[line][i : i + 4].strip() for i in range(0, columns * 4, 4)])

    for i in range(brk + 1, len(jobs)):
        inst = jobs[i].split()
        if alternate:
            item = []
            for _ in range(int(inst[1])):
                item.append(retrieve_box(stack, int(inst[3]) - 1))

            for _ in range(int(inst[1])):
                place_box(stack, int(inst[5]) - 1, item.pop())

        else:
            for _ in range(int(inst[1])):
                item = retrieve_box(stack, int(inst[3]) - 1)
                place_box(stack, int(inst[5]) - 1, item)

    top_boxes = ""
    for col in range(0, len(stack[0])):
        row = find_nonblank_in_column(stack, col)
        if not row == len(stack) - 1:
            row += 1
        if stack[row][col]:
            top_boxes += stack[row][col][1:2]

    return top_boxes.replace(" ", "")


def find_nonblank_in_column(lst: List, col_num: int):

    for i, row in enumerate(lst):
        if row[col_num].strip():
            if i == 0:
                raise Exception
            return i - 1
    return len(lst) - 1


def print_stack(lst: List, pretty=True):

    print("|  1   2   3   4   5   6   7   8   9  |")
    for j, line in enumerate(lst):
        if "".join(line):
            if pretty:
                prt = ""
                for char in line:
                    if char:
                        prt += char
                    else:
                        prt += "   "
            else:
                prt = line

            print(f"|{prt}| - {j}")


def retrieve_box(lst: List, col_num: int):

    row = find_nonblank_in_column(lst, col_num)
    if not row == len(lst) - 1:
        row += 1
    box = lst[row][col_num]
    lst[row][col_num] = ""

    return box


def place_box(lst: List, col_num: int, item: str):

    row = find_nonblank_in_column(lst, col_num)
    lst[row][col_num] = item


ex = [
    "    [D]    ",
    "[N] [C]    ",
    "[Z] [M] [P]",
    " 1   2   3 ",
    " ",
    "move 1 from 2 to 1",
    "move 3 from 1 to 3",
    "move 2 from 2 to 1",
    "move 1 from 1 to 2",
]


def test_05_ex1a():
    assert day05a(ex) == "CMZ"


def test_05_ex1b():
    assert day05a(ex, alternate=True) == "MCD"


def test_05a():
    with open("input/day05.txt", "r") as file:
        lines = file.read().splitlines()
    assert day05a(lines) == "RFFFWBPNS"


def test_05b():
    with open("input/day05.txt", "r") as file:
        lines = file.read().splitlines()
    assert day05a(lines, alternate=True) == "CQQBBJFCS"
