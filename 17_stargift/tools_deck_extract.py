"""Снимает с дека геометрию для сборки PPTX.

    python3 tools_deck_extract.py deck_museum.html --out build/museum
"""
import shutil
import argparse, json, os, asyncio
from playwright.async_api import async_playwright

_ap = argparse.ArgumentParser()
_ap.add_argument('deck')
_ap.add_argument('--out', default=None)
_A = _ap.parse_args()
DECK = os.path.abspath(_A.deck)
OUT = os.path.abspath(_A.out or ('build/' + os.path.basename(DECK).replace('.html','')))
os.makedirs(OUT, exist_ok=True)
PLATE=os.path.join(OUT,'plates')
shutil.rmtree(PLATE, ignore_errors=True)   # чтобы старые плейты не подмешивались
os.makedirs(PLATE, exist_ok=True)

JS_COLLECT = r"""
(sid) => {
  const slide = document.getElementById(sid);
  const sr = slide.getBoundingClientRect();
  const rel = r => ({x:r.left-sr.left, y:r.top-sr.top, w:r.width, h:r.height});
  const out = {bg:null, imgs:[], texts:[], decor:[]};
  out.bg = getComputedStyle(slide).backgroundColor;

  // images
  for (const im of slide.querySelectorAll('img')) {
    const cs = getComputedStyle(im);
    out.imgs.push({
      src: im.getAttribute('src'),
      rect: rel(im.getBoundingClientRect()),
      nat: [im.naturalWidth, im.naturalHeight],
      fit: cs.objectFit, pos: cs.objectPosition,
      filter: cs.filter
    });
  }

  // text leaves
  const hasElemText = el => [...el.children].some(c => {
      if (!c.textContent.trim().length) return false;
      if (c.tagName==='BR') return false;
      const cs = getComputedStyle(c);
      return cs.display !== 'inline' || cs.position !== 'static';
  });
  const walk = el => {
    if (el.tagName==='IMG'||el.tagName==='SCRIPT'||el.tagName==='STYLE') return;
    const txt = el.textContent.replace(/ /g,' ').trim();
    if (txt.length && !hasElemText(el)) {
      const cs = getComputedStyle(el);
      const runs = [];
      const pushNode = (n, ecs) => {
        const t = n.textContent.replace(/ /g,' ');
        if (!t.trim()) return;
        runs.push({text:t, font:ecs.fontFamily.split(',')[0].replace(/["']/g,''),
                   size:parseFloat(ecs.fontSize), weight:parseInt(ecs.fontWeight)||400,
                   color:ecs.color,
                   spacing: ecs.letterSpacing==='normal'?0:parseFloat(ecs.letterSpacing),
                   upper: ecs.textTransform==='uppercase',
                   italic: ecs.fontStyle==='italic'});
      };
      const rec = (node, ecs) => {
        for (const n of node.childNodes) {
          if (n.nodeType===3) pushNode(n, ecs);
          else if (n.tagName==='BR') runs.push({br:true});
          else rec(n, getComputedStyle(n));
        }
      };
      rec(el, cs);
      // однострочные подписи меряем по самой строке: у блока-обёртки в rect
      // попадают padding и вся ширина слайда, и в PPTX текст уезжает к краю.
      let box = el.getBoundingClientRect();
      try {
        const rg = document.createRange();
        rg.selectNodeContents(el);
        const rr = rg.getBoundingClientRect();
        const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2;
        if (rr.width > 0 && rr.height > 0 && rr.height <= lh * 1.6) {
          // запас по ширине, иначе PowerPoint со своими метриками перенесёт строку
          const ta = cs.textAlign;
          const cen = ta === 'center', rgh = ta === 'right' || ta === 'end';
          const l = rr.left - (cen ? 9 : rgh ? 16 : 2);
          const rgt = rr.right + (cen ? 9 : rgh ? 2 : 16);
          box = {left: l, top: rr.top, right: rgt, bottom: rr.bottom,
                 x: l, y: rr.top, width: rgt - l, height: rr.height};
        }
      } catch (e) {}
      if (runs.length) out.texts.push({
        rect: rel(box),
        align: cs.textAlign, lh: parseFloat(cs.lineHeight)||parseFloat(cs.fontSize)*1.2,
        base: parseFloat(cs.fontSize), runs, id: el.className||el.tagName
      });
      return;
    }
    for (const c of el.children) walk(c);
  };
  walk(slide);

  // decorative rules, hairlines and flat colour blocks (no text, no gradient)
  const vis = c => c && c!=='none' && !/rgba\(\s*0,\s*0,\s*0,\s*0\s*\)/.test(c) && c!=='transparent';
  for (const el of slide.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    const r  = rel(el.getBoundingClientRect());
    if (r.w<=0 || r.h<=0) continue;
    const empty = el.tagName!=='IMG' && !el.textContent.trim() && !el.querySelector('img');
    const rad = parseFloat(cs.borderTopLeftRadius) || 0;
    const round = cs.borderTopLeftRadius.includes('%') ? parseFloat(cs.borderTopLeftRadius) >= 45
                                                       : rad >= Math.min(r.w, r.h) * 0.45;
    // фон берём и у элементов с текстом, если это небольшая плашка/кружок (бейдж, точка)
    const small = r.w < 320 && r.h < 320;
    if ((empty || small) && cs.backgroundImage==='none' && vis(cs.backgroundColor))
      out.decor.push({kind:'rect', rect:r, color:cs.backgroundColor, oval:round});
    if ((empty || small) && cs.backgroundImage.includes('gradient') && small) {
      const m = cs.backgroundImage.match(/rgba?\([^)]+\)/g);
      out.decor.push({kind:'rect', rect:r, color:(m && m[m.length-1]) || 'rgb(169,133,69)', oval:round});
    }
    for (const side of ['Top','Bottom','Left','Right']) {
      const w = parseFloat(cs['border'+side+'Width'])||0;
      const c = cs['border'+side+'Color'];
      if (w>0 && vis(c) && cs['border'+side+'Style']!=='none') {
        const rr = side==='Top'    ? {x:r.x, y:r.y, w:r.w, h:w}
                 : side==='Bottom' ? {x:r.x, y:r.y+r.h-w, w:r.w, h:w}
                 : side==='Left'   ? {x:r.x, y:r.y, w:w, h:r.h}
                 :                   {x:r.x+r.w-w, y:r.y, w:w, h:r.h};
        out.decor.push({kind:'rect', rect:rr, color:c});
      }
    }
  }
  return out;
}
"""

# блоки, где фото лежит под градиентной заливкой, — снимаем «плейтом».
# Возвращаем НОМЕРА нужных детей слайда: на обложке первый ребёнок с картинкой —
# это колонка с логотипом, и раньше плейтом уезжала именно она, а фото теряло градиент.
JS_FLATTEN = """
() => {
  const out = [];
  for (const s of document.querySelectorAll('.slide')) {
    const idx = [];
    [...s.children].forEach((c, i) => {
      if (c.querySelector(':scope > img') &&
          [...c.children].some(g => getComputedStyle(g).backgroundImage.includes('gradient')))
        idx.push(i);
    });
    if (idx.length) out.push([s.id, idx]);
  }
  return out;
}
"""

async def main():
    data={}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium',
                                    args=['--no-sandbox','--disable-gpu'])
        pg = await b.new_page(viewport={'width':1280,'height':720})
        await pg.goto('file://'+DECK)
        await pg.wait_for_timeout(2500)
        ids = await pg.eval_on_selector_all('.slide','els=>els.map(e=>e.id)')
        # measure one slide at a time, exactly as the deck lays it out (absolute, inset:0)
        for sid in ids:
            await pg.evaluate("(sid)=>{document.querySelectorAll('.slide').forEach(s=>s.classList.toggle('on', s.id===sid))}", sid)
            await pg.wait_for_timeout(220)
            data[sid] = await pg.evaluate(JS_COLLECT, sid)
        # flattened plates: hide all text, screenshot the photo container
        flatten = await pg.evaluate(JS_FLATTEN)
        print('плейтов:', ', '.join(f'{s}:{len(i)}' for s, i in flatten) or '—')
        for sid, idxs in flatten:
            await pg.evaluate("(sid)=>{document.querySelectorAll('.slide').forEach(s=>s.classList.toggle('on', s.id===sid))}", sid)
            await pg.wait_for_timeout(220)
            await pg.evaluate("""(sid)=>{
               const s=document.getElementById(sid);
               s.querySelectorAll('*').forEach(e=>{
                 if(e.tagName!=='IMG' && !e.querySelector('img') && e.textContent.trim()) e.style.visibility='hidden';
               });
            }""", sid)
            await pg.wait_for_timeout(300)
            plates = []
            for k in idxs:
                el = await pg.query_selector(f'#{sid} > *:nth-child({k + 1})')
                if el is None:
                    continue
                name = f'{sid}_{k}_plate.png'
                await el.screenshot(path=os.path.join(PLATE, name))
                rect = await pg.evaluate("""([sid,k])=>{
                   const s=document.getElementById(sid);
                   const sr=s.getBoundingClientRect(), r=s.children[k].getBoundingClientRect();
                   return {x:r.left-sr.left,y:r.top-sr.top,w:r.width,h:r.height};
                }""", [sid, k])
                plates.append({'file': name, 'rect': rect})
            if plates:
                data[sid]['plates'] = plates
            await pg.evaluate("""(sid)=>{document.getElementById(sid).querySelectorAll('*').forEach(e=>e.style.visibility='')}""", sid)
        await b.close()
    json.dump(data, open(os.path.join(OUT,'geom.json'),'w'), ensure_ascii=False, indent=1)
    for k,v in data.items():
        print(k, 'imgs',len(v['imgs']), 'texts',len(v['texts']),
              f"plates:{len(v['plates'])}" if 'plates' in v else '')

asyncio.run(main())
