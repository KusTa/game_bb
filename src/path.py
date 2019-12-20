# -*- coding: utf-8 -*-

# 路径

import math


# 获取下一步的坐标点（1,1）->（3,7）
def get_next_location(start, end):
    print("")


# 获取可能的下一步（刨除自己）
def get_next_possible_location(start):
    table = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            point = (start[0] + x, start[1] + y)
            if point != start:
                table.append(point)
    return table


# 获取比较好的
def get_better_next_possible_location(start, end):
    better = []
    possible = get_next_possible_location(start)
    for p in possible:
        if in_range(p, start, end):
            better.append(p)
    return better


# 是否在范围内
def in_range(point, start, end):
    if point[0] in range(min(start[0], end[0]), max(start[0], end[0]) + 1) and \
            point[1] in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
        return True
    else:
        return False


# 计算距离
def calc_distance(start, end):
    return int(math.fabs(start[0] - end[0]) + math.fabs(start[1] - end[1]))


if __name__ == '__main__':
    s = (334, 661)
    e = (330, 664)
    next_location = get_better_next_possible_location(s, e)
    for location in next_location:
        # TODO
        print("比较各个的优缺")
