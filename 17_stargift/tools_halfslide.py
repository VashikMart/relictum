#!/usr/bin/env python3
"""Фото лота → кадр ровно под половину слайда (640×720, пропорция 8:9).

Слайд лота показывает фотографию на половине листа целиком: без серых полей
и без обрезки самого предмета. Исходники генераций квадратные, поэтому
`object-fit:cover` съел бы края акрилового бокса. Скрипт делает это заранее
и по-честному: находит границы предмета, добавляет воздух и расширяет кадр
до 8:9 — фоном, а не за счёт предмета.

    python3 tools_halfslide.py img_framing/generated/*.jpg
        → img_framing/halfslide/<имя>.jpg   (1280×1440)
"""
import os
import sys

from PIL import Image

R = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(R, "img_framing", "halfslide")
ASPECT = 640 / 720          # половина слайда 1280×720
TARGET = (1280, 1440)       # 2× для печати
AIR = 0.05                  # воздух вокруг предмета, доля от большей стороны
INSET = 4                   # кромка исходника: у генераций там бывает мусор


def bg_color(im):
    """Цвет фона — по четырём углам."""
    w, h = im.size
    pts = [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)]
    px = [im.getpixel(p) for p in pts]
    return tuple(sum(c[i] for c in px) // len(px) for i in range(3))


def content_bbox(im, bg, tol=12):
    """Границы предмета: всё, что заметно отличается от фона."""
    from PIL import ImageChops
    ref = Image.new("RGB", im.size, bg)
    diff = ImageChops.difference(im, ref).convert("L")
    mask = diff.point(lambda v: 255 if v > tol else 0)
    return mask.getbbox() or (0, 0, *im.size)


def halfslide(src, dst):
    im = Image.open(src).convert("RGB")
    im = im.crop((INSET, INSET, im.width - INSET, im.height - INSET))
    W, H = im.size
    bg = bg_color(im)
    x0, y0, x1, y1 = content_bbox(im, bg)

    air = int(max(x1 - x0, y1 - y0) * AIR)
    x0, y0 = x0 - air, y0 - air
    x1, y1 = x1 + air, y1 + air

    # расширяем до 8:9 — только добавляя поле, никогда не срезая предмет
    w, h = x1 - x0, y1 - y0
    if w / h > ASPECT:
        h = w / ASPECT
    else:
        w = h * ASPECT
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    box = (round(cx - w / 2), round(cy - h / 2), round(cx + w / 2), round(cy + h / 2))

    # если кадр вышел за исходник — дорисовываем поле, предмет не двигаем
    canvas = Image.new("RGB", (box[2] - box[0], box[3] - box[1]), bg)
    canvas.paste(im, (-box[0], -box[1]))
    extend_edges(canvas, (-box[0], -box[1]), im.size)
    canvas.resize(TARGET, Image.LANCZOS).save(dst, quality=94)
    return canvas.size


def extend_edges(canvas, at, size):
    """Растянуть крайние пиксели исходника на дорисованное поле.

    Плоская заливка выдаёт себя полосой: у студийного фона есть градиент
    и виньетка. Тянем крайнюю строку/колонку — стык становится невидим.
    """
    ox, oy = at
    w, h = size
    W, H = canvas.size
    if ox > 0:
        canvas.paste(canvas.crop((ox, 0, ox + 1, H)).resize((ox, H)), (0, 0))
    if ox + w < W:
        r = W - (ox + w)
        canvas.paste(canvas.crop((ox + w - 1, 0, ox + w, H)).resize((r, H)), (ox + w, 0))
    # горизонталь — после вертикали, чтобы углы взялись из растянутых колонок
    if oy > 0:
        canvas.paste(canvas.crop((0, oy, W, oy + 1)).resize((W, oy)), (0, 0))
    if oy + h < H:
        b = H - (oy + h)
        canvas.paste(canvas.crop((0, oy + h - 1, W, oy + h)).resize((W, b)), (0, oy + h))


def main(paths, out=None):
    out = out or OUT
    os.makedirs(out, exist_ok=True)
    for p in paths:
        src = p if os.path.isabs(p) else os.path.join(R, p)
        dst = os.path.join(out, os.path.basename(src))
        size = halfslide(src, dst)
        print(f"{os.path.basename(src)}: {size[0]}×{size[1]} → 1280×1440")


if __name__ == "__main__":
    args = sys.argv[1:]
    outdir = None
    if args and args[0].startswith("--out="):
        outdir = args.pop(0).split("=", 1)[1]
        if not os.path.isabs(outdir):
            outdir = os.path.join(R, outdir)
    if not args:
        g = os.path.join(R, "img_framing", "generated")
        args = [os.path.join(g, f) for f in sorted(os.listdir(g)) if f.endswith(".jpg")]
    main(args, outdir)
