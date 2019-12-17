# -*- coding: utf-8 -*-

# 键盘事件封装


import win32api
import win32con

# Ctrl键
ctrl = win32con.VK_CONTROL
backspace = win32con.VK_BACK


# 按键按下：hwnd句柄，key按键
def press_key(hwnd, key):
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, key, 0)


# 按键抬起：hwnd句柄，key按键
def up_key(hwnd, key):
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, key, 0)


# 键盘输入：hwnd句柄，text文本
def type_string(hwnd, text):
    for item in text:
        win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(item), 0)
