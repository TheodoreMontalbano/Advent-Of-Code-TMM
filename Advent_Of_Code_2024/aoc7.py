def get_ans(data):
    data = format_data(data)
    total = 0

    def canEqual(target, nums):
        def incTernaryNum(ternaryNum=None):
            if ternaryNum is None:
                return [0] * (len(nums) - 1)
            else:
                ternaryNum[len(ternaryNum) - 1] = (ternaryNum[len(ternaryNum) - 1] + 1) % 3
                carry = int(ternaryNum[len(ternaryNum) - 1] == 0)
                if carry > 0:
                    for i in range(len(ternaryNum) - 1):
                        j = len(ternaryNum) - i - 2
                        if ternaryNum[j] >= 2:
                            nextCarry = 1
                        else:
                            nextCarry = 0
                        ternaryNum[j] = (ternaryNum[j] + carry) % 3
                        carry = nextCarry
                        if carry == 0:
                            break
                if sum(ternaryNum) == 0:
                    return None
                else:
                    return ternaryNum

        curr = incTernaryNum()
        while True:
            if curr is None:
                break
            start = int(nums[0])
            for i in range(1, len(nums)):
                if curr[i - 1] == 0:
                    start = start * int(nums[i])
                elif curr[i - 1] == 1:
                    start = start + int(nums[i])
                else:
                    start = int(str(start) + nums[i])
            if start == int(target):
                return True
            curr = incTernaryNum(curr)
        return False

    total = 0
    for row in data:
        if canEqual(row[0], row[1]):
            total = total + int(row[0])
    return total


def get_ans_1(data):
    data = format_data(data)
    total = 0

    def canEqual(target, nums):
        def incBinaryNum(binaryNum=None):
            if binaryNum is None:
                return [0] * (len(nums) - 1)
            else:
                binaryNum[len(binaryNum) - 1] = (binaryNum[len(binaryNum) - 1] + 1) % 2
                carry = int(binaryNum[len(binaryNum) - 1] == 0)
                if carry > 0:
                    for i in range(len(binaryNum) - 1):
                        j = len(binaryNum) - i - 2
                        if binaryNum[j] >= 1:
                            nextCarry = 1
                        else:
                            nextCarry = 0
                        binaryNum[j] = (binaryNum[j] + carry) % 2
                        carry = nextCarry
                        if carry == 0:
                            break
                if sum(binaryNum) == 0:
                    return None
                else:
                    return binaryNum

        curr = incBinaryNum()
        while True:
            if curr is None:
                break
            start = int(nums[0])
            for i in range(1, len(nums)):
                if curr[i - 1] == 0:
                    start = start * int(nums[i])
                else:
                    start = start + int(nums[i])
            if start == int(target):
                return True
            curr = incBinaryNum(curr)
        return False

    total = 0
    for row in data:
        if canEqual(row[0], row[1]):
            total = total + int(row[0])
    return total


def format_data(data):
    data = data.split('\n')
    ret = []
    for i in data:
        curr = i.split(':')
        curr[1] = curr[1][1:].split(' ')
        ret.append(curr)
    return ret
