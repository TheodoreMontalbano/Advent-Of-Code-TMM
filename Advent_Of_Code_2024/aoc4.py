from aoc_apis import rotate_2D_arr as rotate


def get_ans_1(data):
    data = format_data(data)

    def getCount(wSearch):
        arr = ['X', 'M', 'A', 'S']
        count = 0
        for row in wSearch:
            index = 0
            for j in row:

                if j == arr[index]:
                    index = index + 1

                    if index == len(arr):
                        index = 0
                        count = count + 1
                else:
                    index = int(j == arr[0])
        return count

    def getDiagCount(wSearch):
        arr = ['X', 'M', 'A', 'S']
        count = 0
        for i in range(2 * len(wSearch)):
            index = 0
            for j in range(i + 1):
                k = i - j
                if k >= len(wSearch) or j >= len(wSearch):
                    continue
                if wSearch[j][k] == arr[index]:
                    index = index + 1
                    if index == len(arr):
                        index = 0
                        count = count + 1
                else:
                    index = int(wSearch[j][k] == arr[0])
        return count

    total = 0
    for i in range(4):
        total = total + getCount(data)
        total = total + getDiagCount(data)
        data = rotate(data)

    return total


def get_ans(data):
    data = format_data(data)
    total = 0

    def checkMasLD(i, j):
        if not(0 < i < len(data) - 1 and 0 < j < len(data) - 1):
            return False
        else:
            return ((data[i - 1][j - 1] == 'S' and data[i + 1][j + 1] == 'M') or
                    (data[i - 1][j - 1] == 'M' and data[i + 1][j + 1] == 'S'))

    def checkMasUD(i, j):
        if not(0 < i < len(data) - 1 and 0 < j < len(data) - 1):
            return False
        else:
            return ((data[i + 1][j - 1] == 'S' and data[i - 1][j + 1] == 'M') or
                    (data[i + 1][j - 1] == 'M' and data[i - 1][j + 1] == 'S'))

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 'A':
                total = total + int(checkMasUD(i, j) and checkMasLD(i, j))

    return total


def format_data(data):
    data = data.split('\n')
    ret = []
    for i in data:
        ret.append(list(i))
    return ret
