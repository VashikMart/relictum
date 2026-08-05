#!/usr/bin/env python3
"""«Майкл Джексон» — вертикальная версия 720×1280.

    python3 tools_mj_vert.py        # → deck_mj_V.html

Формат дома для вертикали (как в deck_cult_v): фото сверху во всю ширину,
плашка с текстом снизу. Текста намеренно мало — одна строка про предмет:
вертикаль смотрят с телефона на ходу, длинный абзац там не читают.
Данные лотов берём из горизонтального билдера, чтобы цены и названия
не разъезжались между версиями.
"""
import html, os, sys

sys.argv = sys.argv[:1]                     # чтобы билдер не поймал чужой VARIANT
from tools_mj_build import LOTS, ORDER      # noqa: E402

R = os.path.dirname(os.path.abspath(__file__))
C = "img_mj"


def esc(s):
    return html.escape(s or "", quote=False)


def rub(n):
    return f"{n:,}".replace(",", " ") + "&nbsp;₽"


def img(name):
    """Сначала вырез предмета — он занимает всё поле, фон студии на слайд
    не тащим. Берём JPEG-версию на белом: подложка слайда белая, результат
    тот же, а вес деки в разы меньше."""
    for p in (f"{C}/cut/{name}.jpg", f"{C}/{name}.jpg", f"{C}/framed/{name}.jpg",
              f"{C}/hist/{name}.jpg", f"{C}/src/{name}.jpg"):
        if os.path.exists(os.path.join(R, p)):
            return p
    return f"{C}/src/{name}.jpg"


# одна строка на лот — самое важное, без пересказа истории
SHORT = {
 "iwyb":       "Дебютный альбом Jackson 5. Сингл с этой пластинки встал на первое место Billboard в январе 1970-го.",
 "maybe":      "Первый тираж 1971 года, разворотный конверт. Подписан не одним Майклом — росчерки братьев по всей обложке.",
 "gottobe":    "Сольный дебют — Майклу тринадцать. С этой обложки начинается его отдельная биография.",
 "farewell":   "Записи 1973 года пролежали в архиве Motown одиннадцать лет и вышли альбомом только в 1984-м.",
 "offthewall": "Первая работа с Куинси Джонсом. Четыре сингла в первой десятке Billboard — до этого такого не делал никто.",
 "thriller":   "Самый продаваемый альбом в истории. Ранний тираж: каталожный номер QE 38112.",
 "thrillerjp": "Японское издание с оби-полосой. Инструментальная версия выходила только для Японии.",
 "bad":        "Пять синглов с одного альбома на первом месте Billboard. Подписан конкретному человеку, с именем от руки.",
 "badpromo":   "Промо-тираж: рассылался на радио до выхода, в продажу не поступал.",
 "ph1620":     "Эпоха «Billie Jean». Самый крупный формат подборки — 41×51 см.",
 "ph75":       "Расшитый сценический костюм — часть образа, который Джексон выстраивал сам.",
 "ph1114c":    "Поздний сценический образ: чёрная куртка с шевронами. Автограф серебром по тёмному полю.",
 "ph1114hat":  "«Smooth Criminal»: белая шляпа, синий свет и самая копируемая поза в поп-музыке.",
 "cut":        "Росчерк на отдельном листе в капсуле. Оформляется в раму рядом с любой фотографией на выбор.",
}

CSS = """
:root{--noir:#0B0B0C;--gold:#A98545;--gold2:#C9A96A;--ivory:#F5F1E8;
      --paper:#F7F5F1;--ink:#1A1A1A;--mute:#6b6b6b;--cert:#9a958c}
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;overflow:hidden;background:#000;font-family:'Inter',sans-serif}
.deck{height:100%;position:relative}
.slide{position:absolute;inset:0;display:none;overflow:hidden}
.slide.on{display:grid}
.slide>*{min-height:0;min-width:0}
img{display:block}
.serif{font-family:'Cormorant Garamond',serif}
.kick{font:500 15px/1 'Inter';letter-spacing:.28em;text-transform:uppercase;color:var(--gold)}
.kick.d{color:var(--gold2)}
.light{background:var(--paper);color:var(--ink)}
.white{background:#fff;color:var(--ink)}
.dark{background:var(--noir);color:var(--ivory)}
.credit{position:absolute;right:20px;bottom:16px;font:400 12px/1.3 'Inter';
  letter-spacing:.06em;color:rgba(245,241,232,.6)}
.rule{height:1px;width:84px;background:rgba(169,133,69,.55)}

/* лот: фото сверху, плашка снизу */
.solo{grid-template-rows:1fr auto}
.solo .ph{background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden;padding:34px 40px}
.solo .ph img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain}
.solo .info{padding:36px 44px 44px;border-top:1px solid rgba(169,133,69,.35);background:var(--paper)}
.solo .nm{font-family:'Cormorant Garamond';font-weight:500;font-size:40px;line-height:1.05;margin-top:14px}
.solo .era{font:500 14px/1 'Inter';letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-top:16px}
.solo .tp{font:300 22px/1.46 'Inter';color:#4a4a4a;margin-top:10px}
.solo .pr{font-family:'Cormorant Garamond';font-weight:500;font-size:46px;color:var(--gold);margin-top:20px}
.solo .ct{font:400 14px/1.5 'Inter';letter-spacing:.16em;text-transform:uppercase;color:var(--cert);margin-top:10px}

/* разделитель эпохи: кадр во весь экран, текст внизу */
.div-v{grid-template-rows:1fr}
.div-huge{font-family:'Cormorant Garamond';font-weight:300;font-size:66px;line-height:1.02;color:var(--ivory)}
.div-sub{font:300 24px/1.5 'Inter';color:#c9c3b7;margin-top:20px}

.lad-row{display:grid;grid-template-columns:1fr auto;gap:20px;align-items:baseline;
  padding:13px 0;border-bottom:1px solid rgba(169,133,69,.2)}
.lad-nm{font:300 17px/1.32 'Inter';color:#d5cfc3}
.lad-pr{font-family:'Cormorant Garamond';font-weight:500;font-size:24px;color:var(--gold2);white-space:nowrap}
"""


def main():
    S, n = [], 0

    def add(s):
        nonlocal n
        n += 1
        S.append(s.replace("__ID__", f"s{n:02d}"))

    def solo(key, photo, kick):
        it = LOTS[key]
        add(f"""<section class="slide light solo" id="__ID__">
  <div class="ph"><img src="{photo}" alt=""></div>
  <div class="info">
    <div class="kick">{esc(kick)}</div>
    <div class="nm">{esc(it['name'])}</div>
    <div class="era">{esc(it['era'])}</div>
    <div class="tp">{esc(SHORT[key])}</div>
    <div class="pr">{rub(it['price'])}</div>
    <div class="ct">{esc(it['cert'])}</div>
  </div>
</section>""")

    def framing(photo, kick, title, text):
        add(f"""<section class="slide light solo" id="__ID__">
  <div class="ph"><img src="{photo}" alt=""></div>
  <div class="info">
    <div class="kick">{esc(kick)}</div>
    <div class="nm">{esc(title)}</div>
    <div class="tp" style="margin-top:16px">{esc(text)}</div>
  </div>
</section>""")

    def divider(kick, huge, sub, photo, credit, objpos="50% 30%"):
        add(f"""<section class="slide dark div-v" id="__ID__">
  <div style="position:relative">
    <img src="{photo}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:{objpos}">
    <div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,11,12,.97) 0%,rgba(11,11,12,.86) 30%,rgba(11,11,12,.2) 62%,rgba(11,11,12,.05) 100%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:flex-end;padding:0 48px 74px">
      <div class="kick d" style="letter-spacing:.26em;margin-bottom:20px">{esc(kick)}</div>
      <h2 class="div-huge">{huge}</h2>
      <div class="rule" style="margin:24px 0"></div>
      <p class="div-sub">{esc(sub)}</p>
    </div>
    <span class="credit">{esc(credit)}</span>
  </div>
</section>""")

    # ---------- обложка
    add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="position:relative">
    <img src="{img('mj_1984')}" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 22%">
    <div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,11,12,.98) 0%,rgba(11,11,12,.5) 34%,rgba(11,11,12,.1) 70%)"></div>
    <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:flex-end;padding:0 48px 44px">
      <img src="img/stargift_logo.png" alt="Stargift" style="height:120px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start;margin-bottom:34px">
      <div class="kick d" style="margin-bottom:20px">Частное собрание · Музыка</div>
      <h1 class="serif" style="font-weight:300;font-size:80px;line-height:1.02;color:var(--ivory)">Майкл<br>Джексон</h1>
      <p style="font:300 23px/1.5 'Inter';color:#b8b2a6;margin-top:22px">Девять подписанных пластинок и пять фотографий.
      Двадцать лет карьеры, собранные по конвертам.</p>
    </div>
    <span class="credit">Фото: Epic Records · Wikimedia Commons · public domain</span>
  </div>
  <div style="padding:24px 48px 30px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.22em">14 предметов · август 2026</span>
  </div>
</section>""")

    # ---------- Motown
    divider("1969–1971 · Motown", "Пятеро братьев<br>из Гэри, Индиана",
            "Осенью 1969-го Motown выпустил сингл группы, которую никто не знал. "
            "Через три месяца он стоял первым, а солисту было одиннадцать.",
            img("j5_1969"), "Фото: Bernie Ilson, Inc. · Wikimedia Commons · public domain", "50% 22%")

    solo("iwyb", img("clean_iwyb"), "Пластинки · 1 из 14")
    solo("maybe", img("clean_maybe"), "Пластинки · 2 из 14")
    solo("gottobe", img("clean_gottobe"), "Пластинки · 3 из 14")
    solo("farewell", img("clean_farewell"), "Пластинки · 4 из 14")

    # ---------- Epic
    divider("1979–1987 · Epic", "Куинси Джонс<br>и три альбома",
            "Три пластинки подряд, каждая продавалась лучше предыдущей — "
            "случай, которого в поп-музыке больше не было.",
            img("mj_1984"), "Фото: Epic Records · Wikimedia Commons · public domain", "50% 18%")

    solo("offthewall", img("clean_offthewall"), "Пластинки · 5 из 14")
    solo("thriller", img("clean_thriller"), "Пластинки · 6 из 14")

    framing(img("framed_thriller_diptych"), "Оформление · пластинка",
            "Раскрывающаяся рама",
            "Конверт слева, винил справа в глубокой нише на бордовом бархате. "
            "Латунные петли, табличка с именем.")

    framing(img("framed_thriller_square"), "Оформление · пластинка",
            "Закрытый квадрат",
            "Та же пластинка в простой подаче: одна рама, бордовое паспарту, "
            "вдвое меньше места на стене.")

    solo("thrillerjp", img("clean_thrillerjp"), "Пластинки · 7 из 14")
    solo("bad", img("clean_bad"), "Пластинки · 8 из 14")
    solo("badpromo", img("clean_badpromo"), "Пластинки · 9 из 14")

    # ---------- фотографии
    divider("Фотографии", "Белый дом,<br>14 мая 1984",
            "Рейган вручает Джексону благодарность за «Beat It», отданную "
            "кампании против пьяного вождения.",
            img("mj_reagan"), "Фото: Ronald Reagan Presidential Library · Wikimedia Commons · public domain", "50% 38%")

    solo("ph1620", img("clean_ph1620"), "Фотографии · 10 из 14")
    solo("ph75", img("clean_ph75"), "Фотографии · 11 из 14")
    solo("ph1114c", img("clean_ph1114c"), "Фотографии · 12 из 14")
    solo("ph1114hat", img("clean_ph1114hat"), "Фотографии · 13 из 14")

    framing(img("framed_ph1114hat"), "Оформление · фотография",
            "Тёмная рама, синий бархат",
            "Под холодный кадр — синее паспарту: рама не спорит со сценическим светом.")

    framing(img("framed_ph1620"), "Оформление · фотография",
            "Кованое золото, бордо",
            "Тёплый кадр требует тёплой рамы. Цвет паспарту всегда берём "
            "у самой фотографии.")

    solo("cut", img("clean_cut"), "Фотографии · 14 из 14")

    # ---------- упаковка
    add("""<section class="slide light" id="__ID__" style="grid-template-rows:1fr 1fr auto">
  <div style="background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden"><img src="img_packaging/box_kraft.jpg" alt="" style="width:100%;height:100%;object-fit:contain;padding:22px"></div>
  <div style="background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden;border-top:1px solid rgba(169,133,69,.2)"><img src="img_packaging/bag_white.jpg" alt="" style="width:100%;height:100%;object-fit:contain;padding:22px"></div>
  <div style="padding:32px 44px 40px;border-top:1px solid rgba(169,133,69,.35)">
    <div class="kick">Упаковка Stargift</div>
    <div class="serif" style="font-weight:500;font-size:38px;line-height:1.06;margin-top:14px">Как мы отдаём подарок</div>
    <p style="font:300 22px/1.46 'Inter';color:#4a4a4a;margin-top:12px">Крафт-бумага с автографами великих, лента дома
    и плотный пакет. Оформленную работу привозим и вешаем сами.</p>
  </div>
</section>""")

    # ---------- лестница
    rows = "".join(
        f'<div class="lad-row"><div class="lad-nm">{esc(LOTS[k]["name"])}</div>'
        f'<div class="lad-pr">{rub(LOTS[k]["price"])}</div></div>' for k in ORDER)
    add(f"""<section class="slide dark" id="__ID__" style="grid-template-rows:auto 1fr">
  <div style="padding:52px 44px 0">
    <div class="kick d" style="margin-bottom:14px">Подборка целиком</div>
    <h2 class="serif" style="font-weight:300;font-size:52px;line-height:1;color:var(--ivory)">14 предметов</h2>
  </div>
  <div style="padding:24px 44px 44px">{rows}</div>
</section>""")

    # ---------- финал
    add("""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="padding:0 44px;display:flex;flex-direction:column;justify-content:center">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:130px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start">
    <h2 class="serif" style="font-weight:300;font-size:54px;line-height:1.1;color:var(--ivory);margin-top:38px">Майкл Джексон. От первого сингла до последней пластинки с Куинси Джонсом.</h2>
  </div>
  <div style="padding:28px 44px 44px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.22em;color:var(--gold2)">stargift.ru</span>
  </div>
</section>""")

    doc = f"""<meta charset="utf-8">
<title>Stargift · Майкл Джексон · вертикаль</title>
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
<style>@page{{size:720px 1280px;margin:0}}@media print{{html,body{{overflow:visible;height:auto}}*{{box-shadow:none !important}}.slide{{animation:none}}.deck{{height:auto}}
.slide{{position:relative;inset:auto;display:grid !important;width:720px;height:1280px;page-break-after:always}}}}</style>
"""
    open(f"{R}/deck_mj_V.html", "w", encoding="utf-8").write(doc)
    print(f"deck_mj_V.html: {n} слайдов, вертикаль 720×1280")


if __name__ == "__main__":
    main()
