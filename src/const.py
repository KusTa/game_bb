# -*- coding: utf-8 -*-

# 平局时长
draw_duration = 5 * 60
# 平局次数
draw_count = 1
# 误差时长
error_duration = 3 * 60

# 兵力增长系数
troops_increase_factor = 0.03

# 基础兵力列表
land_basics_troops_list = [0, 200, 750, 2100, 6000, 9000, 16500, 21000, 25500, 30000]

# 一次出征时长
one_wipe_out_duration = 60 * 60 - draw_duration * draw_count - error_duration
