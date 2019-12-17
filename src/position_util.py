# -*- coding: utf-8 -*-

# 坐标变换


# 矩形区域获取中心点坐标
def point(rect):
    return int((rect[0] + rect[2]) / 2), int((rect[1] + rect[3]) / 2)


# 矩形的1/4右上
def top_right(rect):
    return int((rect[0] + rect[2]) / 2), rect[1], rect[2], int((rect[1] + rect[3]) / 2)


# 武将兵力数字位置
def hero_troops(rect):
    return int((rect[0] + rect[2]) / 2 + 18), rect[3], rect[2], rect[3] + 35


# 武将状态文字位置
def hero_status(rect):
    return rect[0], rect[3], rect[0] + 81, rect[3] + 35
