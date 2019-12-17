# -*- coding: utf-8 -*-

import src.keyboard as keyboard
import src.mouse as mouse
import src.s2_position as position
import src.time as time
import src.user_input as user_input
import src.window as window


def click_outside(hwnd):
    mouse.click(hwnd, position.outside_rect)
    time.sleep(1)


# 点击中心点
def click_center(hwnd):
    mouse.click_point(hwnd, window.center_x, window.center_y)
    time.sleep(1)


# 点击标记定位菜单按钮
def click_mark_location_menu(hwnd):
    mouse.click(hwnd, position.mark_location_menu_rect)
    time.sleep(0.5)


# 点击地图菜单按钮
def click_map_menu(hwnd):
    mouse.click(hwnd, position.map_menu_rect)
    time.sleep(0.5)


# 点击标记定位->主城
def click_mark_location_main_city(hwnd):
    mouse.click(hwnd, position.mark_location_menu_main_city_rect)
    time.sleep(0.5)


# 点击城市菜单进入城池部队页面
def click_city_menu(hwnd):
    mouse.click(hwnd, position.city_menu_rect)
    time.sleep(1.5)


# 点击城池队伍头像
def click_city_army(hwnd, army_index):
    mouse.click(hwnd, position.city_army_list[army_index])
    time.sleep(0.5)


# 点击出征队伍头像
def click_expedition_army(hwnd, army_index):
    mouse.click(hwnd, position.expedition_army_rect_list[army_index])
    time.sleep(1)


# 点击武将队伍大营
def click_army_camp(hwnd):
    mouse.click(hwnd, position.army_hero_camp_rect)
    time.sleep(0.5)


# 点击出征按钮
def click_wipe_out_button(hwnd):
    mouse.click(hwnd, position.wipe_out_button_rect)
    time.sleep(1)


# 点击页面关闭按钮
def click_page_close(hwnd):
    mouse.click(hwnd, position.page_close_rect)
    time.sleep(1)


# 点击页面返回按钮
def click_page_return(hwnd):
    mouse.click(hwnd, position.page_return_rect)
    time.sleep(1.5)


# 点击征兵中心按钮
def click_conscription_button(hwnd):
    mouse.click(hwnd, position.conscription_button_rect)
    time.sleep(1)


# 点击武将征兵最大值
def click_hero_conscription_max(hwnd, hero_index):
    rect = position.hero_conscription_rect_list[hero_index]
    mouse.click_point(hwnd, rect[2] - window.seek_bar_limit, int((rect[1] + rect[3]) / 2))
    time.sleep(0.2)
    mouse.click_point(hwnd, rect[2], int((rect[1] + rect[3]) / 2))
    time.sleep(0.2)


# 点击征兵条的百分比
def click_hero_conscription_percent(hwnd, hero_index, percent):
    rect = position.hero_conscription_rect_list[hero_index]
    mouse.click_point(hwnd, int(rect[0] + (rect[2] - rect[0]) * percent), int((rect[1] + rect[3]) / 2))
    time.sleep(0.5)


# 点击确认征兵按钮
def click_conscription_confirm_button(hwnd):
    mouse.click(hwnd, position.conscription_confirm_button_rect)
    time.sleep(1)


# 点击确认征兵按钮
def click_conscription_dialog_confirm_button(hwnd):
    mouse.click(hwnd, position.conscription_dialog_confirm_button_rect)
    time.sleep(1)


# 点击确认征兵按钮
def location_jump(hwnd, rect):
    mouse.click(hwnd, position.conscription_dialog_confirm_button_rect)
    time.sleep(1)


# 点击坐标输入框并输入（单个）
def text_input(hwnd, rect, value):
    mouse.click(hwnd, rect)
    time.sleep(0.1)
    # 删除坐标内容
    time.sleep(0.1)
    keyboard.press_key(hwnd, keyboard.backspace)
    time.sleep(0.1)
    keyboard.press_key(hwnd, keyboard.backspace)
    time.sleep(0.1)
    keyboard.press_key(hwnd, keyboard.backspace)
    time.sleep(0.1)
    # 输入坐标
    keyboard.type_string(hwnd, value)
    time.sleep(0.3)


# 坐标输入
def location_input(hwnd, point):
    # 输入X坐标
    text_input(hwnd, position.location_input_x_rect, str(point[0]))
    # 输入Y坐标
    text_input(hwnd, position.location_input_y_rect, str(point[1]))


# 坐标跳转按钮
def click_location_jump_button(hwnd):
    mouse.click(hwnd, position.location_jump_rect)
    time.sleep(2)


# 点击扫荡菜单按钮
def click_wipe_out_menu(hwnd):
    mouse.click(hwnd, position.wipe_out_menu_rect)
    time.sleep(1)


# 地图放大
def map_enlarge(hwnd):
    user_input.ctrl_scroll(hwnd, 120, window.center_x, window.center_y)
    time.sleep(1)


# 地图还原
def map_reduction(hwnd):
    user_input.ctrl_scroll(hwnd, -120, window.center_x, window.center_y)
    time.sleep(1)
