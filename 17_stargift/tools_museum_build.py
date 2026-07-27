#!/usr/bin/env python3
"""
«Музей футбола» — клиентская презентация 1280×720 из выгрузки лотов.

    python3 tools_museum_build.py            # → deck_museum.html

Форматы взяты из отобранной библиотеки (TEMPLATES.md): обложка t01, разделитель t03,
соло q07 (музейный белый), крест 2×2 q01 в белой версии, лестница цен vl07, финал t20.
Фото лотов НИКОГДА не кропаются — везде object-fit:contain.
"""
import html, json, os, re

R = os.path.dirname(os.path.abspath(__file__))

# порядок глав в каталоге
# Месси в дек не входит — по нему отдельная презентация
ORDER = ["ЛЕГЕНДЫ МИРОВОГО ФУТБОЛА", "ВРАТАРИ", "ЗАЩИТНИКИ",
         "ПОЛУЗАЩИТНИКИ", "НАПАДАЮЩИЕ", "БУТСЫ С АВТОГРАФАМИ", "МЯЧИ С АВТОГРАФАМИ",
         "НОВОЕ ПОКОЛЕНИЕ"]

# кадр на разделитель главы: файл, подпись источника, точка кадрирования, сторона текста.
# Где сильного кадра нет — типографика. Обложку держит отдельный кадр (Пеле, 1970).
COVER = ("img_museum2/hero/legends.jpg", "Фото: Wikimedia Commons · public domain")
HERO = {
 "ВРАТАРИ":       ("img_museum2/hero/keepers.jpg", "Фото: Ron Kroon · Anefo · Wikimedia Commons · CC0", "50% 46%", "left"),
 "ПОЛУЗАЩИТНИКИ": ("img_museum2/hero/mids.jpg",    "Фото: Tam Tam · Wikimedia Commons · CC BY-SA 2.0", "50% 34%", "left"),
 "НАПАДАЮЩИЕ":    ("img_museum2/hero/forwards.jpg","Фото: Berlination · Wikimedia Commons · CC BY-SA 4.0", "50% 42%", "left",
   "linear-gradient(__DEG__deg,rgba(11,11,12,.96) 0%,rgba(11,11,12,.92) 20%,"
   "rgba(11,11,12,.55) 33%,rgba(11,11,12,.1) 45%,rgba(11,11,12,0) 60%)", 32),
 "МЯЧИ С АВТОГРАФАМИ": ("img_museum2/hero/balls.jpg", "Фото: Peter Glaser · Wikimedia Commons · CC0", "50% 50%", "right"),
 "НОВОЕ ПОКОЛЕНИЕ": ("img_museum2/hero/young.jpg",  "Фото: Bryan Berlin · Wikimedia Commons · CC BY-SA 4.0", "50% 34%", "left"),
}
# лоты, снятые Вашиком с подборки: реплики трофеев, дубли Каннаваро,
# два мяча и бутса Холанда
DROP = {
    "f3ae11fdfe",   # Кафу — 3D-реплика Кубка Лиги чемпионов
    "a3db28a1dc",   # Пирло — 3D-реплика Кубка Лиги чемпионов
    "bf086cd624",   # Каннаваро — футболка «Реал Мадрида»
    "274ee51056",   # Каннаваро — домашняя футболка сборной Италии №5
    "748f3b54a0",   # Бензема — мяч
    "30ad616a8b",   # Вальдеррама — мяч
    "805c6898b8",   # Холанд — бутса
}
# лоты, которым нужен отдельный слайд из-за сюжетного текста
PIN_SOLO = {"e19f81d305"}   # Пеле — фотография удара через себя
TITLE = {"ЛИОНЕЛЬ МЕССИ": "Лионель Месси", "ЛЕГЕНДЫ МИРОВОГО ФУТБОЛА": "Легенды",
         "ВРАТАРИ": "Вратари", "ЗАЩИТНИКИ": "Защитники", "ПОЛУЗАЩИТНИКИ": "Полузащитники",
         "НАПАДАЮЩИЕ": "Нападающие", "БУТСЫ С АВТОГРАФАМИ": "Бутсы",
         "МЯЧИ С АВТОГРАФАМИ": "Мячи", "НОВОЕ ПОКОЛЕНИЕ": "Новое поколение"}

# символическая сборная всех времён по версии France Football, 3-1-3-3
XI = [
    ("Яшин",        50, 90, "Лев Яшин — подписной лист"),
    ("Кафу",        16, 73, "Кафу — мяч сборной Бразилии"),
    ("Беккенбауэр", 50, 76, None),
    ("Мальдини",    84, 73, "Паоло Мальдини — футболка сборной Италии"),
    ("Маттеус",     50, 57, None),
    ("Пеле",        17, 39, "Пеле — футболка «Сантос»"),
    ("Хави",        50, 35, None),
    ("Марадона",    83, 39, None),
    ("Месси",       18, 16, "Лионель Месси — футболка сборной Аргентины"),
    ("Роналдо",     50, 12, "Роналдо и Роналдиньо — бутса"),
    ("Криштиану",   82, 16, "Пеле, Месси, Роналду — мяч"),
]

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

.div-huge{font-family:'Cormorant Garamond';font-weight:300;line-height:1;color:var(--ivory)}
.div-rule{height:1px;width:70px;background:rgba(169,133,69,.55)}
.div-sub{font:300 19px/1.65 'Inter';color:#c9c3b7;max-width:52ch}

/* соло — топ-лот главы */
.solo{grid-template-columns:1.16fr 1fr}
.solo-ph{display:flex;align-items:center;justify-content:center;padding:50px 24px 50px 58px;background:#fff}
.solo-ph img{max-width:100%;max-height:100%;object-fit:contain}
.solo-side{display:flex;flex-direction:column;justify-content:center;padding:54px 58px 54px 24px}
.solo-name{font-family:'Cormorant Garamond';font-weight:500;font-size:34px;line-height:1.09;color:var(--ink)}
.solo-text{font:300 16.5px/1.65 'Inter';color:#4a4a4a;margin-top:16px}
.solo-price{font-family:'Cormorant Garamond';font-weight:500;font-size:31px;color:var(--gold);margin-top:20px}
.solo-cert{font:400 10px/1 'Inter';letter-spacing:.22em;text-transform:uppercase;color:var(--cert);margin-top:10px}

/* крест 2×2 — рабочая страница главы */
.quad{grid-template-rows:auto 1fr}
.quad-in{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;
  gap:22px 44px;padding:16px 60px 28px}
.qc{display:grid;grid-template-columns:236px 1fr;gap:20px;align-items:center}
.qc-ph{width:236px;height:196px;display:flex;align-items:center;justify-content:center;background:#fff}
.qc-ph img{max-width:100%;max-height:100%;object-fit:contain}
.qc-name{font-family:'Cormorant Garamond';font-weight:500;font-size:20px;line-height:1.14;color:var(--ink)}
.qc-text{font:300 12.5px/1.5 'Inter';color:#4a4a4a;margin-top:7px}
.qc-price{font-family:'Cormorant Garamond';font-weight:500;font-size:20px;color:var(--gold);margin-top:8px}
.qc-cert{font:400 9px/1 'Inter';letter-spacing:.2em;text-transform:uppercase;color:var(--cert);margin-top:6px}

/* дуэт — два экспоната, фото сверху целиком */
.duo2{grid-template-rows:auto 1fr}
.duo2-in{display:grid;grid-template-columns:1fr 1fr;gap:46px;padding:16px 72px 30px;align-items:start}
.dc{display:flex;flex-direction:column;align-items:center;text-align:center}
.dc-ph{width:100%;height:326px;display:flex;align-items:center;justify-content:center;background:#fff}
.dc-ph img{max-width:100%;max-height:100%;object-fit:contain}
.dc-name{font-family:'Cormorant Garamond';font-weight:500;font-size:24px;line-height:1.14;color:var(--ink);margin-top:18px;max-width:28ch}
.dc-text{font:300 14.5px/1.55 'Inter';color:#4a4a4a;margin-top:9px;max-width:48ch}
.dc-price{font-family:'Cormorant Garamond';font-weight:500;font-size:24px;color:var(--gold);margin-top:11px}
.dc-cert{font:400 9.5px/1 'Inter';letter-spacing:.2em;text-transform:uppercase;color:var(--cert);margin-top:8px}

/* поле — символическая сборная */
.pitch{position:relative;width:100%;height:100%;background:linear-gradient(180deg,#101110 0%,#0b0b0c 100%)}
.pitch .ln{position:absolute;border:1px solid rgba(169,133,69,.20)}
.pos{position:absolute;transform:translate(-50%,-50%);text-align:center;width:150px}
.dot{width:38px;height:38px;border-radius:50%;margin:0 auto 7px;display:flex;align-items:center;
  justify-content:center;font-family:'Cormorant Garamond';font-size:16px}
.have .dot{background:radial-gradient(circle at 38% 32%,#E4C88A,#A98545 70%);color:#0B0B0C;
  box-shadow:0 0 0 1px rgba(201,169,106,.55),0 10px 26px rgba(169,133,69,.28)}
.miss .dot{background:transparent;border:1px dashed rgba(245,241,232,.28);color:rgba(245,241,232,.4)}
.pname{font:500 12.5px/1.15 'Inter';white-space:nowrap}
.have .pname{color:var(--ivory)}
.miss .pname{color:rgba(245,241,232,.44)}
.pwhat{font:300 9.5px/1.3 'Inter';color:var(--gold2);margin-top:4px}
.pmiss{font:400 9px/1 'Inter';letter-spacing:.16em;text-transform:uppercase;color:rgba(245,241,232,.32);margin-top:4px}

/* оглавление */
.toc{display:grid;grid-template-columns:repeat(3,1fr);gap:26px 44px;padding:0 60px}
.toc-i{border-top:1px solid rgba(169,133,69,.3);padding-top:13px}
.toc-n{font-family:'Cormorant Garamond';font-weight:500;font-size:26px;color:var(--ivory)}
.toc-c{font:400 10px/1 'Inter';letter-spacing:.2em;text-transform:uppercase;color:var(--gold2);margin-top:8px}

/* лестница цен */
.lad{display:flex;flex-direction:column;height:100%;justify-content:space-between}
.lad-row{display:grid;grid-template-columns:1fr auto;gap:30px;align-items:baseline;
  padding:6px 0;border-bottom:1px solid rgba(169,133,69,.2)}
.lad-nm{font:300 13.5px/1.3 'Inter';color:#d5cfc3}
.lad-pr{font-family:'Cormorant Garamond';font-weight:500;font-size:19px;color:var(--gold2);white-space:nowrap}
"""


def rub(n):
    return f"{n:,}".replace(",", " ") + "&nbsp;₽"


def esc(s):
    return html.escape(s or "", quote=False)


def photo(it):
    # png — вырезанный предмет на прозрачном фоне, jpg — обработанный кадр
    for ext in ("png", "jpg"):
        c = f"img_museum2/clean_{it['key']}.{ext}"
        if os.path.exists(os.path.join(R, c)):
            return c
    return it["photo"]


def main():
    lots = json.load(open(f"{R}/museum_lots.json", encoding="utf-8"))
    lots = [x for x in lots                          # Месси — отдельный дек
            if x["group"] in ORDER and x["key"] not in DROP]
    txt = json.load(open(f"{R}/texts_museum.json", encoding="utf-8"))
    T = txt["lots"]

    def L(it, f, d=""):
        return T.get(it["key"], {}).get(f, d)

    by = {g: [x for x in lots if x["group"] == g] for g in ORDER}
    for g in by:
        by[g].sort(key=lambda x: -x["price"])

    S, n = [], 0

    def add(s):
        nonlocal n
        n += 1
        S.append(s.replace("__ID__", f"s{n:02d}"))

    # ---- обложка: на промо-кадре кроп допустим, это не фотография лота
    hphoto, hcred = COVER
    add(f"""<section class="slide dark on" id="__ID__" style="grid-template-columns:1.02fr 1fr">
  <div class="wrap" style="display:flex;flex-direction:column;justify-content:space-between;padding:62px 58px">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:170px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97">
    <div>
      <div class="kick d" style="margin-bottom:22px">Частное собрание · футбол</div>
      <h1 class="serif" style="font-weight:300;font-size:82px;line-height:1;color:var(--ivory)">Музей<br>футбола</h1>
      <p style="font:300 17px/1.65 'Inter';color:#b8b2a6;margin-top:28px;max-width:44ch">{esc(txt['intro'])}</p>
    </div>
    <div class="kick" style="letter-spacing:.24em">{sum(len(by[g]) for g in ORDER)} предметов · июль 2026</div>
  </div>
  <div style="position:relative;height:720px;overflow:hidden">
    <img src="{hphoto}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 30%">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,var(--noir) 0%,rgba(11,11,12,.34) 20%,rgba(11,11,12,0) 52%)"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,11,12,.5) 0%,rgba(11,11,12,0) 26%)"></div>
    <span style="position:absolute;right:16px;bottom:12px;font:400 8.5px/1.3 'Inter';letter-spacing:.08em;color:rgba(245,241,232,.55)">{esc(hcred)}</span>
  </div>
</section>""")

    # ---- главы
    for gi, g in enumerate(ORDER, 1):
        items = by[g]
        if not items:
            continue
        sub = txt["chapters"].get(g, {}).get("sub", "")
        num = ["первый", "второй", "третий", "четвёртый", "пятый",
               "шестой", "седьмой", "восьмой", "девятый"][gi - 1]
        kick = f"Раздел&nbsp;{num} · {len(items)} предметов"

        if g in HERO:            # разделитель с настоящим кадром
            ph, cred, opos, side = HERO[g][:4]
            # где в кадре стоит герой, там затемнение держим плотным под текстом
            # и обрываем раньше, чтобы фигура не уходила в темноту
            extra = HERO[g][4] if len(HERO[g]) > 4 else 68
            subw = HERO[g][5] if len(HERO[g]) > 5 else 44
            deg = 90 if side == "left" else 270
            if isinstance(extra, str):
                grad = extra.replace("__DEG__", str(deg))
            else:
                grad = (f"linear-gradient({deg}deg,rgba(11,11,12,.93) 0%,"
                        f"rgba(11,11,12,.74) {round(extra * 0.5)}%,"
                        f"rgba(11,11,12,.2) {extra}%,rgba(11,11,12,.05) 100%)")
            box = ("align-items:flex-start;text-align:left" if side == "left"
                   else "align-items:flex-end;text-align:right")
            add(f"""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="position:relative">
    <img src="{ph}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:{opos}">
    <div style="position:absolute;inset:0;background:{grad}"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 60px;{box}">
      <div class="kick d" style="letter-spacing:.34em;margin-bottom:24px">{kick}</div>
      <h2 class="div-huge" style="font-size:74px">{esc(TITLE[g])}</h2>
      <div class="div-rule" style="margin:32px 0"></div>
      <p class="div-sub" style="max-width:{subw}ch">{esc(sub)}</p>
    </div>
    <span style="position:absolute;right:16px;bottom:12px;font:400 8.5px/1.3 'Inter';letter-spacing:.08em;color:rgba(245,241,232,.55)">{esc(cred)}</span>
  </div>
</section>""")
        else:                    # чистая типографика
            add(f"""<section class="slide dark" id="__ID__" style="place-content:center;justify-items:center;text-align:center">
  <div style="max-width:66ch;padding:0 60px;display:flex;flex-direction:column;align-items:center">
    <div class="kick d" style="letter-spacing:.34em;margin-bottom:26px">{kick}</div>
    <h2 class="div-huge" style="font-size:74px">{esc(TITLE[g])}</h2>
    <div class="div-rule" style="margin:34px 0"></div>
    <p class="div-sub" style="text-align:center">{esc(sub)}</p>
  </div>
</section>""")

        # по одному экспонату на слайд — основной формат; хвост главы парами
        # хвост главы уходит парами — одиночная карточка в парной вёрстке смотрится ошибкой
        nsolo = max(1, round(len(items) * 0.65))
        if (len(items) - nsolo) % 2:
            nsolo += 1
        solo, pairs = items[:nsolo], items[nsolo:]
        # лоты с длинным сюжетным текстом держим отдельным слайдом
        moved = [x for x in pairs if x["key"] in PIN_SOLO]
        if moved:
            pairs = [x for x in pairs if x["key"] not in PIN_SOLO]
            while len(pairs) % 2:                    # пару разбивать нельзя
                pairs.append(solo.pop())
            solo = solo + moved
            nsolo = len(solo)

        for j, it in enumerate(solo, 1):
            add(f"""<section class="slide white solo" id="__ID__">
  <div class="solo-ph"><img src="{photo(it)}" alt="{esc(it['title'])}"></div>
  <div class="solo-side">
    <div class="kick" style="margin-bottom:16px">{esc(TITLE[g])} · {j} из&nbsp;{len(items)}</div>
    <div class="solo-name">{esc(L(it,'name',it['title']))}</div>
    <div class="solo-text">{esc(L(it,'text'))}</div>
    <div class="solo-price">{rub(it['price'])}</div>
    {f'<div class="solo-cert">{esc(L(it,"cert"))}</div>' if L(it,'cert') else ''}
  </div>
</section>""")

        for i in range(0, len(pairs), 2):
            two = pairs[i:i + 2]
            cards = "".join(f"""
      <div class="dc">
        <div class="dc-ph"><img src="{photo(p2)}" alt="{esc(p2['title'])}"></div>
        <div class="dc-name">{esc(L(p2,'name',p2['title']))}</div>
        <div class="dc-text">{esc(L(p2,'text'))}</div>
        <div class="dc-price">{rub(p2['price'])}</div>
        {f'<div class="dc-cert">{esc(L(p2,"cert"))}</div>' if L(p2,'cert') else ''}
      </div>""" for p2 in two)
            add(f"""<section class="slide white duo2" id="__ID__">
  <div class="wrap" style="padding:28px 72px 0;display:flex;justify-content:space-between;align-items:baseline">
    <h2 class="serif" style="font-weight:500;font-size:28px;color:var(--ink)">{esc(TITLE[g])}</h2>
    <span class="kick" style="letter-spacing:.2em">{nsolo + i + 1}–{nsolo + i + len(two)} из&nbsp;{len(items)}</span>
  </div>
  <div class="duo2-in">{cards}
  </div>
</section>""")

    # ---- лестница цен
    allx = sorted(lots, key=lambda x: -x["price"])
    pages = max(1, -(-len(allx) // 18))          # 18 строк — предел высоты слайда
    per = -(-len(allx) // pages)
    for pi in range(0, len(allx), per):
        part = allx[pi:pi + per]
        rows = "".join(f"""<div class="lad-row"><div class="lad-nm">{esc(T.get(x['key'],{}).get('name',x['title']))}</div>"""
                       f"""<div class="lad-pr">{rub(x['price'])}</div></div>""" for x in part)
        head = f"{len(allx)} предметов" if pi == 0 else "Продолжение"
        add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:auto 1fr">
  <div class="wrap" style="padding:40px 66px 0">
    <div class="kick d" style="margin-bottom:12px">Подборка целиком</div>
    <h2 class="serif" style="font-weight:300;font-size:44px;line-height:1;color:var(--ivory)">{head}</h2>
  </div>
  <div class="wrap" style="padding:18px 66px 30px"><div class="lad">{rows}</div></div>
</section>""")

    # ---- финал
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
<title>Stargift · Музей футбола</title>
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
    open(f"{R}/deck_museum.html", "w", encoding="utf-8").write(doc)
    print(f"deck_museum.html: {n} слайдов, {len(lots)} лотов")


if __name__ == "__main__":
    main()
