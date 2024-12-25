def get_ans(data):
    data = format_data(data)
    data = set([tuple(i) for i in data])
    currData = data
    nextData = set()
    vals = set()
    rels = {}

    def addToRel(n1, n2):
        if n1 in rels:
            rels[n1].add(n2)
        else:
            rels[n1] = {n2}
    for n1, n2 in data:
        addToRel(n1, n2)
        addToRel(n2, n1)
        vals.add(n1)
        vals.add(n2)

    while len(currData) > 1:
        # get all the possible tuples of the next size
        for group in currData:
            currGroup = set(group)
            for val in vals:
                if val not in currGroup:
                    check = True
                    for member in group:
                        if member not in rels[val]:
                            check = False
                            break
                    if check:
                        toAdd = [i for i in group]
                        toAdd.append(val)
                        toAdd.sort()
                        nextData.add(tuple(toAdd))

        currData = nextData
        nextData = set()
    currData = list(currData)
    ret = list(currData[0])
    return ','.join(ret)


def get_ans_1(data):
    data = format_data(data)
    rels = {}

    def addToRel(n1, n2):
        if n1 in rels:
            rels[n1].add(n2)
        else:
            rels[n1] = {n2}

    tset = set()
    for n1, n2 in data:
        addToRel(n1, n2)
        addToRel(n2, n1)
        if n1[0] == 't':
            tset.add(n1)
        if n2[0] == 't':
            tset.add(n2)
    threeSets = set()
    for tEl in tset:
        for el in rels[tEl]:
            for third in rels[el]:
                if third in rels[tEl]:
                    triple = [tEl, el, third]
                    triple.sort()
                    threeSets.add(tuple(triple))
    return len(threeSets)


def format_data(data):
    data = data.split('\n')
    ret = []
    for row in data:
        curr = row.split('-')
        curr.sort()
        ret.append(curr)
    return ret
