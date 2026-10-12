# -*- coding: utf-8 -*-
"""实测二维码能否被解码，并做降质鲁棒性测试（模拟手机扫码）。"""
import cv2
import numpy as np

TARGET = "https://juice-butterfly.github.io/monetary-finance-rates/"
FILES = [
    r"C:\Users\Lenovo\Desktop\利率传导诊断台-扫码展板.png",
    r"C:\Users\Lenovo\Desktop\利率传导诊断台-二维码.png",
]

det = cv2.QRCodeDetector()


def try_decode(img, label):
    # OpenCV 的签名是 (解码字符串, 角点, 校正图)，不是 (bool, str, ...)
    txt, _pts, _q = det.detectAndDecode(img)
    hit = (txt == TARGET)
    print("  %-28s -> %s" % (label, ("命中 " + txt) if hit else ("失败/不符: " + repr(txt))))
    return hit


def imread_u(path, flags=cv2.IMREAD_GRAYSCALE):
    """cv2.imread 在 Windows 上不支持中文路径，走 numpy 中转。"""
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), flags)


allok = True
for f in FILES:
    img = imread_u(f)
    print("=" * 70)
    print(f.split("\\")[-1], "尺寸", None if img is None else img.shape)
    if img is None:
        print("  读取失败"); allok = False; continue
    allok &= try_decode(img, "原图")
    for s in (0.5, 0.35, 0.25):
        small = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
        if min(small.shape) < 60:
            continue
        allok &= try_decode(small, "缩小到 %.0f%%" % (s * 100))
    # 高斯模糊 + 亮度压到 0.65（模拟光线不足、手抖）
    blur = cv2.GaussianBlur(img, (0, 0), 1.6)
    allok &= try_decode((blur * 0.65).astype(np.uint8), "模糊+偏暗")
    # 旋转 8 度（模拟歪着扫）
    h, w = img.shape
    M = cv2.getRotationMatrix2D((w / 2, h / 2), 8, 1.0)
    allok &= try_decode(cv2.warpAffine(img, M, (w, h), borderValue=255), "旋转 8°")

print("=" * 70)
print("总结：", "全部通过 ✓" if allok else "存在失败项 ✗")
