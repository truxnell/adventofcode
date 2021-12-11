
def day03a(lines):

    l = [0]*len(lines[0])

    for line in lines:
        for i in range(0, len(line)):
            l[i] += int(line[i])
    n = len(lines)/2
    for i in range(0, len(l)):
        if l[i] > n:
            l[i] = 1
        else:
            l[i] = 0

    g = int(''.join(map(str, l)), 2)
    e = 2**len(lines[0])-g-1

    return g*e


def day03a(lines):

    l = [0]*len(lines[0])

    for line in lines
      

    return False


ex1 = ['00100', '11110', '10110', '10111', '10101', '01111',
       '00111', '11100', '10000', '11001', '00010', '01010']


def test_03_ex1a(): assert day03a(ex1) == 198


def test_03a(day03_lines): assert day03a(day03_lines) == 3882564
