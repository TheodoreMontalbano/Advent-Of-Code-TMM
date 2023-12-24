from aoc_apis import values_to_polynomial, load_data
import math
from collections import deque


def get_large_steps_center_start(arr, wanted_steps):
    val_table = []
    offset = math.floor(len(arr) / 2)
    converted_num = (wanted_steps - offset) % len(arr)
    if wanted_steps < len(arr) * len(arr):
        return get_steps(arr, wanted_steps)
    for i in range(5, 10):
        curr = get_steps(arr, offset + i * len(arr) + converted_num)
        val_table.append(curr)
    poly = values_to_polynomial(val_table)
    return poly((wanted_steps - (offset + converted_num)) / len(arr) - 5)


def get_steps(arr, wanted_distance):
    can_reach = []
    pos = (-1, -1)
    odd_count = 0
    even_count = 0
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == "S":
                pos = (i, j)
            if arr[i][j] == "." and (i + j) % 2 == 1:
                odd_count = odd_count + 1
            elif arr[i][j] == ".":
                even_count = even_count + 1

    visited = {
        pos: 1
    }
    stack = deque()
    stack.append((pos, 0))
    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0)
    ]
    while len(stack) > 0:
        curr_pos, curr_distance = stack.popleft()
        if curr_distance % 2 == wanted_distance % 2:
            can_reach.append((curr_pos, curr_distance))
        for i in directions:
            new_pos = (i[0] + curr_pos[0], i[1] + curr_pos[1])
            if (not (arr[new_pos[0] % len(arr)][new_pos[1] % len(arr[0])] == "#") and new_pos not in visited
                    and curr_distance <= wanted_distance):
                visited[new_pos] = 1
                stack.append((new_pos, curr_distance + 1))
    d = {}
    for i in can_reach:
        curr_pos = i[0]
        d[curr_pos] = 1
    return len(d)
