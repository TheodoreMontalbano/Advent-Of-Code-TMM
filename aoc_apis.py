from __future__ import annotations

from copy import deepcopy
from operator import mul
from functools import reduce
from math import factorial
from aocd import get_data
from datetime import date
from queue import PriorityQueue


def get_session_cookie():
    f = open("sensitive.txt", "r")
    return f.read()


def load_data(day=-1, year=-1):
    session_cookie = get_session_cookie()
    today = date.today()
    if day == -1:
        day = today.day
    if year == -1:
        year = today.year
    prod = get_data(session=session_cookie, day=day, year=year)
    return prod


# returns if the two given intervals overlap
def has_overlap(interval_one, interval_two):
    if max(interval_one[0], interval_two[0]) <= min(interval_two[1], interval_one[1]):
        return True
    return False


# creates array of difference of input
def get_differences(value_list: list[int]) -> list[int]:
    ret = []
    for i in range(len(value_list) - 1):
        ret.append(value_list[i + 1] - value_list[i])
    print(ret)
    return ret


# Creates polynomial func from difference tables of input
def values_to_polynomial(value_list: list[int]):
    curr = get_differences(value_list)
    differences_list = [value_list, curr]
    while len(curr) > 1 or max(curr) > 0:
        curr = get_differences(curr)
        differences_list.append(curr)

    def poly(x: float) -> float:
        ret = 0
        for i in range(len(differences_list)):
            val = 1
            for j in range(i):
                val = val * (x - j)
            ret = val / factorial(i) * differences_list[i][0] + ret
        return ret

    return poly


# creates a graph from a list of edges represented as [node1, node2]
def create_graph(nodes, directed=True):
    graph = {}

    def addDirectedEdge(node1, node2):
        if node1 in graph:
            graph[node1].append(node2)
        else:
            graph[node1] = [node2]

    def addEdge(node1, node2):
        addDirectedEdge(node1, node2)
        addDirectedEdge(node2, node1)

    for source, dest in nodes:
        if directed:
            addDirectedEdge(source, dest)
        else:
            addEdge(source, dest)

    return graph


# Rotates a 2d array
def rotate_2D_arr(data):
    return list(zip(*data[::-1]))


# region Models

# region Graphs

class FreeFormGraph:

    # getNeighbors is also assumed to return edgeWeights
    def __init__(self, getNeighbors):
        self.__getNeighbors = getNeighbors

    def getShortestPathDistance(self, start, end):
        pqueue = PriorityQueue()
        pqueue.put((0, start))
        visited = set()
        while not pqueue.empty():
            currDist, curr = pqueue.get()
            if curr in visited:
                continue
            else:
                visited.add(curr)
            if curr == end:
                return currDist
            else:
                for neighbor, weight in self.__getNeighbors(curr):
                    pqueue.put((currDist + weight, neighbor))
        return -1


class GraphVertice:

    def __init__(self, id, value=None, edges: list = None):
        self.id = id
        self.value = value
        if edges is None:
            self.edges = []
        else:
            self.edges = edges

    def addEdge(self, neighbor, weight=None):
        if weight is None:
            weight = 1
        self.edges.append((neighbor, weight))

    # TODO
    def __lt__(self, other):
        return True

    def __gt__(self, other):
        return True


class AdjacencyGraph:

    def __init__(self, edges, directed=False):
        self.__vertices = {}
        for source, dest, weight in edges:
            if directed:
                self.addDirectedEdge(source, dest, weight)
            else:
                self.addEdge(source, dest, weight)

    def addDirectedEdge(self, node1, node2, weight=None):
        _ = self.addNode(node1)
        n1 = self.getVerticeFromId(node1)
        _ = self.addNode(node2)
        n2 = self.getVerticeFromId(node2)
        n1.addEdge(n2, weight)

    def addEdge(self, node1, node2, weight=None):
        self.addDirectedEdge(node1, node2, weight)
        self.addDirectedEdge(node2, node1, weight)

    # Assumes all weights are positive
    def getShortestPathDistance(self, start, end) -> int:
        pqueue = PriorityQueue()
        pqueue.put((0, self.getVerticeFromId(start)))
        visited = set()
        while not pqueue.empty():
            currDist, curr = pqueue.get()
            currId = curr.id
            if currId in visited:
                continue
            else:
                visited.add(currId)
            if currId == end:
                return currDist
            else:
                for neighbor, weight in curr.edges:
                    pqueue.put((currDist + weight, neighbor))
        return -1

    def getShortestPath(self, start, end) -> list:
        pqueue = PriorityQueue()
        pqueue.put((0, self.getVerticeFromId(start), [self.getVerticeFromId(start)]))
        visited = set()
        while not pqueue.empty():
            currDist, curr, currPath = pqueue.get()
            currId = curr.id
            if currId in visited:
                continue
            else:
                visited.add(currId)
            if currId == end:
                return currPath
            else:
                for neighbor, weight in curr.edges:
                    newPath = deepcopy(currPath)
                    newPath.append(neighbor)
                    pqueue.put((currDist + weight, neighbor, newPath))
        return []

    def addNode(self, nodeId):
        if nodeId in self.__vertices:
            return False
        else:
            self.__vertices[nodeId] = GraphVertice(nodeId)
            return True

    # TODO

    # region TODOs
    def removeNode(self):
        return

    def __condenseGraph(self):
        return

    # endregion

    def getVerticeFromId(self, id) -> GraphVertice | None:
        if id in self.__vertices:
            return self.__vertices[id]
        else:
            return None


# endregion

# region LinkedList
class DoublyLinkedNode:
    def __init__(self, val=None, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev
        return


class DoublyLinkedList:

    def __init__(self, data=None):
        self.head = None
        self.tail = None
        if data:
            for i in data:
                self.addNode(i)
        return

    def __insertNode(self, prevNode, nextNode, newNode):
        newNode.prev = prevNode
        newNode.next = nextNode

        prevNode.next = newNode
        nextNode.prev = newNode

    def addNode(self, val):
        if self.head is None:
            self.head = DoublyLinkedNode(val)
            self.tail = self.head
        else:
            newNode = DoublyLinkedNode(val)
            self.tail.next = newNode
            newNode.prev = self.tail
            self.tail = newNode

    def addNodeAfter(self, node, val):
        if self.tail == node:
            self.addNode(val)
        else:
            newNode = DoublyLinkedNode(val)
            prevNode = node
            nextNode = node.next

            self.__insertNode(prevNode, nextNode, newNode)
        return

    def addNodeBefore(self, node, val):
        newNode = DoublyLinkedNode(val)
        if self.head == node:
            self.head.prev = newNode
            newNode.next = self.head
            self.head = newNode
        else:
            prevNode = node.prev
            nextNode = node

            self.__insertNode(prevNode, nextNode, newNode)
        return

    def deleteNode(self, node):
        if node == self.head:
            self.head = node.next
            if self.head:
                self.head.prev = None
            return
        if node == self.tail:
            self.tail = self.tail.prev
            if self.tail:
                self.tail.next = None
            return
        prevNode = node.prev
        nextNode = node.next

        prevNode.next = nextNode
        nextNode.prev = prevNode
        return

    def toList(self):
        ret = []
        curr = self.head
        while curr:
            ret.append(curr.val)
            curr = curr.next
        return ret

# endregion

# endregion
