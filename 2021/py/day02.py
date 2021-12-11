

def day02a(lines):

    h = 0
    d = 0

    for i in range(0, len(lines)):
        a = lines[i].split()
        a[1] = int(a[1])
        if a[0] == "forward":
            h += a[1]
        elif a[0] == "down":
            d += a[1]
        elif a[0] == "up":
            d -= a[1]

    return h*d


def day02b(lines):

    h = 0
    d = 0
    a = 0

    for i in range(0, len(lines)):
        w = lines[i].split()
        w[1] = int(w[1])
        if w[0] == "forward":
            h += w[1]
            d += w[1]*a
        elif w[0] == "down":
            a += w[1]
        elif w[0] == "up":
            a -= w[1]
        else:
            raise Exception("How did you get here?")

    return h*d


ex1 = ['forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2']


def test_02_ex1(): assert day02a(ex1) == 150
def test_02_ex2(): assert day02b(ex1) == 900


def test_02a(day02_lines): assert day02a(day02_lines) == 2147104
def test_02b(day02_lines): assert day02b(day02_lines) == 2044620088
