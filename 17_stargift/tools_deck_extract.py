import json, os, asyncio
from playwright.async_api import async_playwright

DECK='/home/user/relictum/17_stargift/deck_messi.html'
OUT='/tmp/claude-0/-home-user-relictum/76f6e904-ad3d-5c42-861f-a53c8ea39044/scratchpad'
PLATE=os.path.join(OUT,'plates'); os.makedirs(PLATE,exist_ok=True)

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
      if (runs.length) out.texts.push({
        rect: rel(el.getBoundingClientRect()),
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
    if (empty && cs.backgroundImage==='none' && vis(cs.backgroundColor))
      out.decor.push({kind:'rect', rect:r, color:cs.backgroundColor});
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

# slides where the photo layer + gradient overlay must be flattened into one plate
FLATTEN = {'s01':'photo', 's06':'photo', 's09':'photo'}

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
        for sid in FLATTEN:
            await pg.evaluate("(sid)=>{document.querySelectorAll('.slide').forEach(s=>s.classList.toggle('on', s.id===sid))}", sid)
            await pg.wait_for_timeout(220)
            sel = f'#{sid} > div:has(> img)'
            await pg.evaluate("""(sid)=>{
               const s=document.getElementById(sid);
               s.querySelectorAll('*').forEach(e=>{
                 if(e.tagName!=='IMG' && !e.querySelector('img') && e.textContent.trim()) e.style.visibility='hidden';
               });
            }""", sid)
            await pg.wait_for_timeout(300)
            el = await pg.query_selector(sel)
            await el.screenshot(path=os.path.join(PLATE, sid+'_plate.png'))
            data[sid]['plate'] = {'file': sid+'_plate.png',
                                 'rect': await pg.evaluate("""(sid)=>{
                                    const s=document.getElementById(sid);
                                    const c=[...s.children].find(d=>d.querySelector('img'));
                                    const sr=s.getBoundingClientRect(), r=c.getBoundingClientRect();
                                    return {x:r.left-sr.left,y:r.top-sr.top,w:r.width,h:r.height};
                                 }""", sid)}
            await pg.evaluate("""(sid)=>{document.getElementById(sid).querySelectorAll('*').forEach(e=>e.style.visibility='')}""", sid)
        await b.close()
    json.dump(data, open(os.path.join(OUT,'geom.json'),'w'), ensure_ascii=False, indent=1)
    for k,v in data.items():
        print(k, 'imgs',len(v['imgs']), 'texts',len(v['texts']), 'plate' if 'plate' in v else '')

asyncio.run(main())
