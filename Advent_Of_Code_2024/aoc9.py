from collections import deque
from aoc_apis import DoublyLinkedList


def get_ans(data):
    data = list(format_data(data))

    dll = DoublyLinkedList(data)
    curr = dll.tail
    while curr.prev is not None:

        if curr.val[0] >= 0:
            # Find first empty space to slot file into
            currNode = dll.head
            while not (currNode == curr) and not (currNode.val[0] == -1 and currNode.val[1] >= curr.val[1]):
                currNode = currNode.next
            if not currNode == curr:
                dll.addNodeBefore(currNode, curr.val)

                # Reduce space
                _, space = currNode.val
                space = space - curr.val[1]
                currNode.val = (-1, space)

                # Add space to replace old instance of curr
                dll.addNodeAfter(curr, (-1, curr.val[1]))

                # Delete old instance of curr
                toDelete = curr
                curr = curr.prev
                dll.deleteNode(toDelete)
            else:
                curr = curr.prev
        else:
            curr = curr.prev

    editedData = dll.toList()
    total = 0
    pos = 0
    for id, num in editedData:
        for i in range(num):
            if id >= 0:
                total = total + id * pos
            pos = pos + 1

    return total


def get_ans_1(data):
    data = format_data(data)
    editedData = []
    while len(data) > 0:
        id, space = data.popleft()
        if id >= 0:
            editedData.append((id, space))
        else:
            while len(data) > 0 and space > 0:
                toAddId, toAddSpace = data.pop()
                if toAddId >= 0:
                    if toAddSpace <= space:
                        space = space - toAddSpace
                        editedData.append((toAddId, toAddSpace))
                    else:
                        toAddSpace = toAddSpace - space
                        editedData.append((toAddId, space))
                        data.append((toAddId, toAddSpace))
                        space = 0
    total = 0
    pos = 0
    for id, num in editedData:
        for i in range(num):
            total = total + id * pos
            pos = pos + 1

    return total


def format_data(data):
    data = [int(i) for i in list(data)]
    ret = deque()
    id = 0
    for i in range(len(data)):
        if i % 2 == 0:
            ret.append((id, data[i]))
            id = id + 1
        else:
            ret.append((-1, data[i]))
    return ret
