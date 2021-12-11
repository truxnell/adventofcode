def day03a(lines):

    l = [0] * len(lines[0])

    for line in lines:
        for i in range(0, len(line)):
            l[i] += int(line[i])
    n = len(lines) / 2
    for i in range(0, len(l)):
        if l[i] > n:
            l[i] = 1
        else:
            l[i] = 0

    g = int("".join(map(str, l)), 2)
    e = 2 ** len(lines[0]) - g - 1

    return g * e


def day03b(lines):

    i = 0
    oxygen_lines = lines.copy()
    co2_lines = lines.copy()

    while len(oxygen_lines) > 1:
        list_one = []
        list_zero = []
        ones = 0

        for line in oxygen_lines:
            ones += int(line[i])
            if line[i] == "0":
                list_zero.append(line)
            else:
                list_one.append(line)

        if ones >= len(oxygen_lines) / 2:
            [oxygen_lines.remove(x) for x in list_zero]
        else:
            [oxygen_lines.remove(x) for x in list_one]

        i += 1

    oxygen = int(oxygen_lines[0], 2)
    i = 0

    while len(co2_lines) > 1:
        list_one = []
        list_zero = []
        ones = 0

        for line in co2_lines:
            ones += int(line[i])
            if line[i] == "0":
                list_zero.append(line)
            else:
                list_one.append(line)

        if ones < len(co2_lines) / 2:
            [co2_lines.remove(x) for x in list_zero]
        else:
            [co2_lines.remove(x) for x in list_one]

        i += 1
    co2 = int(co2_lines[0], 2)

    return oxygen * co2


ex1 = [
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010",
]


def test_03_ex1():
    assert day03a(ex1) == 198


def test_03_ex2():
    assert day03b(ex1) == 230


def test_03a(day03_lines):
    assert day03a(day03_lines) == 3882564


def test_03b(day03_lines):
    assert day03b(day03_lines) == 3385170
