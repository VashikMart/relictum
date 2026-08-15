#!/usr/bin/env python3
"""Кадр плоского лота под углом → фронтальный кадр на белой студии.

Зачем: продавцы снимают программки, документы и фотографии наклонно, с
завалом и перспективой. Просить у nano выровнять ракурс можно, но у плоского
листа, весь смысл которого в двадцати подписях, любая генерация — риск: модель
перерисовывает росчерк. Здесь ракурс правится геометрией: находим четыре угла
листа и разворачиваем настоящие пиксели. Подписи остаются 1-в-1.

    python3 tools_flatten.py --mode=bright --out=img_box/flat img_box/orig_a.jpg
        → img_box/flat/orig_a.jpg   лист строго фронтально, белый фон, мягкая тень

mode=bright — светлый лист на тёмном фоне, mode=dark — тёмный на светлом,
mode=center — лист одного цвета на пёстром фоне (кирпич, дерево): образец
цвета берём из центра кадра.
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageFilter

R = os.path.dirname(os.path.abspath(__file__))
PAD = 0.075          # поле вокруг листа, доля от его большей стороны
LONG = 2000          # длинная сторона результата
SHRINK = 0.007       # ужать четырёхугольник к центру: срезает волосок фона,
                     # который иначе идёт полоской вдоль нижней кромки


def sheet_mask(bgr, mode):
    """Маска листа: самая крупная связная область нужной светлоты.

    Порог берём по Оцу — он сам находит границу между листом и фоном, а не
    подгоняется под конкретный кадр. Морфология закрывает подписи и логотипы,
    иначе тёмный росчерк рвёт светлый лист на куски.
    """
    if mode == "center":
        # Оцу делит кадр по светлоте, а кирпичная стена местами темнее тёмного
        # листа. Берём цвет: образец из центра кадра, где заведомо лист.
        # Сравниваем по цветности LAB, не по яркости: тени в швах кладки по
        # яркости совпадают с тёмно-синей обложкой, а по цвету — нет.
        lab = cv2.cvtColor(cv2.GaussianBlur(bgr, (7, 7), 0),
                           cv2.COLOR_BGR2LAB).astype(np.int16)
        h, w = lab.shape[:2]
        ref = lab[int(h * .42):int(h * .58),
                  int(w * .42):int(w * .58)].reshape(-1, 3).mean(axis=0)
        m = ((np.abs(lab[:, :, 1] - ref[1]) < 14)
             & (np.abs(lab[:, :, 2] - ref[2]) < 14)
             & (np.abs(lab[:, :, 0] - ref[0]) < 45)).astype(np.uint8) * 255
    else:
        g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        g = cv2.GaussianBlur(g, (7, 7), 0)
        flag = cv2.THRESH_BINARY if mode == "bright" else cv2.THRESH_BINARY_INV
        _, m = cv2.threshold(g, 0, 255, flag | cv2.THRESH_OTSU)

    k = np.ones((25, 25), np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((11, 11), np.uint8))

    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    if n < 2:
        raise SystemExit("лист не найден")
    big = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    return (lab == big).astype(np.uint8) * 255


def corners(mask):
    """Четыре угла листа.

    approxPolyDP на выпуклой оболочке даёт ровно четыре точки, когда лист снят
    целиком. Если контур замялся (загнутый уголок, тень), берём экстремумы
    оболочки по диагоналям — для четырёхугольника в перспективе это те же углы.
    """
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hull = cv2.convexHull(max(cnts, key=cv2.contourArea))
    peri = cv2.arcLength(hull, True)
    for f in (0.01, 0.02, 0.03, 0.04, 0.06):
        ap = cv2.approxPolyDP(hull, f * peri, True)
        if len(ap) == 4:
            return order(ap.reshape(4, 2).astype(np.float32))

    p = hull.reshape(-1, 2).astype(np.float32)
    s, d = p[:, 0] + p[:, 1], p[:, 0] - p[:, 1]
    idx = [int(np.argmin(s)), int(np.argmin(d)), int(np.argmax(s)), int(np.argmax(d))]
    return order(p[idx])


def order(p):
    """Углы по часовой от левого верхнего."""
    s, d = p[:, 0] + p[:, 1], p[:, 0] - p[:, 1]
    return np.array([p[np.argmin(s)], p[np.argmax(d)],
                     p[np.argmax(s)], p[np.argmin(d)]], dtype=np.float32)


def flatten(src, dst, mode):
    bgr = cv2.imread(src)
    q = corners(sheet_mask(bgr, mode))
    q = q + (q.mean(axis=0) - q) * SHRINK

    # стороны меряем по обеим парам: у перспективы дальняя короче ближней,
    # честный размер листа — среднее
    w = int(round((np.linalg.norm(q[1] - q[0]) + np.linalg.norm(q[2] - q[3])) / 2))
    h = int(round((np.linalg.norm(q[3] - q[0]) + np.linalg.norm(q[2] - q[1])) / 2))
    tgt = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], np.float32)
    warp = cv2.warpPerspective(bgr, cv2.getPerspectiveTransform(q, tgt), (w, h),
                               flags=cv2.INTER_LANCZOS4)

    it = Image.fromarray(cv2.cvtColor(warp, cv2.COLOR_BGR2RGB))
    k = LONG / max(it.size)
    it = it.resize((max(1, round(it.width * k)), max(1, round(it.height * k))),
                   Image.LANCZOS)

    pad = int(max(it.size) * PAD)
    canvas = Image.new("RGB", (it.width + pad * 2, it.height + pad * 2), "white")

    # мягкая тень под листом: без неё выровненный прямоугольник на белом
    # выглядит вклейкой, а не студийным кадром
    sh = Image.new("L", canvas.size, 0)
    sh.paste(230, (pad + int(pad * .10), pad + int(pad * .34), pad + it.width + int(pad * .10),
                   pad + it.height + int(pad * .34)))
    sh = sh.filter(ImageFilter.GaussianBlur(pad * 0.42))
    canvas.paste(Image.new("RGB", canvas.size, (176, 174, 170)), (0, 0), sh)
    canvas.paste(it, (pad, pad))
    canvas.save(dst, quality=94)
    return canvas.size, (w, h)


def main(paths, out, mode):
    os.makedirs(out, exist_ok=True)
    for p in paths:
        src = p if os.path.isabs(p) else os.path.join(R, p)
        name = os.path.basename(src)
        size, raw = flatten(src, os.path.join(out, name), mode)
        print(f"{name}: лист {raw[0]}×{raw[1]} → кадр {size[0]}×{size[1]}")


if __name__ == "__main__":
    args, outdir, mode = sys.argv[1:], os.path.join(R, "flat"), "bright"
    while args and args[0].startswith("--"):
        k, _, v = args.pop(0).partition("=")
        if k == "--out":
            outdir = v if os.path.isabs(v) else os.path.join(R, v)
        elif k == "--mode":
            mode = v
    if not args:
        sys.exit("usage: tools_flatten.py [--mode=bright|dark] --out=DIR file.jpg ...")
    main(args, outdir, mode)
