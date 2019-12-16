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
hero_point_list = [(121, 548, 318, 664), (368, 548, 565, 664), (616, 548, 803, 664), (862, 548, 1060, 664),
                   (1110, 548, 1307, 664)]
# 主城武将集合位置
city_hero_point_list = [(121, 604, 318, 720), (364, 604, 561, 720), (607, 604, 803, 720), (850, 604, 1047, 720),
                        (1093, 604, 1290, 720)]

# 扫荡按钮
wipe_out_button_rect = (793, 647, 979, 701)

# 扫荡描述位置
wipe_out_desc_rect = (600, 555, 1172, 588)

# 外部区域
outside_rect = (1243, 31, 1405, 812)

# 城池菜单
city_menu_rect = (841, 295, 1012, 382)

# 武将队伍武将一
army_hero_1_rect = (285, 211, 305, 454)

# 武将体力数值位置
hero_physical_value_rect = (1018, 310, 1118, 336)

# 武将征兵
hero_conscription_rect_list = [(525, 224, 1150, 262), (525, 357, 1150, 394), (525, 490, 1150, 527)]

# 征兵耗时
hero_conscription_duration_rect_list = [(1084, 176, 1176, 202), (1084, 305, 1176, 334), (1084, 440, 1176, 467)]

# 整体关闭按钮
page_close_rect = (1304, 46, 1380, 122)

# 整体回退按钮
page_return_rect = (1314, 106, 1380, 172)

# 征兵按钮
conscription_button_rect = (641, 580, 642, 712)

# 确认征兵按钮
conscription_confirm_button_rect = (620, 695, 791, 750)

# 确认征兵按钮
conscription_dialog_confirm_button_rect = (774, 534, 946, 588)

# 武将队伍页面的兵力
army_hero_troops_rect = (115, 182, 195, 212)

# 征兵中状态文字位置列表
conscription_status_rect_list = [(766, 222, 862, 262), (766, 354, 862, 392), (766, 487, 862, 525)]


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
