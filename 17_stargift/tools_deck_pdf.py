#!/usr/bin/env python3
"""Дек → PDF, страница на слайд. Размер берётся из @page самой деки.

    python3 tools_deck_pdf.py deck_cr7.html STARGIFT_Ronaldo_butsy.pdf

Печатаем через Chromium: в печатной ветке CSS все слайды раскрываются
подряд (`.slide{position:relative;display:grid}`), поэтому одна прогонка
даёт весь дек. Перед печатью ждём загрузки шрифтов и картинок — иначе
первые страницы уезжают на системный шрифт.
"""
import os
import re
import sys

from playwright.sync_api import sync_playwright

R = os.path.dirname(os.path.abspath(__file__))
CHROME = "/opt/pw-browsers/chromium"      # предустановленный браузер окружения


def deck_size(path):
    """Размер слайда читаем из @page — деки бывают и вертикальные."""
    m = re.search(r"@page\s*{\s*size:\s*(\d+)px\s+(\d+)px", open(path, encoding="utf-8").read())
    return (int(m.group(1)), int(m.group(2))) if m else (1280, 720)


def render(deck, out):
    src = deck if os.path.isabs(deck) else os.path.join(R, deck)
    W, H = deck_size(src)
    dst = out if os.path.isabs(out) else os.path.join(R, out)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + src, wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_function(
            "[...document.images].every(i => i.complete && i.naturalWidth > 0)",
            timeout=60_000)
        pg.pdf(path=dst, width=f"{W}px", height=f"{H}px",
               print_background=True, margin={"top": "0", "right": "0",
                                              "bottom": "0", "left": "0"})
        b.close()
    return dst


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: tools_deck_pdf.py deck.html out.pdf")
    path = render(sys.argv[1], sys.argv[2])
    print(f"{os.path.basename(path)}: {os.path.getsize(path) / 1e6:.1f} МБ")
