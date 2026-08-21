#!/usr/bin/env python3
"""«Собрание необычного» — 20 лотов с портала отбора, 1280×720.

    python3 tools_sel_build.py    # → deck_sel.html

Тексты лотов — единым крупным абзацем в регистре сайта, без отдельного
блока-справки. Интерьерные подачи отдельными слайдами с пометкой.
Разделители глав — с историческими фото public domain либо типографские.
"""
import html
import os

from tools_sel_data import LOTS, ORDER, CHAPTERS, INTERIORS

R = os.path.dirname(os.path.abspath(__file__))
W, H = 1280, 720
INT = {k: (f, cap) for k, f, cap in INTERIORS}

CSS = """
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
.dark{background:var(--noir);color:var(--ivory)}
.rule{height:1px;background:rgba(169,133,69,.55)}
.kick{font:500 13px/1 'Inter';letter-spacing:.32em;text-transform:uppercase;color:var(--gold)}
.kick.d{color:var(--gold2)}

.solo{grid-template-columns:640px 1fr}
.ph{background:#fff;overflow:hidden}
.ph img{width:100%;height:100%;object-fit:cover}
.side{display:flex;flex-direction:column;justify-content:center;padding:40px 52px 40px 40px}
.nm{font-family:'Cormorant Garamond';font-weight:500;font-size:32px;line-height:1.12;color:var(--ink)}
.tx{font:300 18px/1.55 'Inter';color:#3f3f3f;margin-top:16px}
.pr{font-family:'Cormorant Garamond';font-weight:500;font-size:40px;color:var(--gold);margin-top:18px}
.ct{font:400 12.5px/1.5 'Inter';letter-spacing:.18em;text-transform:uppercase;color:var(--cert);margin-top:8px}

.lad-row{display:grid;grid-template-columns:1fr auto;gap:28px;align-items:baseline;
  padding:12px 0;border-bottom:1px solid rgba(169,133,69,.22)}
.lad-nm{font:300 17px/1.35 'Inter';color:#d5cfc3}
.lad-pr{font-family:'Cormorant Garamond';font-weight:500;font-size:27px;color:var(--gold2);white-space:nowrap}
"""


def esc(s):
    return html.escape(s or "", quote=False)


def rub(n):
    return f"{n:,}".replace(",", " ") + "&nbsp;₽"


S, n = [], 0


def add(s):
    global n
    n += 1
    S.append(s.replace("__ID__", f"s{n:02d}"))


def main():
    # ---------- обложка
    add("""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr 1fr">
  <div style="display:flex;flex-direction:column;justify-content:space-between;padding:54px 20px 54px 58px">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:134px;width:auto;object-fit:contain;filter:brightness(0) invert(1);align-self:flex-start">
    <div>
      <div class="kick d" style="margin-bottom:20px">Частное собрание · Отбор Stargift</div>
      <h1 class="serif" style="font-weight:300;font-size:60px;line-height:1.04;color:var(--ivory)">Собрание<br>необычного</h1>
      <p style="font:300 19px/1.58 'Inter';color:#b8b2a6;margin-top:20px;max-width:40ch">Двадцать предметов, которые не повторяются:
      от сертификата Standard Oil с подписью Рокфеллера до мяча чемпионата мира, который ещё не начался.</p>
    </div>
    <div class="kick" style="letter-spacing:.24em">20 предметов · август 2026</div>
  </div>
  <div style="display:flex;flex-direction:column;justify-content:center;padding:0 58px;border-left:1px solid rgba(169,133,69,.28)">
    <div class="serif" style="font-weight:300;font-size:126px;line-height:.92;color:var(--gold);opacity:.9">5</div>
    <div class="rule" style="width:76px;margin:24px 0"></div>
    <p style="font:300 20px/1.55 'Inter';color:#b8b2a6;max-width:27ch">миров в одной деке: документы и письма, кино,
    музыка, спорт, искусство и стиль.</p>
    <p style="font:300 20px/1.55 'Inter';color:#b8b2a6;max-width:27ch;margin-top:22px">Рокфеллер и Веттриано, Али и Месси,
    Меркьюри и Дауни-младший.</p>
  </div>
</section>""")

    def divider(kick, huge, sub, photo, credit):
        if photo:
            add(f"""<section class="slide dark" id="__ID__" style="grid-template-columns:1.15fr 1fr">
  <div style="display:flex;flex-direction:column;justify-content:center;padding:0 52px 0 72px">
    <div class="kick d" style="margin-bottom:24px">{esc(kick)}</div>
    <h2 class="serif" style="font-weight:300;font-size:58px;line-height:1.05;color:var(--ivory)">{huge}</h2>
    <div class="rule" style="width:74px;margin:28px 0"></div>
    <p style="font:300 21px/1.58 'Inter';color:#c9c3b7;max-width:44ch">{esc(sub)}</p>
  </div>
  <div style="position:relative">
    <img src="{photo}" alt="" style="width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.04)">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,12,1) 0%,rgba(11,11,12,.25) 30%,rgba(11,11,12,0) 60%)"></div>
    <div style="position:absolute;left:0;right:0;bottom:0;padding:14px 24px;font:300 12px/1.4 'Inter';color:#8f8a80;background:linear-gradient(0deg,rgba(11,11,12,.85),rgba(11,11,12,0))">{esc(credit)}</div>
  </div>
</section>""")
        else:
            add(f"""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="display:flex;flex-direction:column;justify-content:center;padding:0 78px">
    <div class="kick d" style="margin-bottom:24px">{esc(kick)}</div>
    <h2 class="serif" style="font-weight:300;font-size:64px;line-height:1.04;color:var(--ivory)">{huge}</h2>
    <div class="rule" style="width:74px;margin:28px 0"></div>
    <p style="font:300 21px/1.58 'Inter';color:#c9c3b7;max-width:52ch">{esc(sub)}</p>
  </div>
</section>""")

    def solo(tag, kick):
        it = LOTS[tag]
        cert = f'<div class="ct">{esc(it["cert"])}</div>' if it["cert"] else ""
        add(f"""<section class="slide white solo" id="__ID__">
  <div class="ph"><img src="img_sel/half/{tag}.jpg" alt=""></div>
  <div class="side">
    <div class="kick">{esc(kick)}</div>
    <div class="nm" style="margin-top:13px">{esc(it['name'])}</div>
    <div class="tx">{esc(it['text'])}</div>
    <div class="pr">{rub(it['price'])}</div>
    {cert}
  </div>
</section>""")

    def interior(tag):
        f, cap = INT[tag]
        add(f"""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="position:relative">
    <img src="{f}" alt="" style="width:100%;height:100%;object-fit:cover">
    <div style="position:absolute;left:0;right:0;bottom:0;padding:20px 40px;
                background:linear-gradient(0deg,rgba(11,11,12,.88),rgba(11,11,12,0))">
      <span class="kick d">{esc(LOTS[tag]['short'])}</span>
      <div style="font:300 15px/1.5 'Inter';color:#c9c3b7;margin-top:8px;max-width:90ch">{esc(cap)}</div>
    </div>
  </div>
</section>""")

    # ---------- главы
    for grp, kick, huge, sub, photo, credit in CHAPTERS:
        divider(kick, huge, sub, photo, credit)
        keys = [k for k in ORDER if LOTS[k]["grp"] == grp]
        for i, k in enumerate(keys, 1):
            solo(k, f"{kick} · {i} из {len(keys)}")
            if k in INT:
                interior(k)

    # ---------- упаковка
    add("""<section class="slide white" id="__ID__" style="grid-template-rows:auto 1fr auto">
  <div style="padding:30px 62px 0;display:flex;justify-content:space-between;align-items:baseline">
    <h2 class="serif" style="font-weight:500;font-size:32px;color:var(--ink)">Как мы отдаём подарок</h2>
    <span class="kick">Упаковка Stargift</span>
  </div>
  <div style="display:grid;grid-template-columns:1.05fr .95fr;gap:42px;padding:18px 62px 0;align-items:center">
    <div style="height:396px;display:flex;align-items:center;justify-content:center;background:#F7F5F1;overflow:hidden"><img src="img_packaging/box_kraft.jpg" alt="" style="max-width:100%;max-height:100%;object-fit:contain"></div>
    <div style="height:396px;display:flex;align-items:center;justify-content:center;background:#F7F5F1;overflow:hidden"><img src="img_packaging/bag_white.jpg" alt="" style="max-width:100%;max-height:100%;object-fit:contain"></div>
  </div>
  <div style="padding:16px 62px 32px;font:300 18px/1.55 'Inter';color:#4a4a4a;max-width:96ch">Каждый предмет уходит в фирменной упаковке дома:
  крафт-бумага с автографами великих, лента Stargift и плотный подарочный пакет. Оформленную работу привозим и вешаем сами.</div>
</section>""")

    # ---------- прайс: по два-три раздела на слайд
    def price(title, grps):
        rows = "".join(
            f'<div class="lad-row"><div class="lad-nm">{esc(LOTS[k]["short"])}</div>'
            f'<div class="lad-pr">{rub(LOTS[k]["price"])}</div></div>'
            for g in grps for k in ORDER if LOTS[k]["grp"] == g)
        add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:auto 1fr">
  <div style="padding:40px 66px 0">
    <div class="kick d" style="margin-bottom:12px">Собрание · {esc(title)}</div>
    <h2 class="serif" style="font-weight:300;font-size:40px;line-height:1;color:var(--ivory)">Прайс-лист</h2>
  </div>
  <div style="display:flex;flex-direction:column;justify-content:center;padding:0 66px 44px">{rows}</div>
</section>""")

    price("Документы и кино", ["doc", "cine"])
    price("Музыка, спорт, искусство", ["mus", "sport", "art"])

    # ---------- финал
    add("""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="padding:0 66px;display:flex;flex-direction:column;justify-content:center">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:132px;width:auto;object-fit:contain;filter:brightness(0) invert(1);align-self:flex-start">
    <h2 class="serif" style="font-weight:300;font-size:44px;line-height:1.12;color:var(--ivory);margin-top:32px;max-width:36ch">Двадцать предметов, которые не повторяются. Каждый — с историей, которую рассказывают гостям.</h2>
  </div>
  <div style="padding:24px 66px 40px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.24em;color:var(--gold2)">stargift.ru</span>
  </div>
</section>""")

    doc = f"""<meta charset="utf-8">
<title>Stargift · Собрание необычного</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>

<div class="deck">
{chr(10).join(S)}
</div>

<script>
function show(){{const raw=location.hash.slice(1);const k=raw.replace(/^s/,'');const id=k?('s'+k.padStart(2,'0')):'s01';
document.querySelectorAll('.slide').forEach(s=>s.classList.toggle('on', s.id===id));scrollTo(0,0);}}
function go(d){{const cur=+((location.hash.slice(1).replace(/^s/,''))||1);let x=cur+d;if(x<1)x=1;if(x>{n})x={n};location.hash='s'+x;}}
show();addEventListener('hashchange',show);
addEventListener('keydown',e=>{{if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' ')go(1);if(e.key==='ArrowLeft'||e.key==='PageUp')go(-1);}});
addEventListener('click',e=>{{if(e.target.closest('a'))return;go(e.clientX<innerWidth*0.32?-1:1);}});
</script>
<style>@page{{size:{W}px {H}px;margin:0}}@media print{{html,body{{overflow:visible;height:auto}}*{{box-shadow:none !important}}.slide{{animation:none}}.deck{{height:auto}}
.slide{{position:relative;inset:auto;display:grid !important;width:{W}px;height:{H}px;page-break-after:always}}}}</style>
"""
    open(f"{R}/deck_sel.html", "w", encoding="utf-8").write(doc)
    print(f"deck_sel.html: {n} слайдов")


if __name__ == "__main__":
    main()
