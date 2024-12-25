def get_ans(data):
    data = format_data(data)

    def addAntiNodePos(antiNodePos, pos1, pos2):
        if pos1[0] > pos2[0]:
            addAntiNodePos(antiNodePos, pos2, pos1)
            return
        xDiff = pos1[0] - pos2[0]
        yDiff = pos1[1] - pos2[1]
        aNode1 = (pos1[0] + xDiff, pos1[1] + yDiff)
        aNode2 = (pos2[0] - xDiff, pos2[1] - yDiff)

        def addAllAntiNodes(pos, incrementer):
            x, y = pos
            deltax, deltay = incrementer
            while 0 <= x < len(data) and 0 <= y < len(data[x]):
                antiNodePos.add((x, y))
                x = x + deltax
                y = y + deltay
            return

        addAllAntiNodes(aNode1, (xDiff, yDiff))
        addAllAntiNodes(aNode2, (-1 * xDiff, -1 * yDiff))
        antiNodePos.add(pos1)
        antiNodePos.add(pos2)
        return

    positions = getAllPositions(data)
    antiNodePos = set()
    for nodeType in positions.keys():
        posList = positions[nodeType]
        for i in range(len(posList)):
            for j in range(i):
                addAntiNodePos(antiNodePos, posList[i], posList[j])
    return len(antiNodePos)


def getAllPositions(data):
    d = {}
    for i in range(len(data)):
        for j in range(len(data[i])):
            if not data[i][j] == '.':
                if data[i][j] in d:
                    d[data[i][j]].append((i, j))
                else:
                    d[data[i][j]] = [(i, j)]
    return d


def get_ans_1(data):
    data = format_data(data)

    def addAntiNodePos(antiNodePos, pos1, pos2):
        if pos1[0] > pos2[0]:
            addAntiNodePos(antiNodePos, pos2, pos1)
            return
        xDiff = pos1[0] - pos2[0]
        yDiff = pos1[1] - pos2[1]
        aNode1 = (pos1[0] + xDiff, pos1[1] + yDiff)
        aNode2 = (pos2[0] - xDiff, pos2[1] - yDiff)
        for x, y in [aNode1, aNode2]:
            if 0 <= x < len(data) and 0 <= y < len(data[x]):
                antiNodePos.add((x, y))
        return

    positions = getAllPositions(data)
    antiNodePos = set()
    for nodeType in positions.keys():
        posList = positions[nodeType]
        for i in range(len(posList)):
            for j in range(i):
                addAntiNodePos(antiNodePos, posList[i], posList[j])
    return len(antiNodePos)


def format_data(data):
    data = data.split('\n')
    ret = []
    for i in data:
        ret.append(list(i))
    return ret
