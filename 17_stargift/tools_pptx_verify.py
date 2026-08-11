#!/usr/bin/env python3
"""Проверка PPTX: та ли картинка легла на тот слайд.

Собранный PPTX сверяется не на глаз, а по содержимому: для каждого слайда
берём картинки в порядке документа и сравниваем их перцептивным хешем
с тем, что для этого слайда объявлено в geom.json. Любая перестановка,
подмена или дубль всплывают сразу.

    python3 tools_pptx_verify.py build/deck_mar_H STARGIFT_Goodfellas.pptx

Возвращает код 1, если нашлось несовпадение, — чтобы вставать в конвейер.
"""
import io
import json
import os
import re
import sys
import zipfile

import numpy as np
from PIL import Image

R = os.path.dirname(os.path.abspath(__file__))
NS_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
NS_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
NS_P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"


def dhash(im, n=16):
    """Перцептивный хеш: устойчив к пережатию и смене формата."""
    g = im.convert("L").resize((n + 1, n), Image.LANCZOS)
    a = np.asarray(g, dtype=np.int16)
    return (a[:, 1:] > a[:, :-1]).flatten()


def dist(a, b):
    return int((a != b).sum())


def slide_order(zf):
    """Слайды в порядке презентации, а не в порядке имён файлов в архиве."""
    import xml.etree.ElementTree as ET
    pres = ET.fromstring(zf.read("ppt/presentation.xml"))
    rels = ET.fromstring(zf.read("ppt/_rels/presentation.xml.rels"))
    tgt = {r.get("Id"): r.get("Target") for r in rels}
    out = []
    for s in pres.iter(f"{NS_P}sldId"):
        t = tgt[s.get(f"{NS_R}id")].split("/")[-1]
        out.append(f"ppt/slides/{t}")
    return out


def pics_of(zf, path):
    """Картинки слайда в порядке документа → список байтов."""
    import xml.etree.ElementTree as ET
    root = ET.fromstring(zf.read(path))
    rp = f"ppt/slides/_rels/{os.path.basename(path)}.rels"
    rels = ET.fromstring(zf.read(rp))
    tgt = {r.get("Id"): r.get("Target") for r in rels}
    out = []
    for pic in root.iter(f"{NS_P}pic"):
        blip = pic.find(f".//{NS_A}blip")
        if blip is None:
            continue
        rid = blip.get(f"{NS_R}embed")
        media = os.path.normpath(os.path.join("ppt/slides", tgt[rid])).replace("\\", "/")
        out.append((media, zf.read(media)))
    return out


def expected(geom, sid, build, root):
    """Что должно лежать на слайде — той же логикой, что и сборщик."""
    g = geom[sid]
    plates = g.get("plates") or ([g["plate"]] if g.get("plate") else [])
    exp = [os.path.join(build, "plates", p["file"]) for p in plates]

    def in_plate(r):
        for p in plates:
            q = p["rect"]
            if (r["x"] >= q["x"] - 1 and r["y"] >= q["y"] - 1
                    and r["x"] + r["w"] <= q["x"] + q["w"] + 1
                    and r["y"] + r["h"] <= q["y"] + q["h"] + 1):
                return True
        return False

    for im in g["imgs"]:
        if in_plate(im["rect"]):
            continue
        src = os.path.join(build, "logo_white.png") \
            if "invert" in (im.get("filter") or "") else os.path.join(root, im["src"])
        exp.append(src)
    return exp


def main(build, pptx, root=R, tol=12):
    geom = json.load(open(os.path.join(build, "geom.json"), encoding="utf-8"))
    sids = sorted(geom.keys(), key=lambda s: int(re.sub(r"\D", "", s)))
    zf = zipfile.ZipFile(pptx)
    slides = slide_order(zf)

    bad = 0
    if len(slides) != len(sids):
        print(f"! слайдов в PPTX {len(slides)}, в геометрии {len(sids)}")
        bad += 1

    seen = {}
    for sid, sp in zip(sids, slides):
        exp = expected(geom, sid, build, root)
        got = pics_of(zf, sp)
        if len(exp) != len(got):
            print(f"{sid}: картинок в PPTX {len(got)}, ожидалось {len(exp)}")
            bad += 1
        for i, ((media, blob), src) in enumerate(zip(got, exp)):
            try:
                h_got = dhash(Image.open(io.BytesIO(blob)))
                h_exp = dhash(Image.open(src))
            except Exception as e:
                print(f"{sid}[{i}]: не прочиталось — {e}")
                bad += 1
                continue
            d = dist(h_got, h_exp)
            if d > tol:
                print(f"{sid}[{i}]: НЕ ТА КАРТИНКА (расхождение {d}) "
                      f"— ждали {os.path.basename(src)}, лежит {media}")
                bad += 1
            seen.setdefault(media, []).append(f"{sid}[{i}]")

    dup = {m: v for m, v in seen.items() if len(v) > 1}
    if dup:
        print(f"! один media-файл переиспользован: "
              + "; ".join(f"{os.path.basename(m)} → {', '.join(v)}" for m, v in dup.items()))
        bad += 1

    print("картинки на своих местах" if not bad else f"расхождений: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: tools_pptx_verify.py BUILD_DIR file.pptx")
    sys.exit(main(sys.argv[1], sys.argv[2]))
