from queue import PriorityQueue


def get_ans(data, num=2):
    stringData = data
    if num == 1:
        data = set(format_data(data, 1024))
    else:
        data = set(format_data(data))
    start = (0, 0)
    exit = (70, 70)
    directions = [
        (0, 1),
        (1, 0),
        (-1, 0),
        (0, -1)
    ]

    def getShortestPath(start, exit):
        visited = set()
        pqueue = PriorityQueue()
        pqueue.put((0, start))
        while not pqueue.empty():
            distance, (currX, currY) = pqueue.get()
            if (currX, currY) not in visited:
                visited.add((currX, currY))
            else:
                continue

            if (currX, currY) == exit:
                return distance
            else:
                for x, y in directions:
                    newPos = (x + currX, y + currY)
                    if (newPos not in data) and 0 <= newPos[0] <= exit[0] and 0 <= newPos[1] <= exit[1]:
                        pqueue.put((distance + 1, newPos))
        return -1
    # toPrint = []
    # for i in range(7):
    #     curr = []
    #     for j in range(7):
    #         curr.append('.')
    #     toPrint.append(curr)
    # for x, y in data:
    #     toPrint[int(x)][int(y)] = '#'
    #
    # ret = []
    # for i in toPrint:
    #     ret.append(''.join(i))
    # print('\n'.join(ret))

    if num == 1:
        return getShortestPath(start, exit)
    else:
        i = 0
        j = len(data) - 1
        while j - i > 1:
            midPoint = (i + j) // 2
            data = set(format_data(stringData, midPoint))
            if getShortestPath(start, exit) == -1:
                j = midPoint
            else:
                i = midPoint
        currData = format_data(stringData)
        data = set(format_data(stringData, j))
        print(i, j)
        if not getShortestPath(start, exit) == -1:
            return currData[j - 1]
        data = set(format_data(stringData, i))
        if not getShortestPath(start, exit) == -1:
            print(currData[i] in data)
            return currData[i]
        return -1


def format_data(data, cutoff=None):
    data = data.split('\n')
    ret = []
    for i in data:
        curr = i.split(',')
        ret.append((int(curr[0]), int(curr[1])))
    if cutoff is None:
        return ret
    return ret[:cutoff]
