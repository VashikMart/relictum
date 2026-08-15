#!/usr/bin/env python3
"""Зал боксёрской славы — горизонтальная дека 1280×720.

    python3 tools_box_build.py    # → deck_box_H.html

Три предмета, у каждого одно фото объявления. Второй и третий кадр — не
генерация и не чужой ракурс, а увеличенные фрагменты того же листа после
геометрического выравнивания: настоящие пиксели подписей крупно.

Справки о подписантах идут отдельным слайдом после каждого предмета — так
просил Вашик: короткая строка про каждого, чем известен и как связан с Али.
Общий контекст предмета остаётся в его описании рядом с фото.
"""
import html
import os

from tools_box_data import LOTS, ORDER, CHAPTERS, HEROES

R = os.path.dirname(os.path.abspath(__file__))
C = "img_box"
W, H = 1280, 720


def esc(s):
    return html.escape(s or "", quote=False)


def rub(n):
    return f"{n:,}".replace(",", " ") + "&nbsp;₽"


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
.light{background:var(--paper);color:var(--ink)}
.dark{background:var(--noir);color:var(--ivory)}
.rule{height:1px;background:rgba(169,133,69,.55)}
.kick{font:500 13px/1 'Inter';letter-spacing:.32em;text-transform:uppercase;color:var(--gold)}
.kick.d{color:var(--gold2)}

/* Фото занимает ровно половину слайда. Кадры заранее приведены к 8:9
   (tools_halfslide.py): предмет целиком, поле добрано фоном, поэтому cover
   здесь ничего не срезает. */
.solo{grid-template-columns:640px 1fr}
.ph{background:#fff;overflow:hidden}
.ph img{width:100%;height:100%;object-fit:cover}
.side{display:flex;flex-direction:column;justify-content:center;padding:44px 52px 44px 40px}
.nm{font-family:'Cormorant Garamond';font-weight:500;font-size:33px;line-height:1.12;color:var(--ink)}
.hist{margin-top:15px;padding-left:15px;border-left:2px solid var(--gold)}
.era{font:500 12px/1 'Inter';letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:7px}
.histt{font:300 18px/1.5 'Inter';color:#3d3d3d}
.tx{font:300 18px/1.52 'Inter';color:#4a4a4a;margin-top:14px}
.pr{font-family:'Cormorant Garamond';font-weight:500;font-size:40px;color:var(--gold);margin-top:16px}
.ct{font:400 12.5px/1.5 'Inter';letter-spacing:.18em;text-transform:uppercase;color:var(--cert);margin-top:8px}

.hero-nm{font-family:'Cormorant Garamond';font-weight:500;font-size:30px;line-height:1.06;color:var(--ivory)}
.hero-tx{font:300 19px/1.5 'Inter';color:#b5afa3;margin-top:8px}
.sig{font:300 18px/1.5 'Inter';color:#4a4a4a}

.lad-row{display:grid;grid-template-columns:1fr auto;gap:30px;align-items:baseline;
  padding:26px 0;border-bottom:1px solid rgba(169,133,69,.22)}
.lad-nm{font:300 19px/1.4 'Inter';color:#d5cfc3}
.lad-pr{font-family:'Cormorant Garamond';font-weight:500;font-size:36px;color:var(--gold2);white-space:nowrap}
"""


def main():
    S, n = [], 0

    def add(s):
        nonlocal n
        n += 1
        S.append(s.replace("__ID__", f"s{n:02d}"))

    # ---------- обложка: типографская.
    # Фото лота на обложку не ставим — тот же кадр через два слайда читается
    # как сбой сборки, и сборка PPTX на этом честно падает.
    add("""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr 1fr">
  <div style="display:flex;flex-direction:column;justify-content:space-between;padding:54px 20px 54px 58px">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:134px;width:auto;object-fit:contain;filter:brightness(0) invert(1);align-self:flex-start">
    <div>
      <div class="kick d" style="margin-bottom:20px">Частное собрание · Бокс</div>
      <h1 class="serif" style="font-weight:300;font-size:60px;line-height:1.04;color:var(--ivory)">Зал боксёрской<br>славы</h1>
      <p style="font:300 19px/1.58 'Inter';color:#b8b2a6;margin-top:20px;max-width:38ch">Три предмета из Канастоты: программы
      церемоний 1996 и 1997 годов и официальный пресс-кит, подписанный соперниками Мохаммеда&nbsp;Али.</p>
    </div>
    <div class="kick" style="letter-spacing:.24em">3 предмета · август 2026</div>
  </div>
  <div style="position:relative;display:flex;flex-direction:column;justify-content:center;
              padding:0 58px;border-left:1px solid rgba(169,133,69,.28)">
    <div class="serif" style="font-weight:300;font-size:130px;line-height:.92;color:var(--gold);opacity:.9">41</div>
    <div class="rule" style="width:76px;margin:24px 0"></div>
    <p style="font:300 20px/1.55 'Inter';color:#b8b2a6;max-width:26ch">автограф на двух программах — от Арчи Мура
    и Флойда Паттерсона до Марвина Хаглера.</p>
    <p style="font:300 20px/1.55 'Inter';color:#b8b2a6;max-width:26ch;margin-top:22px">Плюс папка для прессы с именами
    Фрейзера, Нортона и Леона Спинкса.</p>
  </div>
</section>""")

    def divider(kick, huge, sub, facts):
        rows = "".join(
            f'<div style="padding:18px 0;border-top:1px solid rgba(169,133,69,.28)">'
            f'<div class="serif" style="font-weight:500;font-size:27px;line-height:1.1;'
            f'color:var(--gold2)">{esc(a)}</div>'
            f'<div style="font:300 18px/1.45 \'Inter\';color:#9d978b;margin-top:6px">{esc(b)}</div>'
            f'</div>' for a, b in facts)
        add(f"""<section class="slide dark" id="__ID__" style="grid-template-columns:1.34fr 1fr">
  <div style="display:flex;flex-direction:column;justify-content:center;padding:0 46px 0 72px">
    <div class="kick d" style="margin-bottom:24px">{esc(kick)}</div>
    <h2 class="serif" style="font-weight:300;font-size:58px;line-height:1.05;color:var(--ivory)">{huge}</h2>
    <div class="rule" style="width:74px;margin:28px 0"></div>
    <p style="font:300 21px/1.58 'Inter';color:#c9c3b7;max-width:44ch">{esc(sub)}</p>
  </div>
  <div style="display:flex;flex-direction:column;justify-content:center;padding:0 72px 0 0">{rows}</div>
</section>""")

    def solo(tag, kick):
        it = LOTS[tag]
        add(f"""<section class="slide white solo" id="__ID__">
  <div class="ph"><img src="{C}/half/orig_{tag}.jpg" alt=""></div>
  <div class="side">
    <div class="kick">{esc(kick)}</div>
    <div class="nm" style="margin-top:13px">{esc(it['name'])}</div>
    <div class="hist"><div class="era">{esc(it['era'])}</div>
      <div class="histt">{esc(it['hist'])}</div></div>
    <div class="tx">{esc(it['text'])}</div>
    <div class="pr">{rub(it['price'])}</div>
    <div class="ct">{esc(it['cert'])}</div>
  </div>
</section>""")

    def details(tag, kick):
        """Два увеличенных фрагмента того же листа плюс перечень имён."""
        it = LOTS[tag]
        cells = "".join(
            f'<div style="background:#F7F5F1;display:flex;align-items:center;'
            f'justify-content:center;overflow:hidden;height:100%">'
            f'<img src="{C}/det/{tag}_{d}.jpg" alt="" '
            f'style="max-width:100%;max-height:100%;object-fit:contain"></div>'
            for d in it["det"])
        names = " · ".join(it["signs"])
        add(f"""<section class="slide white" id="__ID__" style="grid-template-rows:auto 1fr auto">
  <div style="padding:30px 58px 0;display:flex;justify-content:space-between;align-items:baseline;gap:30px">
    <div class="serif" style="font-weight:500;font-size:32px;line-height:1.1;color:var(--ink);max-width:62ch">Подписи крупно</div>
    <span class="kick" style="white-space:nowrap">{esc(kick)}</span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;padding:20px 58px 0">{cells}</div>
  <div style="padding:18px 58px 30px">
    <div class="sig">{esc(names)}</div>
    <div style="font:300 14px/1.5 'Inter';color:#8d8880;margin-top:8px">{esc(it['detcap'])}</div>
  </div>
</section>""")

    def heroes(tag):
        title, rows = HEROES[tag]
        cells = "".join(
            f'<div><div class="hero-nm">{esc(a)}</div>'
            f'<div class="hero-tx">{esc(b)}</div></div>' for a, b in rows)
        add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:auto 1fr">
  <div style="padding:42px 62px 0">
    <div class="kick d" style="margin-bottom:12px">{esc(title)}</div>
    <h2 class="serif" style="font-weight:300;font-size:40px;line-height:1.06;color:var(--ivory)">Кто эти люди</h2>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:30px 58px;
              align-content:center;padding:10px 62px 44px">{cells}</div>
</section>""")

    # ---------- главы
    for grp, kick, huge, sub, facts in CHAPTERS:
        divider(kick, huge, sub, facts)
        keys = [k for k in ORDER if LOTS[k]["grp"] == grp]
        for i, k in enumerate(keys, 1):
            k2 = f"{kick} · {i} из {len(keys)}" if len(keys) > 1 else kick
            solo(k, k2)
            details(k, k2)
            heroes(k)

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

    # ---------- прайс-лист
    rows = "".join(
        f'<div class="lad-row"><div class="lad-nm">{esc(LOTS[k]["name"])}</div>'
        f'<div class="lad-pr">{rub(LOTS[k]["price"])}</div></div>' for k in ORDER)
    add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:auto 1fr">
  <div style="padding:48px 66px 0">
    <div class="kick d" style="margin-bottom:12px">Собрание</div>
    <h2 class="serif" style="font-weight:300;font-size:44px;line-height:1;color:var(--ivory)">Три предмета</h2>
  </div>
  <div style="display:flex;flex-direction:column;justify-content:center;padding:0 66px 54px">{rows}</div>
</section>""")

    # ---------- финал
    add("""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="padding:0 66px;display:flex;flex-direction:column;justify-content:center">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:132px;width:auto;object-fit:contain;filter:brightness(0) invert(1);align-self:flex-start">
    <h2 class="serif" style="font-weight:300;font-size:44px;line-height:1.12;color:var(--ivory);margin-top:32px;max-width:34ch">Канастота, июнь. Один день в году, когда весь бокс расписывается в одной комнате.</h2>
  </div>
  <div style="padding:24px 66px 40px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.24em;color:var(--gold2)">stargift.ru</span>
  </div>
</section>""")

    doc = f"""<meta charset="utf-8">
<title>Stargift · Зал боксёрской славы</title>
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
    open(f"{R}/deck_box_H.html", "w", encoding="utf-8").write(doc)
    print(f"deck_box_H.html: {n} слайдов, {W}×{H}")


if __name__ == "__main__":
    main()
