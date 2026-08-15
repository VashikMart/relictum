#!/usr/bin/env python3
"""Кадр лота → два увеличенных фрагмента с подписями.

У этих лотов одно фото объявления на предмет, а подписи показать крупно нужно:
в них весь смысл. Фрагменты режем из того же кадра — это настоящие пиксели,
просто ближе. Пропорция подогнана под ячейку слайда, иначе кадр висит
в сером поле и слайд выглядит пустым.

Границы предмета ищем сами: у выровненных программ вокруг белое поле, у
студийных кадров халата и трусов — тоже, и доли фрагмента считать удобнее
от самого предмета, а не от края файла.

    python3 tools_box_details.py    → img_box/det/<лот>_<a|b>.jpg
"""
import os

import numpy as np
from PIL import Image

R = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(R, "img_box", "det")
CELL = 572 / 540      # ячейка слайда подписей
WHITE = 232           # светлее — считаем полем вокруг предмета

# кадр-источник и фрагменты: центр и ширина в долях предмета
SPEC = {
    "hof96_22":  ("flat/orig_hof96_22.jpg",  [(0.31, 0.22, 0.62), (0.69, 0.79, 0.62)]),
    "hof97_19":  ("flat/orig_hof97_19.jpg",  [(0.61, 0.22, 0.62), (0.39, 0.78, 0.62)]),
    "hof96_ali": ("flat/orig_hof96_ali.jpg", [(0.45, 0.24, 0.62), (0.51, 0.60, 0.62)]),
    "robe51":    ("orig_robe51.jpg",         [(0.52, 0.30, 0.58), (0.82, 0.47, 0.52)]),
    "trunks28":  ("orig_trunks28.jpg",       [(0.30, 0.58, 0.58), (0.70, 0.52, 0.58)]),
    "trunks20":  ("orig_trunks20.jpg",       [(0.30, 0.62, 0.58), (0.70, 0.56, 0.58)]),
    "trunks18":  ("orig_trunks18.jpg",       [(0.31, 0.53, 0.58), (0.70, 0.48, 0.58)]),
    "glove_ali": ("wht/lay_glove_ali.jpg",   [(0.36, 0.52, 0.50), (0.70, 0.58, 0.46)]),
    "glove5":    ("wht/orig_glove5.jpg",     [(0.27, 0.34, 0.56), (0.73, 0.44, 0.56)]),
}


def item_box(im):
    """Прямоугольник предмета: всё, что темнее белого поля вокруг."""
    g = np.asarray(im.convert("L"), dtype=np.int16)
    m = g < WHITE
    ys, xs = np.where(m)
    if not len(xs):
        return 0, 0, im.width, im.height
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def cut(tag):
    src, spec = SPEC[tag]
    im = Image.open(os.path.join(R, "img_box", src))
    x0, y0, x1, y1 = item_box(im)
    sw, sh = x1 - x0, y1 - y0

    out = []
    for i, (cx, cy, fw) in enumerate(spec):
        # высота — из пропорции ячейки: доля зависит от того,
        # насколько сам предмет вытянут
        fh = fw * sw / sh / CELL
        bx = x0 + round((cx - fw / 2) * sw)
        by = y0 + round((cy - fh / 2) * sh)
        box = (max(0, bx), max(0, by),
               min(im.width, bx + round(fw * sw)),
               min(im.height, by + round(fh * sh)))
        name = f"{tag}_{'ab'[i]}.jpg"
        im.crop(box).save(os.path.join(OUT, name), quality=93)
        out.append((name, box[2] - box[0], box[3] - box[1]))
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for t in SPEC:
        for name, w, h in cut(t):
            print(f"{name}  {w}×{h}  ({w / h:.2f})")
