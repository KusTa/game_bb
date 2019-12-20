# -*- coding: utf-8 -*-

# 鼠标事件封装


import win32api
import win32con
import src.time as time
import src.position_util as position_util
import src.window as window


# 鼠标按下：hwnd窗口句柄，x坐标，y坐标
def click_point(hwnd, x, y):
    # 位置坐标
    long_position = win32api.MAKELONG(x - window.left_space, y - window.top_space)
    # 鼠标左键按下
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
    time.sleep(0.1)
    # 鼠标左键抬起
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)


# 鼠标滚动：hwnd窗口句柄，z滚动距离，x坐标，y坐标
def scroll(hwnd, z, x, y):
    win32api.SendMessage(hwnd, win32con.WM_MOUSEWHEEL, win32api.MAKELONG(0, z),
                         win32api.MAKELONG(x, y))


# 鼠标点击传入矩形
def click(hwnd, rect):
    point = position_util.point(rect)
    click_point(hwnd, point[0], point[1])


# 按住移动
def press_move(hwnd, start, end):
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(start[0], start[1]))
    i = start[1]
    while i >= end[1]:
        win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, win32con.MKF_MOUSEMODE, win32api.MAKELONG(start[0], i))
        i -= 1
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, win32api.MAKELONG(start[0], start[1]))
