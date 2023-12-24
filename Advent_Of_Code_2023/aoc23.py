from collections import deque
from copy import deepcopy


class Node:
    # Should be in the format next node, distance

    def __init__(self):
        self.pos = None
        self.connections = []


def dfs_longest_path(curr, end_pos, visited=None):
    if visited is None:
        visited = {}
    if curr.pos == end_pos:
        return 0
    max_length = float("-inf")
    visited[curr] = 1
    for node, distance in curr.connections:
        if node not in visited or not visited[node]:
            max_length = max(max_length, distance + dfs_longest_path(node, end_pos, visited))
    visited[curr] = 0
    return max_length


def get_ans(arr, start_pos, end_pos, part_one=True):
    head = create_compressed_graph(arr, start_pos, end_pos, part_one)["Head"]
    return dfs_longest_path(head, end_pos)


def get_decision_points(arr, start_pos, end_pos, part_one):
    visited = {
        start_pos: 1
    }
    stack = [start_pos]
    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0)
    ]
    slides = {
        "<": 1,
        ">": 0,
        "v": 2,
        "^": 3,
    }
    decision_points = []
    while len(stack) > 0:
        curr_pos = stack.pop()
        count = 0
        for i in directions:
            new_pos = (curr_pos[0] + i[0], curr_pos[1] + i[1])
            if 0 <= new_pos[0] < len(arr) and 0 <= new_pos[1] < len(arr[1]):
                if part_one:
                    while arr[new_pos[0]][new_pos[1]] in slides:
                        slide_index = slides[arr[new_pos[0]][new_pos[1]]]
                        new_pos = (new_pos[0] + directions[slide_index][0], new_pos[1] + directions[slide_index][1])
                if new_pos in visited:
                    count = count + 1
                    continue
                elif arr[new_pos[0]][new_pos[1]] == "#":
                    continue
                else:
                    count = count + 1
                visited[new_pos] = 1
                stack.append(new_pos)
        if count > 2:
            decision_points.append((curr_pos, count))
    index = 0
    while part_one and index < len(decision_points):
        count = 0
        x, y = decision_points[index][0]
        count = 0
        for xx, yy in directions:
            new_pos = (xx + x, yy + y)
            if 0 <= new_pos[0] < len(arr) and 0 <= new_pos[1] < len(arr[1]):
                if arr[new_pos[0]][new_pos[1]] == ".":
                    count = count + 1
                elif arr[new_pos[0]][new_pos[1]] == "#":
                    continue
                else:
                    check = (directions[slides[arr[new_pos[0]][new_pos[1]]]][0] * -1 == xx
                             and directions[slides[arr[new_pos[0]][new_pos[1]]]][1] * -1 == yy)
                    if not check:
                        count = count + 1

        decision_points[index] = (decision_points[index][0], count)
        index = index + 1
    decision_points.append((start_pos, 1))
    decision_points.append((end_pos, 0))
    return decision_points


def get_shortest_distance(arr, start_pos, end_pos, part_one, impassable_points):
    visited = {
        start_pos: 1
    }
    stack = deque()
    stack.append((start_pos, 0))
    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0)
    ]
    slides = {
        "<": 1,
        ">": 0,
        "v": 2,
        "^": 3,
    }
    while len(stack) > 0:
        curr_pos, curr_distance = stack.popleft()
        if curr_pos == end_pos:
            return curr_distance
        elif not curr_pos == start_pos and curr_pos in impassable_points:
            continue
        else:
            for i in directions:
                new_pos = (curr_pos[0] + i[0], curr_pos[1] + i[1])
                if 0 <= new_pos[0] < len(arr) and 0 <= new_pos[1] < len(arr[1]):
                    count = 1
                    slide = False
                    if part_one:
                        while arr[new_pos[0]][new_pos[1]] in slides:
                            slide = True
                            count = count + 1
                            slide_index = slides[arr[new_pos[0]][new_pos[1]]]
                            new_pos = (new_pos[0] + directions[slide_index][0], new_pos[1] + directions[slide_index][1])
                    if arr[new_pos[0]][new_pos[1]] == "#" or new_pos in visited:
                        continue
                    visited[new_pos] = 1
                    stack.append((new_pos, curr_distance + count))
    return -1


def create_compressed_graph(arr, start_pos, end_pos, part_one):
    decision_points = get_decision_points(arr, start_pos, end_pos, part_one)
    points_arr = []
    for i in decision_points:
        points_arr.append(i[0])
    graph = {}
    for i in points_arr:
        graph[i] = Node()
        graph[i].pos = i
        if i == start_pos:
            graph["Head"] = graph[i]
        elif i == end_pos:
            graph["Tail"] = graph[i]
    for i in range(len(decision_points)):
        point_one = decision_points[i][0]
        num_conn = decision_points[i][1]
        distances = []
        for j in range(len(decision_points)):
            if not i == j:
                point_two = decision_points[j][0]
                curr_dist = get_shortest_distance(arr, point_one, point_two, part_one, points_arr)
                if not curr_dist == -1:
                    distances.append((point_two, curr_dist))
        distances.sort(key=lambda x: x[1])
        for j in range(min([num_conn, len(distances)])):
            graph[point_one].connections.append((graph[distances[j][0]], distances[j][1]))
    return graph


def debug(arr, visited):
    slides = {
        "<": 1,
        ">": 0,
        "v": 2,
        "^": 3,
    }
    count = 0
    temp_arr = deepcopy(arr)
    for i in visited:
        if arr[i[0]][i[1]] in slides:
            count = count + 1
        temp_arr[i[0]][i[1]] = "0"
    to_print = []
    for i in temp_arr:
        to_print.append("".join(i))
    print("\n".join(to_print))
    print(count)


def debug_graph(head):
    visited = {
    }
    stack = [head]
    while len(stack) > 0:
        curr = stack.pop()
        if curr in visited:
            continue
        visited[curr] = 1
        print(curr.pos)
        for i in curr.connections:
            print("     :" + str(i[0].pos), i[1])
            stack.append(i[0])
