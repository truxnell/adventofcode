from typing import List

def day03a(rucksack:List): 

    score=0
    for item in rucksack:
        first,second=string_split_half(item)

        for char in first:

            if char in second:
                score+=char_to_int(char)
                break

    return score

def day03b(rucksack:List): 

    score=0
    for i in range(0,len(rucksack),3):

        for char in rucksack[i]:

            if char_find_in_strings(char,[rucksack[i+1],rucksack[i+2]]):
                score+=char_to_int(char)
                break

    return score


def char_find_in_strings(char:str, strings:List) -> bool:

    if len(strings)==1:

        if char in strings[0]:
            return True
        else:
            return False

    else:
    
        if char in strings[0]:
            return char_find_in_strings(char,strings[1:])
        else:
            return False



def char_to_int(char:str) -> int:
    """Convert a-z & A-Z to int score"""

    num=ord(char)

    if num>96:
        # a-z 1-26
        num-=96
    else:
        # A-Z 27-52 
        num-=38


    return num

def string_split_half(string:str) -> str:

    string1,string2=string[:len(string)//2],string[len(string)//2:]

    return string1,string2

ex=[
"vJrwpWtwJgWrhcsFMMfFFhFp",
"jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
"PmmdzqPrVvPwwTWBwg",
"wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
"ttgJtRGJQctTZtZT",
"CrZsJsPPZsGzwwsLwLmpwMDw"
]

def test_03_ex1a():
    assert day03a(ex) == 157

def test_03_ex1b():
    assert day03b(ex) == 70

def test_03a(day03_lines):
    assert day03a(day03_lines) == 8515

def test_03b(day03_lines):
    assert day03b(day03_lines) == 2434
