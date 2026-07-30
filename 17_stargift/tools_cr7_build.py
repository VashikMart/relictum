#!/usr/bin/env python3
"""«Криштиану Роналду · бутсы» — презентация 1280×720, 4 лота + упаковка.

    python3 tools_cr7_build.py               # → deck_cr7.html
"""
import html, os

R = os.path.dirname(os.path.abspath(__file__))


def esc(s):
    return html.escape(s or "", quote=False)


def rub(n):
    return f"{n:,}".replace(",", " ") + "&nbsp;₽"


C = "img_cr7"

LOTS = {
 "merc_s005": dict(price=520_000, cert="Beckett",
    name="Криштиану Роналду — бутса Nike Mercurial Dream Speed с автографом",
    text=("Бутса Nike Mercurial серии Dream Speed — личной линейки Роналду "
          "внутри Nike — с автографом синим маркером. Бело-голубая расцветка "
          "с фирменной стелькой CR7. Mercurial — силуэт, в котором Роналду "
          "провёл всю карьеру: от «Манчестер Юнайтед» до сборной Португалии.")),
 "witness": dict(price=590_000, cert="Beckett Witnessed",
    name="Криштиану Роналду — бутса Nike Mercurial CR7 с автографом, подпись при представителе Beckett",
    text=("Красная бутса Nike Mercurial линейки CR7 — с автографом, "
          "поставленным в присутствии представителя Beckett. Witnessed — "
          "высший уровень экспертизы: свидетель фиксирует сам момент подписи. "
          "Контрастный чёрный росчерк на алом верхе читается через всю бутсу.")),
 "sealed": dict(price=520_000, cert="Beckett Witnessed",
    name="Криштиану Роналду — бутса Nike Mercurial с автографом (Лиссабон, 2018)",
    text=("Белая бутса Nike Mercurial с гранёным паттерном серии CR7 — "
          "с автографом, поставленным 6 мая 2018 года в Лиссабоне при "
          "представителе Beckett. Экземпляр новый, с пломбой; номер "
          "сертификата проверяется онлайн за минуту. Весна 2018-го — "
          "последние месяцы Роналду в «Реал Мадриде».")),
 "victory": dict(price=520_000, cert="",
    name="Криштиану Роналду — бутса Nike Mercurial Victory CR7 с автографом",
    text=("Белая бутса Nike Mercurial Victory линейки CR7 — с автографом. "
          "Рядом — кадр из сессии подписания: Роналду с этой моделью в руках. "
          "Фотография с предметом в руках героя — редкое дополнение, которое "
          "сразу отвечает на главный вопрос любого гостя вашего дома.")),
}

ORDER_LADDER = ["witness", "merc_s005", "sealed", "victory"]

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
.credit{position:absolute;right:16px;bottom:12px;font:400 8.5px/1.3 'Inter';
  letter-spacing:.08em;color:rgba(245,241,232,.55)}
.div-huge{font-family:'Cormorant Garamond';font-weight:300;line-height:1;color:var(--ivory)}
.div-rule{height:1px;width:70px;background:rgba(169,133,69,.55)}
.div-sub{font:300 19px/1.65 'Inter';color:#c9c3b7}

.solo{grid-template-columns:1fr 1fr}
.ph2{display:flex;align-items:center;justify-content:center;background:#f4f4f4;height:720px;overflow:hidden}
.ph2 img{max-width:100%;max-height:100%;object-fit:contain}
.solo-side{display:flex;flex-direction:column;justify-content:center;padding:50px 56px 50px 22px}
.solo-name{font-family:'Cormorant Garamond';font-weight:500;font-size:29px;line-height:1.14;color:var(--ink)}
.solo-text{font:300 15.5px/1.64 'Inter';color:#4a4a4a;margin-top:14px}
.solo-price{font-family:'Cormorant Garamond';font-weight:500;font-size:30px;color:var(--gold);margin-top:18px}
.solo-cert{font:400 10px/1 'Inter';letter-spacing:.22em;text-transform:uppercase;color:var(--cert);margin-top:10px}

.duo2{grid-template-rows:auto 1fr}
.duo2-in{display:grid;grid-template-columns:1fr 1fr;gap:46px;padding:14px 72px 28px;align-items:start}
.dc{display:flex;flex-direction:column;align-items:center;text-align:center}
.dc-ph{width:100%;height:440px;display:flex;align-items:center;justify-content:center;background:#fff}
.dc-ph img{max-width:100%;max-height:100%;object-fit:contain}
.dc-text{font:300 13.5px/1.5 'Inter';color:#4a4a4a;margin-top:10px;max-width:52ch}

.lad{display:flex;flex-direction:column;height:100%;justify-content:space-between}
.lad-row{display:grid;grid-template-columns:1fr auto;gap:30px;align-items:baseline;
  padding:10px 0;border-bottom:1px solid rgba(169,133,69,.2)}
.lad-nm{font:300 15px/1.35 'Inter';color:#d5cfc3}
.lad-pr{font-family:'Cormorant Garamond';font-weight:500;font-size:21px;color:var(--gold2);white-space:nowrap}
"""


def main():
    S, n = [], 0

    def add(s):
        nonlocal n
        n += 1
        S.append(s.replace("__ID__", f"s{n:02d}"))

    def img(key, suffix):
        cand = f"{C}/clean_{key}_{suffix}.jpg"
        if os.path.exists(os.path.join(R, cand)):
            return cand
        return f"{C}/src/{key}_{suffix}.jpg"

    def solo(k, photos, kick):
        it = LOTS[k]
        cert = f'<div class="solo-cert">{esc(it["cert"])}</div>' if it["cert"] else ""
        add(f"""<section class="slide white solo" id="__ID__">
  <div class="ph2"><img src="{photos[0]}" alt=""></div>
  <div class="solo-side">
    <div class="kick" style="margin-bottom:14px">{kick}</div>
    <div class="solo-name">{esc(it['name'])}</div>
    <div class="solo-text">{esc(it['text'])}</div>
    <div class="solo-price">{rub(it['price'])}</div>
    {cert}
  </div>
</section>""")

    # ---------- обложка
    add("""<section class="slide dark on" id="__ID__" style="grid-template-columns:1fr 1.06fr">
  <div style="display:flex;flex-direction:column;justify-content:space-between;padding:60px 54px">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:150px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start">
    <div>
      <div class="kick d" style="margin-bottom:22px">Частное собрание · Футбол</div>
      <h1 class="serif" style="font-weight:300;font-size:72px;line-height:1.02;color:var(--ivory)">Криштиану<br>Роналду</h1>
      <p style="font:300 16px/1.64 'Inter';color:#b8b2a6;margin-top:24px;max-width:40ch">Четыре бутсы Nike Mercurial с автографом — силуэт,
      в котором сыграна вся его карьера. Разные эпохи, разные расцветки,
      один росчерк.</p>
    </div>
    <div class="kick" style="letter-spacing:.24em">4 предмета · июль 2026</div>
  </div>
  <div style="position:relative;height:720px;overflow:hidden">
    <img src="img_cr7/hero/cover.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:30% 20%">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,var(--noir) 0%,rgba(11,11,12,.32) 24%,rgba(11,11,12,0) 55%)"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,11,12,.5) 0%,rgba(11,11,12,0) 26%)"></div>
    <span class="credit">Фото: Ludovic Péron · Wikimedia Commons · CC BY-SA 3.0</span>
  </div>
</section>""")

    solo("witness", [img("witness", "02")], "Бутсы · 1 из 4")
    solo("merc_s005", [img("merc_s005", "00")], "Бутсы · 2 из 4")
    solo("sealed", [img("sealed", "01")], "Бутсы · 3 из 4")
    solo("victory", [img("victory", "00")], "Бутсы · 4 из 4")

    # ---------- сюжет: Эль Класико
    add("""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="position:relative">
    <img src="img_cr7/hero/clasico.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:22% 30%">
    <div style="position:absolute;inset:0;background:linear-gradient(270deg,rgba(11,11,12,.93) 0%,rgba(11,11,12,.74) 34%,rgba(11,11,12,.16) 66%,rgba(11,11,12,.04) 100%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:flex-end;text-align:right;padding:0 60px">
      <div class="kick d" style="letter-spacing:.3em;margin-bottom:24px">Мадрид · Эль Класико</div>
      <h2 class="div-huge" style="font-size:54px;max-width:16ch">Самый результативный в истории игры</h2>
      <div class="div-rule" style="margin:28px 0"></div>
      <p class="div-sub" style="max-width:38ch">Пять «Золотых мячей», четыре «Золотые бутсы»,
      более девятисот голов за карьеру — и все они забиты в Mercurial.
      Бутса с его подписью — самый прямой предмет из возможных.</p>
    </div>
    <span class="credit">Фото: Jan S0L0 · Wikimedia Commons · CC BY-SA 2.0</span>
  </div>
</section>""")

    # ---------- упаковка
    add("""<section class="slide white duo2" id="__ID__">
  <div style="padding:30px 72px 0;display:flex;justify-content:space-between;align-items:baseline">
    <h2 class="serif" style="font-weight:500;font-size:28px;color:var(--ink)">Как мы отдаём подарок</h2>
    <span class="kick" style="letter-spacing:.2em">Упаковка Stargift</span>
  </div>
  <div class="duo2-in" style="grid-template-columns:1.1fr .9fr;align-items:center">
    <div class="dc"><div class="dc-ph"><img src="img_packaging/box_kraft.jpg" alt=""></div></div>
    <div class="dc"><div class="dc-ph"><img src="img_packaging/bag_white.jpg" alt=""></div></div>
  </div>
  <div style="padding:0 72px 34px;font:300 15px/1.6 'Inter';color:#4a4a4a;max-width:100ch">Каждый предмет уходит в фирменной упаковке дома:
  крафт-бумага с автографами великих, лента Stargift и плотный подарочный пакет.
  Подарок можно вручать сразу — прямо из рук в руки.</div>
</section>""")

    # ---------- лестница
    rows = "".join(
        f'<div class="lad-row"><div class="lad-nm">{esc(LOTS[k]["name"])}</div>'
        f'<div class="lad-pr">{rub(LOTS[k]["price"])}</div></div>' for k in ORDER_LADDER)
    add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:auto 1fr">
  <div style="padding:44px 66px 0">
    <div class="kick d" style="margin-bottom:12px">Подборка целиком</div>
    <h2 class="serif" style="font-weight:300;font-size:44px;line-height:1;color:var(--ivory)">4 предмета</h2>
  </div>
  <div style="padding:22px 66px 40px"><div class="lad">{rows}</div></div>
</section>""")

    # ---------- финал
    add("""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="padding:76px 72px 0;display:flex;flex-direction:column;justify-content:center">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:146px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start">
    <h2 class="serif" style="font-weight:300;font-size:46px;line-height:1.14;color:var(--ivory);margin-top:38px;max-width:30ch">Криштиану Роналду. Четыре бутсы — одна карьера.</h2>
  </div>
  <div style="padding:26px 72px 40px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.24em;color:var(--gold2)">stargift.ru</span>
  </div>
</section>""")

    doc = f"""<meta charset="utf-8">
<title>Stargift · Криштиану Роналду</title>
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
    open(f"{R}/deck_cr7.html", "w", encoding="utf-8").write(doc)
    print(f"deck_cr7.html: {n} слайдов, {len(LOTS)} лотов")


if __name__ == "__main__":
    main()
