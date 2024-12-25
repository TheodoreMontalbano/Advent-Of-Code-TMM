from collections import deque


def getNextValue(sNumber):
    def pruneSN(sNumber):
        PRUNE_MOD = 16777216
        return sNumber % PRUNE_MOD

    def mixSN(sNumber, toMix):
        return sNumber ^ toMix

    sNumber = mixSN(sNumber, sNumber * 64)
    sNumber = pruneSN(sNumber)

    sNumber = mixSN(sNumber, sNumber // 32)
    sNumber = pruneSN(sNumber)

    sNumber = mixSN(sNumber, 2048 * sNumber)
    sNumber = pruneSN(sNumber)
    return sNumber


def get_ans(data, prob=2):
    data = format_data(data)
    amt = 2000
    total = 0
    seqScores = {}
    visited = set()

    def processSeq(num, prev, sequence):
        num = num % 10
        prev = prev % 10
        diff = num - prev
        if len(sequence) >= 4:
            sequence.popleft()
        sequence.append(diff)
        if len(sequence) == 4:
            curr = tuple(sequence)
            if curr not in visited:
                if curr in seqScores:
                    seqScores[curr] = seqScores[curr] + num
                else:
                    seqScores[curr] = num
                visited.add(curr)

    for i in data:
        num = int(i)
        prev = None
        seq = deque()
        visited = set()
        for j in range(amt):
            prev = num
            num = getNextValue(num)
            processSeq(num, prev, seq)
        total = total + num
    if prob == 1:
        return total
    else:
        temp = [(i, seqScores[i]) for i in seqScores.keys()]
        temp.sort(reverse=True, key=lambda x: x[1])
        return temp[0][1]


def format_data(data):
    data = data.split('\n')
    return data
