def get_ans(data):
    toMult = format_data(data)
    return sum([i[0] * i[1] for i in toMult])


def format_data(data):
    ret = []
    index = 0
    do = True
    while index < len(data):
        nums = []
        if data[index: index + 4] == 'do()':
            do = True
            index = index + 4
        elif data[index: index + 7] == 'don\'t()':
            do = False
            index = index + 7
        elif data[index: index + 4] == 'mul(' and do:
            index = index + 4
            start = index
            while data[index].isdigit():
                index = index + 1
            if index - start <= 3 and data[index] == ',':
                nums.append(int(data[start: index]))
                index = index + 1
                start = index
                while data[index].isdigit():
                    index = index + 1
                if index - start <= 3 and data[index] == ')':
                    nums.append(int(data[start: index]))
                    ret.append(nums)
        else:
            index = index + 1
    return ret


def format_data_1(data):
    ret = []
    index = 0
    while index < len(data):
        nums = []
        if data[index: index + 4] == 'mul(':
            index = index + 4
            start = index
            while data[index].isdigit():
                index = index + 1
            if index - start <= 3 and data[index] == ',':
                nums.append(int(data[start: index]))
                index = index + 1
                start = index
                while data[index].isdigit():
                    index = index + 1
                if index - start <= 3 and data[index] == ')':
                    nums.append(int(data[start: index]))
                    ret.append(nums)
        else:
            index = index + 1
    return ret
