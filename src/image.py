# -*- coding: utf-8 -*-

import sys

import numpy as np
import pytesseract
from PIL import ImageQt, Image
from PyQt5.QtWidgets import QApplication

import src.window as window
import src.image_similar as image_similar


# 判断图片是否是灰度图
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


# QImage转Image
def q_image_2_ipl(q_image):
    return ImageQt.fromqimage(q_image)


# 截图（并不会算上外部区域）
def image_grab(hwnd, rect):
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    return q_image_2_ipl(
        screen.grabWindow(hwnd, rect[0] - window.left_space, rect[1] - window.top_space, rect[2] - rect[0],
                          rect[3] - rect[1]).toImage())


# 是否图片颜色都大于这个阈值threshold
def is_above_main_threshold(image, threshold):
    pixel = image.getpixel((50, 50))
    for index in range(0, 3):
        if pixel[index] < threshold:
            return False
    return True


# 图片二值化：黑白图：threshold阈值
def image_two_value(image, threshold):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(1)
        else:
            table.append(0)
    return image.point(table, '1')


# 截图后处理成黑白图（便于识别）
def image_grab_clear(hwnd, rect, threshold):
    # 截图
    image = image_grab(hwnd, rect)
    # 灰度图
    image = image.convert('L')
    # 黑白图
    image = image_two_value(image, threshold=threshold)
    return image


# 获取指定区域内的文字内容：中文内容
def get_text_by_orc(hwnd, rect, threshold):
    # 截图
    image = image_grab_clear(hwnd, rect, threshold=threshold)
    # 图片识别
    return pytesseract.image_to_string(image, lang='chi_sim', config='--psm 7')


# 获取指定区域内的数字内容
def get_number_by_orc(hwnd, rect, threshold):
    # 截图
    image = image_grab_clear(hwnd, rect, threshold=threshold)
    # 图片识别
    number = pytesseract.image_to_string(image, lang='eng',
                                         config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')
    # 如果是数字返回，否则返回0
    if number.isdigit():
        return int(number)
    else:
        return 0


# 获取指定区域内的数字簇内容（包含分割符的时候成功返回）
def get_number_tuple_by_orc(hwnd, rect, threshold, split):
    # 截图
    image = image_grab_clear(hwnd, rect, threshold=threshold)
    # 图片识别
    number_tuple = pytesseract.image_to_string(image, lang='eng',
                                               config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789' + split)
    return number_tuple


# 图片是否相似，传入图片和截图位置
def is_image_similar(hwnd, image_l, rect):
    image_r = image_grab(hwnd, rect)
    image_r.save('../res/land_5_rect.png')
    return image_similar.calc_image_similarity(image_l.convert('L'), image_r.convert('L'))


# 打开图片
def open_image(path):
    return Image.open(path)
