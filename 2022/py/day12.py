import argparse
import sys
from typing import List, Optional

from utils import AocdPuzzle, chr_to_value, value_to_str

YEAR: int = 2022
DAY: int = 12

EXAMPLE = [
    "Sabqponm",
    "abcryxxl",
    "accszExk",
    "acctuvwj",
    "abdefghi",
]
ANS_1: int = 31
ANS_2: int = 29


def bfs_shortest(
    grid: List[List[int]],
    start: tuple[int, int],
    end: Optional[tuple[int, int]] = None,
    end_search: Optional[int] = None,
    max_climb=sys.maxsize,
    max_fall=-sys.maxsize,
    allow_diagonal_movement=False,
) -> List[tuple]:

    if not end and not end_search:
        raise Exception("Cannot be missing both end and end_search")

    if end and end_search:
        raise Exception("Cannot have both end and end_search")

    if max_climb <= max_fall:
        raise Exception(
            "Max fall and max climb cannot be overlapping, no results would be returned"
        )

    if max_climb < 0 or max_fall > 0:
        raise Exception(
            "Max climb cannot be lower than zero, and max fall cannot be greater than one"
        )

    path_list: List = [[start]]
    path_index: int = 0
    previous_nodes: set = {start}

    grid_points: int = len(grid[0]) * len(grid)
    grid_height = len(grid) - 1
    grid_width = len(grid[0]) - 1

    if allow_diagonal_movement:
        adjacent_squares = (
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        )
    else:
        adjacent_squares = (
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
        )

    if start == end:
        return path_list[0]

    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]

        next_nodes = []

        for test_position in adjacent_squares:

            node_position = (
                last_node[0] + test_position[0],
                last_node[1] + test_position[1],
            )
            if (
                node_position[0] > grid_height
                or node_position[0] < 0
                or node_position[1] > grid_width
                or node_position[1] < 0
            ):
                continue
            z_diff = (
                grid[node_position[0]][node_position[1]]
                - grid[last_node[0]][last_node[1]]
            )
            if z_diff > max_climb or z_diff < max_fall:
                continue

            next_nodes.append((node_position[0], node_position[1]))

        if not end_search and end in next_nodes:
            current_path.append(end)
            return current_path

        for node in next_nodes:
            if not end and grid[node[0]][node[1]] == end_search:
                current_path.append(node)
                return current_path

            if not node in previous_nodes:
                new_path = current_path[:]
                new_path.append(node)
                path_list.append(new_path)
                previous_nodes.add(node)

        path_index += 1

    return []


def solve_puzzle(puzzle_inp, part_a=True) -> int:

    start = [
        (ix, iy)
        for ix, row in enumerate(puzzle_inp)
        for iy, i in enumerate(row)
        if i == chr_to_value("S")
    ][0]
    end = [
        (ix, iy)
        for ix, row in enumerate(puzzle_inp)
        for iy, i in enumerate(row)
        if i == chr_to_value("E")
    ][0]

    puzzle_inp[start[0]][start[1]] = chr_to_value("a")
    puzzle_inp[end[0]][end[1]] = chr_to_value("z")

    if part_a:
        path = bfs_shortest(puzzle_inp, start, end=end, max_climb=1)
    else:
        path = bfs_shortest(puzzle_inp, end, end_search=1, max_fall=-1)

    ret = len(path) - 1

    print_maze = True
    if print_maze:
        for step in path:
            puzzle_inp[step[0]][step[1]] = -1

        for row in puzzle_inp:
            line = []
            for col in row:
                if col == -1:
                    line.append("\u2588")
                else:
                    line.append(value_to_str(col))
            print("".join(line))

    print(path)

    return ret


if __name__ == "__main__":

    # Available types
    # lines() list of lines, stripped if strip=True
    # text() list of lines
    # numbers() list(s) of numbers from string
    # grid() grid of inpt
    # grid_value_from_str() grid of numbers, converting a-z to 1-25
    # number_grid() number grid of input

    puzzle = AocdPuzzle(year=YEAR, day=DAY)
    puzzle_input = puzzle.grid_value_from_str()
    example = [[chr_to_value(c) for c in row] for row in EXAMPLE]

    parser = argparse.ArgumentParser(
        description=f"Advent of code for day {DAY}, December {YEAR}"
    )
    parser.add_argument(
        "-p", "--part", help="Part A or B", required=False, choices=["a", "b"]
    )
    parser.add_argument(
        "-s", "--solve", help="Submit solution", required=False, action="store_true"
    )
    args = vars(parser.parse_args())
    args["part"] = "b"

    print(f"Advent of code for day {DAY}, December {YEAR}\n")
    if args["part"] == "a" or not args["part"]:
        print("Example 1")

        answer = solve_puzzle(example)
        print(f"Returned: {answer}, solution {ANS_1}, Equality {answer==ANS_1}")

        print("\n Part 1")
        answer_a = solve_puzzle(puzzle_input)
        print(answer_a)

        if args["solve"]:
            puzzle.submit_answer(answer_a, YEAR, DAY)

    if args["part"] == "b" or not args["part"]:
        print("Example 2")

        answer = solve_puzzle(example, part_a=False)
        print(f"Returned: {answer}, solution {ANS_2}, Equality {answer==ANS_2}")

        print("\n Part 2")
        answer_b = solve_puzzle(puzzle_input, part_a=False)
        print(answer_b)

        if args["solve"]:
            puzzle.submit_answer(answer_b, YEAR, DAY)


def test_examples_pt_a():
    assert solve_puzzle([[chr_to_value(c) for c in row] for row in EXAMPLE]) == ANS_1


def test_pt_a():
    assert solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).grid_value_from_str()) == 534


def test_examples_pt_b():
    assert (
        solve_puzzle([[chr_to_value(c) for c in row] for row in EXAMPLE], False)
        == ANS_2
    )


def test_pt_b():
    assert (
        solve_puzzle(AocdPuzzle(year=YEAR, day=DAY).grid_value_from_str(), False) == 525
    )
