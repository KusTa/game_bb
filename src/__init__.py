# -*- coding: utf-8 -*-

import time
from ctypes import *

import tkinter as tk

import pytesseract
import win32api
import win32con
import win32gui
from PIL import ImageGrab, Image
from pymouse import PyMouse
from pykeyboard import PyKeyboard

import numpy as np
import src.s2_position as position
import src.s2_config as config


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
        self.hwnd = win32gui.FindWindow(0, self.wd_name)
        # 设置窗口显示（防止最小化问题）
        win32gui.ShowWindow(self.hwnd, win32con.SW_NORMAL)
        # 设置为最前显示
        win32gui.SetForegroundWindow(self.hwnd)

        # 调整目标窗口到坐标(0, 0), 大小设置为(1414, 824)
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST, 0, 0, 1414, 824,
                              win32con.SWP_SHOWWINDOW)
        # 屏幕宽高
        self.width_real = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.height_real = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        self.width_px = 1920
        self.height_px = 1080
        # 获取窗口尺寸信息
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(self.hwnd)
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

    # 输入字符串
    def type_string_biu_biu(self, text):
        for number in text:
            self.press_key_biu_biu(win32con.VK_NUMPAD0 + int(number))
            time.sleep(0.05)

    # 键盘事件
    def press_key_biu_biu(self, key):
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, key, 0)

    # 发送
    def click_biu_biu(self, x, y):
        long_position = win32api.MAKELONG(x - 7, y - self.title_bar_height)
        time.sleep(0.05)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        time.sleep(0.05)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)

    # 矩形区域中心点点击
    def click(self, rect):
        point = position.point(rect)
        self.click_biu_biu(point[0], point[1])

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
        self.click_biu_biu(point[0], point[1])
        time.sleep(0.1)
        # 删除坐标内容
        self.press_key_biu_biu(win32con.VK_BACK)
        time.sleep(0.1)
        self.press_key_biu_biu(win32con.VK_BACK)
        time.sleep(0.1)
        self.press_key_biu_biu(win32con.VK_BACK)
        time.sleep(0.1)
        self.press_key_biu_biu(win32con.VK_BACK)
        # 输入坐标
        self.type_string_biu_biu(value)
        time.sleep(0.3)

    # 地图放大
    def enlarge(self):
        self.press_key_biu_biu(win32con.VK_CONTROL)
        time.sleep(0.1)
        self.mouse.scroll(vertical=1000)
        time.sleep(0.5)
        self.keyboard.release_key(self.keyboard.control_key)
        time.sleep(1)

    # 地图还原尺寸
    def reduction(self):
        self.press_key_biu_biu(win32con.VK_CONTROL)
        time.sleep(0.1)
        self.mouse.scroll(vertical=-1000)
        time.sleep(0.5)
        self.keyboard.release_key(self.keyboard.control_key)
        time.sleep(1)

    # 扫荡
    def wipe_out(self, point):
        # 定位到指定坐标（居中）
        self.location_jump(point)
        time.sleep(1.5)
        # 地图放大
        self.enlarge()
        # 点击土地
        self.click_biu_biu(self.center_x, self.center_y)
        time.sleep(0.5)
        # 点图还原
        self.reduction()
        # 点击扫荡菜单
        self.click(position.wipe_out_menu_rect)
        time.sleep(0.8)

    # 武将出征
    def hero_wipe_out(self, point):
        # 点击武将1
        self.click_biu_biu(point[0], point[1])
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

    # 图片二值化
    def image_two_value(self, image):
        threshold = 85
        table = []
        for i in range(256):
            if i < threshold:
                table.append(1)
            else:
                table.append(0)
        return image.point(table, '1')

    # 获取指定区域内的文字内容
    def get_text_by_orc(self, rect):
        image = ImageGrab.grab(rect)
        image = image.convert('L')
        image = self.image_two_value(image)
        return pytesseract.image_to_string(image, lang='chi_sim', config='--psm 7')

    def is_enable_wipe_out(self):
        text = self.get_text_by_orc(position.wipe_out_desc_rect)
        print(text)
        return text.find("强盛") < 0

    # 启动
    def wipe_out_test(self):
        # 武将索引
        location_index = 0
        hero_index = 0
        wipe = True
        while True:
            if wipe:
                self.wipe_out(config.wipe_out_location_list[location_index % len(config.wipe_out_location_list)])
                wipe = False
            image = ImageGrab.grab(position.top_right(position.hero_point_list[hero_index % len(
                position.hero_point_list)]))
            if is_gray_map(image):
                print("武将不可以出征")
                if hero_index % len(position.hero_point_list) == len(position.hero_point_list) - 1:
                    print("最后一个都不能执行任务，重新开始")
                    self.click(position.outside_rect)
                    location_index += 1
                    wipe = True
                time.sleep(0.5)
            else:
                print("武将可以出征")
                time.sleep(0.5)
                self.click(position.hero_point_list[hero_index % len(position.hero_point_list)])
                time.sleep(0.5)
                if self.is_enable_wipe_out():
                    print("武将开始出征了!!!")
                    self.click(position.wipe_out_button_rect)
                    location_index += 1
                    wipe = True
                else:
                    print("但是武将没能力出征")
                    self.click(position.outside_rect)
                    time.sleep(0.5)
                    # 最后一个武将还不能出征就重新选个地
                    if hero_index % len(position.hero_point_list) == len(position.hero_point_list) - 1:
                        print("最后一个都不能执行任务，重新开始")
                        self.click(position.outside_rect)
                        location_index += 1
                        wipe = True
            time.sleep(5)
            hero_index += 1

    # 测试文字识别
    def test(self):
        text = self.get_text_by_orc(position.wipe_out_desc_rect)
        print(text)

    # 创建GUI
    def run(self):
        window = tk.Tk()
        window.title("率土之滨辅助")
        window.geometry("500x300+1414+100")
        start = tk.Button(window, text="开始", command=lambda: self.press_key_biu_biu(win32con.VK_NUMPAD0))
        start.pack()
        window.mainloop()


if __name__ == '__main__':
    ga = GameAuxiliaries()
    ga.run()
