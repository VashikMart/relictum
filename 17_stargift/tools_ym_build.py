#!/usr/bin/env python3
"""«Мбаппе и Ямаль» — клиентская презентация 1280×720, 26 лотов.

    python3 tools_ym_build.py                # → deck_ym.html

Все фото лотов обработаны (nano banana, белая студия, без сертификатов и плашек).
Турнирные кадры — Wikimedia. Фото лотов не кропаются; cover — только промо-кадры.
"""
import html, os

R = os.path.dirname(os.path.abspath(__file__))


def esc(s):
    return html.escape(s or "", quote=False)


def rub(n):
    return f"{n:,}".replace(",", " ") + "&nbsp;₽"


C = "img_ym"          # clean_<key>.jpg — обработанные; src/<key>.jpg — исходники

# ---------------------------------------------------------------- лоты
LOTS = {
 # -------- Ямаль
 "yj_spain": dict(price=380_000, cert="Beckett",
    name="Ламин Ямаль — гостевая футболка сборной Испании Евро-2024 с автографом",
    text=("Гостевая футболка сборной Испании турнира Евро-2024 — с автографом. "
          "Тот чемпионат Ямаль закончил чемпионом Европы в семнадцать лет: самый "
          "молодой игрок и самый молодой автор гола в истории турнира, лучший "
          "молодой игрок Евро. Золотистая выездная форма с патчами турнира — "
          "форма чемпионского лета Испании.")),
 "yj_wc26a": dict(price=380_000, cert="Beckett",
    name="Ламин Ямаль — домашняя футболка сборной Испании ЧМ-2026 с автографом",
    text=("Домашняя футболка сборной Испании образца чемпионата мира 2026 года — "
          "с автографом. Красная с золотыми полосами и патчами турнира. Испания "
          "едет на чемпионат мира действующим чемпионом Европы, и Ямаль — "
          "первое имя этой команды.")),
 "yj_wc26b": dict(price=380_000, cert="Beckett",
    name="Ламин Ямаль — футболка сборной Испании ЧМ-2026 с автографом",
    text=("Футболка сборной Испании образца чемпионата мира 2026 года — "
          "с автографом. Второй экземпляр домашней формы турнира: красная "
          "с тёмно-синими рукавами, номер 19 на спине.")),
 "yj_barca26": dict(price=360_000, cert="Beckett",
    name="Ламин Ямаль — домашняя футболка «Барселоны» 2025/26 с автографом, № 10",
    text=("Домашняя футболка «Барселоны» сезона 2025/26 — с автографом. Летом "
          "2025 года Ямаль получил десятый номер клуба — номер Месси, Роналдиньо "
          "и Марадоны. Первая майка «Барсы» с надписью LAMINE YAMAL и десяткой "
          "на спине — вещь, фиксирующая смену эпох в клубе.")),
 "yj_away25": dict(price=360_000, cert="Beckett",
    name="Ламин Ямаль — гостевая футболка «Барселоны» 2024/25 с автографом",
    text=("Гостевая футболка «Барселоны» сезона 2024/25 — с автографом. Чёрная "
          "выездная форма сезона, в котором «Барса» взяла чемпионат, Кубок "
          "и Суперкубок Испании, а Ямаль стал обладателем Trophée Kopa — приза "
          "лучшему молодому футболисту мира.")),
 "yj_barca": dict(price=380_000, cert="Beckett",
    name="Ламин Ямаль — футболка «Барселоны» с автографом",
    text=("Футболка «Барселоны» — с автографом Ламина Ямаля. Тёмная форма клуба, "
          "в котором он прошёл путь от дебюта в пятнадцать лет до статуса "
          "первой звезды: воспитанник «Ла Масии», самый молодой автор гола "
          "в истории Ла Лиги на момент дебюта.")),
 "yboot": dict(price=360_000, cert="",
    name="Ламин Ямаль — бутса adidas F50 с автографом",
    text=("Бутса adidas F50 League Laceless — с автографом. Модель линейки, "
          "в которой Ямаль играет за клуб и сборную. Подпись поставлена на "
          "закрытой сессии — рядом кадр самого подписания: маркер в руке, "
          "бутса на колене.")),
 "yph_close": dict(price=250_000, cert="Beckett",
    name="Ламин Ямаль — фотография «Барселона» крупным планом с автографом",
    text=("Фотография 28×36 см с автографом: Ямаль в клубной форме ведёт мяч. "
          "Крупный план эпохи, когда весь футбол начал следить за семнадцатилетним.")),
 "yph_barca": dict(price=240_000, cert="Beckett",
    name="Ламин Ямаль — фотография «Барселона» с автографом",
    text=("Фотография 28×36 см с автографом: Ямаль празднует гол за «Барселону» "
          "у ворот соперника, руки раскинуты — фирменный жест.")),
 "yph_sp6": dict(price=240_000, cert="Beckett",
    name="Ламин Ямаль — фотография сборной Испании с автографом (Евро-2024)",
    text=("Фотография 28×36 см с автографом: празднование на Евро-2024. "
          "Тем летом Ямаль сделал четыре результативные передачи — "
          "рекорд турнира для игрока до двадцати лет.")),
 "yph_sp5": dict(price=240_000, cert="Beckett",
    name="Ламин Ямаль — фотография гола сборной Испании с автографом",
    text=("Фотография 28×36 см с автографом: мяч влетает в сетку. Кадр момента, "
          "ради которого стадионы встают.")),
 "yph_sp3": dict(price=240_000, cert="Beckett",
    name="Ламин Ямаль — фотография матча Испания — Англия с автографом",
    text=("Фотография 28×36 см с автографом: эпизод финала Евро-2024 против "
          "Англии — матча, который сделал Испанию четырёхкратным чемпионом Европы.")),
 "yph_sp2": dict(price=240_000, cert="Beckett",
    name="Ламин Ямаль — фотография сборной Испании с автографом (дождь)",
    text=("Фотография 28×36 см с автографом: Ямаль указывает на партнёра после "
          "гола под дождём. Живой кадр — брызги, улыбка, красная форма Испании.")),
 # -------- Мбаппе
 "mph_j1": dict(price=300_000, cert="JSA",
    name="Килиан Мбаппе — фотография с Кубком мира с автографом (Москва, 2018)",
    text=("Фотография 20×25 см с автографом: Мбаппе целует Кубок мира в Лужниках. "
          "15 июля 2018 года, Москва: гол в финале в девятнадцать лет — второй "
          "тинейджер в истории после Пеле, забивавший в финале чемпионата мира, "
          "и лучший молодой игрок того турнира.")),
 "mph_j4": dict(price=300_000, cert="JSA",
    name="Килиан Мбаппе — фотография с Кубком мира с автографом (крупный план)",
    text=("Фотография 20×25 см с автографом: крупный план с золотым кубком. "
          "Трофей, поднятый в Москве, — главный кадр карьеры Мбаппе.")),
 "mph_j5": dict(price=300_000, cert="JSA",
    name="Килиан Мбаппе — фотография с Кубком мира с автографом (конфетти)",
    text=("Фотография 20×25 см с автографом: Мбаппе с кубком на газоне Лужников "
          "под золотым конфетти. Финальная точка чемпионата мира в России.")),
 "mph_j2": dict(price=300_000, cert="JSA",
    name="Килиан Мбаппе — фотография «Реал Мадрид» с автографом",
    text=("Фотография 20×25 см с автографом: празднование гола на «Сантьяго "
          "Бернабеу». В дебютном сезоне за «Реал» Мбаппе забил 44 гола "
          "и получил «Золотую бутсу» лучшего бомбардира Европы.")),
 "mph_j3": dict(price=300_000, cert="JSA",
    name="Килиан Мбаппе — фотография «Реал Мадрид» № 9 с автографом",
    text=("Фотография 20×25 см с автографом: Мбаппе в белой форме «Реала» "
          "с девятым номером — номером первого мадридского сезона.")),
 "mph_monaco": dict(price=300_000, cert="PSA/DNA",
    name="Килиан Мбаппе — арт-принт «Монако» с автографом",
    text=("Арт-принт в цветах «Монако» — с автографом красным маркером. "
          "Оммаж клубу, где всё началось: в семнадцать Мбаппе ворвался "
          "в основу, а в 2017-м взял с «Монако» чемпионство Лиги 1, "
          "обыграв ПСЖ ещё до перехода туда.")),
 "mj_rm1": dict(price=480_000, cert="PSA/DNA",
    name="Килиан Мбаппе — футболка «Реал Мадрид» с автографом, № 9",
    text=("Домашняя футболка «Реал Мадрида» с девятым номером — с автографом. "
          "Белая форма первого мадридского сезона: 44 гола, «Золотая бутса» "
          "и статус наследника великой девятки Роналдо.")),
 "mj_rm2": dict(price=480_000, cert="PSA/DNA",
    name="Килиан Мбаппе — футболка «Реал Мадрид» с автографом",
    text=("Футболка «Реал Мадрида» — с автографом Мбаппе. Второй экземпляр "
          "белой домашней формы, подпись чёрным маркером поверх номера.")),
 "mj_fr22": dict(price=500_000, cert="",
    name="Килиан Мбаппе — гостевая футболка сборной Франции ЧМ-2022 с автографом",
    text=("Гостевая футболка сборной Франции чемпионата мира 2022 года — "
          "с автографом. Белая форма с рисунком туаль-де-жуи, в которой Франция "
          "дошла до финала Катара. Тот турнир Мбаппе закончил лучшим "
          "бомбардиром — восемь голов, включая хет-трик в финале: первый "
          "хет-трик в финале чемпионата мира с 1966 года.")),
 "mj_fr26": dict(price=500_000, cert="Beckett",
    name="Килиан Мбаппе — футболка сборной Франции 2026 с автографом",
    text=("Футболка сборной Франции образца 2026 года — с автографом. Синяя "
          "форма с десятым номером, в которой капитан сборной поведёт Францию "
          "на чемпионат мира 2026 года за третьей звездой.")),
 "mball": dict(price=500_000, cert="Beckett",
    name="Килиан Мбаппе — мяч Nike сборной Франции с автографом",
    text=("Мяч Nike в тёмно-синем оформлении сборной Франции — с автографом "
          "серебряным маркером. Петух федерации, надпись FRANCE и размашистая "
          "подпись капитана сборной на одной панели предмета.")),
 "mcard": dict(price=350_000, cert="PSA",
    name="Килиан Мбаппе — карточка ПСЖ 2019/20 с автографом, капсула PSA",
    text=("Коллекционная карточка ПСЖ сезона 2019/20 с автографом на карточке — "
          "в защитной капсуле PSA. Подписанные карточки Мбаппе той эпохи — "
          "растущий сегмент рынка: тираж мал, спрос мировой.")),
 "mmessi": dict(price=900_000, cert="",
    name="Лионель Месси и Килиан Мбаппе — футболка ПСЖ с двумя автографами",
    text=("Выездная футболка ПСЖ сезона 2022/23 — с автографами Месси и Мбаппе. "
          "Два года они выходили на поле вместе, а в финале ЧМ-2022 оказались "
          "по разные стороны величайшего финала в истории: 3:3, хет-трик Мбаппе "
          "против двух голов Месси. Одна майка с двумя этими подписями — "
          "предмет, в котором сходится целая эпоха.")),
}

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

/* соло с одним или двумя фото слева */
.solo{grid-template-columns:1.28fr 1fr}
.ph2{display:grid;gap:18px;padding:44px 22px 44px 52px;background:#fff;align-items:center}
.ph2 .cell{height:100%;display:flex;align-items:center;justify-content:center;overflow:hidden}
.ph2 img{max-width:100%;max-height:100%;object-fit:contain}
.solo-side{display:flex;flex-direction:column;justify-content:center;padding:50px 56px 50px 22px}
.solo-name{font-family:'Cormorant Garamond';font-weight:500;font-size:29px;line-height:1.14;color:var(--ink)}
.solo-text{font:300 15px/1.62 'Inter';color:#4a4a4a;margin-top:14px}
.solo-price{font-family:'Cormorant Garamond';font-weight:500;font-size:29px;color:var(--gold);margin-top:18px}
.solo-cert{font:400 10px/1 'Inter';letter-spacing:.22em;text-transform:uppercase;color:var(--cert);margin-top:10px}

/* дуэт: два лота на слайде */
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
  padding:6px 0;border-bottom:1px solid rgba(169,133,69,.2)}
.lad-nm{font:300 13.5px/1.3 'Inter';color:#d5cfc3}
.lad-pr{font-family:'Cormorant Garamond';font-weight:500;font-size:18px;color:var(--gold2);white-space:nowrap}
"""


def main():
    S, n = [], 0

    def add(s):
        nonlocal n
        n += 1
        S.append(s.replace("__ID__", f"s{n:02d}"))

    def img(key, suffix=None):
        # clean_<key>_<suffix>.jpg приоритетнее; иначе src
        cand = f"{C}/clean_{key}.jpg" if suffix is None else f"{C}/clean_{key}_{suffix}.jpg"
        if os.path.exists(os.path.join(R, cand)):
            return cand
        return f"{C}/src/{key}.jpg" if suffix is None else f"{C}/src/{key}_{suffix}.jpg"

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

    def hero_div(photo, cred, kick, title, sub, pos="50% 30%"):
        add(f"""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="position:relative">
    <img src="{photo}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:{pos}">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,12,.94) 0%,rgba(11,11,12,.78) 32%,rgba(11,11,12,.22) 62%,rgba(11,11,12,.05) 100%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 60px">
      <div class="kick d" style="letter-spacing:.34em;margin-bottom:24px">{kick}</div>
      <h2 class="div-huge" style="font-size:70px">{title}</h2>
      <div class="div-rule" style="margin:32px 0"></div>
      <p class="div-sub" style="max-width:40ch">{sub}</p>
    </div>
    <span class="credit">{cred}</span>
  </div>
</section>""")

    # ---------- обложка
    add("""<section class="slide dark on" id="__ID__" style="grid-template-columns:1fr .62fr .62fr">
  <div style="display:flex;flex-direction:column;justify-content:space-between;padding:58px 20px 58px 54px">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:150px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start">
    <div>
      <div class="kick d" style="margin-bottom:20px">Частное собрание · Футбол</div>
      <h1 class="serif" style="font-weight:300;font-size:66px;line-height:1.04;color:var(--ivory)">Мбаппе<br>и Ямаль</h1>
      <p style="font:300 15.5px/1.62 'Inter';color:#b8b2a6;margin-top:22px;max-width:36ch">Двадцать шесть предметов двух главных имён современного футбола:
      майки, мячи, бутса и фотографии — каждая вещь с автографом.</p>
    </div>
    <div class="kick" style="letter-spacing:.24em">26 предметов · июль 2026</div>
  </div>
  <div style="position:relative;height:720px;overflow:hidden">
    <img src="img_ym/hero/mbappe.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:62% 20%">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,12,.65) 0%,rgba(11,11,12,0) 40%)"></div>
    <span class="credit">Фото: Balkan Photos · Wikimedia Commons · CC BY 2.0</span>
  </div>
  <div style="position:relative;height:720px;overflow:hidden">
    <img src="img_ym/hero/yamal.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:44% 20%">
    <div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,11,12,.4) 0%,rgba(11,11,12,0) 22%)"></div>
    <span class="credit">Фото: Berlination · Wikimedia Commons · CC BY-SA 4.0</span>
  </div>
</section>""")

    # ---------- глава I · Ямаль
    hero_div("img_ym/hero/barca_campeones.jpg",
             "Фото: Junta de Andalucía · Wikimedia Commons · CC BY-SA 2.0",
             "Раздел первый · 13 предметов", "Ламин Ямаль",
             "Чемпион Европы в семнадцать, десятый номер «Барселоны», "
             "лучший молодой футболист мира. Рынок его вещей рождается прямо сейчас.",
             "50% 42%")

    solo("yj_spain", [img("yj_spain", "00")], "Ламин Ямаль · 1 из 13")
    add(f"""<section class="slide white duo2" id="__ID__">
  <div style="padding:26px 72px 0;display:flex;justify-content:space-between;align-items:baseline">
    <h2 class="serif" style="font-weight:500;font-size:27px;color:var(--ink)">Золото Евро-2024 · форма целиком</h2>
    <span class="kick" style="letter-spacing:.2em">Ламин Ямаль · 1 из 13</span>
  </div>
  <div class="duo2-in" style="grid-template-columns:1fr 1fr">
    <div class="dc"><div class="dc-ph" style="height:470px"><img src="{img('yj_spain', '01')}" alt=""></div>
      <div class="dc-text" style="margin-top:12px">Лицевая сторона: эмблема федерации и патч чемпионата Европы 2024 года.</div></div>
    <div class="dc"><div class="dc-ph" style="height:470px"><img src="{img('yj_spain', '03')}" alt=""></div>
      <div class="dc-text" style="margin-top:12px">Спина: LAMINE YAMAL, № 19 — номер, под которым он стал чемпионом Европы.</div></div>
  </div>
</section>""")

    solo("yj_wc26a", [img("yj_wc26a", "01"), img("yj_wc26a", "00")], "Ламин Ямаль · 2 из 13")
    solo("yj_wc26b", [img("yj_wc26b", "00"), img("yj_wc26b", "01")], "Ламин Ямаль · 3 из 13")
    solo("yj_barca26", [img("yj_barca26", "00"), img("yj_barca26", "01")], "Ламин Ямаль · 4 из 13")
    solo("yj_away25", [img("yj_away25", "00"), img("yj_away25", "01")], "Ламин Ямаль · 5 из 13")
    solo("yj_barca", [img("yj_barca", "01"), img("yj_barca", "00")], "Ламин Ямаль · 6 из 13")
    solo("yboot", [img("yboot", "00"), f"{C}/src/yboot_01.jpg"], "Ламин Ямаль · 7 из 13")

    duo("yph_close", "yph_barca", "Фотографии с автографом", "Ламин Ямаль · 8–9 из 13")
    duo("yph_sp6", "yph_sp2", "Фотографии с автографом · Евро-2024", "Ламин Ямаль · 10–11 из 13")
    duo("yph_sp5", "yph_sp3", "Фотографии с автографом · Евро-2024", "Ламин Ямаль · 12–13 из 13")

    # ---------- глава II · Мбаппе
    hero_div("img_ym/hero/wc18.jpg",
             "Фото: Пресс-служба Президента России · Wikimedia Commons · CC BY 4.0",
             "Раздел второй · 13 предметов", "Килиан Мбаппе",
             "Чемпион мира в девятнадцать, капитан Франции, первая девятка "
             "«Реал Мадрида». Кубок мира он поднял в Москве.", "50% 26%")

    solo("mph_j1", [img("mph_j1", "00")], "Килиан Мбаппе · 1 из 13")
    add("""<section class="slide dark" id="__ID__" style="place-content:center;justify-items:center;text-align:center">
  <div style="max-width:64ch;padding:0 60px;display:flex;flex-direction:column;align-items:center">
    <div class="kick d" style="letter-spacing:.3em;margin-bottom:26px">Москва · Лужники · 15 июля 2018 года</div>
    <h2 class="serif" style="font-weight:300;font-size:50px;line-height:1.14;color:var(--ivory);max-width:24ch">Кубок мира, поднятый в Москве</h2>
    <div class="div-rule" style="margin:30px 0"></div>
    <p class="div-sub" style="text-align:center;max-width:52ch">Гол в финале в девятнадцать лет — до Мбаппе такое удавалось
    только Пеле. Тот чемпионат мира прошёл в России, и кадры с золотым кубком в Лужниках
    сделали его мировой звездой за один вечер. Три фотографии этой серии — память
    о турнире, который случился дома.</p>
  </div>
</section>""")
    duo("mph_j4", "mph_j5", "Фотографии с Кубком мира · Москва-2018", "Килиан Мбаппе · 2–3 из 13")
    duo("mph_j2", "mph_j3", "Фотографии «Реал Мадрид»", "Килиан Мбаппе · 4–5 из 13")
    solo("mph_monaco", [img("mph_monaco", "01")], "Килиан Мбаппе · 6 из 13")
    solo("mj_fr22", [img("mj_fr22", "00"), img("mj_fr22", "01")], "Килиан Мбаппе · 7 из 13")
    solo("mj_fr26", [img("mj_fr26", "03"), img("mj_fr26", "00")], "Килиан Мбаппе · 8 из 13")
    solo("mj_rm1", [img("mj_rm1", "05"), img("mj_rm1", "00")], "Килиан Мбаппе · 9 из 13")
    solo("mj_rm2", [img("mj_rm2", "00")], "Килиан Мбаппе · 10 из 13")
    solo("mball", [img("mball", "00"), img("mball", "05")], "Килиан Мбаппе · 11 из 13")
    solo("mcard", [img("mcard", "00")], "Килиан Мбаппе · 12 из 13")

    solo("mmessi", [img("mmessi", "00")], "Килиан Мбаппе · 13 из 13")
    add("""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="position:relative">
    <img src="img_ym/hero/psg_trio.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 30%">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,12,.92) 0%,rgba(11,11,12,.72) 34%,rgba(11,11,12,.16) 64%,rgba(11,11,12,.04) 100%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 60px">
      <div class="kick d" style="letter-spacing:.3em;margin-bottom:24px">Париж · 2021–2023</div>
      <h2 class="div-huge" style="font-size:54px;max-width:16ch">Два имени на одной майке</h2>
      <div class="div-rule" style="margin:28px 0"></div>
      <p class="div-sub" style="max-width:38ch">Величайший игрок прошлой эпохи и первый игрок нынешней
      два сезона выходили на поле вместе. Майка ПСЖ с подписями обоих — редкий предмет,
      где эти карьеры пересекаются буквально.</p>
    </div>
    <span class="credit">Фото: Liondartois · Wikimedia Commons · CC BY-SA 4.0</span>
  </div>
</section>""")

    # ---------- лестница цен
    order = sorted(LOTS, key=lambda k: -LOTS[k]["price"])
    half = (len(order) + 1) // 2
    for pi, part in enumerate((order[:half], order[half:])):
        rows = "".join(
            f'<div class="lad-row"><div class="lad-nm">{esc(LOTS[k]["name"])}</div>'
            f'<div class="lad-pr">{rub(LOTS[k]["price"])}</div></div>' for k in part)
        head = "26 предметов" if pi == 0 else "Продолжение"
        add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:auto 1fr">
  <div style="padding:40px 66px 0">
    <div class="kick d" style="margin-bottom:12px">Подборка целиком</div>
    <h2 class="serif" style="font-weight:300;font-size:42px;line-height:1;color:var(--ivory)">{head}</h2>
  </div>
  <div style="padding:18px 66px 32px"><div class="lad">{rows}</div></div>
</section>""")

    # ---------- финал
    add("""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="padding:76px 72px 0;display:flex;flex-direction:column;justify-content:center">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:146px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start">
    <h2 class="serif" style="font-weight:300;font-size:44px;line-height:1.16;color:var(--ivory);margin-top:38px;max-width:32ch">Мбаппе и Ямаль. Настоящее и будущее футбола — в одном собрании.</h2>
  </div>
  <div style="padding:26px 72px 40px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.24em;color:var(--gold2)">stargift.ru</span>
  </div>
</section>""")

    doc = f"""<meta charset="utf-8">
<title>Stargift · Мбаппе и Ямаль</title>
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
    open(f"{R}/deck_ym.html", "w", encoding="utf-8").write(doc)
    print(f"deck_ym.html: {n} слайдов, {len(LOTS)} лотов")


if __name__ == "__main__":
    main()
