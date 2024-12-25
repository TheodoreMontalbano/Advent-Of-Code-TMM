from functools import lru_cache


def get_ans(data, num=2):
    map, instructions = format_data(data, num)
    start = None
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == '@':
                start = (i, j)
                break
    directionsToMove = {
        '^': (-1, 0),
        '>': (0, 1),
        '<': (0, -1),
        'v': (1, 0)
    }

    def movebot(move, pos):
        xdir, ydir = directionsToMove[move]
        newPos = xdir + pos[0], ydir + pos[1]
        xNew, yNew = newPos
        if num == 1:
            while map[xNew][yNew] == 'O':
                xNew, yNew = xdir + xNew, ydir + yNew
            if map[xNew][yNew] == '#':
                return pos
            else:
                map[xNew][yNew] = 'O'
                xNew, yNew = newPos
                map[xNew][yNew] = '@'
                x, y = pos
                map[x][y] = '.'
                return newPos
        else:
            boxPos = None

            def moveBox(boxPos, direction):
                if boxPos is None:
                    return
                newBoxPos = []
                xdir, ydir = direction
                for x, y in boxPos:
                    newBoxPos.append((x + xdir, y + ydir))
                newBoxPos = tuple(newBoxPos)
                currPosList = {boxPos[0], boxPos[1]}
                boxesInFront = set()
                for x, y in newBoxPos:
                    if map[x][y] == '[' and not (x, y) in currPosList:
                        boxesInFront.add(((x, y), (x, y + 1)))
                    elif map[x][y] == ']' and not (x, y) in currPosList:
                        boxesInFront.add(((x, y - 1), (x, y)))

                for box in boxesInFront:
                    moveBox(box, direction)
                map[newBoxPos[0][0]][newBoxPos[0][1]] = '['
                map[newBoxPos[1][0]][newBoxPos[1][1]] = ']'
                if not (boxPos[0] == newBoxPos[0] or boxPos[0] == newBoxPos[1]):
                    map[boxPos[0][0]][boxPos[0][1]] = '.'
                if not (boxPos[1] == newBoxPos[0] or boxPos[1] == newBoxPos[1]):
                    map[boxPos[1][0]][boxPos[1][1]] = '.'

            @lru_cache(maxsize=None)
            def canMoveBox(boxPos, direction):
                if boxPos is None:
                    return True
                newBoxPos = []
                xdir, ydir = direction
                for x, y in boxPos:
                    newBoxPos.append((x + xdir, y + ydir))
                newBoxPos = tuple(newBoxPos)
                currPosList = {boxPos[0], boxPos[1]}
                boxesInFront = set()
                for x, y in newBoxPos:
                    if map[x][y] == '[' and not (x, y) in currPosList:
                        boxesInFront.add(((x, y), (x, y + 1)))
                    elif map[x][y] == ']' and not (x, y) in currPosList:
                        boxesInFront.add(((x, y - 1), (x, y)))
                    elif map[x][y] == '#':
                        return False

                for box in boxesInFront:
                    if not canMoveBox(box, direction):
                        return False
                return True

            if map[xNew][yNew] == '[':
                boxPos = (xNew, yNew), (xNew, yNew + 1)
            elif map[xNew][yNew] == ']':
                boxPos = (xNew, yNew - 1), (xNew, yNew)
            elif map[xNew][yNew] == '#':
                return pos
            if canMoveBox(boxPos, (xdir, ydir)):
                moveBox(boxPos, (xdir, ydir))
                map[xNew][yNew] = '@'
                x, y = pos
                map[x][y] = '.'
                return newPos
            else:
                return pos

    curr = start
    for move in instructions:

        curr = movebot(move, curr)
        toPrint = [''.join(i) for i in map]
        print(move)
        print('\n'.join(toPrint))
        print()
    total = 0
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == '[':
                total = total + 100 * i + j
            if map[i][j] == 'O':
                total = total + 100 * i + j
    return total


def format_data(data, num=2):
    data = data.split('\n\n')
    map = data[0]
    map = map.split('\n')
    for i in range(len(map)):
        map[i] = list(map[i])
    instructions = data[1]
    instructions = instructions.replace('\n', '')
    instructions = list(instructions)
    if num == 2:
        # widen data
        data = map
        map = []
        for i in data:
            row = []
            for j in i:
                if j == '#':
                    row.append('#')
                    row.append('#')
                elif j == '.':
                    row.append('.')
                    row.append('.')
                elif j == 'O':
                    row.append('[')
                    row.append(']')
                else:
                    row.append('@')
                    row.append('.')
            map.append(row)

    return map, instructions
