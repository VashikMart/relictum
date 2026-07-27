#!/usr/bin/env python3
"""PDF → «плоский» PPTX: один слайд = один цельный кадр страницы.

    python3 tools_pdf_to_pptx_flat.py STARGIFT_Muzey_futbola.pdf --out out.pptx

Ничего не редактируется, зато совпадает с PDF пиксель в пиксель и
никакой вьюер не может перепутать картинки местами: каждый слайд —
один файл со своим именем и уникальными байтами (текстовая метка в JPEG).
"""
import argparse, os, shutil, subprocess, tempfile

from PIL import Image
from pptx import Presentation
from pptx.util import Emu

ap = argparse.ArgumentParser()
ap.add_argument('pdf')
ap.add_argument('--out', required=True)
ap.add_argument('--dpi', type=int, default=192)   # 1280x720 css-px → 2560x1440
A = ap.parse_args()

PX = lambda v: Emu(int(round(v / 96 * 914400)))

tmp = tempfile.mkdtemp(prefix='flat_')
subprocess.run(['pdftoppm', '-jpeg', '-r', str(A.dpi),
                os.path.abspath(A.pdf), os.path.join(tmp, 'p')], check=True)
pages = sorted(os.listdir(tmp))
assert pages, 'pdftoppm не отдал страниц'

prs = Presentation()
prs.slide_width = PX(1280)
prs.slide_height = PX(720)
blank = prs.slide_layouts[6]

for i, name in enumerate(pages, 1):
    src = os.path.join(tmp, name)
    dst = os.path.join(tmp, 'slide_%03d.jpg' % i)      # своё имя каждой странице
    im = Image.open(src).convert('RGB')
    # уникальная метка в комментарии JPEG — байты у всех файлов разные,
    # склейка одинаковых картинок по хешу содержимого невозможна в принципе
    im.save(dst, quality=90, comment=('stargift-page-%03d' % i).encode())
    sl = prs.slides.add_slide(blank)
    sl.shapes.add_picture(dst, 0, 0, PX(1280), PX(720))

prs.save(A.out)
shutil.rmtree(tmp, ignore_errors=True)
print('saved', A.out, os.path.getsize(A.out) // 1024, 'KB,', len(pages), 'слайдов')
