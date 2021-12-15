import numpy as np
import matplotlib.pyplot as plt


def draw_line(mat, x0, y0, x1, y1, inplace=False):
    # Thankyou, Stack overflow stranger.  You will not be forgotten
    # https://stackoverflow.com/questions/50387606/python-draw-line-between-two-coordinates-in-a-matrix/50388226
    if not (
        0 <= x0 < mat.shape[0]
        and 0 <= x1 < mat.shape[0]
        and 0 <= y0 < mat.shape[1]
        and 0 <= y1 < mat.shape[1]
    ):
        raise ValueError("Invalid coordinates.")
    if not inplace:
        mat = mat.copy()
    if (x0, y0) == (x1, y1):
        mat[x0, y0] += 1
        return mat if not inplace else None
    # Swap axes if Y slope is smaller than X slope
    transpose = abs(x1 - x0) < abs(y1 - y0)
    if transpose:
        mat = mat.T
        x0, y0, x1, y1 = y0, x0, y1, x1
    # Swap line direction to go left-to-right if necessary
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    # Write line ends
    mat[x0, y0] += 1
    mat[x1, y1] += 1
    # Compute intermediate coordinates using line equation
    x = np.arange(x0 + 1, x1)
    y = np.round(((y1 - y0) / (x1 - x0)) * (x - x0) + y0).astype(x.dtype)
    # Write intermediate coordinates
    mat[x, y] += 1
    if not inplace:
        return mat if not transpose else mat.T


def vector(vectors):
    # I did write everything else thou...
    vectors = (x.split(" -> ") for x in vectors)
    for lst in vectors:
        (x0, y0) = lst[0].split(",")
        (x1, y1) = lst[1].split(",")
        yield int(x0), int(y0), int(x1), int(y1)


def get_max_coords(lst):
    tmp = [x.split(" -> ") for x in lst]
    tmp = [item for sublist in tmp for item in sublist]
    tmp = [x.split(",") for x in tmp]
    x, y = map(list, zip(*tmp))

    return int(max(x, key=int)), int(max(y, key=int))


def day05(lst, diag=False):
    vectors = lst.copy()
    x_size, y_size = get_max_coords(vectors)
    print(x_size, y_size)
    grid = np.zeros((x_size + 2, y_size + 2))

    for x0, y0, x1, y1 in vector(vectors):
        if diag or x0 == x1 or y0 == y1:
            print(f"{x0},{y0} -> {x1},{y1}")
            draw_line(grid, y0, x0, y1, x1, True)
        else:
            print(f"Skipping {x0},{y0} -> {x1},{y1}")

    plt.imshow(grid, interpolation="nearest")
    plt.savefig(f"day05a-{x_size}x{y_size}-{diag}.png")

    return np.sum(grid > 1)


ex = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""".split(
    "\n"
)

# print(day05a(ex))

# with open("../input/day05.txt") as f:
#     _ = f.readlines()
#     lines = [line.strip() for line in _]


def test_05_ex1a():
    assert day05(ex) == 5


def test_05_ex1b():
    assert day05(ex, True) == 12


def test_05a(day05_lines):
    assert day05(day05_lines) == 5147


def test_05b(day05_lines):
    assert day05(day05_lines, True) == 5147
