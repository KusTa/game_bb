# -*- coding: utf-8 -*-

# 字符串处理


# 通过字符串获取数字对：1/23
def get_number_pair_by_split(text, split):
    if text.find(split) < 0:
        return [0, 0]
    else:
        pair = text.split(split)
        if pair[0].isdigit() and pair[1].isdigit():
            return [int(pair[0]), int(pair[1])]
        else:
            return [0, 0]


# 将时间串转换成数值（单位秒）
def get_time_by_string(text):
    time_split = text.split(":")
    if len(time_split) != 3:
        return 0
    else:
        return int(time_split[0]) * 60 * 60 + int(time_split[1]) * 60 + int(time_split[2])
