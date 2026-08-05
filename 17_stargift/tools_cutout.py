#!/usr/bin/env python3
"""Студийный кадр → чистый вырез предмета (PNG с прозрачностью).

Зачем: ставить экспонат на слайд вместе с куском студийного фона — значит
тащить на страницу чужой полусерый прямоугольник и терять размер самого
предмета. Вырезанный предмет ложится на фон страницы и занимает всё место,
которое ему отведено.

Почему не `remove_background`: у плоских лотов (конверт пластинки, фотография)
он вырезает фигуру, НАПЕЧАТАННУЮ внутри кадра, и уничтожает экспонат. Здесь
работаем геометрией: предмет снят фронтально, значит он — самая крупная
связная область, отличная от фона. Пиксели предмета не трогаем вообще.

    python3 tools_cutout.py --out=img_mj/cut img_mj/clean_*.jpg
        → img_mj/cut/<имя>.png
"""
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

R = os.path.dirname(os.path.abspath(__file__))
MARGIN = 0.008      # доля от большей стороны предмета — чтобы не срезать кромку
INSET = 4           # мусорная кромка исходника
TOL = 26            # порог «это не фон», по каналу яркости
MAXPX = 1500        # больше на слайде не нужно, а вес PNG растёт быстро


def item_mask(im):
    """Маска предмета: самая крупная связная область, не похожая на фон.

    Порог по одному значению не годится — у студийного фона есть градиент,
    а под предметом мягкая тень. Поэтому берём всё, что отличается от угловых
    пикселей, и оставляем крупнейший кусок: тень к предмету не примыкает
    сплошняком, а фон отсекается сам.
    """
    a = np.asarray(im, dtype=np.int16)
    h, w = a.shape[:2]
    corners = np.array([a[2, 2], a[2, w - 3], a[h - 3, 2], a[h - 3, w - 3]])
    bg = corners.mean(axis=0)
    diff = np.abs(a - bg).max(axis=2)
    m = diff > TOL

    m = ndimage.binary_closing(m, np.ones((5, 5)))
    lab, n = ndimage.label(m)
    if n == 0:
        return np.ones((h, w), bool)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    m = lab == (int(np.argmax(sizes)) + 1)
    return ndimage.binary_fill_holes(m)


def cutout(src, dst):
    im = Image.open(src).convert("RGB")
    im = im.crop((INSET, INSET, im.width - INSET, im.height - INSET))
    m = item_mask(im)

    ys, xs = np.where(m)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    pad = int(max(x1 - x0, y1 - y0) * MARGIN)
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(im.width, x1 + pad), min(im.height, y1 + pad)

    it = im.crop((x0, y0, x1, y1)).convert("RGBA")
    alpha = Image.fromarray((m[y0:y1, x0:x1] * 255).astype("uint8"))
    it.putalpha(alpha)
    if max(it.size) > MAXPX:          # прозрачный PNG весит много, а на слайде
        it.thumbnail((MAXPX, MAXPX), Image.LANCZOS)   # он всё равно меньше
    it.save(dst, optimize=True)

    # версия на белом: PNG с альфой весит в разы больше, а подложка слайда
    # всё равно белая — на странице результат неотличим
    flat = Image.new("RGB", it.size, "white")
    flat.paste(it, (0, 0), it)
    flat.save(os.path.splitext(dst)[0] + ".jpg", quality=92)
    return it.size


def main(paths, out):
    os.makedirs(out, exist_ok=True)
    for p in paths:
        src = p if os.path.isabs(p) else os.path.join(R, p)
        name = os.path.splitext(os.path.basename(src))[0] + ".png"
        size = cutout(src, os.path.join(out, name))
        print(f"{os.path.basename(src)} → {name}  {size[0]}×{size[1]}")


if __name__ == "__main__":
    args = sys.argv[1:]
    outdir = os.path.join(R, "cutout")
    while args and args[0].startswith("--"):
        k, _, v = args.pop(0).partition("=")
        if k == "--out":
            outdir = v if os.path.isabs(v) else os.path.join(R, v)
    if not args:
        sys.exit("usage: tools_cutout.py --out=DIR file.jpg ...")
    main(args, outdir)
