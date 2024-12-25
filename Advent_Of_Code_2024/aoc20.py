from queue import PriorityQueue


def get_ans(data, num=2):
    data = format_data(data)
    directions = [
        (0, 1),
        (1, 0),
        (-1, 0),
        (0, -1)
    ]
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i][j] == 'S':
                start = (i, j)
            elif data[i][j] == 'E':
                end = (i, j)

    visited = set()
    path = []
    stack = [(start, 0)]
    while len(stack) > 0:
        curr, currDist = stack.pop()
        if curr in visited:
            continue
        else:
            visited.add(curr)
            path.append((curr, currDist))
            for x, y in directions:
                newPos = curr[0] + x, curr[1] + y
                if (0 <= newPos[0] < len(data) and 0 <= newPos[1] < len(data[1])
                        and not data[newPos[0]][newPos[1]] == '#'):
                    stack.append((newPos, currDist + 1))
    def getManhattanDistance(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1-x2) + abs(y1 - y2)
    origTime = len(path) - 1
    total = 0
    for i in range(len(path)):
        for j in range(i):
            pos1 = path[i][0]
            pos2 = path[j][0]
            if num == 1:
                if getManhattanDistance(pos1, pos2) <= 2 and abs(path[i][1] - path[j][1]) - 2 >= 100:
                    total = total + 1
            elif num == 2:
                if (getManhattanDistance(pos1, pos2) <= 20
                        and abs(path[i][1] - path[j][1]) - getManhattanDistance(pos1, pos2) >= 100):
                    total = total + 1
    return total


def format_data(data):
    data = data.split('\n')
    ret = []
    for i in data:
        ret.append(list(i))
    return ret
