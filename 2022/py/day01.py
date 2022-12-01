from typing import List


def parse_rations(rations_input: List, num=1) -> int:

    rations=[]
    calories=0
    for item in rations_input:
        calories+=item
        if item==0:
            rations.append(calories)
            calories=0
    rations.append(calories)
    rations=sorted(rations, reverse=True)

    print(rations[:num])
    return sum(rations[:num])

def day01a(rations:List): 

    return parse_rations([int(x) if x != '' else 0 for x in rations])

def day01b(rations:List): 

    return parse_rations([int(x) if x != '' else 0 for x in rations],num=3)

ex=[1000,2000,3000,0,4000,0,5000,6000,0,7000,8000,9000,0,10000]

print(parse_rations(ex))

def test_01_ex1a():
    assert day01a(ex) == 24000

def test_01_ex1b():
    assert day01b(ex) == 45000

def test_01a(day01_lines):
    assert day01a(day01_lines) == 69310

def test_01b(day01_lines):
    assert day01b(day01_lines) == 206104
