# -*- coding: utf-8 -*-

import sys
import time
import tkinter as tk
from ctypes import *

import numpy as np
import pytesseract
import win32api
import win32con
import win32gui
from PIL import ImageQt
from PyQt5.QtWidgets import QApplication
from pykeyboard import PyKeyboard
from pymouse import PyMouse

import src.s2_config as config
import src.s2_position as position


# 判断是否是：灰度图
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


# 睡眠seconds秒时长
def sleep(seconds):
    time.sleep(seconds)


# QImage转Image
def q_2_ipl_image(q_image):
    return ImageQt.fromqimage(q_image)


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

        # 部队兵力列表
        self.army_troops_list = [0, 0, 0, 0, 0]
        # 土地的扫荡索引
        self.manor_index_list = [0, 0]

    # 截图（并不会算上外部区域）
    def image_grab(self, rect):
        # 截图工具
        app = QApplication(sys.argv)
        screen = app.primaryScreen()
        return q_2_ipl_image(
            screen.grabWindow(self.hwnd, rect[0] - 7, rect[1] - self.title_bar_height, rect[2] - rect[0],
                              rect[3] - rect[1]).toImage())

    # 输入数字串
    def type_number_biu_biu(self, text):
        for item in text:
            win32api.SendMessage(self.hwnd, win32con.WM_CHAR, 48 + int(item), 0)

    # 键盘按下事件
    def press_key_biu_biu(self, key):
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, key, 0)

    # 键盘抬起释放
    def release_key_biu_biu(self, key):
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, key, 0)

    # 发送
    def click_biu_biu(self, x, y):
        long_position = win32api.MAKELONG(x - 7, y - self.title_bar_height)
        sleep(0.05)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        sleep(0.05)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)

    # 发送
    def click_biu_biu_send(self, x, y):
        self.mouse.click(x, y)

    # 矩形区域中心点点击
    def click(self, rect):
        point = position.point(rect)
        self.click_biu_biu(point[0], point[1])

    # 矩形左中点击
    def click_left(self, rect):
        self.click_biu_biu(rect[0] + 5, int((rect[1] + rect[3]) / 2))
        sleep(0.1)
        self.click_biu_biu(rect[0], int((rect[1] + rect[3]) / 2))
        sleep(0.1)

    # 矩形右中点击
    def click_right(self, rect):
        self.click_biu_biu(rect[2] - 5, int((rect[1] + rect[3]) / 2))
        sleep(0.1)
        self.click_biu_biu(rect[2], int((rect[1] + rect[3]) / 2))
        sleep(0.1)

    # 矩形百分比点击
    def click_percent(self, rect, percent):
        self.click_biu_biu(int(rect[0] + (rect[2] - rect[0]) * percent), int((rect[1] + rect[3]) / 2))

    # 矩形区域中心点移动
    def move(self, rect):
        point = position.point(rect)
        self.mouse.move(point[0], point[1])

    # 点击地图菜单按钮
    def click_map_menu(self):
        self.click(position.map_menu_rect)
        sleep(0.2)

    # 点击标记定位菜单按钮
    def click_location_menu(self):
        self.click(position.location_menu_rect)
        sleep(0.2)

    # 定位主城
    def location_main_city(self):
        self.click_location_menu()
        self.click(position.location_menu_main_city_rect)
        sleep(1.5)

    # 定位跳转
    def location_jump(self, point):
        self.click_map_menu()
        self.location_input(position.location_input_x_rect, str(point[0]))
        self.location_input(position.location_input_y_rect, str(point[1]))
        self.click(position.location_jump_rect)

    # 回退键
    def backspace(self):
        self.press_key_biu_biu(win32con.VK_BACK)

    # 点击坐标输入框并输入（单个）
    def location_input(self, rect, value):
        point = position.point(rect)
        # 点击坐标输入框
        self.click_biu_biu(point[0], point[1])
        sleep(0.1)
        # 删除坐标内容
        self.backspace()
        sleep(0.1)
        self.backspace()
        sleep(0.1)
        self.backspace()
        sleep(0.1)
        self.backspace()
        # 输入坐标
        self.type_number_biu_biu(value)
        sleep(0.3)

    # 地图放大
    def enlarge(self):
        self.press_key_biu_biu(win32con.VK_CONTROL)
        sleep(0.1)
        win32api.SendMessage(self.hwnd, win32con.WM_MOUSEWHEEL, win32api.MAKELONG(0, 120),
                             win32api.MAKELONG(self.center_x, self.center_y))
        sleep(0.5)
        self.release_key_biu_biu(win32con.VK_CONTROL)
        sleep(1)

    # 地图还原尺寸
    def reduction(self):
        self.press_key_biu_biu(win32con.VK_CONTROL)
        sleep(0.1)
        win32api.SendMessage(self.hwnd, win32con.WM_MOUSEWHEEL, win32api.MAKELONG(0, -120),
                             win32api.MAKELONG(self.center_x, self.center_y))
        sleep(0.5)
        self.release_key_biu_biu(win32con.VK_CONTROL)
        sleep(1)

    # 扫荡
    def wipe_out(self, point):
        # 定位到指定坐标（居中）
        self.location_jump(point)
        sleep(1.5)
        # 地图放大
        self.enlarge()
        # 点击土地
        self.click_biu_biu(self.center_x, self.center_y)
        sleep(0.5)
        # 点图还原
        self.reduction()
        # 点击扫荡菜单
        self.click(position.wipe_out_menu_rect)
        sleep(0.8)

    # 武将出征
    def hero_wipe_out(self, point):
        # 点击武将1
        self.click_biu_biu(point[0], point[1])
        sleep(0.8)

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
    def image_two_value(self, image, threshold=85):
        table = []
        for i in range(256):
            if i < threshold:
                table.append(1)
            else:
                table.append(0)
        return image.point(table, '1')

    # 获取指定区域内的文字内容
    def get_text_by_orc(self, rect, threshold=85):
        image = self.image_grab(rect)
        image = image.convert('L')
        image = self.image_two_value(image, threshold=threshold)
        return pytesseract.image_to_string(image, lang='chi_sim', config='--psm 7')

    # 获取指定区域内的数字内容
    def get_number_by_orc(self, rect, threshold=200):
        image = self.image_grab(rect)
        image = image.convert('L')
        image = self.image_two_value(image, threshold=threshold)
        number = pytesseract.image_to_string(image, lang='eng',
                                             config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')
        if number.isdigit():
            return int(number)
        else:
            return 0

    # 获取指定区域内的数字内容
    def get_number_pair_by_orc(self, rect, threshold=200):
        image = self.image_grab(rect)
        image = image.convert('L')
        image = self.image_two_value(image, threshold=threshold)
        number = pytesseract.image_to_string(image, lang='eng',
                                             config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789/')
        if number.find("/") < 0:
            return [0, 0]
        else:
            pair = number.split("/")
            if pair[0].isdigit() and pair[1].isdigit():
                return [int(pair[0]), int(pair[1])]
            else:
                return [0, 0]

    # 获取指定区域内的数字内容
    def get_time_by_orc(self, rect, threshold=200):
        image = self.image_grab(rect)
        image = image.convert('L')
        image = self.image_two_value(image, threshold=threshold)
        time_str = pytesseract.image_to_string(image, lang='eng',
                                               config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789:')
        print(time_str)
        return time_str

    # 是否可以出征（通过系统提示语）
    def is_enable_wipe_out_by_system(self):
        text = self.get_text_by_orc(position.wipe_out_desc_rect)
        print("系统出征提示： %s" % text)
        return text.find("强盛") < 0

    # 是否可以出征
    def is_enable_wipe_out(self, hero_index, manor_index, troops):
        threshold = config.wipe_out_threshold_dict[hero_index][manor_index]
        print("推荐兵力：{threshold}，当前兵力：{troops}".format(threshold=str(threshold), troops=str(troops)))
        return threshold <= troops

    # 时间转换
    def time_str_2_seconds(self, time_str):
        time_split = time_str.split(":")
        if len(time_split) != 3:
            return 0
        else:
            return int(time_split[0]) * 60 * 60 + int(time_split[1]) * 60 + int(time_split[2])

    # 寻找合适的征兵时间
    def fit_conscription(self, physical):
        # 最大时长
        max_duration = 0
        max_index = -1
        for rect in position.hero_conscription_duration_rect_list:
            max_index += 1
            duration = self.time_str_2_seconds(self.get_time_by_orc(rect, threshold=130))
            print("武将 " + str(max_index + 1) + "征兵时长：" + str(duration))
            if duration > max_duration:
                max_duration = duration
        print("最大征兵时长：%d" % max_duration)
        # 可用时长，即体力满之前的时长
        enable_duration = (130 - physical) * 60 * 60 / 20
        print("可用征兵时长：%d" % enable_duration)
        # 总时长
        if max_duration > enable_duration:
            percent = enable_duration / max_duration
            print("征兵时间大于剩余体力恢复：占比：%s" % str(percent))
            self.click_percent(position.hero_conscription_rect_list[max_index], percent)
        else:
            print("征兵时间小于剩余体力恢复")

    # 单个武将征兵
    def hero_conscription(self, hero_index):
        print("判断武将是否是灰色状态：")
        if is_gray_map(self.image_grab(position.top_right(position.city_hero_point_list[hero_index]))):
            print("武将灰色状态不能征兵")
            sleep(2)
            return
        if self.get_text_by_orc(position.hero_status(position.city_hero_point_list[hero_index]), threshold=180).find(
                "征") >= 0:
            print("武将正在征兵")
            sleep(2)
            return
        print("点击第一个武将队伍")
        self.click(position.city_hero_point_list[hero_index])
        sleep(1)
        self.army_troops_list[hero_index] = self.get_number_by_orc(position.army_hero_troops_rect)
        print("获取武将兵力数量：%d" % self.army_troops_list[hero_index])
        print("点击武将一")
        self.click(position.army_hero_1_rect)
        sleep(1)
        physical = self.get_number_pair_by_orc(position.hero_physical_value_rect, threshold=80)
        print("获取武将体力值：%d" % physical[0])
        print("关闭武将属性页面")
        self.click(position.page_close_rect)
        sleep(0.5)
        print("判断兵力是否够最低的，不够就征兵：")
        # TODO 判断兵力是否够最低的，不够就征兵：
        print("判断体力是否不太满：")
        # TODO 征兵逻辑待完善
        if physical[0] < 130 - 20:
            print("体力不太满：")
            print("点击征兵按钮")
            self.click(position.conscription_button_rect)
            sleep(0.5)
            print("判断是否是在征兵状态")
            for rect in position.conscription_status_rect_list:
                if self.get_text_by_orc(rect, threshold=160).find("征兵中") >= 0:
                    print("征兵中，返回上一页面")
                    self.click(position.outside_rect)
                    sleep(1)
                    self.click(position.page_return_rect)
                    sleep(2)
                    return
            print("征兵数量拖动到最大")
            for rect in position.hero_conscription_rect_list:
                self.click_right(rect)
            print("寻找合适的征兵数量")
            self.fit_conscription(physical[0])
            sleep(1)
            print("确认征兵")
            self.click(position.conscription_confirm_button_rect)
            sleep(1)
            print("弹框确认征兵")
            self.click(position.conscription_dialog_confirm_button_rect)
            sleep(1)
            print("回到上一页")
            self.click(position.page_return_rect)
        else:
            print("体力有点满：")
            print("回到上一页")
            self.click(position.page_return_rect)
        sleep(2)

    # 征兵操作
    def conscription(self):
        print("定位主城位置")
        self.location_main_city()
        print("点击主城菜单")
        self.click(position.city_menu_rect)
        sleep(2)

        # 遍历武将征兵
        for index in range(0, 5):
            self.hero_conscription(index)

        print("返回上一页")
        self.click(position.page_return_rect)
        sleep(2)

    # 武将扫荡分析
    def hero_wipe_out_analysis(self, hero_index, troops):
        manor_dict = config.wipe_out_threshold_dict[hero_index]
        enable_index = -1
        for index in range(0, 2):
            if manor_dict[index] <= troops:
                print(manor_dict[index])
                print(troops)
                enable_index = index
                break
        if enable_index >= 0:
            print("有能战胜的土地：%d 级地" % (6 - enable_index))
            print("寻找合适的土地：")
            rect = config.wipe_out_location_dict["manor_%d" % (6 - enable_index)][self.manor_index_list[enable_index]]
            print("合适的土地坐标：" + str(rect))
            print("定位扫荡地点")
            self.wipe_out(rect)
            print("判断武将灰度状态")
            image = self.image_grab(position.top_right(position.hero_point_list[hero_index]))
            if is_gray_map(image) or not self.is_enable_wipe_out(hero_index, enable_index,
                                                                 self.get_number_by_orc(position.hero_troops(
                                                                     position.hero_point_list[hero_index % len(
                                                                         position.hero_point_list)]))):
                print("武将是灰色状态，无法出征")
                print("点击外部区域回到上一页")
                sleep(0.5)
                self.click(position.outside_rect)
            else:
                print("武将可以出征")
                sleep(0.5)
                self.click(position.hero_point_list[hero_index % len(position.hero_point_list)])
                sleep(0.5)
                print("武将开始出征了")
                self.click(position.wipe_out_button_rect)
                print(enable_index)
                print(self.manor_index_list[enable_index])
                print(len(manor_dict))
                self.manor_index_list[enable_index] = (self.manor_index_list[enable_index] + 1) % len(manor_dict)
                print(self.manor_index_list[enable_index])
                sleep(2)

        else:
            print("没有能战胜的土地")

    # 扫荡测试
    def hero_wipe_out_test(self):

        while True:
            # 征兵
            self.conscription()

            print(self.army_troops_list)

            for index in range(0, 5):
                self.hero_wipe_out_analysis(index, self.army_troops_list[index])
            sleep(7 * 60)

    # 测试文字识别
    def test(self):
        print(self.get_text_by_orc(position.conscription_status_rect_list[2], threshold=160))

    # 创建GUI
    def run(self):
        window = tk.Tk()
        window.title("率土之滨辅助")
        window.geometry("500x300+1414+100")
        start = tk.Button(window, text="开始", command=lambda: self.hero_wipe_out_test())
        start.pack()
        window.mainloop()


if __name__ == '__main__':
    ga = GameAuxiliaries()
    ga.run()
