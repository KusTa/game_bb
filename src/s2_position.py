# -*- coding: utf-8 -*-


# 位置信息

# 地图按钮菜单位置
map_menu_rect = (1180, 97, 1234, 150)
# 标记定位菜单位置
location_menu_rect = (1335, 97, 1389, 150)
# 标记定位菜单--主城
location_menu_main_city_rect = (1032, 144, 1325, 197)
# 坐标输入X
location_input_x_rect = (991, 757, 1077, 797)
# 坐标输入Y
location_input_y_rect = (1100, 757, 1186, 797)
# 坐标跳转
location_jump_rect = (1200, 751, 1387, 806)
# 扫荡菜单按钮
wipe_out_menu_rect = (851, 397, 1048, 450)

# 5武将，武将1
hero_1_rect = (121, 548, 318, 664)
# 5武将，武将2
hero_2_rect = (368, 548, 565, 664)
# 5武将，武将3
hero_3_rect = (616, 548, 812, 664)
# 5武将，武将4
hero_4_rect = (862, 548, 1060, 664)
# 5武将，武将4
hero_5_rect = [1110, 548, 1307, 664]
# 武将集合
hero_point_list = [hero_1_rect, hero_2_rect, hero_3_rect, hero_4_rect, hero_5_rect]

# 扫荡按钮
wipe_out_button_rect = (793, 647, 979, 701)

# 扫荡描述位置
wipe_out_desc_rect = (600, 555, 1172, 588)

# 外部区域
outside_rect = (1243, 31, 1405, 812)


# 矩形区域获取中心点坐标
def point(rect):
    return int((rect[0] + rect[2]) / 2), int((rect[1] + rect[3]) / 2)


# 矩形的1/4右上
def top_right(rect):
    return int((rect[0] + rect[2]) / 2), rect[1], rect[2], int((rect[1] + rect[3]) / 2)


# 武将兵力数字位置
def hero_troops(rect):
    return int((rect[0] + rect[2]) / 2 + 18), rect[3], rect[2], rect[3] + 35
