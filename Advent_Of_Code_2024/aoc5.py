from collections import defaultdict
from functools import lru_cache
from copy import deepcopy
from aoc_apis import create_graph


def get_ans(data):
    nodes, data = format_data(data)
    graph = create_graph(nodes)

    def isCorrectOrder(before, after):
        if before in graph and after in graph[before]:
            return True
        return False

    def isSorted(row):
        for i in range(len(row)):
            for j in range(i):
                if not isCorrectOrder(row[j], row[i]):
                    return False
        return True

    def comparator(tup):
        x, y = tup
        if x in graph and y in graph[x]:
            return 1
        else:
            return -1

    def scoreRow(row):
        scores = defaultdict(int)
        for i in range(len(row)):
            for j in range(i):
                if not isCorrectOrder(row[j], row[i]):
                    scores[row[j]] = scores[row[j]] + 1
                else:
                    scores[row[i]] = scores[row[i]] + 1
        return scores

    total = 0
    for row in data:
        if not isSorted(row):
            scores = scoreRow(row)
            row.sort(key=lambda x: scores[x])
            total = total + int(row[(len(row) - 1) // 2])
    return total


def get_ans_1(data):
    nodes, data = format_data(data)
    graph = create_graph(nodes)

    def isCorrectOrder(before, after):
        if before in graph and after in graph[before]:
            return True
        return False

    def isSorted(row):
        for i in range(len(row)):
            for j in range(i):
                if not isCorrectOrder(row[j], row[i]):
                    return False
        return True

    total = 0
    for row in data:
        if isSorted(row):
            total = total + int(row[(len(row) - 1) // 2])
    return total


def format_data(data):
    data = data.split('\n\n')
    nodes, data = data
    nodeList = []
    nodes = nodes.split('\n')
    data = data.split('\n')

    for i in nodes:
        curr = i.split('|')
        nodeList.append(curr)
    for i in range(len(data)):
        data[i] = data[i].split(',')
    return nodeList, data
