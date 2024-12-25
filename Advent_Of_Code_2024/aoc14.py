def get_ans(data, num=2):
    data = format_data(data)
    n = 101  # width
    m = 103  # height

    # n = 11
    # m = 7
    def getPositionAfter(robotData, seconds):
        currPos = robotData['P']
        velocity = robotData['V']
        velocity = velocity[0] * seconds, velocity[1] * seconds
        return (currPos[0] + velocity[0]) % n, (currPos[1] + velocity[1]) % m

    quadrants = [[0, 0], [0, 0]]

    def incrementQuadrants(pos):
        halfN = (n - 1) / 2
        halfM = (m - 1) / 2
        i = -1
        j = -1
        if pos[0] < halfN:
            i = 0
        elif pos[0] > halfN:
            i = 1
        if pos[1] < halfM:
            j = 0
        elif pos[1] > halfM:
            j = 1
        if i >= 0 and j >= 0:
            quadrants[i][j] = quadrants[i][j] + 1

    if num == 1:
        seconds = 100
        for robot in data:
            newPos = getPositionAfter(robot, seconds)
            incrementQuadrants(newPos)
        return quadrants[0][0] * quadrants[0][1] * quadrants[1][0] * quadrants[1][1]
    else:
        seen = set()

        def avgDistFromCenter(data):
            halfN = (n - 1) / 2
            halfM = (m - 1) / 2
            total = 0
            for robot in data:
                x, y = robot['P']
                total = total + abs(x - halfN) + abs(y - halfM)
            return total / len(data)

        def displayRobots(data):
            toPrint = []
            for i in range(m):
                toPrint.append(['.'] * n)
            for robot in data:
                x, y = robot['P']
                if toPrint[y][x] == '.':
                    toPrint[y][x] = 1
                else:
                    toPrint[y][x] = toPrint[y][x] + 1
            for i in range(len(toPrint)):
                for j in range(len(toPrint[0])):
                    toPrint[i][j] = str(toPrint[i][j])
            for i in range(len(toPrint)):
                toPrint[i] = ''.join(toPrint[i])
            return '\n'.join(toPrint)

        i = 0
        while True:
            for robot in data:
                robot['P'] = getPositionAfter(robot, 1)

            i = i + 1
            curr = displayRobots(data)
            if avgDistFromCenter(data) < 34:
                print(i)
                print(avgDistFromCenter(data))
                print(curr)
                print()
            if curr not in seen:
                seen.add(curr)
            else:
                break
        # i = 1
        # for pic in seen:
        #     print(i)
        #     print(pic)
        #     i = i + 1
        return len(seen)


def format_data(data):
    data = data.split('\n')
    ret = []

    def getData(value):
        value = value.split(',')
        return int(value[0][2:]), int(value[1])

    for row in data:
        curr = row.split(' ')
        toAdd = {}
        toAdd['P'] = getData(curr[0])
        toAdd['V'] = getData(curr[1])
        ret.append(toAdd)
    return ret
