#!/usr/bin/env python3
"""Выровненный лист → два увеличенных фрагмента с подписями.

У этих лотов одно фото объявления на предмет, а показать подписи крупно нужно.
Фрагменты режем из выровненного кадра (tools_flatten.py): это настоящие
пиксели листа, просто ближе. Пропорция фрагмента подогнана под ячейку слайда —
иначе кадр висит в сером поле и слайд выглядит пустым.

    python3 tools_box_details.py    → img_box/det/<лот>_<a|b>.jpg
"""
import os

from PIL import Image

R = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(R, "img_box", "flat")
OUT = os.path.join(R, "img_box", "det")
PAD = 0.075          # поле вокруг листа, каким его оставил tools_flatten
CELL = 572 / 540     # ячейка слайда подписей

# центр фрагмента и его ширина — в долях листа
SPEC = {
    "hof96_22": [(0.31, 0.22, 0.62), (0.69, 0.79, 0.62)],
    "hof97_19": [(0.61, 0.22, 0.62), (0.39, 0.78, 0.62)],
    "hof96_ali": [(0.45, 0.24, 0.62), (0.51, 0.60, 0.62)],
}


def cut(tag):
    im = Image.open(os.path.join(SRC, f"orig_{tag}.jpg"))
    W, H = im.size
    pad = round(max(W, H) / (1 + 2 * PAD) * PAD)
    sx, sy, sw, sh = pad, pad, W - 2 * pad, H - 2 * pad

    out = []
    for i, (cx, cy, fw) in enumerate(SPEC[tag]):
        # высоту считаем из пропорции ячейки: доля высоты листа зависит от
        # того, насколько сам лист вытянут
        fh = fw * sw / sh / CELL
        x0 = sx + round((cx - fw / 2) * sw)
        y0 = sy + round((cy - fh / 2) * sh)
        box = (max(sx, x0), max(sy, y0),
               min(sx + sw, x0 + round(fw * sw)), min(sy + sh, y0 + round(fh * sh)))
        name = f"{tag}_{'ab'[i]}.jpg"
        im.crop(box).save(os.path.join(OUT, name), quality=93)
        out.append((name, box[2] - box[0], box[3] - box[1]))
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for t in SPEC:
        for name, w, h in cut(t):
            print(f"{name}  {w}×{h}  ({w / h:.2f})")
