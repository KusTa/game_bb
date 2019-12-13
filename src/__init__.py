# -*- coding: utf-8 -*-

import time
from ctypes import *

import tkinter as tk

import pytesseract
import win32api
import win32con
import win32gui
from PIL import ImageGrab
from pymouse import PyMouse
from pykeyboard import PyKeyboard

import numpy as np
import src.position as position
import src.config as config


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
        self.title_bar_height = 30
        self.top = self.top + self.title_bar_height
        # 中心位置坐标
        self.center_x = int((self.right + self.left) / 2)
        self.center_y = int((self.bottom + self.top) / 2)
        print("窗口宽：%s" % (self.right - self.left))
        print("窗口高：%s" % (self.bottom - self.top))

    # 矩形区域中心点点击
    def click(self, rect):
        point = position.point(rect)
        self.mouse.click(point[0], point[1])

    # 矩形区域中心点移动
    def move(self, rect):
        point = position.point(rect)
        self.mouse.move(point[0], point[1])

    # 点击地图菜单按钮
    def click_map_menu(self):
        self.click(position.map_menu_rect)
        time.sleep(0.2)

    # 点击标记定位菜单按钮
    def click_location_menu(self):
        self.click(position.location_menu_rect)
        time.sleep(0.2)

    # 定位主城
    def location_main_city(self):
        self.click_location_menu()
        self.click(position.location_menu_main_city_rect)
        time.sleep(1.5)

    # 定位跳转
    def location_jump(self, point):
        self.click_map_menu()
        self.location_input(position.location_input_x_rect, str(point[0]))
        self.location_input(position.location_input_y_rect, str(point[1]))
        self.click(position.location_jump_rect)

    # 点击坐标输入框并输入（单个）
    def location_input(self, rect, value):
        point = position.point(rect)
        # 点击坐标输入框
        self.mouse.click(point[0], point[1])
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
    def wipe_out(self, point):
        self.location_jump(point)
        time.sleep(1.5)
        self.mouse.click(self.center_x, self.center_y)
        time.sleep(0.5)
        self.click(position.wipe_out_menu_rect)
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
        text = self.get_text_by_orc(position.wipe_out_button_rect)
        return text.find("扫") > 0

    # 启动
    def wipe_out_test(self):
        # 武将索引
        hero_index = 0
        wipe = True
        while True:
            if wipe:
                self.wipe_out(config.wipe_out_location_5_1)
                wipe = False
            image = ImageGrab.grab(position.top_right(position.hero_point_list[hero_index % 5]))
            if is_gray_map(image):
                print("武将不可以出征")
                if hero_index == 4:
                    self.click(position.outside_rect)
                time.sleep(0.5)
            else:
                print("武将可以出征")
                time.sleep(0.5)
                self.click(position.hero_point_list[hero_index % 5])
                time.sleep(0.5)
                self.click(position.wipe_out_button_rect)
                wipe = True
            time.sleep(5)
            hero_index += 1

    def stop(self):
        self.flag = False

    # 创建GUI
    def run(self):
        window = tk.Tk()
        window.title("率土之滨辅助")
        window.geometry("500x300")
        start = tk.Button(window, text="开始", command=lambda: self.wipe_out_test())
        start.pack(side=tk.LEFT)
        end = tk.Button(window, text="结束", command=lambda: self.stop())
        end.pack(side=tk.RIGHT)
        window.mainloop()


if __name__ == '__main__':
    ga = GameAuxiliaries()
    ga.run()
