
def get_ans(data):
    data = format_data(data)
    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]

    def getNeighbors(pos):
        x, y = pos
        currVal = int(data[x][y])
        for x_1, y_1 in directions:
            if 0 <= x + x_1 < len(data) and 0 <= y + y_1 < len(data[0]):
                newVal = int(data[x + x_1][y + y_1])
                if newVal == currVal + 1:
                    yield x + x_1, y + y_1

    def getScore(pos):
        stack = [pos]
        score = 0
        while len(stack) > 0:
            curr = stack.pop()
            currVal = data[curr[0]][curr[1]]
            if int(currVal) == 9:
                score = score + 1
            else:
                for neighbor in getNeighbors(curr):
                    stack.append(neighbor)
        return score

    def getZeroes(data):
        ret = []
        for i in range(len(data)):
            for j in range(len(data)):
                if int(data[i][j]) == 0:
                    ret.append((i, j))
        return ret

    startPos = getZeroes(data)
    total = 0
    for pos in startPos:
        total = total + getScore(pos)
    return total
def get_ans_1(data):
    data = format_data(data)
    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]

    def getNeighbors(pos):
        x, y = pos
        currVal = int(data[x][y])
        for x_1, y_1 in directions:
            if 0 <= x + x_1 < len(data) and 0 <= y + y_1 < len(data[0]):
                newVal = int(data[x + x_1][y + y_1])
                if newVal == currVal + 1:
                    yield x + x_1, y + y_1

    def getScore(pos):
        stack = [pos]
        visited = set(stack)
        score = 0
        while len(stack) > 0:
            curr = stack.pop()
            currVal = data[curr[0]][curr[1]]
            if int(currVal) == 9:
                score = score + 1
            else:
                for neighbor in getNeighbors(curr):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
        return score

    def getZeroes(data):
        ret = []
        for i in range(len(data)):
            for j in range(len(data)):
                if int(data[i][j]) == 0:
                    ret.append((i, j))
        return ret

    startPos = getZeroes(data)
    total = 0
    for pos in startPos:
        total = total + getScore(pos)
    return total


def format_data(data):
    data = data.split('\n')
    ret = []
    for row in data:
        ret.append(list(row))
    return ret
