def get_ans(data, num=2):
    data = format_data(data)
    visited = set()
    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]

    def getRegion(pos):
        area = 1
        perimeter = 0
        sides = 0
        value = data[pos[0]][pos[1]]
        stack = [pos]
        visited.add(pos)

        def getCorners(pos):
            value = data[pos[0]][pos[1]]
            corners = 0
            x, y = pos
            # Count all corners of the following form (R is region we are looking at X is not)
            #   RX
            #   X
            # accounting for rotations of the above
            for i in range(len(directions)):
                xDelta, yDelta = directions[i]
                xDelta2, yDelta2 = directions[(i + 1) % 4]
                check = True
                if (0 <= x + xDelta < len(data) and 0 <= y + yDelta < len(data[0])
                        and value == data[x + xDelta][y + yDelta]):
                    check = False
                if (0 <= x + xDelta2 < len(data) and 0 <= y + yDelta2 < len(data[0])
                        and value == data[x + xDelta2][y + yDelta2]):
                    check = False
                if check:
                    corners = corners + 1

            # Count all corners of the following form (R is region we are looking at X is not)
            # XR
            # R
            # accounting for rotations of the above
            for i in range(len(directions)):
                xDelta, yDelta = directions[i]
                xDelta2, yDelta2 = directions[(i + 1) % 4]
                fxDelta = xDelta + xDelta2
                fyDelta = yDelta + yDelta2
                check = True
                if not (0 <= x + xDelta < len(data) and 0 <= y + yDelta < len(data[0])
                        and value == data[x + xDelta][y + yDelta]):
                    check = False
                if not (0 <= x + xDelta2 < len(data) and 0 <= y + yDelta2 < len(data[0])
                        and value == data[x + xDelta2][y + yDelta2]):
                    check = False
                if not (0 <= x + fxDelta < len(data) and 0 <= y + fyDelta < len(data[0])
                        and not value == data[x + fxDelta][y + fyDelta]):
                    check = False
                if check:
                    corners = corners + 1

            return corners

        while len(stack) > 0:
            curr = stack.pop()
            x, y = curr
            for xDelta, yDelta in directions:
                if 0 <= x + xDelta < len(data) and 0 <= y + yDelta < len(data[0]):
                    if value == data[x + xDelta][y + yDelta]:
                        if (x + xDelta, y + yDelta) not in visited:
                            area = area + 1
                            stack.append((x + xDelta, y + yDelta))
                            visited.add((x + xDelta, y + yDelta))
                    else:
                        perimeter = perimeter + 1
                else:
                    perimeter = perimeter + 1
            sides = sides + getCorners(curr)
        return area, perimeter, sides

    total = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            if (i, j) not in visited:
                area, perimeter, sides = getRegion((i, j))
                if num == 1:
                    total = total + area * perimeter
                else:
                    total = total + area * sides

    return total


def format_data(data):
    data = data.split('\n')
    ret = []
    for i in data:
        ret.append(list(i))
    return ret
