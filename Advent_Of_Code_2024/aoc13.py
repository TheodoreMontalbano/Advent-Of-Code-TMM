def get_ans(data):
    data = format_data(data)
    total = 0

    def getAmtOfAandB(subproblem):
        bx = subproblem['B']['X']
        by = subproblem['B']['Y']
        ax = subproblem['A']['X']
        ay = subproblem['A']['Y']
        wx = subproblem['P']['X']
        wy = subproblem['P']['Y']

        # wx = ax * i + bx * j
        # wy = ay * i + by * j

        # wx * ay / ax = ay * i + bx * ay / ax * j
        # wy = ay * i + by * j

        # wx * ay / ax - wy = (bx * ay / ax - by) * j
        # j = (wx * ay / ax - wy) / (bx * ay / ax - by)
        j = (wx * ay / ax - wy) / (bx * ay / ax - by)
        i = (wx - bx * j) / ax
        i = int(i)
        j = int(j)
        for k in range(-2, 3, 1):
            for l in range(-2, 3, 1):
                if (i + k) * ax + (l + j) * bx == wx and (i + k) * ay + (l + j) * by == wy:
                    return 3 * (i + k) + (l + j)
        return float('inf')

    for subProblem in data:
        tokens = getAmtOfAandB(subProblem)
        if tokens < float('inf'):
            total = tokens + total
    return total


def format_data(data, num=2):
    data = data.split('\n\n')
    ret = []
    for subproblem in data:
        ret.append(subproblem.split('\n'))
    data = ret
    ret = []

    def getXandY(row):
        row = row[row.find(':') + 1:]
        row = row.split(',')
        ret = {}
        ret['X'] = int(row[0][3:])
        ret['Y'] = int(row[1][3:])
        return ret

    for subproblem in data:
        curr = {}
        curr['A'] = getXandY(subproblem[0])
        curr['B'] = getXandY(subproblem[1])
        curr['P'] = getXandY(subproblem[2])
        if num == 2:
            curr['P']['X'] = curr['P']['X'] + 10000000000000
            curr['P']['Y'] = curr['P']['Y'] + 10000000000000
        ret.append(curr)
    data = ret
    return data
