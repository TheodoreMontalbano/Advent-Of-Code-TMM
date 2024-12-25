from copy import deepcopy


def isSafe(row):
    arr = []
    for i in range(len(row) - 1):
        arr.append(int(row[i]) - int(row[i + 1]))
    gtzero = [int(i > 0) for i in arr]
    rangeCorrect = [int(0 < abs(i) < 4) for i in arr]
    return (len(gtzero) == sum(gtzero) or sum(gtzero) == 0) and sum(rangeCorrect) == len(rangeCorrect)


def get_ans_1(data):
    reports = format_data(data)
    total = 0

    for row in reports:
        total = total + int(isSafe(row))
    return total


def get_ans(data):
    reports = format_data(data)
    total = 0

    for row in reports:
        if isSafe(row):
            total = total + 1
        else:
            left = deepcopy(row)
            right = []
            while left:
                curr = left.pop()
                if isSafe(left + right[::-1]):
                    total = total + 1
                    break
                right.append(curr)
    return total


def format_data(data):
    data = data.split('\n')
    reports = []
    for i in data:
        reports.append(i.split(' '))
    return reports
