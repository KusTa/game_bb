# -*- coding: utf-8 -*-
import math
import src.const as const


# 是否列表有相同数据
def is_list_has_common(list_l, list_r):
    for l in list_l:
        for r in list_r:
            if l == r:
                return False
    return True


# 计算两个坐标的距离
def calc_distance(start, end):
    return math.sqrt(math.pow(math.fabs(start[0] - end[0]), 2) + math.pow(math.fabs(start[1] - end[1]), 2))


# 计算耗时(单位秒)
def calc_march_duration(start, end, speed):
    return int(calc_distance(start, end) / speed * 60 * 60)


# 计算兵力
def calc_land_troops(start, end, land_level):
    return const.land_basics_troops_list[land_level] * (1 + calc_distance(start, end) * const.troops_increase_factor)


# 计算最优距离坐标列表（倒序：最耗时->最不耗时）
def calc_best_march_duration(start, location_list, speed):
    duration_list = []
    # 按耗时排序（小到大）
    location_list = sorted(location_list, key=lambda x: calc_march_duration(start, x, speed), reverse=True)
    # 获取时间合适的列表
    for item in location_list:
        duration = calc_march_duration(start, item, speed)
        if duration <= const.one_wipe_out_duration:
            duration_list.append(item)
    return duration_list


if __name__ == '__main__':
    print(calc_march_duration((1, 1), (4, 5), 118))
