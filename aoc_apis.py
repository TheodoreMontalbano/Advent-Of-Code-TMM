from operator import mul
from functools import reduce
from math import factorial
from aocd import get_data
from datetime import date


def load_data(day=-1, year=-1):
    session_cookie = "53616c7465645f5f7c2e017af2406b3ec98232747ffe0554485cfbb28d3cd27d8996af399b5a10e203225f948507d2ed9143d12cb0857ac918b8a305810e195c"
    today = date.today()
    if day == -1:
        day = today.day
    if year == -1:
        year = today.year
    prod = get_data(session=session_cookie, day=day, year=year)
    return prod


# returns if the two given intervals overlap
def has_overlap(interval_one, interval_two):
    if max(interval_one[0], interval_two[0]) <= min(interval_two[1], interval_one[1]):
        return True
    return False


# creates array of difference of input
def get_differences(value_list: list[int]) -> list[int]:
    ret = []
    for i in range(len(value_list) - 1):
        ret.append(value_list[i + 1] - value_list[i])
    print(ret)
    return ret


# Creates polynomial func from difference tables of input
def values_to_polynomial(value_list: list[int]):
    curr = get_differences(value_list)
    differences_list = [value_list, curr]
    while len(curr) > 1 or max(curr) > 0:
        curr = get_differences(curr)
        differences_list.append(curr)

    def poly(x: float) -> float:
        ret = 0
        for i in range(len(differences_list)):
            val = 1
            for j in range(i):
                val = val * (x - j)
            ret = val / factorial(i) * differences_list[i][0] + ret
        return ret

    return poly
