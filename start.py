# -*- coding: utf-8 -*-

import time
from ctypes import *

import pytesseract
import win32api
import win32con
import win32gui
from PIL import ImageGrab
from pykeyboard import PyKeyboard
from pymouse import PyMouse
import numpy as np


# 判断是否是：黑白照片（灰度图）
def is_gray_map(image, threshold=15):
    if len(image.getbands()) == 1:
        return True
    img1 = np.asarray(image.getchannel(channel=0), dtype=np.int16)
    img2 = np.asarray(image.getchannel(channel=1), dtype=np.int16)
    img3 = np.asarray(image.getchannel(channel=2), dtype=np.int16)
    diff1 = (img1 - img2).var()
    diff2 = (img2 - img3).var()
    diff3 = (img3 - img1).var()
    diff_sum = (diff1 + diff2 + diff3) / 3.0
    if diff_sum <= threshold:
        return True
    else:
        return False


class GameAuxiliaries(object):

    def __init__(self):
        self.wd_name = u'率土之滨'
        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()

        # 取得窗口句柄
        hwnd = win32gui.FindWindow(0, self.wd_name)
        # 设置窗口显示（防止最小化问题）
        win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
        # 设置为最前显示
        win32gui.SetForegroundWindow(hwnd)

        # 调整目标窗口到坐标(0, 0), 大小设置为(1414, 824)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 1414, 824,
                              win32con.SWP_SHOWWINDOW)
        # 屏幕宽高
        self.width_real = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.height_real = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        self.width_px = 1920
        self.height_px = 1080
        # 获取窗口尺寸信息
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(hwnd)
        # 设置窗口尺寸信息
        self.width = self.right - self.left
        self.height = self.bottom - self.top
        # 标题栏的高度
        self.title_bar_height = 32
        self.top = self.top + self.title_bar_height
        # 中心位置坐标
        self.center_x = int((self.right + self.left) / 2)
        self.center_y = int((self.bottom + self.top) / 2)
        print("窗口宽：%s" % (self.right - self.left))
        print("窗口高：%s" % (self.bottom - self.top))

        # 地图按钮菜单位置
        self.map_menu_point = (self.right - 200, self.top + 92)
        # 标记定位菜单位置
        self.location_menu_point = (self.right - 50, self.top + 92)
        # 标记定位菜单--主城
        self.location_menu_main_city_point = (self.right - 222, self.top + 142)
        # 坐标输入X
        self.location_input_x_point = (self.right - 340, self.bottom - 40)
        # 坐标输入Y
        self.location_input_y_point = (self.right - 230, self.bottom - 40)
        # 坐标跳转
        self.location_jump_point = (self.right - 112, self.bottom - 40)
        # 扫荡菜单按钮
        self.wipe_out_menu_point = (self.right - 472, self.top + 336)

        # 5武将，武将1
        self.hero_1_point = (self.left + 220, self.bottom - 210)
        # 5武将，武将2
        self.hero_2_point = (self.left + 472, self.bottom - 210)
        # 5武将，武将3
        self.hero_3_point = (self.left + 720, self.bottom - 210)
        # 5武将，武将4
        self.hero_4_point = (self.left + 968, self.bottom - 210)
        # 5武将，武将4
        self.hero_5_point = (self.left + 1216, self.bottom - 210)
        # 武将集合
        self.hero_point_list = [self.hero_1_point, self.hero_2_point, self.hero_3_point, self.hero_4_point,
                                self.hero_5_point]

        # 扫荡按钮
        self.wipe_out_button_point = (self.right - 530, self.bottom - 148)

        # 扫荡按钮
        self.wipe_out_button_rect = (self.right - 620, self.bottom - 172, self.right - 438, self.bottom - 124)
        # 木材资源数量
        self.wood_amount_rect = (self.left + 134, self.top + 24, self.left + 235, self.top + 50)
        # 铁矿资源数量
        self.iron_amount_rect = (self.left + 260, self.top + 24, self.left + 381, self.top + 50)
        # 石料资源数量
        self.tone_amount_rect = (self.left + 390, self.top + 24, self.left + 517, self.top + 50)
        # 粮草资源数量
        self.food_amount_rect = (self.left + 530, self.top + 24, self.left + 657, self.top + 50)

        # 外部区域
        self.outside_point = (self.right - 80, self.center_y)

    # 点击地图菜单按钮
    def click_map_menu(self):
        self.mouse.click(self.map_menu_point[0], self.map_menu_point[1])
        time.sleep(0.2)

    # 点击标记定位菜单按钮
    def click_location_menu(self):
        self.mouse.click(self.location_menu_point[0], self.location_menu_point[1])
        time.sleep(0.2)

    # 定位主城
    def location_main_city(self):
        self.click_location_menu()
        self.mouse.click(self.location_menu_main_city_point[0], self.location_menu_main_city_point[1])
        time.sleep(1.5)

    # 定位跳转
    def location_jump(self, x, y):
        self.click_map_menu()
        self.location_input(self.location_input_x_point, x)
        self.location_input(self.location_input_y_point, y)
        self.mouse.click(self.location_jump_point[0], self.location_jump_point[1])

    # 点击坐标输入框并输入（单个）
    def location_input(self, location, value):
        # 点击坐标输入框
        self.mouse.click(location[0], location[1])
        time.sleep(0.1)
        # 删除坐标内容
        self.keyboard.press_key(self.keyboard.backspace_key)
        time.sleep(0.1)
        self.keyboard.press_key(self.keyboard.backspace_key)
        time.sleep(0.1)
        self.keyboard.press_key(self.keyboard.backspace_key)
        time.sleep(0.1)
        self.keyboard.press_key(self.keyboard.backspace_key)
        # 输入坐标
        self.keyboard.type_string(value)
        time.sleep(0.3)

    # 扫荡
    def wipe_out(self, x, y):
        self.location_jump(x, y)
        time.sleep(1.5)
        self.mouse.click(self.center_x, self.center_y)
        time.sleep(0.5)
        self.mouse.click(self.wipe_out_menu_point[0], self.wipe_out_menu_point[1])
        time.sleep(0.8)

    # 武将出征
    def hero_wipe_out(self, point):
        # 点击武将1
        self.mouse.click(point[0], point[1])
        time.sleep(0.8)

    # 获取屏幕点颜色
    def get_color(self, x, y):
        gdi32 = windll.gdi32
        user32 = windll.user32
        hdc = user32.GetDC(None)
        # 获取颜色值
        pixel = gdi32.GetPixel(hdc, x, y)
        # 提取RGB值
        r = pixel & 0x0000ff
        g = (pixel & 0x00ff00) >> 8
        b = pixel >> 16
        return [r, g, b]

    # 获取指定区域内的文字内容
    def get_text_by_orc(self, rect):
        image = ImageGrab.grab(rect)
        image = image.convert('L')
        return pytesseract.image_to_string(image, lang='chi_sim')

    def is_enable_wipe_out(self):
        text = self.get_text_by_orc(self.wipe_out_button_rect)
        return text.find("扫") > 0

    def run(self):
        # 找到游戏运行窗口
        self.wipe_out("202", "1444")
        rect = (self.left + 1230, self.bottom - 270, self.left + 1330, self.bottom - 207)
        print(rect)
        image = ImageGrab.grab(rect)
        image.show()
        if is_gray_map(image):
            print("武将%d 不可以出征" % 1)
        else:
            print("武将%d 可以出征" % 1)
        # n = 0
        # while n < 5:
        #     self.hero_wipe_out(self.hero_point_list[n])
        #     if self.is_enable_wipe_out():
        #         print("武将%d 可以出征" % (n + 1))
        #         print("点击外部区域")
        #     else:
        #         print("武将%d 不可以出征" % (n + 1))
        #         self.mouse.click(self.outside_point[0], self.outside_point[1])
        #         time.sleep(0.5)
        #         n += 1


if __name__ == '__main__':
    ga = GameAuxiliaries()
    ga.run()
