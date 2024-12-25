def populateAllVals(allVals, toEvalVals):
    def getValue(param1, expr, param2):
        if allVals[param1] is None:
            v1p1, v1expr, v1p2 = toEvalVals[param1]
            allVals[param1] = getValue(v1p1, v1expr, v1p2)
        v1 = allVals[param1]
        if allVals[param2] is None:
            v2p1, v2expr, v2p2 = toEvalVals[param2]
            allVals[param2] = getValue(v2p1, v2expr, v2p2)
        v2 = allVals[param2]
        if expr == 'XOR':
            return v1 ^ v2
        elif expr == 'AND':
            return v1 & v2
        elif expr == 'OR':
            return v1 | v2
        print("ERROR: Recursion depth should not have made it this far by problem specs", param1, expr, param2)

    for value in allVals.keys():
        if allVals[value] is None:
            p1, expr, p2 = toEvalVals[value]
            allVals[value] = getValue(p1, expr, p2)


def getLetterReg(letter, allVals):
    zNums = []
    for value in allVals.keys():
        if value[0] == letter:
            zNums.append((value, allVals[value]))
    zNums.sort(key=lambda x: x[0])
    ret = [i[1] for i in zNums]
    return ret


def binArrToNum(arr):
    return sum([2 ** i * arr[i] for i in range(len(arr))])


class LogicTreeNode:

    # operator could be the name
    def __init__(self, operator, name):
        self.__operator = operator
        self.__name = name
        self.leftChild = None
        self.rightChild = None

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getOperator(self):
        return self.__operator

    def __eq__(self, other):
        if other is None:
            return False
        elif not other.getOperator() == self.getOperator():
            return False
        else:
            c1 = self.leftChild == other.leftChild and self.rightChild == other.rightChild
            c2 = self.rightChild == other.leftChild and self.leftChild == other.rightChild
            return c1 or c2

    @staticmethod
    def __createTreeNode(treeNode1, treeNode2, name, operation):
        ret = LogicTreeNode(operation, name)
        ret.leftChild = treeNode1
        ret.rightChild = treeNode2
        return ret

    @staticmethod
    def createXOR(treeNode1, treeNode2, name=None):
        return LogicTreeNode.__createTreeNode(treeNode1, treeNode2, name, 'XOR')

    @staticmethod
    def createAND(treeNode1, treeNode2, name=None):
        return LogicTreeNode.__createTreeNode(treeNode1, treeNode2, name, 'AND')

    @staticmethod
    def createOR(treeNode1, treeNode2, name=None):
        return LogicTreeNode.__createTreeNode(treeNode1, treeNode2, name, 'OR')


# Validates boolean logic is in the proper format for summation
# assumes logic is in most reduced form
# Assumes len is greater than 2
def validateSummation(toEvalVals, allValues):
    validNodes = set()
    invalidNodes = []

    def getInvalidNode(currTree, properFormat):
        if not currTree.getOperator() == properFormat.getOperator():
            return currTree.getName(), properFormat
        ll = currTree.leftChild == properFormat.leftChild
        lr = currTree.leftChild == properFormat.rightChild
        rl = currTree.rightChild == properFormat.leftChild
        rr = currTree.rightChild == properFormat.rightChild
        if ll and not rr:
            return getInvalidNode(currTree.rightChild, properFormat.rightChild)
        elif rr and not ll:
            return getInvalidNode(currTree.leftChild, properFormat.leftChild)
        elif rl and not lr:
            return getInvalidNode(currTree.leftChild, properFormat.rightChild)
        elif lr and not rl:
            return getInvalidNode(currTree.rightChild, properFormat.leftChild)
        return currTree.getName(), properFormat

    # Adds a tree to the set of valid nodes
    def addToValid(tree: LogicTreeNode):
        if tree is None:
            return
        validNodes.add(tree.getName())
        addToValid(tree.leftChild)
        addToValid(tree.rightChild)

    def createLogicTree(base):
        if base not in toEvalVals:
            return LogicTreeNode(base, base)
        else:
            l, op, r = toEvalVals[base]
            ret = LogicTreeNode(op, base)
            ret.leftChild = createLogicTree(l)
            ret.rightChild = createLogicTree(r)
            return ret

    def updateNames(tree: LogicTreeNode, treeToName: LogicTreeNode):
        if tree is None:
            return
        treeToName.setName(tree.getName())
        if tree.leftChild == treeToName.leftChild:
            updateNames(tree.leftChild, treeToName.leftChild)
            updateNames(tree.rightChild, treeToName.rightChild)
        else:
            updateNames(tree.leftChild, treeToName.rightChild)
            updateNames(tree.rightChild, treeToName.leftChild)

    # Current Tree
    zZero = createLogicTree('z00')

    # Correct Tree
    left = LogicTreeNode('x00', 'x00')
    right = LogicTreeNode('y00', 'y00')
    properFormat = LogicTreeNode.createXOR(left, right)
    if zZero == properFormat:
        updateNames(zZero, properFormat)

    # Current Tree
    zOne = createLogicTree('z01')
    # Correct Tree
    bAND = LogicTreeNode.createAND(left, right)
    left = LogicTreeNode('x01', 'x01')
    right = LogicTreeNode('y01', 'y01')
    bXOR = LogicTreeNode.createXOR(left, right)
    properFormat = LogicTreeNode.createXOR(bXOR, bAND)
    if zOne == properFormat:
        updateNames(zOne, properFormat)

    currTree = createLogicTree('z02')

    # Proper Format
    uAND = LogicTreeNode.createAND(bAND, bXOR)
    bAND = LogicTreeNode.createAND(left, right)
    left = LogicTreeNode('x02', 'x02')
    right = LogicTreeNode('y02', 'y02')
    bXOR = LogicTreeNode.createXOR(left, right)
    uOR = LogicTreeNode.createOR(bAND, uAND)
    properFormat = LogicTreeNode.createXOR(uOR, bXOR)
    if properFormat == currTree:
        updateNames(currTree, properFormat)

    index = 3
    strIndex = '03'
    while 'x' + strIndex in allValues:
        # This is not the last zValue
        # zValue to Check
        zValue = 'z' + strIndex
        xValue = 'x' + strIndex
        yValue = 'y' + strIndex
        currTree = createLogicTree(zValue)

        # Proper Format
        uAND = LogicTreeNode.createAND(uOR, bXOR)
        bAND = LogicTreeNode.createAND(left, right)
        uOR = LogicTreeNode.createOR(uAND, bAND)
        left = LogicTreeNode(xValue, xValue)
        right = LogicTreeNode(yValue, yValue)
        bXOR = LogicTreeNode.createXOR(left, right)
        properFormat = LogicTreeNode.createXOR(bXOR, uOR)
        if not properFormat == currTree:
            n1, newTree = getInvalidNode(currTree, properFormat)
            n2 = None
            for i in toEvalVals:
                if createLogicTree(i) == newTree:
                    n2 = i
                    break
            invalidNodes.append(n1)
            invalidNodes.append(n2)
            temp = toEvalVals[n1]
            toEvalVals[n1] = toEvalVals[n2]
            toEvalVals[n2] = temp
            currTree = createLogicTree(zValue)

        addToValid(currTree)
        updateNames(currTree, properFormat)

        # increment index
        index = index + 1
        if index < 10:
            strIndex = '0' + str(index)
        else:
            strIndex = str(index)
    # TODO check final case

    return invalidNodes


def get_ans(data, num=2):
    allVals, toEvalVals = format_data(data)
    if num == 1:
        populateAllVals(allVals, toEvalVals)
        ret = getLetterReg('z', allVals)
        return binArrToNum(ret)
    else:
        arr = validateSummation(toEvalVals, allVals)
        arr.sort()
        populateAllVals(allVals, toEvalVals)
        xNum = binArrToNum(getLetterReg('x', allVals))
        yNum = binArrToNum(getLetterReg('y', allVals))
        return ','.join(arr)


def format_data(data):
    data = data.split('\n\n')
    data[0] = data[0].split('\n')
    data[1] = data[1].split('\n')

    allVals = {}
    for i in data[0]:
        curr = i.split(': ')
        allVals[curr[0]] = int(curr[1])
    logicExpr = {}
    for i in data[1]:
        curr = i.split(' ')
        logicExpr[curr[4]] = (curr[0], curr[1], curr[2])
        allVals[curr[4]] = None

    return allVals, logicExpr
