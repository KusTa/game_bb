# -*- coding: utf-8 -*-

import src.mouse as mouse
import src.keyboard as keyboard


# Ctrl + 鼠标滚动
def ctrl_scroll(hwnd, z, x, y):
    keyboard.press_key(hwnd, keyboard.ctrl)
    mouse.scroll(hwnd, z, x, y)
    keyboard.up_key(hwnd, keyboard.ctrl)
