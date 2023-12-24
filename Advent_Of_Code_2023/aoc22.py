from collections import deque

from aoc_apis import has_overlap


def get_ans(str_arr, part_one=True):
    bricks = []
    for i in str_arr:
        curr = i.split("~")
        bricks.append([curr[0].split(","), curr[1].split(",")])
    bricks.sort(key=lambda x: int(x[0][2]))
    dep_buckets = create_dep_buckets(bricks)

    total = 0
    d = {}
    dep_tree_up = {}
    dep_tree_down = {}
    for i in range(len(dep_buckets) - 1):
        for brick_up in dep_buckets[i + 1]:
            sums = 0
            to_add = -1
            for j in range(len(dep_buckets[i])):
                if (on_top_of(dep_buckets[i][j][0], brick_up[0], True)
                        and not brick_up[1] == dep_buckets[i][j][1]):
                    sums = sums + 1
                    to_add = dep_buckets[i][j][1]
                    if not part_one:
                        if to_add in dep_tree_up:
                            dep_tree_up[to_add].append(brick_up[1])
                        else:
                            dep_tree_up[to_add] = [brick_up[1]]
                        if brick_up[1] in dep_tree_down:
                            dep_tree_down[brick_up[1]].append(to_add)
                        else:
                            dep_tree_down[brick_up[1]] = [to_add]

            if sums == 1:
                d[to_add] = 1
    if part_one:
        return len(bricks) - len(d)
    else:
        total = 0
        index = 0
        checked = {}
        for i in dep_buckets:
            for j in i:
                if j[1] not in checked:
                    checked[j[1]] = 1
                    total = total + get_direct_dependencies(j[1], dep_tree_up, dep_tree_down)
            index = index + 1
        return total


def get_direct_dependencies(curr, dep_tree_up, dep_tree_down):
    to_check = deque()
    if curr not in dep_tree_up:
        return 0
    for i in dep_tree_up[curr]:
        to_check.append(i)
    will_fall = {
        curr: 1
    }
    while len(to_check) > 0:
        curr_val = to_check.popleft()
        # first check if this will fall
        fall = True
        for j in dep_tree_down[curr_val]:
            if j not in will_fall:
                fall = False
                break
        if fall:
            will_fall[curr_val] = 1
            if curr_val in dep_tree_up:
                for j in dep_tree_up[curr_val]:
                    to_check.append(j)
    return len(will_fall) - 1


def create_dep_buckets(bricks):
    dep_buckets = [[] for i in range(len(bricks))]
    curr_max_index = 1
    dep_buckets[0] = [(bricks[0], 0)]
    for i in range(1, len(bricks)):
        for j in range(curr_max_index):
            index = curr_max_index - j - 1
            check = False
            for brick in dep_buckets[index]:
                if on_top_of(brick[0], bricks[i]):
                    for k in range(int(bricks[i][1][2]) - int(bricks[i][0][2]) + 1):
                        dep_buckets[index + 1 + k].append((bricks[i], i))
                        if index + 1 + k >= curr_max_index:
                            curr_max_index = curr_max_index + 1
                    check = True
                    break
            if check:
                break
            if index == 0:
                for k in range(int(bricks[i][1][2]) - int(bricks[i][0][2]) + 1):
                    dep_buckets[index + k].append((bricks[i], i))
                    if index + k >= curr_max_index:
                        curr_max_index = curr_max_index + 1
    return dep_buckets


# returns if brick_two is on top of brick_one
def on_top_of(brick_one, brick_two, ignore_height=False):
    if ignore_height or int(brick_one[0][2]) < int(brick_two[0][2]):
        brick_one_x = [int(brick_one[0][0]), int(brick_one[1][0])]
        brick_one_y = [int(brick_one[0][1]), int(brick_one[1][1])]
        brick_two_x = [int(brick_two[0][0]), int(brick_two[1][0])]
        brick_two_y = [int(brick_two[0][1]), int(brick_two[1][1])]
        return has_overlap(brick_one_x, brick_two_x) and has_overlap(brick_one_y, brick_two_y)
    else:
        return False
