from queue import PriorityQueue
from copy import deepcopy

def get_ans(data, num=2):
    directions = [
        (0, 1),
        (1, 0),
        (-1, 0),
        (0, -1)
    ]
    data = format_data(data)
    start = None
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i][j] == 'S':
                start = (i, j)
                break

    def getShortestPath(start):
        visited = set()
        pqueue = PriorityQueue()
        pqueue.put((0, start, 0))
        while not pqueue.empty():
            points, (currX, currY), currDir = pqueue.get()
            if (currX, currY) not in visited:
                visited.add((currX, currY))
            else:
                continue

            if data[currX][currY] == 'E':
                return points
            else:
                for x, y in directions:
                    if not data[x + currX][y + currY] == '#':
                        newPos = (x + currX, y + currY)
                        if currDir is None or (x, y) == currDir:
                            pqueue.put((points + 1, newPos, (x, y)))
                        else:
                            pqueue.put((points + 1001, newPos, (x, y)))
        return -1

    shortestPath = getShortestPath(start)
    if num == 1:
        return shortestPath
    else:
        def getAllShortestPathTiles(start, bestPath=None):
            visited = {}
            pqueue = PriorityQueue()
            allTiles = set()
            pqueue.put((0, start, 0, [(start, (0, 1))]))
            relatedTiles = {}
            while not pqueue.empty():
                points, (currX, currY), currDir, currPath = pqueue.get()
                print(points)
                if ((currX, currY), currDir) not in visited:
                    visited[((currX, currY), currDir)] = points
                    relatedTiles[((currX, currY), currDir)] = set()
                else:
                    if points == visited[((currX, currY), currDir)]:
                        for i in currPath:
                            relatedTiles[((currX, currY), currDir)].add(i[0])
                    continue

                if bestPath is not None and points > bestPath:
                    break
                elif data[currX][currY] == 'E':
                    if bestPath is None:
                        bestPath = points
                    for i in currPath:
                        allTiles.add(i)
                else:
                    for x, y in directions:
                        if not data[x + currX][y + currY] == '#':
                            newPos = (x + currX, y + currY)
                            newPath = deepcopy(currPath)

                            if currDir is None or (x, y) == currDir:
                                pqueue.put((points + 1, newPos, (x, y), newPath))
                                newPath.append((newPos, (x, y)))
                            else:
                                pqueue.put((points + 1001, newPos, (x, y), newPath))
                                newPath.append((newPos, (x, y)))
            ret = set()
            for i in allTiles:
                ret.add(i[0])
                if i in relatedTiles:
                    for j in relatedTiles[i]:
                        ret.add(j)
            return ret
        ans = getAllShortestPathTiles(start, shortestPath)
        ###########
        for x, y in ans:
            data[x][y] = 'O'
        print('\n'.join([''.join(i) for i in data]))
        ###########
        return len(ans)


def format_data(data):
    data = data.split('\n')
    ret = []
    for i in data:
        ret.append(list(i))
    return ret
