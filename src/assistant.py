# -*- coding: utf-8 -*-

import src.image as image
import src.position_util as position_util
import src.s2_position as position
import src.string_util as string_util


# 城池的武将是否是灰色状态（调动的）
def is_city_hero_gray(hwnd, hero_index):
    return image.is_gray_map(image.image_grab(hwnd, position_util.top_right(position.city_army_list[hero_index])))


# 出征的武将是否是灰色状态（调动的）
def is_expedition_hero_gray(hwnd, hero_index):
    return image.is_gray_map(
        image.image_grab(hwnd, position_util.top_right(position.expedition_army_rect_list[hero_index])))


# 城池的武将是否征兵中（状态判断）
def is_city_hero_conscription(hwnd, hero_index):
    return image.get_text_by_orc(hwnd, position_util.hero_status(position.city_army_list[hero_index]), 180).find(
        "征") >= 0


# 获取武将队伍页面的兵力
def get_city_army_troops(hwnd):
    return image.get_number_by_orc(hwnd, position.army_troops_rect, 160)


# 获取武将体力
def get_hero_physical(hwnd):
    number = image.get_number_tuple_by_orc(hwnd, position.hero_physical_value_rect, 80, '/')
    number_pair = string_util.get_number_pair_by_split(number, '/')
    return number_pair[0]


# 获取武将征兵时长
def get_hero_conscription_duration(hwnd, hero_index):
    text = image.get_number_tuple_by_orc(hwnd, position.hero_conscription_duration_rect_list[hero_index], 130, ':')
    duration = string_util.get_time_by_string(text)
    return duration


# 武将是否兵力足够
def is_troops_enough(hwnd, hero_index):
    return image.get_number_by_orc(hwnd, position_util.hero_troops(position.expedition_army_rect_list[
                                                                       hero_index % len(
                                                                           position.expedition_army_rect_list)]), 85)


# 征兵不可用
def is_conscription_disable(hwnd):
    return image.is_above_main_threshold(image.image_grab(hwnd, position.conscription_button_rect), 60)


# 征兵队列已满
def is_conscription_tip(hwnd):
    return image.get_text_by_orc(hwnd, position.conscription_tip_rect, 120).find(
        "预备兵") >= 0


# 是否是五级地
def is_land_5_tone(hwnd):
    return image.is_image_similar(hwnd, image.open_image('../res/land_5_tone.png'), position.center_land_rect)
