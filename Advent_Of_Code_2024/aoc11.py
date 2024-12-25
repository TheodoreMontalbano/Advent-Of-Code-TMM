from functools import lru_cache


def get_ans(data, blinks=75):
    data = format_data(data)
    total = 0

    @lru_cache(maxsize=None)
    def getFinalLength(num, blinks):
        if blinks == 0:
            return 1
        else:
            if num == '0':
                return getFinalLength('1', blinks - 1)
            elif len(num) % 2 == 0:
                return (getFinalLength(str(int(num[: len(num) // 2])), blinks - 1)
                        + getFinalLength(str(int(num[len(num) // 2:])), blinks - 1))
            else:
                return getFinalLength(str(int(num) * 2024), blinks - 1)

    for i in data:
        total = total + getFinalLength(i, blinks)
    return total


def format_data(data):
    data = data.split(' ')
    return data
