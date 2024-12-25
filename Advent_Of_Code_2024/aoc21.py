from functools import lru_cache

from aoc_apis import AdjacencyGraph, FreeFormGraph


def getGraph(numOfGraphs):
    def getNeighborsBase(graphValue):
        if graphValue == '>':
            yield 'A', 1
            yield 'v', 1
        elif graphValue == 'v':
            yield '>', 1
            yield '<', 1
            yield '^', 1
        elif graphValue == '<':
            yield 'v', 1
        elif graphValue == '^':
            yield 'v', 1
            yield 'A', 1
        elif graphValue == 'A':
            yield '^', 1
            yield '>', 1

    startGraph = FreeFormGraph(getNeighborsBase)

    def getDirectionalDirection(start, end):
        if start == '<':
            if end == 'v':
                return '>'
        elif start == 'v':
            if end == '<':
                return '<'
            elif end == '^':
                return '^'
            elif end == '>':
                return '>'
        elif start == '^':
            if end == 'A':
                return '>'
            elif end == 'v':
                return 'v'
        elif start == '>':
            if end == 'A':
                return '^'
            elif end == 'v':
                return '<'
        elif start == 'A':
            if end == '^':
                return '<'
            elif end == '>':
                return 'v'
        print('ERROR')

    def getGetNeighbors(graphBase: FreeFormGraph, useBase=False):
        memo = {}

        def getNeighbors(graphValue):
            graphValue, prevDir = graphValue
            for neighbor, _ in getNeighborsBase(graphValue):
                direction = getDirectionalDirection(graphValue, neighbor)
                if direction == prevDir:
                    yield (neighbor, direction), 1
                # get direction from graphValue to neighbor
                # edgeweight is path from A to direction to A + 1 in the subgraph
                if useBase:
                    if (prevDir, direction) not in memo:
                        memo[(prevDir, direction)] = graphBase.getShortestPathDistance(prevDir, direction)
                else:
                    if (prevDir, direction) not in memo:
                        memo[(prevDir, direction)] = graphBase.getShortestPathDistance(
                            (prevDir, 'A'), (direction, 'A')
                        )

                yield (neighbor, direction), memo[(prevDir, direction)] + 1

            if not prevDir == 'A':
                if useBase:
                    if (prevDir, 'A') not in memo:
                        memo[(prevDir, 'A')] = graphBase.getShortestPathDistance(prevDir, 'A')
                else:
                    if (prevDir, 'A') not in memo:
                        memo[(prevDir, 'A')] = graphBase.getShortestPathDistance((prevDir, 'A'), ('A', 'A'))

                yield (graphValue, 'A'), memo[(prevDir, 'A')]

        return getNeighbors

    newGraph = startGraph
    for i in range(numOfGraphs - 1):

        if i == 0:
            newGraph = FreeFormGraph(getGetNeighbors(newGraph, True))
        else:
            newGraph = FreeFormGraph(getGetNeighbors(newGraph, False))

    def getNumericNeighbors(graphValue):
        if graphValue == 'A':
            yield '0', 1
            yield '3', 1
        elif graphValue == '0':
            yield 'A', 1
            yield '2', 1
        else:
            graphValue = int(graphValue)
            left = graphValue - 1
            if left % 3 > 0 and left > 0:
                yield str(left), 1
            right = graphValue + 1
            if not right % 3 == 1 and right > 1:
                yield str(right), 1
            up = graphValue + 3
            if up <= 9:
                yield str(up), 1
            down = graphValue - 3
            if down > 0:
                yield str(down), 1

        if graphValue == 2:
            yield '0', 1
        if graphValue == 3:
            yield 'A', 1

    def getNumericalDirection(i, j):
        if i == 'A':
            if j == '0':
                return '<'
            elif j == '3':
                return '^'
        elif i == '0':
            if j == 'A':
                return '>'
            elif j == '2':
                return '^'
        elif i == '2' and j =='0':
            return 'v'
        elif i == '3' and j == 'A':
            return 'v'
        i = int(i)
        j = int(j)
        diff = i - j
        if diff == -3:
            return '^'
        elif diff == 3:
            return 'v'
        elif diff == 1:
            return '<'
        elif diff == -1:
            return '>'
        print("ERROR")

    def getGetNumericalNeighbors(graphBase, useBase=False):
        memo = {}

        def getNeighbors(graphValue):
            graphValue, prevDir = graphValue
            for neighbor, _ in getNumericNeighbors(graphValue):
                direction = getNumericalDirection(graphValue, neighbor)
                if direction == prevDir:
                    yield (neighbor, direction), 1
                # get direction from graphValue to neighbor
                # edgeweight is path from A to direction to A + 1 in the subgraph
                if useBase:
                    if (prevDir, direction) not in memo:
                        memo[(prevDir, direction)] = graphBase.getShortestPathDistance(prevDir, direction)
                else:
                    if (prevDir, direction) not in memo:
                        memo[(prevDir, direction)] = graphBase.getShortestPathDistance(
                            (prevDir, 'A'), (direction, 'A')
                        )

                yield (neighbor, direction), memo[(prevDir, direction)] + 1
            if not prevDir == 'A':
                if useBase:
                    if (prevDir, 'A') not in memo:
                        memo[(prevDir, 'A')] = graphBase.getShortestPathDistance(prevDir, 'A')
                else:
                    if (prevDir, 'A') not in memo:
                        memo[(prevDir, 'A')] = graphBase.getShortestPathDistance((prevDir, 'A'), ('A', 'A'))

                yield (graphValue, 'A'), memo[(prevDir, 'A')]

        return getNeighbors

    return FreeFormGraph(getGetNumericalNeighbors(newGraph, (numOfGraphs <= 1)))


def get_ans(data, prob=2):
    data = format_data(data)
    if prob == 1:
        numRobots = 2
    else:
        numRobots = 25
    graph = getGraph(numRobots)
    total = 0
    for row in data:
        start = ('A', 'A')
        curr = 0
        for i in row:
            end = (i, 'A')
            curr = curr + graph.getShortestPathDistance(start, end) + 1
            start = end
        total = total + curr * int(''.join(row[:-1]))

    return total


def get_ans_1(data):
    data = format_data(data)
    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]
    # +---+---+---+
    # | 7 | 8 | 9 |
    # +---+---+---+
    # | 4 | 5 | 6 |
    # +---+---+---+
    # | 1 | 2 | 3 |
    # +---+---+---+
    #     | 0 | A |
    #     +---+---+
    numericKeyPadGraph = [
        [7, 8, 9],
        [4, 5, 6],
        [1, 2, 3],
        [None, 0, 'A']
    ]

    @lru_cache(maxsize=None)
    def getNumericPos(number):
        for i in range(len(numericKeyPadGraph)):
            for j in range(len(numericKeyPadGraph[0])):
                if numericKeyPadGraph[i][j] == number:
                    return i, j

    #     +---+---+
    #     | ^ | A |
    # +---+---+---+
    # | < | v | > |
    # +---+---+---+
    directionKeyPadGraph = [
        [None, '^', 'A'],
        ['<', 'v', '>']
    ]
    directionMap = {
        '^': (-1, 0),
        '>': (0, 1),
        '<': (0, -1),
        'v': (1, 0)
    }

    @lru_cache(maxsize=None)
    def getDirectionPos(direction):
        for i in range(len(directionKeyPadGraph)):
            for j in range(len(directionKeyPadGraph[0])):
                if directionKeyPadGraph[i][j] == direction:
                    return i, j

    start = ('A', 'A', 'A')
    keyPadValues = {'A', '<', '>', '^', 'v'}
    numericValues = {'A', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    graphValues = []
    for i in keyPadValues:
        for j in keyPadValues:
            for k in numericValues:
                graphValues.append((i, j, k))
    graphEdges = []

    def getNeighbors(graphValue):
        x, y = getDirectionPos(graphValue[0])
        for x1, y1 in directions:
            if 0 <= x + x1 < len(directionKeyPadGraph) and 0 <= y + y1 < len(directionKeyPadGraph[0]):
                if directionKeyPadGraph[x + x1][y + y1] is not None:
                    yield directionKeyPadGraph[x + x1][y + y1], graphValue[1], graphValue[2]
        # Handle pressing A
        pos = 0
        while pos < len(graphValue) and graphValue[pos] == 'A':
            pos = pos + 1
        if not pos >= len(graphValue) - 1:
            x1, y1 = directionMap[graphValue[pos]]
            if pos == len(graphValue) - 2:
                x, y = getNumericPos(graphValue[pos + 1])
                if 0 <= x + x1 < len(numericKeyPadGraph) and 0 <= y + y1 < len(numericKeyPadGraph[0]):
                    if numericKeyPadGraph[x + x1][y + y1] is not None:
                        yield graphValue[0], graphValue[1], numericKeyPadGraph[x + x1][y + y1]
            else:
                x, y = getDirectionPos(graphValue[pos + 1])
                if 0 <= x + x1 < len(directionKeyPadGraph) and 0 <= y + y1 < len(directionKeyPadGraph[0]):
                    if directionKeyPadGraph[x + x1][y + y1] is not None:
                        yield graphValue[0], directionKeyPadGraph[x + x1][y + y1], graphValue[2]
        return

    for i in graphValues:
        for neighbor in getNeighbors(i):
            graphEdges.append([i, neighbor, 1])
    graph = AdjacencyGraph(graphEdges, True)
    total = 0
    for row in data:
        curr = 0
        start = ('A', 'A', 'A')
        for i in range(len(row) - 1):
            end = ('A', 'A', int(row[i]))
            curr = curr + graph.getShortestPathDistance(start, end) + 1
            start = ('A', 'A', int(row[i]))
        end = ('A', 'A', 'A')
        curr = curr + graph.getShortestPathDistance(start, end) + 1
        total = total + curr * int(''.join(row)[:-1])
    return total


def format_data(data):
    data = data.split('\n')
    ret = []
    for i in data:
        ret.append(list(i))
    return ret
