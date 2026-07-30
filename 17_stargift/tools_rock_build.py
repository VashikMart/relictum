#!/usr/bin/env python3
"""«Скала» — клиентская презентация 1280×720, 15 лотов + страница упаковки.

    python3 tools_rock_build.py              # → deck_rock.html

Фото лотов обработаны (nano banana, белая студия), кадры — Wikimedia,
упаковка — собственные фотографии дома (img_packaging).
"""
import html, os

R = os.path.dirname(os.path.abspath(__file__))


def esc(s):
    return html.escape(s or "", quote=False)


def rub(n):
    return f"{n:,}".replace(",", " ") + "&nbsp;₽"


C = "img_rock"

LOTS = {
 "belt": dict(price=850_000, cert="JSA",
    name="Скала и Рик Флэр — чемпионский пояс WWE с двумя автографами",
    text=("Чемпионский пояс WWE с автографами Дуэйна «Скалы» Джонсона и Рика "
          "Флэра. Две эпохи рестлинга на одном титуле: десятикратный чемпион "
          "мира, ставший самым кассовым актёром Голливуда, — и «Природный "
          "парень», шестнадцатикратный чемпион, чья цифра 16x выведена рядом "
          "с подписью. Центральный предмет подборки.")),
 "ph90s": dict(price=220_000, cert="PSA/DNA",
    name="Скала — фотография WWE 1990-х с автографом, в капсуле",
    text=("Коллаж эпохи Attitude в защитной капсуле: молодой Рок в деле — "
          "броски, титул, кураж конца девяностых. Подпись серебром поверх "
          "тёмного кадра.")),
 "maivia": dict(price=220_000, cert="JSA",
    name="Скала — фотография «The People's Champ» с автографом",
    text=("Промо-фотография WWF конца девяностых: Роки Майвия — под этим "
          "именем Джонсон дебютировал в 1996-м — с интерконтинентальным "
          "титулом на плече. Ранний формат, с которого началась легенда.")),
 "hobbs_a": dict(price=260_000, cert="Beckett",
    name="Скала — фотография «Форсаж-5» с автографом (портрет)",
    text=("Фотография 28×36 см с автографом: агент Люк Хоббс. Роль, которая "
          "сделала Джонсона центром главной автомобильной саги кино и "
          "принесла франшизе новые миллиарды.")),
 "hobbs_b": dict(price=260_000, cert="JSA",
    name="Скала — фотография «Форсаж-5» с автографом (в снаряжении)",
    text=("Фотография 28×36 см с автографом: Хоббс в полном тактическом "
          "снаряжении в джунглях Рио. Второй кадр той же роли — для тех, "
          "кто собирает пару.")),
 "early": dict(price=220_000, cert="PSA/DNA",
    name="Скала — ранняя фотография с автографом",
    text=("Ранний портрет с автографом, заверенный ещё первым поколением "
          "экспертизы PSA/DNA. Улыбка человека, который уже знает, что "
          "станет самым узнаваемым лицом планеты.")),
 "ph1114": dict(price=260_000, cert="JSA",
    name="Скала — фотография 28×36 см с автографом (пустыня)",
    text=("Кинокадр в пустыне — фотография 28×36 см с автографом и полным "
          "письмом JSA. Большой формат и редкий сюжет вне ринга.")),
 "cut": dict(price=250_000, cert="PSA/DNA + Beckett",
    name="Скала — автограф «The Rock» в капсуле, двойная экспертиза",
    text=("Крупный росчерк «The Rock» синим маркером в защитной капсуле — "
          "редкий случай, когда один автограф прошёл две независимые "
          "экспертизы сразу. Чистая каллиграфия имени, которое знает мир.")),
 "rstone": dict(price=260_000, cert="PSA/DNA",
    name="Скала — журнал Rolling Stone 2000 года с автографом",
    text=("Rolling Stone весны 2000 года с автографом на обложке: «What "
          "Makes the Rock Hard» — момент, когда рестлер впервые стал "
          "обложкой главного музыкального журнала планеты.")),
 "mag": dict(price=250_000, cert="PSA/DNA",
    name="Скала — журнал Rolling Stone 2018 года с автографом",
    text=("Rolling Stone 2018 года с автографом: «Dwayne's World» — "
          "разворотная история о том, как самый занятой человек Голливуда "
          "устроен изнутри. Подпись поверх собственного портрета за рулём.")),
 "nintendo": dict(price=200_000, cert="PSA",
    name="Скала — постер «Царь скорпионов» Nintendo Power с автографом",
    text=("Двусторонний постер Nintendo Power к «Царю скорпионов» — "
          "с автографом. Первая главная роль Джонсона в кино и игровая "
          "эпоха начала нулевых в одном предмете.")),
 "fig_jakks": dict(price=300_000, cert="JSA",
    name="Скала — фигурка Jakks WrestleMania XV в блистере с автографом",
    text=("Фигурка Jakks Pacific серии WrestleMania XV в оригинальном "
          "нераспечатанном блистере — с автографом. WrestleMania XV, 1999 год: "
          "первый мейн-ивент Рока против Остина. Игрушка эпохи, подписанная "
          "её героем.")),
 "fig_psa": dict(price=280_000, cert="PSA",
    name="Скала — фигурка WWF в блистере с автографом, полное письмо PSA",
    text=("Фигурка WWF конца девяностых в блистере — с автографом и полным "
          "письмом PSA. Второй вариант формата «игрушка с подписью» — "
          "для витрины или детской коллекции, которая переживёт поколения.")),
 "duo98": dict(price=400_000, cert="Beckett (BGS)",
    name="Скала — карточка Duocards 1998 года с автографом, в слабе",
    text=("Карточка Duocards 1998 года с автографом — в слабе Beckett. "
          "Рукки-эпоха: первые массовые карточки Рока, подписанные экземпляры "
          "которых рынок разбирает быстрее всего. Топ-позиция среди карточек "
          "подборки.")),
 "topps12": dict(price=300_000, cert="PSA",
    name="Скала — карточка Topps WWE 2012 года с автографом, в капсуле",
    text=("Карточка Topps WWE 2012 года с автографом на карте — в капсуле "
          "PSA. Эпоха великого возвращения: Рок против Джона Сины на двух "
          "WrestleMania подряд.")),
}

ORDER_LADDER = ["belt", "duo98", "fig_jakks", "topps12", "fig_psa",
                "hobbs_a", "hobbs_b", "ph1114", "rstone", "cut", "mag",
                "ph90s", "maivia", "early", "nintendo"]

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

.solo{grid-template-columns:1.22fr 1fr}
.ph2{display:grid;gap:18px;padding:44px 22px 44px 52px;background:#fff;align-items:center}
.ph2 .cell{height:100%;display:flex;align-items:center;justify-content:center;overflow:hidden}
.ph2 img{max-width:100%;max-height:100%;object-fit:contain}
.solo-side{display:flex;flex-direction:column;justify-content:center;padding:50px 56px 50px 22px}
.solo-name{font-family:'Cormorant Garamond';font-weight:500;font-size:30px;line-height:1.13;color:var(--ink)}
.solo-text{font:300 15.5px/1.64 'Inter';color:#4a4a4a;margin-top:14px}
.solo-price{font-family:'Cormorant Garamond';font-weight:500;font-size:30px;color:var(--gold);margin-top:18px}
.solo-cert{font:400 10px/1 'Inter';letter-spacing:.22em;text-transform:uppercase;color:var(--cert);margin-top:10px}

.duo2{grid-template-rows:auto 1fr}
.duo2-in{display:grid;grid-template-columns:1fr 1fr;gap:46px;padding:14px 72px 28px;align-items:start}
.dc{display:flex;flex-direction:column;align-items:center;text-align:center}
.dc-ph{width:100%;height:330px;display:flex;align-items:center;justify-content:center;background:#fff}
.dc-ph img{max-width:100%;max-height:100%;object-fit:contain}
.dc-name{font-family:'Cormorant Garamond';font-weight:500;font-size:21px;line-height:1.16;color:var(--ink);margin-top:16px;max-width:34ch}
.dc-text{font:300 13.5px/1.5 'Inter';color:#4a4a4a;margin-top:8px;max-width:52ch}
.dc-price{font-family:'Cormorant Garamond';font-weight:500;font-size:22px;color:var(--gold);margin-top:10px}
.dc-cert{font:400 9.5px/1 'Inter';letter-spacing:.2em;text-transform:uppercase;color:var(--cert);margin-top:7px}

.lad{display:flex;flex-direction:column;height:100%;justify-content:space-between}
.lad-row{display:grid;grid-template-columns:1fr auto;gap:30px;align-items:baseline;
  padding:7px 0;border-bottom:1px solid rgba(169,133,69,.2)}
.lad-nm{font:300 14px/1.3 'Inter';color:#d5cfc3}
.lad-pr{font-family:'Cormorant Garamond';font-weight:500;font-size:19px;color:var(--gold2);white-space:nowrap}
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
        cols = "1fr " * len(photos)
        cells = "".join(f'<div class="cell"><img src="{p}" alt=""></div>' for p in photos)
        cert = f'<div class="solo-cert">{esc(it["cert"])}</div>' if it["cert"] else ""
        add(f"""<section class="slide white solo" id="__ID__">
  <div class="ph2" style="grid-template-columns:{cols.strip()};height:720px">{cells}</div>
  <div class="solo-side">
    <div class="kick" style="margin-bottom:14px">{kick}</div>
    <div class="solo-name">{esc(it['name'])}</div>
    <div class="solo-text">{esc(it['text'])}</div>
    <div class="solo-price">{rub(it['price'])}</div>
    {cert}
  </div>
</section>""")

    def duo(k1, k2, title, kick):
        cards = ""
        for k in (k1, k2):
            it = LOTS[k]
            cert = f'<div class="dc-cert">{esc(it["cert"])}</div>' if it["cert"] else ""
            cards += f"""
      <div class="dc">
        <div class="dc-ph"><img src="{img(k, '00')}" alt=""></div>
        <div class="dc-name">{esc(it['name'])}</div>
        <div class="dc-text">{esc(it['text'])}</div>
        <div class="dc-price">{rub(it['price'])}</div>
        {cert}
      </div>"""
        add(f"""<section class="slide white duo2" id="__ID__">
  <div style="padding:26px 72px 0;display:flex;justify-content:space-between;align-items:baseline">
    <h2 class="serif" style="font-weight:500;font-size:27px;color:var(--ink)">{esc(title)}</h2>
    <span class="kick" style="letter-spacing:.2em">{kick}</span>
  </div>
  <div class="duo2-in">{cards}
  </div>
</section>""")

    # ---------- обложка: выход на рампу WrestleMania с поясом
    add("""<section class="slide dark on" id="__ID__" style="grid-template-columns:1fr 1.08fr">
  <div style="display:flex;flex-direction:column;justify-content:space-between;padding:60px 54px">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:150px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start">
    <div>
      <div class="kick d" style="margin-bottom:22px">Частное собрание · Рестлинг и кино</div>
      <h1 class="serif" style="font-weight:300;font-size:84px;line-height:1;color:var(--ivory)">Скала</h1>
      <p style="font:300 16px/1.64 'Inter';color:#b8b2a6;margin-top:24px;max-width:40ch">Дуэйн Джонсон — пятнадцать предметов от ринга до Голливуда:
      чемпионский пояс с двумя автографами, фотографии, журналы, фигурки в блистерах
      и карточки рукки-эпохи.</p>
    </div>
    <div class="kick" style="letter-spacing:.24em">15 предметов · июль 2026</div>
  </div>
  <div style="position:relative;height:720px;overflow:hidden">
    <img src="img_rock/hero/cover.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:42% 18%">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,var(--noir) 0%,rgba(11,11,12,.32) 24%,rgba(11,11,12,0) 55%)"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,11,12,.5) 0%,rgba(11,11,12,0) 26%)"></div>
    <span class="credit">Фото: Schen · WrestleMania 29 · Wikimedia Commons · CC BY 2.0</span>
  </div>
</section>""")

    # ---------- главный лот: пояс
    solo("belt", [img("belt", "00")], "Главный лот")
    add(f"""<section class="slide white duo2" id="__ID__">
  <div style="padding:26px 72px 0;display:flex;justify-content:space-between;align-items:baseline">
    <h2 class="serif" style="font-weight:500;font-size:27px;color:var(--ink)">Две подписи на одном титуле</h2>
    <span class="kick" style="letter-spacing:.2em">Главный лот</span>
  </div>
  <div class="duo2-in" style="grid-template-columns:1fr 1fr">
    <div class="dc"><div class="dc-ph" style="height:470px"><img src="{img('belt', '01')}" alt=""></div>
      <div class="dc-text" style="margin-top:12px">Подпись Скалы на ремне пояса.</div></div>
    <div class="dc"><div class="dc-ph" style="height:470px"><img src="{img('belt', '02')}" alt=""></div>
      <div class="dc-text" style="margin-top:12px">Подпись Рика Флэра с пометкой 16x — шестнадцать чемпионств.</div></div>
  </div>
</section>""")

    # ---------- ринг: фотографии
    add("""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="position:relative">
    <img src="img_rock/hero/ring.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 34%">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,12,.94) 0%,rgba(11,11,12,.78) 32%,rgba(11,11,12,.22) 62%,rgba(11,11,12,.05) 100%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 60px">
      <div class="kick d" style="letter-spacing:.34em;margin-bottom:24px">Раздел первый · 7 предметов</div>
      <h2 class="div-huge" style="font-size:70px">Фотографии</h2>
      <div class="div-rule" style="margin:32px 0"></div>
      <p class="div-sub" style="max-width:40ch">От промо Роки Майвии девяностых до Люка Хоббса —
      семь кадров с автографом, каждый со своей эпохой.</p>
    </div>
    <span class="credit">Фото: Simon Q · WrestleMania XXVIII · Wikimedia Commons · CC BY 2.0</span>
  </div>
</section>""")

    duo("hobbs_a", "hobbs_b", "Форсаж · Люк Хоббс", "Фотографии · 1–2 из 7")
    duo("ph1114", "early", "Большой формат и ранний автограф", "Фотографии · 3–4 из 7")
    duo("maivia", "ph90s", "Эпоха Attitude", "Фотографии · 5–6 из 7")
    solo("cut", [img("cut", "00")], "Фотографии и автографы · 7 из 7")

    # ---------- Голливуд: сюжет
    add("""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="position:relative">
    <img src="img_rock/hero/hollywood.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:28% 20%">
    <div style="position:absolute;inset:0;background:linear-gradient(270deg,rgba(11,11,12,.93) 0%,rgba(11,11,12,.74) 34%,rgba(11,11,12,.16) 66%,rgba(11,11,12,.04) 100%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:flex-end;text-align:right;padding:0 60px">
      <div class="kick d" style="letter-spacing:.3em;margin-bottom:24px">От ринга до Голливуда</div>
      <h2 class="div-huge" style="font-size:54px;max-width:16ch">Самое узнаваемое имя планеты</h2>
      <div class="div-rule" style="margin:28px 0"></div>
      <p class="div-sub" style="max-width:38ch">Десятикратный чемпион мира по версиям WWE и WCW,
      затем — многолетний лидер списков самых кассовых актёров. Вещи Скалы работают сразу
      в двух коллекционных мирах: рестлинга и большого кино.</p>
    </div>
    <span class="credit">Фото: Harald Krichel · Wikimedia Commons · CC BY-SA 4.0</span>
  </div>
</section>""")

    # ---------- печать
    duo("rstone", "mag", "Rolling Stone · 2000 и 2018", "Печать · 1–2 из 3")
    solo("nintendo", [img("nintendo", "00")], "Печать · 3 из 3")

    # ---------- фигурки и карточки
    duo("fig_jakks", "fig_psa", "Фигурки в блистерах", "Фигурки · 1–2 из 2")
    duo("duo98", "topps12", "Карточки с автографом", "Раритеты · 1–2 из 2")

    # ---------- упаковка
    add("""<section class="slide white duo2" id="__ID__">
  <div style="padding:30px 72px 0;display:flex;justify-content:space-between;align-items:baseline">
    <h2 class="serif" style="font-weight:500;font-size:28px;color:var(--ink)">Как мы отдаём подарок</h2>
    <span class="kick" style="letter-spacing:.2em">Упаковка Stargift</span>
  </div>
  <div class="duo2-in" style="grid-template-columns:1.1fr .9fr;align-items:center">
    <div class="dc"><div class="dc-ph" style="height:440px;background:#fff"><img src="img_packaging/box_kraft.jpg" alt=""></div></div>
    <div class="dc"><div class="dc-ph" style="height:440px;background:#fff"><img src="img_packaging/bag_white.jpg" alt=""></div></div>
  </div>
  <div style="padding:0 72px 34px;font:300 15px/1.6 'Inter';color:#4a4a4a;max-width:100ch">Каждый предмет уходит в фирменной упаковке дома:
  крафт-бумага с автографами великих, лента Stargift и плотный подарочный пакет.
  Подарок можно вручать сразу — прямо из рук в руки.</div>
</section>""")

    # ---------- лестница цен
    rows = "".join(
        f'<div class="lad-row"><div class="lad-nm">{esc(LOTS[k]["name"])}</div>'
        f'<div class="lad-pr">{rub(LOTS[k]["price"])}</div></div>' for k in ORDER_LADDER)
    add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:auto 1fr">
  <div style="padding:40px 66px 0">
    <div class="kick d" style="margin-bottom:12px">Подборка целиком</div>
    <h2 class="serif" style="font-weight:300;font-size:42px;line-height:1;color:var(--ivory)">15 предметов</h2>
  </div>
  <div style="padding:18px 66px 30px"><div class="lad">{rows}</div></div>
</section>""")

    # ---------- финал
    add("""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="padding:76px 72px 0;display:flex;flex-direction:column;justify-content:center">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:146px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start">
    <h2 class="serif" style="font-weight:300;font-size:44px;line-height:1.16;color:var(--ivory);margin-top:38px;max-width:32ch">Скала. Пятнадцать предметов человека, который построил две легенды.</h2>
  </div>
  <div style="padding:26px 72px 40px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.24em;color:var(--gold2)">stargift.ru</span>
  </div>
</section>""")

    doc = f"""<meta charset="utf-8">
<title>Stargift · Скала</title>
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
    open(f"{R}/deck_rock.html", "w", encoding="utf-8").write(doc)
    print(f"deck_rock.html: {n} слайдов, {len(LOTS)} лотов")


if __name__ == "__main__":
    main()
