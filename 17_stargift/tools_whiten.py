#!/usr/bin/env python3
"""Предмет на сером фоне → предмет на чистом белом, без вырезания.

Зачем не `tools_cutout.py`: у него жёсткая граница. Когда фон снят неровно —
стена, стол, мягкая тень, — маска цепляет куски фона, и по краю остаётся
рваная кромка. Вашик такие кромки уже отклонял.

Здесь границы нет вообще. Фон опознаётся по цвету — светлый и бесцветный —
и плавно уводится в белый; предмет (тёмный или насыщенный) не трогаем.
Переход мягкий, поэтому и рвать нечему. Тень под предметом уходит вместе
с фоном, её возвращаем аккуратной новой.

    python3 tools_whiten.py --out=img_box/wht img_box/orig_glove5.jpg
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

R = os.path.dirname(os.path.abspath(__file__))
V_LO, V_HI = -46, -9       # сдвиг от уровня фона: ниже — предмет, выше — фон
S_LO, S_HI = 26, 62        # насыщенный пиксель фоном не бывает
FEATHER = 2.2              # размытие маски, px: убирает ступеньку на кромке
MAXPX = 1600


def smoothstep(x, lo, hi):
    t = np.clip((x - lo) / max(1e-6, hi - lo), 0, 1)
    return t * t * (3 - 2 * t)


def bg_alpha(im):
    """Насколько пиксель похож на фон: 1 — точно фон, 0 — точно предмет.

    Одного цвета мало: стык стены со столом и складка светотени по яркости
    попадают в середину шкалы и остаются серыми пятнами. Поэтому к цвету
    добавлено расстояние: всё, что лежит поодаль от предмета, — фон, чем бы
    оно ни было. Рядом с предметом решает цвет, и переход остаётся мягким.
    """
    hsv = np.asarray(im.convert("HSV"), dtype=np.float32)
    s, v = hsv[:, :, 1], hsv[:, :, 2]

    # уровень фона снимаем с рамки кадра, а не задаём числом: у одного продавца
    # стена почти белая, у другого серая, и фиксированный порог оставляет
    # на втором серую тень вдоль предмета
    edge = np.concatenate([v[:6].ravel(), v[-6:].ravel(),
                           v[:, :6].ravel(), v[:, -6:].ravel()])
    lvl = float(np.median(edge))
    a = smoothstep(v, lvl + V_LO, lvl + V_HI) * (1 - smoothstep(s, S_LO, S_HI))

    core = a < 0.35
    core = ndimage.binary_closing(core, np.ones((9, 9)))
    lab, n = ndimage.label(core)
    if n:
        sizes = ndimage.sum(core, lab, range(1, n + 1))
        # держим все крупные куски, а не один: перчаток в кадре бывает две
        keep = np.isin(lab, 1 + np.flatnonzero(sizes >= sizes.max() * 0.15))
        near = ndimage.binary_dilation(
            ndimage.binary_fill_holes(keep),
            iterations=max(4, int(min(im.size) * 0.02)))
        near = np.asarray(
            Image.fromarray((near * 255).astype("uint8")).filter(
                ImageFilter.GaussianBlur(min(im.size) * 0.012)),
            dtype=np.float32) / 255.0
        a = 1 - (1 - a) * near

    a = Image.fromarray((a * 255).astype("uint8")).filter(
        ImageFilter.GaussianBlur(FEATHER))
    return np.asarray(a, dtype=np.float32)[:, :, None] / 255.0


def whiten(src, dst, rot=0):
    im = Image.open(src).convert("RGB")
    if rot:
        # перчатку продавец снял лежащей; на слайде она стоит, как её и
        # выставляют — так предмет занимает всю высоту, а не полосу посередине
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC,
                       fillcolor=(255, 255, 255))
    if max(im.size) > MAXPX:
        im.thumbnail((MAXPX, MAXPX), Image.LANCZOS)
    a = bg_alpha(im)
    arr = np.asarray(im, dtype=np.float32)
    out = arr * (1 - a) + 255.0 * a

    # обрезаем по предмету: пустое поле вокруг ни к чему, раскладка слайда
    # добавит своё
    m = a[:, :, 0] < 0.55
    ys, xs = np.where(m)
    if len(xs):
        pad = int(max(xs.max() - xs.min(), ys.max() - ys.min()) * 0.05)
        x0, y0 = max(0, xs.min() - pad), max(0, ys.min() - pad)
        x1, y1 = min(im.width, xs.max() + pad), min(im.height, ys.max() + pad)
        out, a, m = out[y0:y1, x0:x1], a[y0:y1, x0:x1], m[y0:y1, x0:x1]

    h, w = m.shape
    # мягкая тень: на чистом белом предмет без неё висит в воздухе
    sh = Image.fromarray((m * 130).astype("uint8"))
    sh = sh.transform((w, h), Image.AFFINE, (1, 0, 0, 0, 1, -h * 0.014))
    sh = np.asarray(sh.filter(ImageFilter.GaussianBlur(max(6, w // 40))),
                    dtype=np.float32)[:, :, None] / 255.0
    base = 255.0 - sh * np.array([67.0, 69.0, 73.0])

    obj = 1 - a                      # мягкий край, поэтому рвать нечему
    res = base * (1 - obj) + out * obj
    # заведомый фон добиваем в чистый белый: иначе кадрирование под слайд
    # растягивает кромку и по краю идёт серая полоса
    res = np.where(a > 0.88, 255.0, res)
    im2 = Image.fromarray(np.clip(res, 0, 255).round().astype("uint8"))
    im2.save(dst, quality=94)
    return im2.size


def main(paths, out, rot):
    os.makedirs(out, exist_ok=True)
    for p in paths:
        src = p if os.path.isabs(p) else os.path.join(R, p)
        name = os.path.basename(src)
        print(f"{name} → {whiten(src, os.path.join(out, name), rot)}")


if __name__ == "__main__":
    args, outdir, rot = sys.argv[1:], os.path.join(R, "whiten"), 0
    while args and args[0].startswith("--"):
        k, _, v = args.pop(0).partition("=")
        if k == "--out":
            outdir = v if os.path.isabs(v) else os.path.join(R, v)
        elif k == "--rot":          # градусы против часовой
            rot = float(v)
    if not args:
        sys.exit("usage: tools_whiten.py [--rot=90] --out=DIR file.jpg ...")
    main(args, outdir, rot)
