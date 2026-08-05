#!/usr/bin/env python3
"""Проверяет, что ничего не вылезает за пределы слайда.

    python3 tools_deck_check.py deck_museum.html

Ловит ровно тот случай, из-за которого лестница цен теряла нижние строки:
контент выходит за срез, а в PDF это выглядит как «просто короткий список».
"""
import argparse, asyncio, os
from playwright.async_api import async_playwright

_ap = argparse.ArgumentParser()
_ap.add_argument('deck')
_ap.add_argument('--slack', type=float, default=2.0, help='допуск в px')
_A = _ap.parse_args()
DECK = os.path.abspath(_A.deck)

JS = """
([sid, slack]) => {
  const s = document.getElementById(sid);
  const sr = s.getBoundingClientRect();
  const out = [];
  for (const el of s.querySelectorAll('*')) {
    const r = el.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) continue;
    const over = {
      right:  r.right  - sr.right,
      bottom: r.bottom - sr.bottom,
      left:   sr.left  - r.left,
      top:    sr.top   - r.top,
    };
    const worst = Object.entries(over).filter(([, v]) => v > slack)
                        .sort((a, b) => b[1] - a[1])[0];
    if (!worst) continue;
    // интересует сам вылезший контент, а не его контейнеры
    if ([...el.children].some(c => {
          const cr = c.getBoundingClientRect();
          return cr.right - sr.right > slack || cr.bottom - sr.bottom > slack ||
                 sr.left - cr.left > slack   || sr.top - cr.top > slack;
        })) continue;
    out.push({tag: el.tagName, cls: el.className || '',
              side: worst[0], px: Math.round(worst[1]),
              text: (el.textContent || '').trim().slice(0, 60)});
  }
  return out;
}
"""


def deck_size(path):
    """Размер слайда берём из @page самой деки — деки бывают и вертикальные."""
    import re as _re
    m = _re.search(r'@page\s*{\s*size:\s*(\d+)px\s+(\d+)px', open(path, encoding='utf-8').read())
    return (int(m.group(1)), int(m.group(2))) if m else (1280, 720)


async def main():
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium',
                                    args=['--no-sandbox', '--disable-gpu'])
        W, H = deck_size(DECK)
        pg = await b.new_page(viewport={'width': W, 'height': H})
        await pg.goto('file://' + DECK)
        await pg.wait_for_timeout(2500)
        ids = await pg.eval_on_selector_all('.slide', 'els=>els.map(e=>e.id)')
        for sid in ids:
            await pg.evaluate(
                "(sid)=>{document.querySelectorAll('.slide')"
                ".forEach(s=>s.classList.toggle('on', s.id===sid))}", sid)
            await pg.wait_for_timeout(120)
            for o in await pg.evaluate(JS, [sid, _A.slack]):
                bad += 1
                print(f"{sid}: {o['tag']}.{o['cls']} вылезает за {o['side']} "
                      f"на {o['px']}px — «{o['text']}»")
        await b.close()
    print('за срез ничего не уходит' if not bad else f'нарушений: {bad}')
    raise SystemExit(1 if bad else 0)

asyncio.run(main())
