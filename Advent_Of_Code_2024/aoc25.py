def convertToHeight(val, lock):
    if not lock:
        return convertToHeight(val[::-1], True)

    ret = []
    for i in range(len(val[0])):
        j = 0
        while j < len(val) and val[j][i] == '#':
            j = j + 1
        ret.append(j - 1)
    return tuple(ret)


def get_ans(data):
    locks, keys = format_data(data)
    hLocks = [convertToHeight(i, True) for i in locks]
    hKeys = [convertToHeight(i, False) for i in keys]
    total = 0
    for lock in hLocks:
        for key in hKeys:
            check = True
            for i in range(5):
                if lock[i] + key[i] > 5:
                    check = False
            if check:
                total = total + 1
    # Keys bottom marked off
    # locks top marked off
    return total


def format_data(data):
    data = data.split('\n\n')
    locks = []
    keys = []
    for i in data:
        toAdd = []
        curr = i.split('\n')
        for j in curr:
            toAdd.append(list(j))
        if curr[0] == '#####':
            locks.append(toAdd)
        else:
            keys.append(toAdd)
    return locks, keys
