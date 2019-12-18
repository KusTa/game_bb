from functools import reduce

import numpy
import cv2
from PIL import Image


# 图片相似度对比


# 计算两个图片相似度函数ORB算法
def orb_image_similar(image_l, image_r):
    try:
        # 图片转换
        img1 = cv2.cvtColor(numpy.asarray(image_l), cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(numpy.asarray(image_r), cv2.COLOR_BGR2GRAY)

        # 初始化ORB检测器
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        # 提取并计算特征点
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        # knn筛选结果
        matches = bf.knnMatch(des1, trainDescriptors=des2, k=2)

        # 查看最大匹配点数目
        good = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
        similar = len(good) / len(matches)
        return similar
    except:
        return '0'

    # 计算图片的局部哈希值--pHash


def p_hash(img):
    img = img.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, img.getdata()) / 64.
    hash_value = reduce(lambda x, y: x | (y[1] << y[0]), enumerate(map(lambda i: 0 if i < avg else 1, img.getdata())),
                        0)
    return hash_value


# 计算两个图片相似度函数局部敏感哈希算法
def p_hash_image_similarity(image_l, image_r):
    # 计算汉明距离
    distance = bin(p_hash(image_l) ^ p_hash(image_r)).count('1')
    similar = 1 - distance / max(len(bin(p_hash(image_l))), len(bin(p_hash(image_l))))
    return similar


# 直方图计算图片相似度算法
def make_specs_image(img, size=(256, 256)):
    return img.resize(size).convert('RGB')


def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)


def calc_similar(li, ri):
    return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0


# 计算相似度
def calc_similar_by_image(image_l, image_r):
    li, ri = make_specs_image(image_l), make_specs_image(image_r)
    return calc_similar(li, ri)


# 图片分割
def split_image(img, part_size=(64, 64)):
    w, h = img.size
    pw, ph = part_size
    assert w % pw == h % ph == 0
    return [img.crop((i, j, i + pw, j + ph)).copy() for i in range(0, w, pw) \
            for j in range(0, h, ph)]


# 融合相似度阈值
threshold1 = 0.85
# 最终相似度较高判断阈值
threshold2 = 0.98


# 融合函数计算图片相似度
def calc_image_similarity(image_l, image_r):
    similar_orb = float(orb_image_similar(image_l, image_r))
    similar_p_hash = float(p_hash_image_similarity(image_l, image_r))
    similar_hist = float(calc_similar_by_image(image_l, image_r))
    # 如果三种算法的相似度最大的那个大于0.85，则相似度取最大，否则，取最小。
    max_three_similarity = max(similar_orb, similar_p_hash, similar_hist)
    min_three_similarity = min(similar_orb, similar_p_hash, similar_hist)
    if max_three_similarity > threshold1:
        result = max_three_similarity
    else:
        result = min_three_similarity
    return round(result, 3)


if __name__ == '__main__':
    print(calc_image_similarity(Image.open('j.png'), Image.open('k.png')))
