def day01a(numbers):
    i = 0
    c = 0

    for i in range(1, len(numbers)):
        if numbers[i] > numbers[i - 1]:
            c += 1
            # print("({0}){1} - {2}".format(i, f[i-1], f[i]))

    return c


def day01b(numbers):
    i = 0
    c = 0

    for i in range(0, len(numbers)):
        if sum(numbers[i : i + 3]) < sum(numbers[i + 1 : i + 4]):
            c += 1

    return c


def test_01_ex1():
    assert day01a([199, 200, 208, 210, 200, 207, 240, 269, 260, 263]) == 7


def test_01_ex2():
    assert day01b([199, 200, 208, 210, 200, 207, 240, 269, 260, 263]) == 5


def test_01a(day01_numbers):
    assert day01a(day01_numbers) == 1233


def test_01b(day01_numbers):
    assert day01b(day01_numbers) == 1275
