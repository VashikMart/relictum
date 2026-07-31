#!/usr/bin/env python3
"""«Гольф · клюшки легенд и флаги Мастерса» — презентация 1280×720.

    python3 tools_golf_build.py      # → deck_golf.html
"""
import html, os

R = os.path.dirname(os.path.abspath(__file__))
C = "img_golf"


def esc(s):
    return html.escape(s or "", quote=False)


def rub(n):
    return f"{n:,}".replace(",", " ") + "&nbsp;₽"


def img(name, half=False):
    """Кадр под половину слайда, обработанный или исходник — в этом порядке."""
    base = os.path.basename(name)
    if half:
        h = f"{C}/halfslide/{base}.jpg"
        if os.path.exists(os.path.join(R, h)):
            return h
    for p in (f"{C}/{name}.jpg", f"{C}/src/{name}.jpg"):
        if os.path.exists(os.path.join(R, p)):
            return p
    return f"{C}/src/{name}.jpg"


LOTS = {
 "jones": dict(price=1_050_000, name="Бобби Джонс — драйвер Jack White из его личных клюшек и подписанная фотография"),
 "picard": dict(price=800_000, name="Генри Пикард — комплект персональных айронов и подписанная фотография"),
 "palmer": dict(price=400_000, name="Арнольд Палмер — айрон The Standard forged 2 с автографом"),
 "flag22": dict(price=900_000, name="Флаг Мастерса 2022 года с автографами пятнадцати чемпионов турнира"),
 "flag16a": dict(price=900_000, name="Флаг Мастерса 2016 года с автографами тринадцати чемпионов турнира"),
 "flag16b": dict(price=900_000, name="Флаг Мастерса 2016 года с автографами двенадцати чемпионов турнира"),
}
ORDER = ["jones", "flag22", "flag16a", "flag16b", "picard", "palmer"]

CSS = """
:root{--noir:#0B0B0C;--gold:#A98545;--gold2:#C9A96A;--ivory:#F5F1E8;
      --ink:#1A1A1A;--green:#1E3B2C}
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
.div-rule{height:1px;width:70px;background:rgba(169,133,69,.55)}
.div-huge{font-family:'Cormorant Garamond';font-weight:300;line-height:1;color:var(--ivory)}
.div-sub{font:300 18px/1.65 'Inter';color:#c9c3b7}

/* слайд лота: фото ровно на половину слайда */
.solo{grid-template-columns:1fr 1fr}
.ph2{height:720px;overflow:hidden;background:#fff}
.ph2 img{width:100%;height:100%;object-fit:cover;object-position:50% 50%}
.solo-side{display:flex;flex-direction:column;justify-content:center;padding:50px 56px 50px 26px}
.solo-name{font-family:'Cormorant Garamond';font-weight:500;font-size:28px;line-height:1.15;color:var(--ink)}
.solo-text{font:300 15px/1.64 'Inter';color:#4a4a4a;margin-top:14px}
.solo-price{font-family:'Cormorant Garamond';font-weight:500;font-size:30px;color:var(--gold);margin-top:18px}
.solo-spec{font:400 10px/1.5 'Inter';letter-spacing:.18em;text-transform:uppercase;color:#9a958c;margin-top:10px}

/* галерея ракурсов */
.gal{grid-template-rows:auto 1fr auto}
.gal-head{display:flex;justify-content:space-between;align-items:baseline;padding:30px 60px 0}
.gal-name{font-family:'Cormorant Garamond';font-weight:500;font-size:26px;color:var(--ink)}
.gal-grid{display:grid;gap:16px;padding:20px 60px 0}
.gal-cell{background:#F7F5F1;display:flex;align-items:center;justify-content:center;overflow:hidden}
.gal-cell img{max-width:100%;max-height:100%;object-fit:contain}
.gal-foot{padding:18px 60px 30px;font:300 14px/1.6 'Inter';color:#4a4a4a;max-width:104ch}

/* разворот «предмет + документ» */
.duo{grid-template-rows:auto 1fr auto}
.duo-in{display:grid;grid-template-columns:1fr 1fr;gap:38px;padding:18px 62px 0;align-items:center}
.duo-cell{height:430px;display:flex;align-items:center;justify-content:center;background:#F7F5F1;overflow:hidden}
.duo-cell img{max-width:100%;max-height:100%;object-fit:contain}
.duo-cap{font:400 10px/1.5 'Inter';letter-spacing:.16em;text-transform:uppercase;color:#9a958c;margin-top:9px;text-align:center}

.lad{display:flex;flex-direction:column;height:100%;justify-content:space-between}
.lad-row{display:grid;grid-template-columns:1fr auto;gap:30px;align-items:baseline;
  padding:11px 0;border-bottom:1px solid rgba(169,133,69,.2)}
.lad-nm{font:300 14.5px/1.4 'Inter';color:#d5cfc3}
.lad-pr{font-family:'Cormorant Garamond';font-weight:500;font-size:21px;color:var(--gold2);white-space:nowrap}
"""


def main():
    S, n = [], 0

    def add(s):
        nonlocal n
        n += 1
        S.append(s.replace("__ID__", f"s{n:02d}"))

    def solo(key, photo, kick, text, spec=""):
        it = LOTS[key]
        sp = f'<div class="solo-spec">{esc(spec)}</div>' if spec else ""
        add(f"""<section class="slide white solo" id="__ID__">
  <div class="ph2"><img src="{photo}" alt=""></div>
  <div class="solo-side">
    <div class="kick" style="margin-bottom:14px">{kick}</div>
    <div class="solo-name">{esc(it['name'])}</div>
    <div class="solo-text">{esc(text)}</div>
    <div class="solo-price">{rub(it['price'])}</div>
    {sp}
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

    def duo(title, kick, a, acap, b, bcap, foot):
        add(f"""<section class="slide white duo" id="__ID__">
  <div class="gal-head"><div class="gal-name">{esc(title)}</div>
    <span class="kick">{esc(kick)}</span></div>
  <div class="duo-in">
    <div><div class="duo-cell"><img src="{a}" alt=""></div>
      <div class="duo-cap">{esc(acap)}</div></div>
    <div><div class="duo-cell"><img src="{b}" alt=""></div>
      <div class="duo-cap">{esc(bcap)}</div></div>
  </div>
  <div class="gal-foot">{esc(foot)}</div>
</section>""")

    def divider(kick, huge, sub, photo, objpos="50% 50%"):
        add(f"""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="position:relative">
    <img src="{photo}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:{objpos}">
    <div style="position:absolute;inset:0;background:linear-gradient(270deg,rgba(11,11,12,.94) 0%,rgba(11,11,12,.76) 36%,rgba(11,11,12,.2) 68%,rgba(11,11,12,.05) 100%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:flex-end;text-align:right;padding:0 62px">
      <div class="kick d" style="letter-spacing:.3em;margin-bottom:22px">{esc(kick)}</div>
      <h2 class="div-huge" style="font-size:50px;max-width:17ch">{huge}</h2>
      <div class="div-rule" style="margin:26px 0"></div>
      <p class="div-sub" style="max-width:40ch">{esc(sub)}</p>
    </div>
  </div>
</section>""")

    # ---------- обложка
    add(f"""<section class="slide dark on" id="__ID__" style="grid-template-columns:1fr 1.04fr">
  <div style="display:flex;flex-direction:column;justify-content:space-between;padding:58px 52px">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:142px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start">
    <div>
      <div class="kick d" style="margin-bottom:22px">Частное собрание · Гольф</div>
      <h1 class="serif" style="font-weight:300;font-size:64px;line-height:1.04;color:var(--ivory)">Клюшки легенд<br>и флаги Мастерса</h1>
      <p style="font:300 16px/1.64 'Inter';color:#b8b2a6;margin-top:22px;max-width:44ch">Шесть предметов: три клюшки, которыми играли
      Бобби Джонс, Генри Пикард и Арнольд Палмер, и три флага Огасты
      с автографами чемпионов турнира.</p>
    </div>
    <div class="kick" style="letter-spacing:.24em">6 предметов · июль 2026</div>
  </div>
  <div style="position:relative;height:720px;overflow:hidden;background:#0B0B0C">
    <img src="{img('framed_flag22')}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 50%">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,var(--noir) 0%,rgba(11,11,12,.3) 22%,rgba(11,11,12,0) 52%)"></div>
  </div>
</section>""")

    # ---------- раздел: клюшки
    divider("Клюшки легенд", "Инструмент, которым<br>выигрывали",
            "Клюшка отличается от любого другого экспоната одним: ею работали. "
            "Следы на подошве и потёртая рукоять — это отпечаток самой игры, "
            "а не хранения.", img("clean_jones_00"), "50% 45%")

    # ---------- Бобби Джонс, 3 слайда
    solo("jones", img("clean_jones_00", half=True), "Клюшки · 1 из 6",
         "Драйвер работы Джека Уайта из Гуллана — мастера, выигравшего Открытый "
         "чемпионат Британии 1904 года. Джонс перепробовал шестнадцать драйверов "
         "этой мастерской, прежде чем выбрать один для сезона 1930 года, когда взял "
         "все четыре главных турнира подряд. Головка из хурмы, латунная лента с "
         "клеймом мастера, древко из гикори.",
         "Драйвер · хурма и гикори · Jack White, Gullane")

    duo("Бобби Джонс · провенанс", "Клюшки · 1 из 6",
        img("src/jones_06"), "Справочник клюшек Джонса · глава «The Jack White Driver»",
        img("src/jones_10"), "Письмо Джонса, 25 января 1934 года, подписано «Bob»",
        "К клюшке приложены страницы каталога клюшек Джонса с отдельной главой об этой модели "
        "и машинописное письмо 1934 года на его бланке — Джонс отвечает Фрэнку Сэмпсону "
        "о материале для мартовского номера The American Golfer и подписывает его коротким «Bob».")

    solo("jones", img("framed_jones", half=True), "Клюшки · 1 из 6",
         "Оформление дома: глубокий короб с зелёным замшевым полем, клюшка на кожаных "
         "держателях по диагонали, рядом — та самая подписанная фотография. Латунная "
         "табличка с именем. Формат рассчитан на стену кабинета: предмет читается "
         "с трёх метров, фотография объясняет его вблизи.",
         "Оформление · короб 120×60 см · зелёная замша")

    # ---------- флаги: раздел
    divider("Флаги чемпионов", "Огаста, второе<br>воскресенье апреля",
            "Флаг с лунки Огасты — единственный предмет Мастерса, который турнир "
            "выпускает официально. Подписи собираются годами: чемпионы приезжают "
            "на ужин победителей каждую весну.", img("framed_flag22"), "50% 50%")

    solo("flag22", img("flag22_00", half=True), "Флаги · 2 из 6",
         "Пятнадцать чемпионов Мастерса на одном полотне — среди них Джек Никлаус, "
         "шестикратный победитель турнира, и Фил Микельсон. Собрать столько подписей "
         "можно только на ужине победителей: посторонних там не бывает.",
         "Флаг лунки · 51×38 см · сезон 2022")

    solo("flag22", img("framed_flag22", half=True), "Флаги · 2 из 6",
         "Оформление дома: тёмная рама, зелёное замшевое паспарту цвета пиджака "
         "победителя, тонкая золотая линия и латунная табличка. Жёлтый флаг на "
         "зелёном — сочетание, которое узнают без единой подписи.",
         "Оформление · рама 70×55 см · зелёная замша")

    solo("flag16a", img("flag16a_00", half=True), "Флаги · 3 из 6",
         "Тринадцать чемпионов, сезон 2016 года. Тот же ужин победителей, другой год "
         "и другой состав подписей — среди них Джек Никлаус и Том Уотсон, "
         "двукратный чемпион Мастерса и пятикратный победитель Открытого чемпионата Британии.",
         "Флаг лунки · 51×38 см · сезон 2016")

    solo("flag16b", img("flag16b_00", half=True), "Флаги · 4 из 6",
         "Двенадцать чемпионов, тот же сезон 2016 года. Два флага одного года никогда "
         "не совпадают по составу: каждый собирался отдельно и в своём порядке. "
         "Пара из двух флагов 2016-го — редкий случай, когда можно показать это рядом.",
         "Флаг лунки · 51×38 см · сезон 2016")

    duo("Флаги Мастерса 2016 · два полотна", "Флаги · 3 и 4 из 6",
        img("flag16a_00"), "Тринадцать чемпионов",
        img("flag16b_00"), "Двенадцать чемпионов",
        "Оба флага выпущены к одному турниру, но собирались независимо: разное число подписей, "
        "разные автографы, разный порядок. Рядом это видно сразу — и именно поэтому пара "
        "работает сильнее, чем два одинаковых предмета.")

    # ---------- Пикард
    solo("picard", img("clean_picard_02", half=True), "Клюшки · 5 из 6",
         "Комплект персональных айронов Генри Пикарда — чемпиона Мастерса 1938 года "
         "и Чемпионата PGA 1939-го. Пикард известен не только титулами: именно он "
         "поставил свинг Бену Хогану и оплатил ему выход на тур, когда тот был на грани "
         "ухода из гольфа. Древки гикори, кованые головки, следы игры на подошвах. "
         "В кадре лота — портрет Пикарда и мяч с его росчерком.",
         "Комплект айронов · гикори и кованая сталь")

    duo("Генри Пикард · комплект", "Клюшки · 5 из 6",
        img("src/picard_00"), "Подписанная фотография Пикарда",
        img("src/picard_03"), "Древки комплекта",
        "К комплекту приложена подписанная фотография Пикарда — она и объясняет предмет: "
        "без портрета набор старых айронов остаётся набором старых айронов. "
        "Дом ставит их в один глубокий короб, фотографию — в отдельное окно рядом.")

    # ---------- Палмер
    solo("palmer", img("clean_palmer_02", half=True), "Клюшки · 6 из 6",
         "Айрон The Standard forged 2 с автографом Арнольда Палмера — человека, который "
         "сделал гольф телевизионным видом спорта. Подпись поставлена прямо по клюшке, "
         "поперёк бороздок: крупная, уверенная, ровно та, что знают по его автограф-сессиям.",
         "Айрон · кованая сталь · автограф маркером")

    gallery("Арнольд Палмер · ракурсы", "Клюшки · 6 из 6",
            [img("src/palmer_00"), img("src/palmer_03"), img("src/palmer_05"),
             img("src/palmer_09"), img("src/palmer_10"), img("src/palmer_06")],
            3, 200,
            "Клюшка снята со всех сторон: подошва, обух с маркировкой модели, шафт и рукоять. "
            "Это самый доступный предмет подборки и самый понятный в подарок — "
            "узнаваемое имя, компактный формат, живая подпись на металле.")

    # ---------- как оформляем
    add(f"""<section class="slide dark" id="__ID__" style="grid-template-columns:1.1fr .9fr">
  <div style="height:720px;overflow:hidden"><img src="{img('framed_jones')}" alt="" style="width:100%;height:100%;object-fit:cover"></div>
  <div style="display:flex;flex-direction:column;justify-content:center;padding:56px 58px 56px 40px">
    <div class="kick d" style="margin-bottom:20px">Оформление</div>
    <h2 class="serif" style="font-weight:300;font-size:38px;line-height:1.14;color:var(--ivory);max-width:20ch">Зелёная замша и латунь</h2>
    <div class="div-rule" style="margin:24px 0"></div>
    <p style="font:300 15px/1.68 'Inter';color:#b8b2a6;max-width:38ch">Для гольфа дом берёт зелёное замшевое поле —
    цвет Огасты и пиджака победителя. Клюшка ложится в глубокий короб на кожаных держателях,
    флаг растягивается под стеклом на паспарту. К предмету всегда добавляется второй элемент:
    фотография героя или документ, чтобы экспонат читался без подписи.</p>
    <p style="font:300 13px/1.6 'Inter';color:#8e887c;margin-top:20px;max-width:38ch">Размеры и оттенок замши согласовываем
    под конкретную стену.</p>
  </div>
</section>""")

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
    add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:auto 1fr">
  <div style="padding:42px 64px 0">
    <div class="kick d" style="margin-bottom:12px">Подборка целиком</div>
    <h2 class="serif" style="font-weight:300;font-size:42px;line-height:1;color:var(--ivory)">6 предметов</h2>
  </div>
  <div style="padding:20px 64px 38px"><div class="lad">{rows}</div></div>
</section>""")

    # ---------- финал
    add("""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="padding:74px 66px 0;display:flex;flex-direction:column;justify-content:center">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:140px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start">
    <h2 class="serif" style="font-weight:300;font-size:44px;line-height:1.14;color:var(--ivory);margin-top:36px;max-width:30ch">Гольф. Три клюшки, три флага, сто лет игры.</h2>
  </div>
  <div style="padding:24px 66px 38px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.24em;color:var(--gold2)">stargift.ru</span>
  </div>
</section>""")

    doc = f"""<meta charset="utf-8">
<title>Stargift · Гольф</title>
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
    open(f"{R}/deck_golf.html", "w", encoding="utf-8").write(doc)
    print(f"deck_golf.html: {n} слайдов, {len(LOTS)} лотов")


if __name__ == "__main__":
    main()
