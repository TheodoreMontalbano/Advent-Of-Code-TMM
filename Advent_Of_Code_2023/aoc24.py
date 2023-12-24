from z3 import *


def get_ans_part_two(str_arr):
    arr = []
    for i in str_arr:
        curr = i.split("@")
        arr.append([curr[0].strip().split(", "), curr[1].strip().split(", ")])
    s = Solver()
    set_option(max_args=1000, max_lines=1000, max_depth=1000, max_visited=1000)
    change_x = Int('cx')
    change_y = Int('cy')
    change_z = Int('cz')
    pos_x = Int('x')
    pos_y = Int('y')
    pos_z = Int('z')
    to_compute = [
        [pos_x, change_x],
        [pos_y, change_y],
        [pos_z, change_z]
    ]
    times = [Int('t' + str(i)) for i in range(len(arr))]
    for i in range(len(arr)):
        curr_pos = arr[i][0]
        curr_vel = arr[i][1]
        t = times[i]
        for (pos, change), k_pos, k_change in zip(to_compute, curr_pos, curr_vel):
            s.add(pos + change * t == k_pos + k_change * t)
    for t in times:
        s.add(t > 0)
    s.check()
    model = s.model()
    return model[pos_x].as_long() + model[pos_y].as_long() + model[pos_z].as_long()


def get_ans_part_one(str_arr, test_area):
    arr = []
    for i in str_arr:
        curr = i.split("@")
        arr.append([curr[0].strip().split(", "), curr[1].strip().split(", ")])
    total = 0
    for i in range(len(arr)):
        pos_one, velocity_one = arr[i]
        for j in range(i + 1, len(arr)):
            pos_two, velocity_two = arr[j]
            if intersect(pos_one, velocity_one, pos_two, velocity_two, test_area):
                total = total + 1
    return total


def intersect(pos_one, velocity_one, pos_two, velocity_two, test_area):
    equations_one = [
        [int(velocity_one[0]), int(pos_one[0]), 1],
        [int(velocity_one[1]), int(pos_one[1]), 1]
    ]
    equations_two = [
        [int(velocity_two[0]), int(pos_two[0]), 1],
        [int(velocity_two[1]), int(pos_two[1]), 1]
    ]
    for i in [equations_one, equations_two]:
        if i[1][0] == 0:
            return False
        multiplier = i[0][0] / i[1][0] * -1
        for j in range(len(i[1])):
            i[1][j] = i[1][j] * multiplier
    final_equation_one = [
        equations_one[0][1] + equations_one[1][1], equations_one[0][2], equations_one[1][2]
    ]
    final_equation_two = [
        equations_two[0][1] + equations_two[1][1], equations_two[0][2], equations_two[1][2]
    ]
    if final_equation_two[1] == 0:
        return False

    multiplier = final_equation_one[1] / final_equation_two[1] * -1
    for i in range(len(final_equation_two)):
        final_equation_two[i] = final_equation_two[i] * multiplier

    if (final_equation_one[2] + final_equation_two[2]) == 0 or final_equation_one[1] == 0:
        return False
    y = (final_equation_one[0] + final_equation_two[0]) / (final_equation_one[2] + final_equation_two[2])
    x = (final_equation_one[0] - final_equation_one[2] * y) / final_equation_one[1]

    # First check if we are in the past
    if (x - equations_one[0][1]) / equations_one[0][0] < 0 or (x - equations_two[0][1]) / equations_two[0][0] < 0:
        return False

    return test_area[0] <= x <= test_area[1] and test_area[0] <= y <= test_area[1]
