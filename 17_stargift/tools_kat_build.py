#!/usr/bin/env python3
"""«Металлика и Depeche Mode» — дека в двух раскладках.

    python3 tools_kat_build.py H    # → deck_kat_H.html  1280×720
    python3 tools_kat_build.py V    # → deck_kat_V.html  720×1280

Контекст лота идёт первым абзацем описания рядом с фото — отдельных
слайдов-справок нет, разделителями остаются только главы.
"""
import html, os, sys

import json

from tools_kat_data import LOTS, ORDER, CHAPTERS

V = (sys.argv[1].upper() if len(sys.argv) > 1 else "H") == "V"
R = os.path.dirname(os.path.abspath(__file__))
C = "img_kat"
W, H = (720, 1280) if V else (1280, 720)


def esc(s):
    return html.escape(s or "", quote=False)


def rub(n):
    return f"{n:,}".replace(",", " ") + "&nbsp;₽"


_oi = os.path.join(R, C, "orig", "index.json")
ORIG = json.load(open(_oi, encoding="utf-8")) if os.path.exists(_oi) else {}


def img(tag):
    """Фото лота.

    У предметов со сложной границей (вырубной конверт, нотный лист, накладка
    гитары) автоматический вырез оставляет рваный край — для них берём
    оригинальный кадр объявления как есть. Остальным вырез идёт на пользу.
    """
    if tag in ORIG:
        return f"{C}/orig/{tag}_0.jpg"
    for p in (f"{C}/cut/{tag}.jpg", f"{C}/pick/{tag}.jpg"):
        if os.path.exists(os.path.join(R, p)):
            return p
    return f"{C}/pick/{tag}.jpg"


def extra(tag):
    """Дополнительные кадры объявления — на отдельный слайд ракурсов."""
    return [f"{C}/orig/{tag}_{i}.jpg" for i in range(1, len(ORIG.get(tag, [])))]


BASE = """
:root{--noir:#0B0B0C;--gold:#A98545;--gold2:#C9A96A;--ivory:#F5F1E8;
      --paper:#F7F5F1;--ink:#1A1A1A;--cert:#9a958c}
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;overflow:hidden;background:#000;font-family:'Inter',sans-serif}
.deck{height:100%;position:relative}
.slide{position:absolute;inset:0;display:none;overflow:hidden}
.slide.on{display:grid}
.slide>*{min-height:0;min-width:0}
img{display:block}
.serif{font-family:'Cormorant Garamond',serif}
.white{background:#FFFFFF;color:var(--ink)}
.light{background:var(--paper);color:var(--ink)}
.dark{background:var(--noir);color:var(--ivory)}
.rule{height:1px;background:rgba(169,133,69,.55)}
.div-huge{font-family:'Cormorant Garamond';font-weight:300;line-height:1.02;color:var(--ivory)}
"""

CSS_H = BASE + """
.kick{font:500 13px/1 'Inter';letter-spacing:.34em;text-transform:uppercase;color:var(--gold)}
.kick.d{color:var(--gold2)}
.solo{grid-template-columns:1.24fr 1fr}
.ph{background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden;padding:44px 40px}
.ph img{max-width:100%;max-height:100%;object-fit:contain}
.side{display:flex;flex-direction:column;justify-content:center;padding:48px 54px 48px 30px}
.nm{font-family:'Cormorant Garamond';font-weight:500;font-size:34px;line-height:1.13;color:var(--ink)}
.hist{margin-top:16px;padding-left:16px;border-left:2px solid var(--gold)}
.era{font:500 12px/1 'Inter';letter-spacing:.22em;text-transform:uppercase;color:var(--gold);margin-bottom:8px}
.histt{font:300 17px/1.52 'Inter';color:#3d3d3d}
.tx{font:300 18px/1.56 'Inter';color:#4a4a4a;margin-top:15px}
.pr{font-family:'Cormorant Garamond';font-weight:500;font-size:38px;color:var(--gold);margin-top:18px}
.ct{font:400 12.5px/1.5 'Inter';letter-spacing:.18em;text-transform:uppercase;color:var(--cert);margin-top:9px}
.div-sub{font:300 22px/1.6 'Inter';color:#c9c3b7}
.lad-row{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:baseline;
  padding:9px 0;border-bottom:1px solid rgba(169,133,69,.2)}
.lad-nm{font:300 16px/1.32 'Inter';color:#d5cfc3}
.lad-pr{font-family:'Cormorant Garamond';font-weight:500;font-size:23px;color:var(--gold2);white-space:nowrap}
.lad{display:grid;grid-template-columns:1fr 1fr;gap:0 44px;align-content:start}
"""

CSS_V = BASE + """
.kick{font:500 15px/1 'Inter';letter-spacing:.28em;text-transform:uppercase;color:var(--gold)}
.kick.d{color:var(--gold2)}
.solo{grid-template-rows:1fr auto}
.ph{background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden;padding:34px 40px}
.ph img{max-width:100%;max-height:100%;object-fit:contain}
.side{padding:34px 44px 42px;border-top:1px solid rgba(169,133,69,.35);background:var(--paper)}
.nm{font-family:'Cormorant Garamond';font-weight:500;font-size:38px;line-height:1.06;color:var(--ink);margin-top:13px}
.hist{display:none}
.era{font:500 14px/1 'Inter';letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-top:15px}
.histt{display:none}
.tx{font:300 21px/1.45 'Inter';color:#4a4a4a;margin-top:10px}
.pr{font-family:'Cormorant Garamond';font-weight:500;font-size:44px;color:var(--gold);margin-top:18px}
.ct{font:400 14px/1.5 'Inter';letter-spacing:.16em;text-transform:uppercase;color:var(--cert);margin-top:9px}
.div-sub{font:300 24px/1.5 'Inter';color:#c9c3b7;margin-top:20px}
.lad-row{display:grid;grid-template-columns:1fr auto;gap:18px;align-items:baseline;
  padding:9px 0;border-bottom:1px solid rgba(169,133,69,.2)}
.lad-nm{font:300 15px/1.28 'Inter';color:#d5cfc3}
.lad-pr{font-family:'Cormorant Garamond';font-weight:500;font-size:21px;color:var(--gold2);white-space:nowrap}
.lad{display:grid;grid-template-columns:1fr;align-content:start}
"""


def main():
    S, n = [], 0

    def add(s):
        nonlocal n
        n += 1
        S.append(s.replace("__ID__", f"s{n:02d}"))

    def solo(tag, kick):
        it = LOTS[tag]
        if V:
            body = (f'<div class="nm">{esc(it["name"])}</div>'
                    f'<div class="era">{esc(it["era"])}</div>'
                    f'<div class="tx">{esc(it["hist"])}</div>')
        else:
            body = (f'<div class="nm">{esc(it["name"])}</div>'
                    f'<div class="hist"><div class="era">{esc(it["era"])}</div>'
                    f'<div class="histt">{esc(it["hist"])}</div></div>'
                    f'<div class="tx">{esc(it["text"])}</div>')
        add(f"""<section class="slide {'light' if V else 'white'} solo" id="__ID__">
  <div class="ph"><img src="{img(tag)}" alt=""></div>
  <div class="side">
    <div class="kick">{esc(kick)}</div>
    {body}
    <div class="pr">{rub(it['price'])}</div>
    <div class="ct">{esc(it['cert'])}</div>
  </div>
</section>""")

    def angles(tag, kick, shots):
        cells = "".join(
            f'<div style="background:#F7F5F1;display:flex;align-items:center;'
            f'justify-content:center;overflow:hidden;height:100%">'
            f'<img src="{p}" alt="" style="max-width:100%;max-height:100%;object-fit:contain"></div>'
            for p in shots)
        cols = len(shots)
        if V:
            add(f"""<section class="slide light" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="display:grid;grid-template-rows:repeat({cols},1fr);gap:12px;padding:34px 40px 0">{cells}</div>
  <div style="padding:26px 44px 38px;border-top:1px solid rgba(169,133,69,.35)">
    <div class="kick">{esc(kick)}</div>
    <div class="serif" style="font-weight:500;font-size:34px;line-height:1.06;margin-top:12px">{esc(LOTS[tag]['name'])}</div>
    <p style="font:300 20px/1.45 'Inter';color:#4a4a4a;margin-top:10px">Оригинальные кадры объявления: предмет с других сторон.</p>
  </div>
</section>""")
        else:
            add(f"""<section class="slide white" id="__ID__" style="grid-template-rows:auto 1fr auto">
  <div style="padding:32px 60px 0;display:flex;justify-content:space-between;align-items:baseline">
    <div class="serif" style="font-weight:500;font-size:30px;color:var(--ink);max-width:60ch">{esc(LOTS[tag]['name'])}</div>
    <span class="kick">{esc(kick)}</span>
  </div>
  <div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:20px;padding:22px 60px 0">{cells}</div>
  <div style="padding:18px 60px 32px;font:300 17.5px/1.5 'Inter';color:#4a4a4a">Оригинальные кадры объявления: предмет с других сторон.</div>
</section>""")

    def divider(kick, huge, sub, photo):
        if V:
            add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr">
  <div style="position:relative">
    <img src="{photo}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 40%">
    <div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,11,12,.97) 0%,rgba(11,11,12,.84) 32%,rgba(11,11,12,.25) 64%,rgba(11,11,12,.08) 100%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:flex-end;padding:0 48px 72px">
      <div class="kick d" style="margin-bottom:20px">{esc(kick)}</div>
      <h2 class="div-huge" style="font-size:62px">{huge}</h2>
      <div class="rule" style="width:84px;margin:24px 0"></div>
      <p class="div-sub">{esc(sub)}</p>
    </div>
  </div>
</section>""")
        else:
            add(f"""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="position:relative">
    <img src="{photo}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 40%">
    <div style="position:absolute;inset:0;background:linear-gradient(270deg,rgba(11,11,12,.95) 0%,rgba(11,11,12,.8) 36%,rgba(11,11,12,.25) 68%,rgba(11,11,12,.06) 100%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:flex-end;text-align:right;padding:0 62px">
      <div class="kick d" style="margin-bottom:22px">{esc(kick)}</div>
      <h2 class="div-huge" style="font-size:58px;max-width:15ch">{huge}</h2>
      <div class="rule" style="width:70px;margin:26px 0"></div>
      <p class="div-sub" style="max-width:40ch">{esc(sub)}</p>
    </div>
  </div>
</section>""")

    # ---------- обложка
    cover = img("ph_band_x2")
    if V:
        add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="position:relative;background:#0B0B0C">
    <img src="{cover}" alt="" style="width:100%;height:100%;object-fit:contain;padding:40px 30px 0">
    <div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,11,12,.99) 0%,rgba(11,11,12,.72) 30%,rgba(11,11,12,0) 62%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:flex-end;padding:0 48px 40px">
      <img src="img/stargift_logo.png" alt="Stargift" style="height:112px;width:auto;object-fit:contain;filter:brightness(0) invert(1);align-self:flex-start;margin-bottom:30px">
      <div class="kick d" style="margin-bottom:18px">Частное собрание · Музыка</div>
      <h1 class="serif" style="font-weight:300;font-size:66px;line-height:1.03;color:var(--ivory)">Metallica<br>Depeche Mode</h1>
      <p style="font:300 22px/1.5 'Inter';color:#b8b2a6;margin-top:20px">Тридцать один предмет: пластинки, барабанные пластики,
      накладки гитар и фотографии.</p>
    </div>
  </div>
  <div style="padding:22px 48px 28px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.22em">31 предмет · август 2026</span>
  </div>
</section>""")
    else:
        add(f"""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr 1.04fr">
  <div style="display:flex;flex-direction:column;justify-content:space-between;padding:56px 52px">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:138px;width:auto;object-fit:contain;filter:brightness(0) invert(1);align-self:flex-start">
    <div>
      <div class="kick d" style="margin-bottom:22px">Частное собрание · Музыка</div>
      <h1 class="serif" style="font-weight:300;font-size:62px;line-height:1.04;color:var(--ivory)">Metallica<br>Depeche&nbsp;Mode</h1>
      <p style="font:300 18px/1.6 'Inter';color:#b8b2a6;margin-top:22px;max-width:42ch">Тридцать один предмет: пластинки, барабанные
      пластики, накладки гитар, тексты песен и фотографии. Две группы, каждая — со своим составом на стене.</p>
    </div>
    <div class="kick" style="letter-spacing:.24em">31 предмет · август 2026</div>
  </div>
  <div style="position:relative;background:#fff;display:flex;align-items:center;justify-content:center;padding:56px 46px">
    <img src="{cover}" alt="" style="max-width:100%;max-height:100%;object-fit:contain">
  </div>
</section>""")

    # ---------- главы
    HERO = {"band": img("ph_black_promo"), "solo": img("ph_lars_c"), "dm": img("ph_gahan_11x14")}
    NAMES = {"band": "Весь состав", "solo": "Участники", "dm": "Depeche Mode"}
    for grp, kick, huge, sub in CHAPTERS:
        divider(kick, huge, sub, HERO[grp])
        keys = [k for k in ORDER if LOTS[k]["grp"] == grp]
        for i, k in enumerate(keys, 1):
            kick = f"{NAMES[grp]} · {i} из {len(keys)}"
            solo(k, kick)
            sh = extra(k)
            if sh:
                angles(k, kick, sh)

    # ---------- упаковка
    if V:
        add("""<section class="slide light" id="__ID__" style="grid-template-rows:1fr 1fr auto">
  <div style="background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden"><img src="img_packaging/box_kraft.jpg" alt="" style="width:100%;height:100%;object-fit:contain;padding:22px"></div>
  <div style="background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden;border-top:1px solid rgba(169,133,69,.2)"><img src="img_packaging/bag_white.jpg" alt="" style="width:100%;height:100%;object-fit:contain;padding:22px"></div>
  <div style="padding:30px 44px 40px;border-top:1px solid rgba(169,133,69,.35)">
    <div class="kick">Упаковка Stargift</div>
    <div class="serif" style="font-weight:500;font-size:36px;line-height:1.06;margin-top:12px">Как мы отдаём подарок</div>
    <p style="font:300 21px/1.45 'Inter';color:#4a4a4a;margin-top:10px">Крафт-бумага с автографами великих, лента дома
    и плотный пакет. Оформленную работу привозим и вешаем сами.</p>
  </div>
</section>""")
    else:
        add("""<section class="slide white" id="__ID__" style="grid-template-rows:auto 1fr auto">
  <div style="padding:30px 66px 0;display:flex;justify-content:space-between;align-items:baseline">
    <h2 class="serif" style="font-weight:500;font-size:32px;color:var(--ink)">Как мы отдаём подарок</h2>
    <span class="kick">Упаковка Stargift</span>
  </div>
  <div style="display:grid;grid-template-columns:1.05fr .95fr;gap:44px;padding:18px 66px 0;align-items:center">
    <div style="height:400px;display:flex;align-items:center;justify-content:center;background:#F7F5F1;overflow:hidden"><img src="img_packaging/box_kraft.jpg" alt="" style="max-width:100%;max-height:100%;object-fit:contain"></div>
    <div style="height:400px;display:flex;align-items:center;justify-content:center;background:#F7F5F1;overflow:hidden"><img src="img_packaging/bag_white.jpg" alt="" style="max-width:100%;max-height:100%;object-fit:contain"></div>
  </div>
  <div style="padding:16px 66px 34px;font:300 18px/1.55 'Inter';color:#4a4a4a;max-width:96ch">Каждый предмет уходит в фирменной упаковке дома:
  крафт-бумага с автографами великих, лента Stargift и плотный подарочный пакет. Оформленную работу привозим и вешаем сами.</div>
</section>""")

    # ---------- прайс-лист, по главам чтобы влезал крупным кеглем
    for grp, kick, huge, sub in CHAPTERS:
        keys = [k for k in ORDER if LOTS[k]["grp"] == grp]
        rows = "".join(
            f'<div class="lad-row"><div class="lad-nm">{esc(LOTS[k]["name"])}</div>'
            f'<div class="lad-pr">{rub(LOTS[k]["price"])}</div></div>' for k in keys)
        pad = "44px" if V else "62px"
        add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:auto 1fr">
  <div style="padding:{'48px' if V else '40px'} {pad} 0">
    <div class="kick d" style="margin-bottom:12px">{esc(kick)}</div>
    <h2 class="serif" style="font-weight:300;font-size:{'48px' if V else '40px'};line-height:1;color:var(--ivory)">{len(keys)} предметов</h2>
  </div>
  <div style="padding:20px {pad} 36px"><div class="lad">{rows}</div></div>
</section>""")

    # ---------- финал
    add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="padding:0 {'44px' if V else '66px'};display:flex;flex-direction:column;justify-content:center">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:{'126px' if V else '136px'};width:auto;object-fit:contain;filter:brightness(0) invert(1);align-self:flex-start">
    <h2 class="serif" style="font-weight:300;font-size:{'50px' if V else '44px'};line-height:1.12;color:var(--ivory);margin-top:34px;max-width:{'100%' if V else '32ch'}">Металлика и Depeche Mode. Два состава, тридцать один предмет.</h2>
  </div>
  <div style="padding:24px {'44px' if V else '66px'} 40px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.24em;color:var(--gold2)">stargift.ru</span>
  </div>
</section>""")

    css = CSS_V if V else CSS_H
    tag = "V" if V else "H"
    doc = f"""<meta charset="utf-8">
<title>Stargift · Metallica и Depeche Mode</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>{css}</style>

<div class="deck">
{chr(10).join(S)}
</div>

<script>
function show(){{const raw=location.hash.slice(1);const n=raw.replace(/^s/,'');const id=n?('s'+n.padStart(2,'0')):'s01';
document.querySelectorAll('.slide').forEach(s=>s.classList.toggle('on', s.id===id));scrollTo(0,0);}}
function go(d){{const cur=+((location.hash.slice(1).replace(/^s/,''))||1);let x=cur+d;if(x<1)x=1;if(x>{n})x={n};location.hash='s'+x;}}
show();addEventListener('hashchange',show);
addEventListener('keydown',e=>{{if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' ')go(1);if(e.key==='ArrowLeft'||e.key==='PageUp')go(-1);}});
addEventListener('click',e=>{{if(e.target.closest('a'))return;go(e.clientX<innerWidth*0.32?-1:1);}});
</script>
<style>@page{{size:{W}px {H}px;margin:0}}@media print{{html,body{{overflow:visible;height:auto}}*{{box-shadow:none !important}}.slide{{animation:none}}.deck{{height:auto}}
.slide{{position:relative;inset:auto;display:grid !important;width:{W}px;height:{H}px;page-break-after:always}}}}</style>
"""
    open(f"{R}/deck_kat_{tag}.html", "w", encoding="utf-8").write(doc)
    print(f"deck_kat_{tag}.html: {n} слайдов, {W}×{H}")


if __name__ == "__main__":
    main()
