# -*- coding: utf-8 -*-

import src.time as time
import tkinter as tk

import src.util as util

import win32api
import win32con
import win32gui
from pykeyboard import PyKeyboard
from pymouse import PyMouse

import src.assistant as assistant
import src.event as event
import src.s3_config as config
import src.path as path


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

    # 定位跳转
    def location_jump(self, point):
        print("点击地图菜单")
        event.click_map_menu(self.hwnd)
        print("输入坐标")
        event.location_input(self.hwnd, point)
        print("点击坐标跳转按钮")
        event.click_location_jump_button(self.hwnd)

    # 扫荡
    def wipe_out(self, point):
        print("定位到指定位置")
        self.location_jump(point)
        print("地图放大")
        event.map_enlarge(self.hwnd)
        print("点击土地")
        event.click_center(self.hwnd)
        print("地图还原")
        event.map_reduction(self.hwnd)
        print("点击扫荡菜单按钮")
        event.click_wipe_out_menu(self.hwnd)

    # 是否可以出征
    def is_enable_wipe_out(self, hero_index, manor_index, troops):
        threshold = config.wipe_out_threshold_dict[hero_index][manor_index]
        print("推荐兵力：{threshold}，当前兵力：{troops}".format(threshold=str(threshold), troops=str(troops)))
        return threshold <= troops

    # 寻找合适的征兵时间
    def fit_conscription(self, physical):
        # 最大时长
        max_duration = 0
        max_index = -1

        for index in range(0, 3):
            max_index += 1
            duration = assistant.get_hero_conscription_duration(self.hwnd, index)
            print("武将 " + str(max_index + 1) + "征兵时长：" + str(duration))
            if duration > max_duration:
                max_duration = duration

        print("最大征兵时长：%d" % max_duration)
        # 可用时长，即体力满之前的时长
        enable_duration = (130 - physical) * 60 * 60 / 20
        print("可用征兵时长：%d" % enable_duration)
        # 总时长
        if max_duration > enable_duration and max_duration != 0:
            percent = enable_duration / max_duration
            print("征兵时间大于剩余体力恢复：占比：%s" % str(percent))
            event.click_hero_conscription_percent(self.hwnd, max_index, percent)
        else:
            print("征兵时间小于剩余体力恢复")

    # 单个武将征兵
    def hero_conscription(self, army_index):
        print("判断武将是否是灰色状态：")
        if assistant.is_city_hero_gray(self.hwnd, army_index):
            print("武将灰色状态不能征兵")
            return
        if assistant.is_city_hero_conscription(self.hwnd, army_index):
            print("武将正在征兵中")
            return

        print("点击第一个武将队伍")
        event.click_city_army(self.hwnd, army_index)

        self.army_troops_list[army_index] = assistant.get_city_army_troops(self.hwnd)
        print("获取武将兵力数量：%d" % self.army_troops_list[army_index])

        print("点击队伍 武将大营")
        event.click_army_camp(self.hwnd)

        physical = assistant.get_hero_physical(self.hwnd)
        print("获取武将体力值：%d" % physical)

        print("关闭武将属性页面")
        event.click_page_close(self.hwnd)

        print("判断兵力是否够最低的，不够就征兵：")

        # TODO 判断兵力是否够最低的，不够就征兵：
        print("判断体力是否不太满：")
        # TODO 征兵逻辑待完善

        if physical < 130 - 20:
            print("体力不太满：")

            print("点击征兵按钮")
            event.click_conscription_button(self.hwnd)

            print("判断是否还在原来的页面")
            if assistant.is_conscription_disable(self.hwnd):
                print("征兵不可用")
                print("返回上个页面")
                event.click_page_return(self.hwnd)
                return

            print("征兵数量拖动到最大")
            for index in range(0, 3):
                event.click_hero_conscription_max(self.hwnd, index)

            print("判断是否征兵队列已满")
            if assistant.is_conscription_tip(self.hwnd):
                print("征兵队列已满, 点击外部返回")
                event.click_outside(self.hwnd)
                print("再次点击返回")
                event.click_page_return(self.hwnd)
                return

            print("寻找合适的征兵数量")
            self.fit_conscription(physical)

            print("确认征兵")
            event.click_conscription_confirm_button(self.hwnd)
            print("弹框确认征兵")
            event.click_conscription_dialog_confirm_button(self.hwnd)
            print("回到上一页")
            event.click_page_return(self.hwnd)
        else:
            print("体力有点满：")
            print("回到上一页")
            event.click_page_return(self.hwnd)

    # 征兵操作
    def conscription(self):

        print("点击标记定位菜单")
        event.click_mark_location_menu(self.hwnd)
        print("点击主城项")
        event.click_mark_location_main_city(self.hwnd)
        print("点击城池菜单")
        event.click_city_menu(self.hwnd)

        # 遍历武将征兵
        for index in range(0, 5):
            self.hero_conscription(index)

        print("返回上一页")
        event.click_page_return(self.hwnd)

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
            manor_list = config.wipe_out_location_dict["manor_%d" % (6 - enable_index)]
            manor_index = self.manor_index_list[enable_index]
            print(manor_index)
            rect = manor_list[manor_index]
            print("合适的土地坐标：" + str(rect))
            print("定位扫荡地点")
            self.wipe_out(rect)
            print("判断武将灰度状态")
            if assistant.is_expedition_hero_gray(self.hwnd, hero_index) or not \
                    self.is_enable_wipe_out(hero_index, enable_index, assistant.is_troops_enough(self.hwnd,
                                                                                                 hero_index)):
                print("武将是灰色状态，无法出征")
                print("点击外部区域回到上一页")
                event.click_outside(self.hwnd)
            else:
                print("武将可以出征")
                event.click_expedition_army(self.hwnd, hero_index)
                print("武将开始出征了")
                event.click_wipe_out_button(self.hwnd)
                self.manor_index_list[enable_index] = (self.manor_index_list[enable_index] + 1) % len(manor_dict)
                time.sleep(2)
        else:
            print("没有能战胜的土地")

    # 扫荡测试
    def hero_wipe_out_test(self):

        self.init_wipe_out_land_info()

        while True:
            # 征兵
            self.conscription()

            print(self.army_troops_list)

            for index in range(0, 5):
                self.hero_wipe_out_analysis(index, self.army_troops_list[index])
            time.sleep(20)

    # 获取坐标列表
    def get_location_list(self):
        location_list = set()
        while True:
            item_list = assistant.get_one_page_land_location_list(self.hwnd)
            before_count = len(location_list) + len(item_list)
            location_list.update(item_list)
            after_count = len(location_list)
            # 比较是否有重复的有就认为是到底了
            if before_count < 8 or before_count != after_count:
                break
            time.sleep(1)
            event.scroll_one_page(self.hwnd)
        return location_list

    # 初始化扫荡信息
    def init_wipe_out_land_info(self):
        print("打开内政页面")
        event.click_interior_menu(self.hwnd)
        print("打开内政详情页面")
        event.click_interior_detail_menu(self.hwnd)
        print("重置土地统计选项")
        event.reset_land_option(self.hwnd)

        self.init_wipe_out_land_by_level(6)
        self.init_wipe_out_land_by_level(5)

        print("返回上一页")
        event.click_page_close(self.hwnd)
        print("返回上一页")
        event.click_page_return(self.hwnd)

    # 根据土地等级获取可出征列表
    def init_wipe_out_land_by_level(self, level):
        event.click_interior_detail_menu(self.hwnd)
        print("重置土地统计选项")
        event.reset_land_option(self.hwnd)
        print("选择图地选项")
        event.click(self.hwnd, assistant.get_land_option_rect(self.hwnd, level))
        print("获取所有土地坐标")
        location_list = self.get_location_list()
        print("筛选合适的土地出征列表")
        wipe_out_land_list = util.calc_best_march_duration((201, 1442), location_list, 118)
        print("移除最后一个")
        wipe_out_land_list.pop(len(wipe_out_land_list) - 1)
        print(wipe_out_land_list)
        config.wipe_out_location_dict['manor_%d' % level] = wipe_out_land_list

    # 占领下一个土地
    def occupy_next_land(self, start, end):
        next_location = path.get_better_next_possible_location(start, end)
        min_level = 10
        fit_location = None
        for location in next_location:
            print("土地：" + str(location))
            self.location_jump(location)
            print("点击土地")
            event.click_center(self.hwnd)
            print("识别土地等级")
            land_level = assistant.get_land_level(self.hwnd)
            print("等级：%d" % land_level)
            if min_level > land_level:
                min_level = land_level
                fit_location = location
        return fit_location

    # 队伍出征
    def army_expedition(self, point):
        print("定位到指定位置")
        self.location_jump(point)
        print("地图放大")
        event.map_enlarge(self.hwnd)
        print("点击土地")
        event.click_center(self.hwnd)
        print("地图还原")
        event.map_reduction(self.hwnd)
        print("点击出征菜单按钮")
        event.click_army_expedition_menu(self.hwnd)

    # 选择部队
    def choose_army(self):
        for hero_index in range(5):
            print("判断武将灰度状态")
            # TODO 判断兵力
            if assistant.is_expedition_hero_gray(self.hwnd, hero_index):
                print("武将是灰色状态，无法出征")
                print("点击外部区域回到上一页")
            else:
                print("武将可以出征")
                event.click_expedition_army(self.hwnd, hero_index)
                print("武将开始出征了")
                duration = assistant.get_march_duration(self.hwnd)
                print("计算行军时长: " + str(duration))
                event.click_wipe_out_button(self.hwnd)
                time.sleep(duration * 2 + 30)
                return True
        return False

    def test(self):
        start = (202, 1443)
        end = (206, 1444)
        while start != end:
            temp = self.occupy_next_land(start, end)
            print("武将出征")
            self.army_expedition(temp)
            print("选择合适的武将出征")
            while not self.choose_army():
                print("重新选择武将")
                time.sleep(60)
            start = temp

    # 创建GUI
    def run(self):
        window = tk.Tk()
        window.title("率土之滨辅助")
        window.geometry("500x300+1414+100")
        start = tk.Button(window, text="开始", command=lambda: self.test())
        start.pack()
        window.mainloop()


if __name__ == '__main__':
    ga = GameAuxiliaries()
    ga.run()
