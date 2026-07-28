#!/usr/bin/env python3
"""«Тайгер Вудс» — клиентская презентация 1280×720, 8 лотов, по 1–3 слайда на лот.

    python3 tools_woods_build.py             # → deck_woods.html

Фото лотов из объявлений (img_woods/src), турнирные кадры — Wikimedia (img_woods/hero).
Фото лотов не кропаются (object-fit:contain); cover — только на промо-кадрах.
"""
import html, os

R = os.path.dirname(os.path.abspath(__file__))


def esc(s):
    return html.escape(s or "", quote=False)


def rub(n):
    return f"{n:,}".replace(",", " ") + "&nbsp;₽"


# ---------------------------------------------------------------- данные
LOTS = {
 "glove": dict(price=11_100_000,
    name="Тайгер Вудс — игровая перчатка Nike с автографом",
    text=("Игровая перчатка Nike с автографом. Тайгер Вудс — пятнадцатикратный "
          "победитель мейджоров, вернувший гольфу статус большого зрелища. "
          "Перчатка прошла с ним игровые раунды: кожа хранит складки его хвата. "
          "Вещи из личного обихода Вудса выходят на рынок единицами — "
          "он почти никогда с ними не расстаётся.")),
 "polo07": dict(price=9_900_000,
    name="Тайгер Вудс — поло Nike третьего раунда US Open 2007 с автографом",
    text=("Поло Nike, в котором Вудс играл третий раунд US Open 2007 в Окмонте, — "
          "с автографом. Субботний раунд вывел его в финальную пару воскресенья, "
          "а завершил он тот розыгрыш в одном ударе от титула. Экземпляр "
          "сопоставлен с телетрансляцией раунда покадрово. Единственный — 1 из 1.")),
 "polo1of1": dict(price=6_300_000,
    name="Тайгер Вудс — турнирное поло Nike с автографом, 1 из 1",
    text=("Турнирное поло Nike с автографом, нумерация 1 из 1. Тёмная полоска "
          "конца 2000-х — эпохи, когда Вудс собирал титулы PGA Tour сериями. "
          "Автограф выполнен золотым маркером — в вещах Вудса этот вариант "
          "встречается заметно реже чёрного.")),
 "hat": dict(price=2_500_000,
    name="Тайгер Вудс — турнирная кепка Nike с автографом, 1 из 1",
    text=("Турнирная кепка Nike с автографом и ручной нумерацией 1 из 1. "
          "Сзади — монограмма TW, личный знак Вудса. Самый узнаваемый силуэт "
          "гольфа нулевых: эта кепка была на нём в каждое чемпионское "
          "воскресенье. В комплекте оригинальная коробка и чехол.")),
 "driver": dict(price=10_000_000,
    name="Тайгер Вудс — личный драйвер Nike SasQuatch Tour с гравировкой TW-1",
    text=("Личный драйвер Вудса 2006–2008 годов: Nike SasQuatch Tour 460cc "
          "с лофтом 7,5° на турнирном шафте Mitsubishi Diamana Blue 83 — сборка "
          "по его персональной спецификации, которой не существовало в рознице. "
          "Гравировка TW-1 — так Nike метила клюшки, изготовленные лично для "
          "него. Драйвер получен от игрока PGA Tour, которому его передал сам "
          "Вудс. На эти годы приходятся четыре его победы в мейджорах.")),
 "bag_buick": dict(price=7_800_000,
    name="Тайгер Вудс — личная турнирная сумка Buick с автографом",
    text=("Личная сумка Вудса эпохи Buick — с автографом. Серебристо-синий "
          "стафф-бэг с именной панелью TIGER WOODS происходит из "
          "благотворительного аукциона его фонда. Потёртости легли там, где "
          "сумка год за годом ложилась на плечо кедди, — честный турнирный "
          "износ, который невозможно имитировать.")),
 "bags_mj": dict(price=7_100_000,
    name="Майкл Джордан и Тайгер Вудс — пара сумок для гольфа с автографами",
    text=("Пара сумок с автографами двух главных спортсменов своего поколения. "
          "Красно-белый Wilson подписан Джорданом и пронумерован 18 из 23 — "
          "в честь двух его игровых номеров; серый бэг эпохи Buick подписан "
          "Вудсом. Два имени, определившие спорт девяностых и нулевых, — "
          "в одном лоте.")),
 "flag02": dict(price=3_600_000,
    name="Флаг Masters 2002 — автографы Тайгера Вудса и 23 чемпионов турнира",
    text=("Флаг «Мастерс» 2002 года с автографами Тайгера Вудса и ещё двадцати "
          "трёх чемпионов Огасты. В 2002-м Вудс выиграл турнир второй год "
          "подряд — третий зелёный пиджак в карьере. На одном полотне — "
          "Джек Никлаус, Гэри Плеер, Ник Фалдо, Фил Микельсон, Бен Креншоу "
          "и другие обладатели пиджаков за полвека истории турнира.")),
}

ORDER_LADDER = ["glove", "driver", "polo07", "bag_buick",
                "bags_mj", "polo1of1", "flag02", "hat"]

SRC = "img_woods/src"

CSS = """
:root{--noir:#0B0B0C;--gold:#A98545;--gold2:#C9A96A;--ivory:#F5F1E8;
      --ink:#1A1A1A;--mute:#6b6b6b}
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

/* соло: фото слева, текст справа */
.solo{grid-template-columns:1.16fr 1fr}
.solo-ph{display:flex;align-items:center;justify-content:center;padding:50px 24px 50px 58px;background:#fff}
.solo-ph img{max-width:100%;max-height:100%;object-fit:contain}
.solo-side{display:flex;flex-direction:column;justify-content:center;padding:54px 58px 54px 24px}
.solo-name{font-family:'Cormorant Garamond';font-weight:500;font-size:33px;line-height:1.12;color:var(--ink)}
.solo-text{font:300 16px/1.66 'Inter';color:#4a4a4a;margin-top:16px}
.solo-price{font-family:'Cormorant Garamond';font-weight:500;font-size:31px;color:var(--gold);margin-top:20px}

/* детали: два-три кадра в ряд, подпись снизу */
.det{grid-template-rows:auto 1fr auto}
.det-head{display:flex;justify-content:space-between;align-items:baseline;padding:30px 72px 0}
.det-in{display:grid;gap:34px;padding:20px 72px 8px;align-items:center}
.det-ph{height:100%;display:flex;align-items:center;justify-content:center;background:#fff;overflow:hidden}
.det-ph img{max-width:100%;max-height:100%;object-fit:contain}
.det-note{font:300 15px/1.6 'Inter';color:#4a4a4a;max-width:88ch;padding:6px 72px 34px}

/* тёмный сюжетный слайд */
.story{grid-template-columns:1.05fr .95fr}
.story-side{display:flex;flex-direction:column;justify-content:center;padding:0 58px}
.story-ph{display:flex;align-items:center;justify-content:center;padding:56px;background:#0f0f11}
.story-ph img{max-width:100%;max-height:100%;object-fit:contain}

.lad{display:flex;flex-direction:column;height:100%;justify-content:space-between}
.lad-row{display:grid;grid-template-columns:1fr auto;gap:30px;align-items:baseline;
  padding:9px 0;border-bottom:1px solid rgba(169,133,69,.2)}
.lad-nm{font:300 15px/1.35 'Inter';color:#d5cfc3}
.lad-pr{font-family:'Cormorant Garamond';font-weight:500;font-size:21px;color:var(--gold2);white-space:nowrap}
"""


def main():
    S, n = [], 0

    def add(s):
        nonlocal n
        n += 1
        S.append(s.replace("__ID__", f"s{n:02d}"))

    def L(k):
        return LOTS[k]

    def ph(k, i):
        return f"{SRC}/{k}_{i:02d}.jpg"

    def solo(k, img, kick):
        it = L(k)
        add(f"""<section class="slide white solo" id="__ID__">
  <div class="solo-ph"><img src="{img}" alt=""></div>
  <div class="solo-side">
    <div class="kick" style="margin-bottom:16px">{kick}</div>
    <div class="solo-name">{esc(it['name'])}</div>
    <div class="solo-text">{esc(it['text'])}</div>
    <div class="solo-price">{rub(it['price'])}</div>
  </div>
</section>""")

    def det(title, imgs, note, kick):
        cols = "1fr " * len(imgs)
        cells = "".join(f'<div class="det-ph"><img src="{i}" alt=""></div>' for i in imgs)
        add(f"""<section class="slide white det" id="__ID__">
  <div class="det-head">
    <h2 class="serif" style="font-weight:500;font-size:27px;color:var(--ink)">{esc(title)}</h2>
    <span class="kick" style="letter-spacing:.2em">{kick}</span>
  </div>
  <div class="det-in" style="grid-template-columns:{cols.strip()}">{cells}</div>
  <div class="det-note">{esc(note)}</div>
</section>""")

    # ---- обложка: замах с драйвером (промо-кадр, cover допустим)
    add("""<section class="slide dark on" id="__ID__" style="grid-template-columns:1fr 1.06fr">
  <div style="display:flex;flex-direction:column;justify-content:space-between;padding:62px 54px">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:160px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97">
    <div>
      <div class="kick d" style="margin-bottom:22px">Частное собрание · Гольф</div>
      <h1 class="serif" style="font-weight:300;font-size:84px;line-height:1;color:var(--ivory)">Тайгер<br>Вудс</h1>
      <p style="font:300 16.5px/1.65 'Inter';color:#b8b2a6;margin-top:26px;max-width:42ch">Восемь предметов личного происхождения: игровые вещи,
      драйвер с персональной гравировкой, турнирные сумки и флаг «Мастерс».
      Вещи Вудса почти не выходят на рынок — перед вами исключения.</p>
    </div>
    <div class="kick" style="letter-spacing:.24em">8 предметов · июль 2026</div>
  </div>
  <div style="position:relative;height:720px;overflow:hidden">
    <img src="img_woods/hero/cover.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:38% 20%">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,var(--noir) 0%,rgba(11,11,12,.3) 22%,rgba(11,11,12,0) 55%)"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,11,12,.45) 0%,rgba(11,11,12,0) 24%)"></div>
    <span class="credit">Фото: Keith Allison · Wikimedia Commons · CC BY-SA 2.0</span>
  </div>
</section>""")

    # ---- глава I
    add("""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="position:relative">
    <img src="img_woods/hero/div1.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 30%">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,12,.94) 0%,rgba(11,11,12,.78) 32%,rgba(11,11,12,.22) 62%,rgba(11,11,12,.05) 100%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 60px">
      <div class="kick d" style="letter-spacing:.34em;margin-bottom:24px">Раздел первый · 4 предмета</div>
      <h2 class="div-huge" style="font-size:70px">Личные игровые вещи</h2>
      <div class="div-rule" style="margin:32px 0"></div>
      <p class="div-sub" style="max-width:40ch">Перчатка, два турнирных поло и кепка — то, в чём Вудс
      выходил на поле. Игровые вещи он отдаёт реже всего.</p>
    </div>
    <span class="credit">Фото: Flash and Mel · US Open 2008 · Wikimedia Commons · CC BY-SA 2.0</span>
  </div>
</section>""")

    solo("glove", ph("glove", 0), "Личные игровые вещи · 1 из 4")
    det("Перчатка изнутри", [ph("glove", 2), ph("glove", 1)],
        "Ладонная сторона и автограф. Складки на коже — след настоящих раундов: "
        "перчатка снималась и надевалась между ударами, как это делает Вудс на каждом круге.",
        "Личные игровые вещи · 1 из 4")

    solo("polo07", ph("polo07", 0), "Личные игровые вещи · 2 из 4")
    add("""<section class="slide dark" id="__ID__" style="place-content:center;justify-items:center;text-align:center">
  <div style="max-width:62ch;padding:0 60px;display:flex;flex-direction:column;align-items:center">
    <div class="kick d" style="letter-spacing:.3em;margin-bottom:26px">Окмонт · 16 июня 2007 года</div>
    <h2 class="serif" style="font-weight:300;font-size:52px;line-height:1.14;color:var(--ivory);max-width:22ch">Суббота, которая вывела его в финальную пару</h2>
    <div class="div-rule" style="margin:30px 0"></div>
    <p class="div-sub" style="text-align:center;max-width:52ch">US Open любит тишину и наказывает всё остальное.
    В ту субботу Вудс прошёл самое жёсткое поле сезона и вышел на воскресенье в последней группе,
    а розыгрыш завершил в одном ударе от титула. Поло конкретного раунда конкретного мейджора —
    формат, который в вещах Вудса почти не встречается.</p>
  </div>
</section>""")

    solo("polo1of1", ph("polo1of1", 0), "Личные игровые вещи · 3 из 4")
    det("Автограф золотым маркером", [ph("polo1of1", 1)],
        "Крупный спокойный росчерк золотом. Большинство автографов Вудса на рынке "
        "сделаны чёрным — золотой маркер встречается заметно реже.",
        "Личные игровые вещи · 3 из 4")

    solo("hat", ph("hat", 0), "Личные игровые вещи · 4 из 4")
    det("Кепка с трёх сторон", [ph("hat", 1), ph("hat", 3), ph("hat", 2)],
        "Профиль, монограмма TW на затылке и правая сторона. Ручная нумерация "
        "1 из 1, в комплекте оригинальная коробка и чехол.",
        "Личные игровые вещи · 4 из 4")

    # ---- глава II
    add("""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="position:relative">
    <img src="img_woods/hero/div2.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 24%">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,12,.94) 0%,rgba(11,11,12,.78) 32%,rgba(11,11,12,.22) 62%,rgba(11,11,12,.05) 100%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 60px">
      <div class="kick d" style="letter-spacing:.34em;margin-bottom:24px">Раздел второй · 3 предмета</div>
      <h2 class="div-huge" style="font-size:70px">Клюшки и сумки</h2>
      <div class="div-rule" style="margin:32px 0"></div>
      <p class="div-sub" style="max-width:40ch">Личный драйвер с гравировкой TW-1
      и две турнирные сумки — инструменты профессии.</p>
    </div>
    <span class="credit">Фото: Flash and Mel · US Open 2008 · Wikimedia Commons · CC BY-SA 2.0</span>
  </div>
</section>""")

    solo("driver", ph("driver", 0), "Клюшки и сумки · 1 из 3")
    det("Спецификация, которой не было в рознице",
        [ph("driver", 6), ph("driver", 4), ph("driver", 7)],
        "Гравировка TW-1, головка Tour-спецификации 7,5° и шафт Mitsubishi Diamana "
        "Blue 83 — персональная сборка Nike для первого игрока своего стаффа.",
        "Клюшки и сумки · 1 из 3")

    solo("bag_buick", ph("bag_buick", 0), "Клюшки и сумки · 2 из 3")
    det("Именная панель и следы работы", [ph("bag_buick", 7), ph("bag_buick", 13)],
        "Панель TIGER WOODS и честный турнирный износ. Сумка датируется примерно "
        "2006–2007 годами — пиком контракта Вудса с Buick.",
        "Клюшки и сумки · 2 из 3")

    solo("bags_mj", ph("bags_mj", 0), "Клюшки и сумки · 3 из 3")
    add("""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="position:relative">
    <img src="img_woods/hero/jordan.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:60% 40%">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,12,.92) 0%,rgba(11,11,12,.72) 34%,rgba(11,11,12,.16) 64%,rgba(11,11,12,.04) 100%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 60px">
      <div class="kick d" style="letter-spacing:.3em;margin-bottom:24px">Клюшки и сумки · 3 из 3</div>
      <h2 class="div-huge" style="font-size:56px;max-width:16ch">Вторая игра Джордана</h2>
      <div class="div-rule" style="margin:28px 0"></div>
      <p class="div-sub" style="max-width:38ch">Гольф — многолетняя страсть Джордана: он выходит на поле
      почти ежедневно и десятилетиями играет с Вудсом дружеские раунды. Пара подписанных сумок —
      предмет, в котором эти двое сходятся буквально.</p>
    </div>
    <span class="credit">Фото: shgmom56 · Wikimedia Commons · CC BY-SA 2.0</span>
  </div>
</section>""")
    det("Два автографа", [ph("bags_mj", 4), ph("bags_mj", 3)],
        "Подпись Джордана с нумерацией 18 из 23 — в честь двух его игровых номеров — "
        "и подпись Вудса на сумке эпохи Buick.",
        "Клюшки и сумки · 3 из 3")

    # ---- глава III
    add("""<section class="slide dark" id="__ID__" style="place-content:center;justify-items:center;text-align:center">
  <div style="max-width:66ch;padding:0 60px;display:flex;flex-direction:column;align-items:center">
    <div class="kick d" style="letter-spacing:.34em;margin-bottom:26px">Раздел третий · 1 предмет</div>
    <h2 class="div-huge" style="font-size:70px">Легенды вместе</h2>
    <div class="div-rule" style="margin:34px 0"></div>
    <p class="div-sub" style="text-align:center;max-width:44ch">Один флаг, двадцать четыре чемпиона «Мастерс»
    и почти четыре десятка зелёных пиджаков.</p>
  </div>
</section>""")

    solo("flag02", ph("flag02", 1), "Легенды вместе · 1 из 1")
    add("""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr">
  <div style="position:relative">
    <img src="img_woods/hero/augusta.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 62%">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,12,.93) 0%,rgba(11,11,12,.78) 36%,rgba(11,11,12,.24) 66%,rgba(11,11,12,.06) 100%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 60px">
      <div class="kick d" style="letter-spacing:.3em;margin-bottom:22px">Огаста · Национальный гольф-клуб</div>
      <h2 class="div-huge" style="font-size:52px;max-width:18ch">Двадцать четыре чемпиона на одном полотне</h2>
      <div class="div-rule" style="margin:26px 0"></div>
      <p class="div-sub" style="max-width:44ch;font-size:16px">Джек Никлаус — шесть побед, Гэри Плеер и Ник Фалдо — по три,
      Фил Микельсон — три, Бен Креншоу, Бабба Уотсон и Бернхард Лангер — по две.
      Рядом — Спит, Скотт, Гарсия, Капплс, Сингх и другие обладатели зелёных пиджаков
      пяти десятилетий.</p>
    </div>
    <span class="credit">Фото: Wikimedia Commons · public domain</span>
  </div>
</section>""")

    # ---- лестница цен
    rows = "".join(
        f'<div class="lad-row"><div class="lad-nm">{esc(LOTS[k]["name"])}</div>'
        f'<div class="lad-pr">{rub(LOTS[k]["price"])}</div></div>'
        for k in ORDER_LADDER)
    add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:auto 1fr">
  <div style="padding:44px 66px 0">
    <div class="kick d" style="margin-bottom:12px">Подборка целиком</div>
    <h2 class="serif" style="font-weight:300;font-size:44px;line-height:1;color:var(--ivory)">8 предметов</h2>
  </div>
  <div style="padding:22px 66px 36px"><div class="lad">{rows}</div></div>
</section>""")

    # ---- финал
    add("""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="padding:76px 72px 0;display:flex;flex-direction:column;justify-content:center">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:146px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start">
    <h2 class="serif" style="font-weight:300;font-size:46px;line-height:1.14;color:var(--ivory);margin-top:38px;max-width:30ch">Тайгер Вудс. Восемь предметов, каждый — личного происхождения.</h2>
  </div>
  <div style="padding:26px 72px 40px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.24em;color:var(--gold2)">stargift.ru</span>
  </div>
</section>""")

    doc = f"""<meta charset="utf-8">
<title>Stargift · Тайгер Вудс</title>
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
    open(f"{R}/deck_woods.html", "w", encoding="utf-8").write(doc)
    print(f"deck_woods.html: {n} слайдов")


if __name__ == "__main__":
    main()
