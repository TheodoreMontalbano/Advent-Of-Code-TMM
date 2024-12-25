from copy import deepcopy


def get_ans(data):
    data = format_data(data)
    directions = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]
    start = (-1, -1)
    for i in range(len(data)):
        for j in range(len(data)):
            if not data[i][j] == '.' and not data[i][j] == '#':
                start = (i, j)
                break

    def getDirIndex(start):
        x, y = start
        if data[x][y] == '^':
            return 0
        elif data[x][y] == '>':
            return 1
        elif data[x][y] == '<':
            return 3
        elif data[x][y] == 'v':
            return 2
        return -1

    startIndex = getDirIndex(start)
    dirIndex = startIndex
    visited = set()
    placedObstacleLocs = set()
    currPos = start

    def printLoop(start, loop1):
        print(start)
        tempData = deepcopy(data)
        x, y = start
        tempData[x][y] = 'O'
        for (x, y), _ in visited:
            tempData[x][y] = '|'
        for (x, y), _ in loop1:
            if not data[x][y] == '#':
                tempData[x][y] = '+'
        toPrint = []
        for i in tempData:
            toPrint.append(''.join(i))
        print('\n'.join(toPrint))
        print()

    def checkForLoop(pos, currDir):
        currVisited = set()
        while (pos, currDir) not in currVisited:
            currVisited.add((pos, currDir))
            x, y = pos
            nextPos = (x + directions[currDir][0], y + directions[currDir][1])
            x, y = nextPos
            if not (0 <= x < len(data)) or not (0 <= y < len(data[0])):
                return False
            if data[x][y] == '#':
                currDir = (currDir + 1) % 4
            else:
                pos = nextPos
        #printLoop(pos, currVisited)
        return True

    while True:
        visited.add((currPos, dirIndex))
        x, y = currPos
        nextPos = (x + directions[dirIndex][0], y + directions[dirIndex][1])
        x, y = nextPos
        if not (0 <= x < len(data)) or not (0 <= y < len(data[0])):
            break
        if data[x][y] == '#':
            dirIndex = (dirIndex + 1) % 4
        else:
            data[x][y] = '#'
            if checkForLoop(start, startIndex) and nextPos not in placedObstacleLocs:
                placedObstacleLocs.add(nextPos)
            data[x][y] = '.'
            currPos = nextPos

    return len(placedObstacleLocs) - int(start in placedObstacleLocs)


def get_ans_1(data):
    data = format_data(data)
    directions = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]
    start = (-1, -1)
    for i in range(len(data)):
        for j in range(len(data)):
            if not data[i][j] == '.' and not data[i][j] == '#':
                start = (i, j)
                break

    def getDirIndex(start):
        x, y = start
        if data[x][y] == '^':
            return 0
        elif data[x][y] == '>':
            return 1
        elif data[x][y] == '<':
            return 3
        elif data[x][y] == 'v':
            return 2
        return -1

    dirIndex = getDirIndex(start)

    visited = set()
    currPos = start
    while True:
        visited.add(currPos)
        x, y = currPos
        nextPos = (x + directions[dirIndex][0], y + directions[dirIndex][1])
        x, y = nextPos
        if not (0 <= x < len(data)) or not (0 <= y < len(data[0])):
            break
        if data[x][y] == '#':
            dirIndex = (dirIndex + 1) % 4
        else:
            currPos = nextPos
    return len(visited)


def format_data(data):
    data = data.split('\n')
    ret = []
    for i in data:
        ret.append(list(i))
    return ret
