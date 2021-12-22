def day07a(st, exp_fuel=False):
    crabs = st.split(",")
    crabs = [x.rstrip() for x in crabs]
    crabs = [int(x) for x in crabs]
    fuel_option = []

    for i in range(max(crabs) + 1):
        fuel = [abs(x - i) for x in crabs]
        if exp_fuel:
            fuel = [x / 2 * (x + 1) for x in fuel]
        fuel_option.append(sum(fuel))

    return min(fuel_option)


ex = "16,1,2,0,4,2,7,1,2,14"


def test_07_ex1a():
    assert day07a(ex) == 37


def test_07_ex1b():
    assert day07a(ex, True) == 168


def test_07a(day07_text):
    assert day07a(day07_text) == 356992


def test_07b(day07_text):
    assert day07a(day07_text, True) == 101268110
