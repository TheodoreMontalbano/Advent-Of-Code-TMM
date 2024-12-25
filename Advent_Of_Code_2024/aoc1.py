from collections import Counter


def get_ans(data):
    l1, l2 = format_data(data)
    count2 = Counter(l2)
    total = 0
    for i in l1:
        if i in count2:
            total = total + i * count2[i]
    return total


def get_ans_1(data):
    l1, l2 = format_data(data)
    l1.sort()
    l2.sort()
    total = 0
    for i in range(len(l1)):
        total = total + abs(l1[i] - l2[i])
    return total

def format_data(data):
    data = data.split('\n')
    l1 = []
    l2 = []
    for i in data:
        curr = i.split('   ')
        l1.append(int(curr[0]))
        l2.append(int(curr[1]))
    return l1, l2
