#!/usr/bin/env python3
"""«Майкл Джексон · пластинки и фотографии» — презентация 1280×720.

    python3 tools_mj_build.py       # → deck_mj.html

Дека построена по эпохам: Motown и Jackson 5 → сольный дебют → Epic и Куинси
Джонс → Bad → фотографии. Перед каждой главой — архивный кадр в public domain,
у каждого альбома — справка с датой выхода и тем, чем эта пластинка известна.
"""
import html, os

import sys
VARIANT = (sys.argv[1] if len(sys.argv) > 1 else "A").upper()
R = os.path.dirname(os.path.abspath(__file__))
C = "img_mj"


def esc(s):
    return html.escape(s or "", quote=False)


def rub(n):
    return f"{n:,}".replace(",", " ") + "&nbsp;₽"


def img(name, half=False):
    """Обработанный кадр под половину слайда, затем обычный, затем исходник."""
    base = os.path.basename(name)
    for p in ([f"{C}/halfslide/{base}.jpg"] if half else []) + \
             [f"{C}/{name}.jpg", f"{C}/src/{name}.jpg", f"{C}/hist/{name}.jpg"]:
        if os.path.exists(os.path.join(R, p)):
            return p
    return f"{C}/src/{name}.jpg"


LOTS = {
 "iwyb":       dict(price=900_000,   cert="PSA/DNA",
   era='1969 · Motown', hist='Дебютный альбом Jackson 5. Имя Дайаны Росс на обложке было рекламным ходом лейбла: группу она не открывала, но её имя открывало радиостанции. Сингл с этой пластинки встал на первое место Billboard в январе 1970-го.',
   name="«Diana Ross Presents The Jackson 5» — конверт с автографом"),
 "maybe":      dict(price=1_850_000, cert="PSA",
   era='1971 · Motown', hist='Четвёртый альбом Jackson 5, вышедший на пике их первой славы. Экземпляр из первого тиража: разворотный конверт и оригинальные синие лейблы Motown на самом виниле.',
   name="«Maybe Tomorrow» — первый тираж 1971 года с автографами братьев Джексон"),
 "gottobe":    dict(price=1_000_000, cert="JSA",
   era='1972 · Motown', hist='Сольный дебют — Майклу тринадцать. Motown выпустил альбом, не выводя его из состава Jackson 5. С этой обложки начинается его отдельная биография.',
   name="«Got To Be There» — конверт сольного дебюта с автографом"),
 "farewell":   dict(price=1_050_000, cert="PSA/DNA",
   era='1984 · Motown', hist='Записи 1973 года пролежали в архиве лейбла одиннадцать лет. В 1984-м, на волне успеха «Thriller» у другого лейбла, их достали, добавили современную аранжировку и выпустили как новый альбом — без участия артиста.',
   name="«Farewell My Summer Love» — конверт с автографом"),
 "offthewall": dict(price=4_000_000, cert="JSA",
   era='1979 · Epic', hist='Первая совместная работа с Куинси Джонсом. Четыре сингла с альбома вошли в первую десятку Billboard — до этого ни один сольный исполнитель такого не добивался.',
   name="«Off The Wall» — конверт с автографом"),
 "thriller":   dict(price=2_400_000, cert="PSA/DNA",
   era='1982 · Epic', hist='Самый продаваемый альбом в истории звукозаписи. Экземпляр из раннего тиража: каталожный номер QE 38112, то есть пластинка отпечатана в первые месяцы после выхода, ещё до того, как продажи стали рекордными.',
   name="«Thriller» — ранний тираж QE 38112 с автографом"),
 "thrillerjp": dict(price=1_750_000, cert="JSA",
   era='1982 · Epic Japan', hist='Японское издание с оби-полосой — узкой бумажной лентой на корешке, которую печатали отдельно и почти всегда выбрасывали при вскрытии. Инструментальная версия выпускалась только для японского рынка.',
   name="«Thriller» — японское издание инструментальной версии с оби-полосой и автографом"),
 "bad":        dict(price=3_000_000, cert="PSA",
   era='1987 · Epic', hist='Третья и последняя пластинка, сделанная с Куинси Джонсом. Пять синглов с одного альбома поднялись на первое место Billboard — до «Bad» этого не удавалось никому.',
   name="«Bad» — конверт с именным посвящением и автографом"),
 "badpromo":   dict(price=3_800_000, cert="JSA",
   era='1987 · Epic', hist='Промо-тираж печатался ограниченным числом и рассылался на радио до официального выхода. В продажу такие экземпляры не поступали, поэтому уцелевших мало.',
   name="«Bad» — промо-тираж с автографом"),
 "ph1620":     dict(price=1_300_000, cert="JSA",
   era='1983 · эпоха «Billie Jean»', hist='Год после выхода «Thriller»: сингл «Billie Jean» держится в верхней строчке, а лунная походка на юбилейном концерте Motown только что превратила Джексона в главную фигуру десятилетия.',
   name="Фотография эпохи «Billie Jean» с автографом, 41×51 см"),
 "ph75":       dict(price=1_600_000, cert="PSA/DNA",
   era='1980-е · сцена', hist='Расшитый сценический костюм — часть образа, который Джексон выстраивал сам: военная выправка, блеск, узнаваемый силуэт с последнего ряда зала.',
   name="Фотография в расшитом сценическом костюме с автографом, 19×28 см"),
 "ph1114c":    dict(price=1_850_000, cert="PSA/DNA",
   era='1990-е', hist='Кадр периода, когда Джексон уже не выступал регулярно, но оставался самым узнаваемым лицом в мире. Чёрная куртка с шевронами — его поздний сценический образ.',
   name="Цветная фотография с автографом, 28×36 см"),
 "ph1114hat":  dict(price=2_000_000, cert="PSA",
   era='1987–1988 · «Smooth Criminal»', hist='Белая шляпа, синий свет и наклон корпуса — самая копируемая поза в истории поп-музыки, снятая на съёмках «Moonwalker».',
   name="Фотография в белой шляпе с автографом, 28×36 см"),
 "cut":        dict(price=750_000,   cert="PSA/DNA",
   era='Автограф', hist='Отдельный лист с росчерком, запечатанный в капсулу. Самый гибкий предмет подборки: его оформляют в раму рядом с любой фотографией на выбор.',
   name="Автограф на отдельном листе в капсуле, 23×9 см"),
}

ORDER = ["offthewall", "badpromo", "bad", "thriller", "ph1114hat", "ph1114c",
         "maybe", "thrillerjp", "ph75", "ph1620", "farewell", "gottobe",
         "iwyb", "cut"]

CSS = """
:root{--noir:#0B0B0C;--gold:#A98545;--gold2:#C9A96A;--ivory:#F5F1E8;--ink:#1A1A1A}
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;overflow:hidden;background:#000;font-family:'Inter',sans-serif}
.deck{height:100%;position:relative}
.slide{position:absolute;inset:0;display:none;overflow:hidden}
.slide.on{display:grid}
.slide>*{min-height:0;min-width:0}
img{display:block}
.serif{font-family:'Cormorant Garamond',serif}
.kick{font:500 13px/1 'Inter';letter-spacing:.36em;text-transform:uppercase;color:var(--gold)}
.kick.d{color:var(--gold2)}
.white{background:#FFFFFF;color:var(--ink)}
.dark{background:var(--noir);color:var(--ivory)}
.credit{position:absolute;right:16px;bottom:12px;font:400 11px/1.3 'Inter';
  letter-spacing:.08em;color:rgba(245,241,232,.55)}
.div-rule{height:1px;width:70px;background:rgba(169,133,69,.55)}
.div-huge{font-family:'Cormorant Garamond';font-weight:300;line-height:1;color:var(--ivory)}
.div-sub{font:300 22px/1.6 'Inter';color:#c9c3b7}

.solo{grid-template-columns:__COLS__}
.ph2{height:720px;overflow:hidden;background:#fff}
.ph2 img{width:100%;height:100%;object-fit:cover;object-position:50% 50%}
.solo-side{display:flex;flex-direction:column;justify-content:center;padding:48px 54px 48px 26px}
.solo-name{font-family:'Cormorant Garamond';font-weight:500;font-size:34px;line-height:1.14;color:var(--ink)}
.solo-text{font:300 18.5px/1.58 'Inter';color:#4a4a4a;margin-top:13px}
.solo-price{font-family:'Cormorant Garamond';font-weight:500;font-size:38px;color:var(--gold);margin-top:16px}
.lot-era{font-weight:500;font-size:30px;line-height:1;color:var(--gold);margin-bottom:12px;letter-spacing:.01em}
.lot-hist{margin-top:15px;padding-left:16px;border-left:2px solid var(--gold)}
.lot-era-s{font:500 12px/1 'Inter';letter-spacing:.22em;text-transform:uppercase;color:var(--gold);margin-bottom:8px}
.lot-hist-t{font:300 17px/1.55 'Inter';color:#3d3d3d}
.solo-spec{font:400 12.5px/1.5 'Inter';letter-spacing:.18em;text-transform:uppercase;color:#9a958c;margin-top:9px}

/* справка об альбоме: тёмная страница с цифрами */
.fact{grid-template-columns:.92fr 1.08fr}
.fact-side{display:flex;flex-direction:column;justify-content:center;padding:54px 46px 54px 58px}
.fact-tt{font-family:'Cormorant Garamond';font-weight:300;font-size:44px;line-height:1.06;color:var(--ivory)}
.fact-tx{font:300 15px/1.68 'Inter';color:#b8b2a6;margin-top:20px}
.fact-rows{margin-top:26px;border-top:1px solid rgba(169,133,69,.28)}
.fact-row{display:grid;grid-template-columns:auto 1fr;gap:20px;padding:9px 0;
  border-bottom:1px solid rgba(169,133,69,.18);align-items:baseline}
.fact-k{font:500 9.5px/1.4 'Inter';letter-spacing:.2em;text-transform:uppercase;color:var(--gold);min-width:96px}
.fact-v{font:300 13px/1.5 'Inter';color:#d5cfc3}

/* справка без кадра: год крупно слева, факты справа */
.fp{grid-template-columns:.62fr 1.38fr}
.fp-l{display:flex;flex-direction:column;justify-content:center;padding:0 0 0 58px;
  border-right:1px solid rgba(169,133,69,.24)}
.fp-year{font-weight:300;font-size:92px;line-height:1;color:var(--gold);letter-spacing:-.02em}
.fp-r{display:flex;flex-direction:column;justify-content:center;padding:54px 62px}
.fp-rows{margin-top:26px;display:grid;grid-template-columns:1fr 1fr;gap:0 44px;
  border-top:1px solid rgba(169,133,69,.28)}
.fp-row{display:grid;grid-template-columns:auto 1fr;gap:18px;padding:10px 0;
  border-bottom:1px solid rgba(169,133,69,.18);align-items:baseline}

.gal{grid-template-rows:auto 1fr auto}
.gal-head{display:flex;justify-content:space-between;align-items:baseline;padding:30px 60px 0}
.gal-name{font-family:'Cormorant Garamond';font-weight:500;font-size:32px;color:var(--ink)}
.gal-grid{display:grid;gap:16px;padding:20px 60px 0}
.gal-cell{background:#F7F5F1;display:flex;align-items:center;justify-content:center;overflow:hidden}
.gal-cell img{max-width:100%;max-height:100%;object-fit:contain}
.gal-foot{padding:18px 60px 30px;font:300 17.5px/1.55 'Inter';color:#4a4a4a;max-width:104ch}

/* прайс-лист в две колонки: с крупным кеглем 14 строк в один столбец не влезают,
   а кегль уменьшать нельзя — правило шаблона */
.lad{display:grid;grid-template-columns:1fr 1fr;gap:0 46px;align-content:start}
.lad-row{display:grid;grid-template-columns:1fr auto;gap:26px;align-items:baseline;
  padding:9px 0;border-bottom:1px solid rgba(169,133,69,.2)}
.lad-nm{font:300 16px/1.35 'Inter';color:#d5cfc3}
.lad-pr{font-family:'Cormorant Garamond';font-weight:500;font-size:24px;color:var(--gold2);white-space:nowrap}
"""


def main():
    S, n = [], 0

    def add(s):
        nonlocal n
        n += 1
        S.append(s.replace("__ID__", f"s{n:02d}"))

    def solo(key, photo, kick, text):
        """Слайд лота. История альбома идёт первым абзацем описания —
        отдельным слайдом-справкой она ломает логику деки при открытии."""
        it = LOTS[key]
        if VARIANT == "B":
            lead = (f'<div class="lot-era serif">{esc(it["era"])}</div>'
                    f'<div class="solo-name">{esc(it["name"])}</div>'
                    f'<div class="solo-text">{esc(it["hist"])} {esc(text)}</div>')
        else:
            lead = (f'<div class="solo-name">{esc(it["name"])}</div>'
                    f'<div class="lot-hist"><div class="lot-era-s">{esc(it["era"])}</div>'
                    f'<div class="lot-hist-t">{esc(it["hist"])}</div></div>'
                    f'<div class="solo-text">{esc(text)}</div>')
        add(f"""<section class="slide white solo" id="__ID__">
  <div class="ph2"><img src="{photo}" alt=""></div>
  <div class="solo-side">
    <div class="kick" style="margin-bottom:13px">{kick}</div>
    {lead}
    <div class="solo-price">{rub(it['price'])}</div>
    <div class="solo-spec">{esc(it['cert'])}</div>
  </div>
</section>""")

    def fact(kick, title, text, rows, photo, objpos="50% 40%"):
        rr = "".join(f'<div class="fact-row"><div class="fact-k">{esc(k)}</div>'
                     f'<div class="fact-v">{esc(v)}</div></div>' for k, v in rows)
        add(f"""<section class="slide dark fact" id="__ID__">
  <div class="fact-side">
    <div class="kick d" style="margin-bottom:18px">{esc(kick)}</div>
    <h2 class="fact-tt">{title}</h2>
    <p class="fact-tx">{esc(text)}</p>
    <div class="fact-rows">{rr}</div>
  </div>
  <div style="position:relative;height:720px;overflow:hidden">
    <img src="{photo}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:{objpos}">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,var(--noir) 0%,rgba(11,11,12,.34) 20%,rgba(11,11,12,0) 46%)"></div>
  </div>
</section>""")

    def fact_plain(kick, year, title, text, rows):
        """Справка без кадра: у альбома нет архивного фото своей эпохи,
        а ставить рядом ту же обложку, что на слайде лота, — дубль."""
        rr = "".join(f'<div class="fp-row"><div class="fact-k">{esc(k)}</div>'
                     f'<div class="fact-v">{esc(v)}</div></div>' for k, v in rows)
        add(f"""<section class="slide dark fp" id="__ID__">
  <div class="fp-l">
    <div class="kick d" style="margin-bottom:16px">{esc(kick)}</div>
    <div class="fp-year serif">{esc(year)}</div>
  </div>
  <div class="fp-r">
    <h2 class="fact-tt" style="font-size:46px">{title}</h2>
    <p class="fact-tx" style="max-width:46ch">{esc(text)}</p>
    <div class="fp-rows">{rr}</div>
  </div>
</section>""")


    def framing(photo, kick, title, text, note):
        add(f"""<section class="slide white solo" id="__ID__">
  <div class="ph2"><img src="{photo}" alt=""></div>
  <div class="solo-side">
    <div class="kick" style="margin-bottom:13px">{esc(kick)}</div>
    <div class="solo-name">{esc(title)}</div>
    <div class="solo-text">{esc(text)}</div>
    <div class="lot-hist" style="margin-top:20px"><div class="lot-hist-t">{esc(note)}</div></div>
  </div>
</section>""")

    def gallery(title, kick, cells, cols, rowh, foot):
        cc = "".join(f'<div class="gal-cell" style="height:{rowh}px">'
                     f'<img src="{p}" alt=""></div>' for p in cells)
        add(f"""<section class="slide white gal" id="__ID__">
  <div class="gal-head"><div class="gal-name">{esc(title)}</div>
    <span class="kick">{esc(kick)}</span></div>
  <div class="gal-grid" style="grid-template-columns:repeat({cols},1fr)">{cc}</div>
  <div class="gal-foot">{esc(foot)}</div>
</section>""")

    def divider(kick, huge, sub, photo, credit, objpos="50% 30%"):
        add(f"""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="position:relative">
    <img src="{photo}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:{objpos}">
    <div style="position:absolute;inset:0;background:linear-gradient(270deg,rgba(11,11,12,.95) 0%,rgba(11,11,12,.78) 34%,rgba(11,11,12,.22) 66%,rgba(11,11,12,.06) 100%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:flex-end;text-align:right;padding:0 62px">
      <div class="kick d" style="letter-spacing:.3em;margin-bottom:22px">{esc(kick)}</div>
      <h2 class="div-huge" style="font-size:58px;max-width:15ch">{huge}</h2>
      <div class="div-rule" style="margin:26px 0"></div>
      <p class="div-sub" style="max-width:40ch">{esc(sub)}</p>
    </div>
    <span class="credit">{esc(credit)}</span>
  </div>
</section>""")

    # ---------- обложка
    add(f"""<section class="slide dark on" id="__ID__" style="grid-template-columns:1fr 1.02fr">
  <div style="display:flex;flex-direction:column;justify-content:space-between;padding:56px 52px">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:140px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start">
    <div>
      <div class="kick d" style="margin-bottom:22px">Частное собрание · Музыка</div>
      <h1 class="serif" style="font-weight:300;font-size:66px;line-height:1.03;color:var(--ivory)">Майкл<br>Джексон</h1>
      <p style="font:300 16px/1.64 'Inter';color:#b8b2a6;margin-top:22px;max-width:44ch">Девять подписанных пластинок — от первого сингла
      Jackson 5 до «Bad» — и пять фотографий. Двадцать лет карьеры, собранные
      по конвертам, которые он держал в руках.</p>
    </div>
    <div class="kick" style="letter-spacing:.24em">14 предметов · август 2026</div>
  </div>
  <div style="position:relative;height:720px;overflow:hidden">
    <img src="{img('mj_1984')}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 25%">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,var(--noir) 0%,rgba(11,11,12,.3) 24%,rgba(11,11,12,0) 54%)"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,11,12,.5) 0%,rgba(11,11,12,0) 28%)"></div>
    <span class="credit">Фото: Epic Records · Wikimedia Commons · public domain</span>
  </div>
</section>""")

    # ================= 1969–1971 · Motown
    divider("1969–1971 · Motown", "Пятеро братьев<br>из Гэри, Индиана",
            "Осенью 1969 года Motown выпустил сингл группы, которую ещё никто не знал. "
            "Через три месяца он стоял на первой строчке, а солисту было одиннадцать лет.",
            img("j5_1969"), "Фото: Bernie Ilson, Inc. · Wikimedia Commons · public domain", "50% 24%")

    solo("iwyb", img("clean_iwyb", half=True), "Пластинки · 1 из 14",
         "Конверт в состоянии, редком для тиража 1969 года: углы целы, картон "
         "не расслоился. Росчерк идёт наискось через всю обложку — так Джексон "
         "подписывал в ранние годы, размашисто и во всю площадь.")


    solo("maybe", img("clean_maybe", half=True), "Пластинки · 2 из 14",
         "Автографы Jackson 5 того периода встречаются реже сольных: группа "
         "подписывала мало и почти всегда на бегу. Здесь росчерки идут "
         "по светлой части обложки и читаются все до одного.")

    gallery("«Maybe Tomorrow» · разворот и винил", "Пластинки · 2 из 14",
            [img("src/maybe_01"), img("src/maybe_02"), img("src/maybe_07"),
             img("src/maybe_12"), img("src/maybe_13"), img("src/maybe_16")],
            3, 200,
            "Разворотный конверт с росчерками, внутренний разворот с фотографиями группы, "
            "оригинальные синие лейблы Motown и сам винил. Первый пресс отличается именно "
            "лейблом: у поздних переизданий он другого цвета и с другим шрифтом.")

    # ================= 1972 · сольный дебют

    solo("gottobe", img("clean_gottobe", half=True), "Пластинки · 3 из 14",
         "Конверт сольного дебюта с автографом. Точка, с которой начинается "
         "всё остальное в этой подборке: до «Got To Be There» Майкл Джексон был "
         "солистом группы, после — самостоятельным именем на обложке.")

    solo("farewell", img("clean_farewell", half=True), "Пластинки · 4 из 14",
         "Конверт с автографом. Экземпляр полный: с бонусным цветным постером, "
         "который вкладывался в первый тираж и обычно теряется первым. "
         "Обложка — ночной концертный кадр, редкий для его пластинок сюжет.")

    gallery("«Farewell My Summer Love» · комплект", "Пластинки · 4 из 14",
            [img("src/farewell_00"), img("src/farewell_05"), img("src/farewell_06"),
             img("src/farewell_07"), img("src/farewell_02"), img("src/farewell_03")],
            3, 200,
            "Лицевая сторона с автографом, оборот с указанием на вложенный постер, "
            "внутренний конверт со списком композиций и сам винил. "
            "Сохранность конверта для тиража 1984 года выше средней.")

    # ================= 1979–1982 · Epic
    divider("1979–1987 · Epic", "Куинси Джонс<br>и три альбома",
            "Уйдя с Motown, Джексон записал с продюсером Куинси Джонсом три пластинки "
            "подряд. Каждая следующая продавалась лучше предыдущей — случай, которого "
            "в поп-музыке больше не было.",
            img("mj_1984"), "Фото: Epic Records · Wikimedia Commons · public domain", "50% 20%")


    solo("offthewall", img("clean_offthewall", half=True), "Пластинки · 5 из 14",
         "Конверт с автографом — самый дорогой предмет подборки. "
         "Обложка снята в смокинге у кирпичной стены: образ, который Джексон "
         "потом повторял на сцене годами. Росчерк лежит по светлому полю "
         "и читается целиком.")


    solo("thriller", img("clean_thriller", half=True), "Пластинки · 6 из 14",
         "Конверт «Thriller» раннего тиража с автографом. Белый костюм на чёрном "
         "фоне — обложка, которую узнают без подписи в любой стране. "
         "Автограф поставлен по светлому пиджаку и не спорит с изображением.")

    gallery("«Thriller» · конверт и внутренний разворот", "Пластинки · 6 из 14",
            [img("src/thriller_00"), img("src/thriller_01"), img("src/thriller_05")],
            3, 330,
            "Лицевая сторона с автографом, внутренний разворот с текстами песен "
            "и сам винил. Ранний пресс узнаётся по каталожному номеру на этикетке.")

    framing(img("framed_thriller_diptych", half=True), "Оформление · пластинка",
            "Раскрывающаяся рама: конверт и сам диск",
            "Две квадратные панели на латунных петлях, бордовый бархат внутри. "
            "Закрытой рама показывает конверт, открытой — конверт и винил в глубокой нише. "
            "Формат дома для пластинки, у которой хочется показать обе части.",
            "Бархат подбираем под палитру конверта: бордовый, тёмно-синий или бирюзовый.")

    framing(img("framed_thriller_square", half=True), "Оформление · пластинка",
            "Закрытый квадрат: только конверт",
            "Тот же экземпляр в простой подаче — одна квадратная рама, бордовое "
            "бархатное паспарту, тонкая золотая линия и латунная табличка внизу. "
            "Вешается как картина и занимает вдвое меньше стены.",
            "Выбор между диптихом и квадратом — вопрос места и того, подписан ли сам винил.")

    solo("thrillerjp", img("clean_thrillerjp", half=True), "Пластинки · 7 из 14",
         "Оби-полоса сохранена целиком, с иероглифами и ценой в иенах — по ней "
         "японский экземпляр отличают от европейского с первого взгляда. "
         "Автограф поставлен по светлому полю обложки и не перекрывает лицо.")


    solo("bad", img("clean_bad", half=True), "Пластинки · 8 из 14",
         "Конверт с автографом и именным посвящением — Джексон подписал его "
         "конкретному человеку, надписав имя от руки. Такие экземпляры "
         "ценятся отдельно: они доказывают, что подпись поставлена вживую, "
         "а не на стопке конвертов у стола промоутера.")

    solo("badpromo", img("clean_badpromo", half=True), "Пластинки · 9 из 14",
         "Промо-экземпляр узнаётся по обороту: вместо торгового оформления там "
         "служебная разметка для радиостанции. Автограф крупный, поставлен "
         "по белому полю рядом с логотипом.")

    # ================= фотографии
    divider("Фотографии", "Белый дом,<br>14 мая 1984",
            "Рейган вручает Джексону благодарность за то, что тот отдал «Beat It» "
            "для кампании против пьяного вождения. Год «Thriller» — и единственный "
            "визит поп-музыканта в Розовый сад в таком качестве.",
            img("mj_reagan"), "Фото: Ronald Reagan Presidential Library · Wikimedia Commons · public domain", "50% 40%")

    solo("ph1620", img("clean_ph1620", half=True), "Фотографии · 10 из 14",
         "Крупноформатный кадр эпохи «Billie Jean» с автографом. "
         "Формат 41×51 см — самый большой в подборке, рассчитанный на то, "
         "чтобы висеть отдельно, а не в ряду.")

    solo("ph75", img("clean_ph75", half=True), "Фотографии · 11 из 14",
         "Сценический кадр в расшитом костюме с автографом. Небольшой формат, "
         "плотная композиция: лицо, костюм и росчерк умещаются в одном кадре "
         "без пустот.")

    solo("ph1114c", img("clean_ph1114c", half=True), "Фотографии · 12 из 14",
         "Цветной портрет в чёрной куртке с шевронами — образ конца восьмидесятых. "
         "Автограф серебряным маркером по тёмному полю, читается на просвет.")

    solo("ph1114hat", img("clean_ph1114hat", half=True), "Фотографии · 13 из 14",
         "Кадр в белой шляпе и синем сценическом свете — узнаваемая поза "
         "из «Smooth Criminal». Один из тех снимков, где герой опознаётся "
         "по силуэту, даже если закрыть лицо.")

    framing(img("framed_ph1114hat", half=True), "Оформление · фотография",
            "Тёмная рама, синее замшевое паспарту",
            "Под холодный кадр берём синее паспарту и тёмную раму: рамка не спорит "
            "со сценическим светом, а золотая линия по краю окна отделяет снимок "
            "от поля. Латунная табличка с именем внизу.",
            "Цвет паспарту всегда берём у самой фотографии, а не по каталогу.")

    framing(img("framed_ph1620", half=True), "Оформление · фотография",
            "Кованое золото, бордовый бархат",
            "Тёплый кадр требует тёплой рамы: кованое золото и бордовый бархат — "
            "классический регистр дома для портретов. Тот же снимок в тёмной раме "
            "выглядел бы холоднее, чем он есть.",
            "Две фотографии рядом на одной стене оформляем в одном материале рамы.")

    solo("cut", img("clean_cut", half=True), "Фотографии · 14 из 14",
         "Автограф на отдельном листе, запечатанный в капсулу. "
         "Самый доступный предмет подборки и самый гибкий: капсулу можно "
         "оформить в раму рядом с любой фотографией на выбор.")

    # ---------- упаковка
    add("""<section class="slide white" id="__ID__" style="grid-template-rows:auto 1fr auto">
  <div style="padding:30px 66px 0;display:flex;justify-content:space-between;align-items:baseline">
    <h2 class="serif" style="font-weight:500;font-size:27px;color:var(--ink)">Как мы отдаём подарок</h2>
    <span class="kick" style="letter-spacing:.2em">Упаковка Stargift</span>
  </div>
  <div style="display:grid;grid-template-columns:1.05fr .95fr;gap:44px;padding:18px 66px 0;align-items:center">
    <div style="height:430px;display:flex;align-items:center;justify-content:center;background:#F7F5F1;overflow:hidden"><img src="img_packaging/box_kraft.jpg" alt="" style="max-width:100%;max-height:100%;object-fit:contain"></div>
    <div style="height:430px;display:flex;align-items:center;justify-content:center;background:#F7F5F1;overflow:hidden"><img src="img_packaging/bag_white.jpg" alt="" style="max-width:100%;max-height:100%;object-fit:contain"></div>
  </div>
  <div style="padding:16px 66px 32px;font:300 14.5px/1.6 'Inter';color:#4a4a4a;max-width:104ch">Каждый предмет уходит в фирменной упаковке дома:
  крафт-бумага с автографами великих, лента Stargift и плотный подарочный пакет. Оформленную работу
  привозим и вешаем сами.</div>
</section>""")

    # ---------- лестница
    rows = "".join(
        f'<div class="lad-row"><div class="lad-nm">{esc(LOTS[k]["name"])}</div>'
        f'<div class="lad-pr">{rub(LOTS[k]["price"])}</div></div>' for k in ORDER)
    # порядок по колонкам сверху вниз, а не змейкой
    add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:auto 1fr">
  <div style="padding:34px 62px 0">
    <div class="kick d" style="margin-bottom:10px">Подборка целиком</div>
    <h2 class="serif" style="font-weight:300;font-size:38px;line-height:1;color:var(--ivory)">14 предметов</h2>
  </div>
  <div style="padding:14px 62px 28px"><div class="lad">{rows}</div></div>
</section>""")

    # ---------- финал
    add("""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="padding:74px 66px 0;display:flex;flex-direction:column;justify-content:center">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:140px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start">
    <h2 class="serif" style="font-weight:300;font-size:44px;line-height:1.14;color:var(--ivory);margin-top:36px;max-width:32ch">Майкл Джексон. От первого сингла до последней пластинки с Куинси Джонсом.</h2>
  </div>
  <div style="padding:24px 66px 38px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.24em;color:var(--gold2)">stargift.ru</span>
  </div>
</section>""")

    doc = f"""<meta charset="utf-8">
<title>Stargift · Майкл Джексон</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>{CSS.replace("__COLS__", "1.28fr 1fr" if VARIANT == "A" else "1fr 1.12fr")}</style>

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
    open(f"{R}/deck_mj_{VARIANT}.html", "w", encoding="utf-8").write(doc)
    print(f"deck_mj_{VARIANT}.html: {n} слайдов, {len(LOTS)} лотов")


if __name__ == "__main__":
    main()
