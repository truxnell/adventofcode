def parse(str):
    str = "".join(str).split(",")
    str = [int(x.rstrip()) for x in str]
    return str


def day06(str, days=80):
    fish = parse(str)
    return day06_process(fish, days)


def day06_process(fish, days):

    fish_swarm = {}
    for i in range(-1, 9):
        fish_swarm[i] = fish.count(i)

    for i in range(days):
        for j in range(0, 9):
            fish_swarm[j - 1] = fish_swarm[j]
        fish_swarm[8] = fish_swarm[-1]
        fish_swarm[6] += fish_swarm[-1]
        fish_swarm[-1] = 0

    return sum(fish_swarm.values())


def read_file(fname):
    with open(fname, "r") as f:
        return f.readlines()


ex = "3, 4, 3, 1, 2"

print(day06(ex, 256))


def test_06_ex1a():
    assert day06(ex) == 5934


def test_06_ex1b():
    assert day06(ex, 256) == 26984457539


def test_06a(day06_text):
    assert day06(day06_text) == 380758


def test_06b(day06_text):
    assert day06(day06_text, 256) == 1710623015163
