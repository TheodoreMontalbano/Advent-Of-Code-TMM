from functools import lru_cache


def get_ans(data, num=2):
    towels, wanted = format_data(data)
    towels = set(towels)

    @lru_cache(maxsize=None)
    def findWanted(start, string):
        if start == len(string):
            return 1
        total = 0
        for i in range(start, len(string)):
            if string[start: i + 1] in towels:
                total = total + findWanted(i + 1, string)
        return total

    total = 0
    for i in wanted:
        if num == 1:
            total = total + int(findWanted(0, i) > 0)
        else:
            total = total + findWanted(0, i)
    return total


def format_data(data):
    data = data.split('\n\n')
    colors = data[0].split(', ')
    towels = data[1].split('\n')
    return colors, towels
