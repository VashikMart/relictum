#!/usr/bin/env python3
"""Мастер-референс категории оформления: сетка примеров с подписями.

Мастер — это один кадр, который отдаём в Higgsfield первым референсом:
модель видит сразу все варианты формата дома и держит стиль. Подпись на
каждой ячейке нужна не для красоты — по ней в промпте адресуем нужный
вариант («use the GREEN VELVET variant from the first reference»).

    python3 tools_master_sheet.py img_framing/frames_script \\
        --out master_frames_script.jpg --cols 3

Без --files берёт все .jpg папки, кроме самих master_*. Подпись ячейки —
имя файла без префикса категории; можно задать явно: «файл=ПОДПИСЬ».
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont

R = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(R, "fonts_ttf", "Inter.ttf")
CELL = (900, 675)          # 4:3 — под горизонтальные кадры рам
PAD = 10


def label_of(path):
    n = os.path.splitext(os.path.basename(path))[0]
    return n.split("_", 1)[-1].replace("_", " ").upper()


def sheet(paths, out, cols=2, cell=CELL, fit="cover"):
    cw, ch = cell
    rows = -(-len(paths) // cols)
    g = Image.new("RGB", (cw * cols, ch * rows), "white")
    dr = ImageDraw.Draw(g)
    try:
        f = ImageFont.truetype(FONT, 26)
    except OSError:
        f = ImageFont.load_default()

    for i, p in enumerate(paths):
        src, _, lab = p.partition("=")
        lab = lab or label_of(src)
        im = Image.open(src).convert("RGB")
        # cover — для горизонтальных кадров рам: обрезка по краям безопасна,
        # а поля рвали бы сетку. contain — для вертикальных предметов
        # (гитара во весь рост), которым cover срезал бы гриф.
        if fit == "contain":
            im.thumbnail((cw, ch), Image.LANCZOS)
            pad = Image.new("RGB", (cw, ch), "white")
            pad.paste(im, ((cw - im.width) // 2, (ch - im.height) // 2))
            im = pad
        else:
            s = max(cw / im.width, ch / im.height)
            im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            im = im.crop(((im.width - cw) // 2, (im.height - ch) // 2,
                          (im.width - cw) // 2 + cw, (im.height - ch) // 2 + ch))
        x, y = cw * (i % cols), ch * (i // cols)
        g.paste(im, (x, y))
        box = dr.textbbox((0, 0), lab, font=f)
        dr.rectangle([x, y, x + box[2] + PAD * 2, y + box[3] + PAD * 2], fill=(11, 11, 12))
        dr.text((x + PAD, y + PAD), lab, fill=(245, 241, 232), font=f)

    g.save(out, quality=94)
    return g.size, len(paths)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--out", required=True, help="имя файла внутри той же папки")
    ap.add_argument("--cols", type=int, default=2)
    ap.add_argument("--fit", choices=("cover", "contain"), default="cover",
                    help="contain — для вертикальных предметов во весь рост")
    ap.add_argument("--files", nargs="*", help="файл или файл=ПОДПИСЬ, по порядку")
    a = ap.parse_args()

    d = a.folder if os.path.isabs(a.folder) else os.path.join(R, a.folder)
    if a.files:
        paths = [os.path.join(d, x) if not os.path.isabs(x.split("=")[0]) else x
                 for x in a.files]
    else:
        paths = [os.path.join(d, f) for f in sorted(os.listdir(d))
                 if f.endswith(".jpg") and not f.startswith("master")]
    out = os.path.join(d, a.out)
    size, n = sheet(paths, out, a.cols, fit=a.fit)
    print(f"{a.out}: {n} примеров, {size[0]}×{size[1]}")


if __name__ == "__main__":
    main()
