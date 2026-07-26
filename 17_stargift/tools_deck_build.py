#!/usr/bin/env python3
"""
Сборка клиентского дека 1280×720 из манифеста лотов сайта + текстов.

    python3 tools_deck_build.py --deck kino

ПРАВИЛО, РАДИ КОТОРОГО ЭТО НАПИСАНО: фотографии лотов НИКОГДА не кропаются.
Везде object-fit:contain, раскладка подогнана под пропорции фото (с сайта они 4:3),
вокруг фото — воздух. Кроп допустим только на промо-кадрах, которых тут нет.
"""
import argparse, html, json, os

R = os.path.dirname(os.path.abspath(__file__))

CSS = """
:root{--noir:#0B0B0C;--gold:#A98545;--gold2:#C9A96A;--ivory:#F5F1E8;
      --ink:#1A1A1A;--mute:#6b6b6b;--cert:#9a958c}
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;overflow:hidden;background:#000;font-family:'Inter',sans-serif}
.deck{height:100%;position:relative}
.slide{position:absolute;inset:0;display:none;overflow:hidden}
.slide.on{display:grid}
.slide>*{min-height:0;min-width:0}
img{display:block}
.serif{font-family:'Cormorant Garamond',serif}
.kick{font:500 11px/1 'Inter';letter-spacing:.36em;text-transform:uppercase;color:var(--gold)}
.kick.d{color:var(--gold2)}
.white{background:#FFFFFF;color:var(--ink)}
.dark{background:var(--noir);color:var(--ivory)}
.wrap{padding:40px 60px}

/* разделитель главы */
.div-huge{font-family:'Cormorant Garamond';font-weight:300;line-height:1;color:var(--ivory)}
.div-rule{height:1px;width:70px;background:rgba(169,133,69,.55)}
.div-sub{font:300 19px/1.65 'Inter';color:#c9c3b7;max-width:52ch}

/* СОЛО: фото целиком слева, текст справа */
.solo{grid-template-columns:1.18fr 1fr}
.solo-ph{display:flex;align-items:center;justify-content:center;padding:52px 26px 52px 60px;background:#fff}
.solo-ph img{max-width:100%;max-height:100%;object-fit:contain}
.solo-side{display:flex;flex-direction:column;justify-content:center;padding:56px 60px 56px 26px}
.solo-name{font-family:'Cormorant Garamond';font-weight:500;font-size:36px;line-height:1.08;color:var(--ink)}
.solo-text{font:300 17px/1.65 'Inter';color:#4a4a4a;margin-top:16px}
.solo-price{font-family:'Cormorant Garamond';font-weight:500;font-size:32px;color:var(--gold);margin-top:22px}
.solo-cert{font:400 10px/1 'Inter';letter-spacing:.22em;text-transform:uppercase;color:var(--cert);margin-top:11px}

/* ДУЭТ: два лота, фото сверху целиком, подпись под фото */
.duo2{grid-template-rows:1fr}
.duo2-in{display:grid;grid-template-columns:1fr 1fr;gap:46px;padding:40px 72px 34px;align-items:start}
.dc{display:flex;flex-direction:column;align-items:center;text-align:center}
.dc-ph{width:100%;height:352px;display:flex;align-items:center;justify-content:center;background:#fff}
.dc-ph img{max-width:100%;max-height:100%;object-fit:contain}
.dc-name{font-family:'Cormorant Garamond';font-weight:500;font-size:25px;line-height:1.14;color:var(--ink);margin-top:20px;max-width:28ch}
.dc-text{font:300 15px/1.55 'Inter';color:#4a4a4a;margin-top:10px;max-width:48ch}
.dc-price{font-family:'Cormorant Garamond';font-weight:500;font-size:25px;color:var(--gold);margin-top:12px}
.dc-cert{font:400 9.5px/1 'Inter';letter-spacing:.2em;text-transform:uppercase;color:var(--cert);margin-top:8px}

/* КВАРТЕТ: четыре лота, фото целиком слева, подпись справа */
.quad{grid-template-rows:auto 1fr}
.quad-in{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;
  gap:24px 44px;padding:22px 64px 30px}
.qc{display:grid;grid-template-columns:238px 1fr;gap:20px;align-items:center}
.qc-ph{width:238px;height:190px;display:flex;align-items:center;justify-content:center;background:#fff}
.qc-ph img{max-width:100%;max-height:100%;object-fit:contain}
.qc-name{font-family:'Cormorant Garamond';font-weight:500;font-size:21px;line-height:1.12;color:var(--ink)}
.qc-text{font:300 13px/1.5 'Inter';color:#4a4a4a;margin-top:7px}
.qc-price{font-family:'Cormorant Garamond';font-weight:500;font-size:20px;color:var(--gold);margin-top:8px}
.qc-cert{font:400 9px/1 'Inter';letter-spacing:.2em;text-transform:uppercase;color:var(--cert);margin-top:6px}

/* лестница цен */
.lad{display:flex;flex-direction:column}
.lad-row{display:grid;grid-template-columns:1fr auto;gap:30px;align-items:baseline;
  padding:9px 0;border-bottom:1px solid rgba(169,133,69,.2)}
.lad-nm{font:300 14px/1.35 'Inter';color:#d5cfc3}
.lad-pr{font-family:'Cormorant Garamond';font-weight:500;font-size:21px;color:var(--gold2);white-space:nowrap}
"""


def rub(n):
    return f"{n:,}".replace(",", " ") + "&nbsp;₽"


def esc(s):
    return html.escape(s or "", quote=False)


def cert_line(c, cls):
    return f'<div class="{cls}">{esc(c)}</div>' if c else ""


def build(deck):
    man = json.load(open(f"{R}/manifest_{deck}.json", encoding="utf-8"))
    txt = json.load(open(f"{R}/texts_{deck}.json", encoding="utf-8"))
    lots_t = txt["lots"]

    def T(it, field, default=""):
        return lots_t.get(it["key"], {}).get(field, default)

    S, n = [], 0

    def add(s):
        nonlocal n
        n += 1
        S.append(s.replace("__ID__", f"s{n:02d}"))

    # ---------- обложка ----------
    hero = max((i for c in man["chapters"] for i in c["items"]), key=lambda x: x["price"])
    add(f"""<section class="slide dark on" id="__ID__" style="grid-template-columns:1.02fr 1fr">
  <div class="wrap" style="display:flex;flex-direction:column;justify-content:space-between;padding:62px 58px">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:170px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97">
    <div>
      <div class="kick d" style="margin-bottom:22px">Stargift · {esc(man['kicker'])}</div>
      <h1 class="serif" style="font-weight:300;font-size:80px;line-height:1;color:var(--ivory)">{esc(man['title'])}</h1>
      <p style="font:300 17px/1.65 'Inter';color:#b8b2a6;margin-top:28px;max-width:44ch">{esc(txt['intro'])}</p>
    </div>
    <div class="kick" style="letter-spacing:.24em">Июль 2026</div>
  </div>
  <div style="height:720px;overflow:hidden;background:#0e0f0e;display:flex;align-items:center;justify-content:center;padding:56px">
    <img src="{hero['photos'][0]}" alt="{esc(hero['title'])}" style="max-width:100%;max-height:100%;object-fit:contain;box-shadow:0 40px 90px rgba(0,0,0,.6)">
  </div>
</section>""")

    # ---------- главы ----------
    for ci, ch in enumerate(man["chapters"], 1):
        sub = txt["chapters"].get(ch["name"], {}).get("sub", ch["sub"])
        roman = ["первая", "вторая", "третья", "четвёртая", "пятая", "шестая", "седьмая", "восьмая"][ci - 1]
        add(f"""<section class="slide dark" id="__ID__" style="place-content:center;justify-items:center;text-align:center">
  <div style="max-width:66ch;padding:0 60px;display:flex;flex-direction:column;align-items:center">
    <div class="kick d" style="letter-spacing:.34em;margin-bottom:26px">Глава&nbsp;{roman}</div>
    <h2 class="div-huge" style="font-size:74px">{esc(ch['name'])}</h2>
    <div class="div-rule" style="margin:34px 0"></div>
    <p class="div-sub" style="text-align:center">{esc(sub)}</p>
  </div>
</section>""")

        items = sorted(ch["items"], key=lambda x: -x["price"])
        top, rest = items[0], items[1:]

        add(f"""<section class="slide white solo" id="__ID__">
  <div class="solo-ph"><img src="{top['photos'][0]}" alt="{esc(top['title'])}"></div>
  <div class="solo-side">
    <div class="kick" style="margin-bottom:16px">{esc(ch['name'])}</div>
    <div class="solo-name">{esc(T(top,'name',top['title']))}</div>
    <div class="solo-text">{esc(T(top,'text'))}</div>
    <div class="solo-price">{rub(top['price'])}</div>
    {cert_line(T(top,'cert'), 'solo-cert')}
  </div>
</section>""")

        # остальные — парами (фото крупные, целиком)
        for i in range(0, len(rest), 2):
            pair = rest[i:i + 2]
            cards = "".join(f"""
      <div class="dc">
        <div class="dc-ph"><img src="{p['photos'][0]}" alt="{esc(p['title'])}"></div>
        <div class="dc-name">{esc(T(p,'name',p['title']))}</div>
        <div class="dc-text">{esc(T(p,'text'))}</div>
        <div class="dc-price">{rub(p['price'])}</div>
        {cert_line(T(p,'cert'), 'dc-cert')}
      </div>""" for p in pair)
            add(f"""<section class="slide white duo2" id="__ID__">
  <div class="duo2-in">{cards}
  </div>
</section>""")

    # ---------- лестница цен ----------
    allx = sorted((i for c in man["chapters"] for i in c["items"]), key=lambda x: -x["price"])
    for pi, part in enumerate((allx[:18], allx[18:])):
        if not part:
            continue
        head = f"{len(allx)} предметов" if pi == 0 else "Продолжение"
        kick = "Подборка целиком" if pi == 0 else f"Подборка целиком · {len(allx[:18])+1}–{len(allx)}"
        rowsh = "".join(f"""<div class="lad-row"><div class="lad-nm">{esc(lots_t.get(x['key'],{}).get('name',x['title']))}</div>"""
                        f"""<div class="lad-pr">{rub(x['price'])}</div></div>""" for x in part)
        add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:auto 1fr">
  <div class="wrap" style="padding:42px 66px 0">
    <div class="kick d" style="margin-bottom:13px">{kick}</div>
    <h2 class="serif" style="font-weight:300;font-size:46px;line-height:1;color:var(--ivory)">{head}</h2>
  </div>
  <div class="wrap" style="padding:22px 66px 34px"><div class="lad">{rowsh}</div></div>
</section>""")

    # ---------- финал ----------
    add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div class="wrap" style="padding:76px 72px 0;display:flex;flex-direction:column;justify-content:center">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:146px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start">
    <h2 class="serif" style="font-weight:300;font-size:46px;line-height:1.14;color:var(--ivory);margin-top:38px;max-width:32ch">{esc(txt['final'])}</h2>
  </div>
  <div class="wrap" style="padding:26px 72px 40px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.24em;color:var(--gold2)">stargift.ru</span>
  </div>
</section>""")

    doc = f"""<meta charset="utf-8">
<title>Stargift · {esc(man['title'])}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>

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
<style>@page{{size:1280px 720px;margin:0}}@media print{{html,body{{overflow:visible;height:auto}}*{{box-shadow:none !important}}.slide{{animation:none}}.deck{{height:auto}}
.slide{{position:relative;inset:auto;display:grid !important;width:1280px;height:720px;page-break-after:always}}}}</style>
"""
    out = f"{R}/deck_{deck}.html"
    open(out, "w", encoding="utf-8").write(doc)
    print(f"{out}: {n} слайдов, {len(allx)} лотов")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", required=True)
    build(ap.parse_args().deck)
