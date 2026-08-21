#!/usr/bin/env python3
"""Канон Stargift: каждый формат — и сразу его кухня.

    python3 tools_canon_build.py    # → deck_canon.html  1280×720

Учебная дека: слайд-пример в точности в боевом формате, следом слайд-рецепт —
исходное фото продавца, промпт или команда, результат. Показывает, ЧТО мы
отдаём клиенту и КАК это получено. Повторы фото на рецептах намеренные,
поэтому там отдельные копии из img_canon/.
"""
import html
import os

R = os.path.dirname(os.path.abspath(__file__))
W, H = 1280, 720

NANO = ("Put this on a clean white studio background and photograph it "
        "perfectly straight on, square to the camera: the item's edges "
        "parallel to the frame edges, no tilt, no rotation, no perspective, "
        "viewed flat from directly in front and centred. Beautiful studio "
        "photography with a soft shadow under the item. Do not change the "
        "item itself in any way. Keep every printed detail and the "
        "handwritten signature exactly as in the reference.")

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
.side{display:flex;flex-direction:column;justify-content:center;padding:44px 52px 44px 40px}
.nm{font-family:'Cormorant Garamond';font-weight:500;font-size:33px;line-height:1.12;color:var(--ink)}
.hist{margin-top:15px;padding-left:15px;border-left:2px solid var(--gold)}
.era{font:500 12px/1 'Inter';letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:7px}
.histt{font:300 18px/1.5 'Inter';color:#3d3d3d}
.tx{font:300 18px/1.52 'Inter';color:#4a4a4a;margin-top:14px}
.pr{font-family:'Cormorant Garamond';font-weight:500;font-size:40px;color:var(--gold);margin-top:16px}
.ct{font:400 12.5px/1.5 'Inter';letter-spacing:.18em;text-transform:uppercase;color:var(--cert);margin-top:8px}

/* рецепт */
.rc{grid-template-rows:auto 1fr auto;background:var(--noir);color:var(--ivory)}
.rc-h{padding:26px 54px 0;display:flex;justify-content:space-between;align-items:baseline}
.rc-t{font-family:'Cormorant Garamond';font-weight:400;font-size:30px;color:var(--ivory)}
.rc-imgs{display:grid;grid-template-columns:1fr 1fr;gap:22px;padding:18px 54px 0}
.rc-cell{display:grid;grid-template-rows:1fr auto;gap:8px;min-height:0}
.rc-frame{background:#141416;border:1px solid rgba(169,133,69,.25);display:flex;
  align-items:center;justify-content:center;overflow:hidden}
.rc-frame img{max-width:100%;max-height:100%;object-fit:contain}
.rc-cap{font:500 12px/1.4 'Inter';letter-spacing:.18em;text-transform:uppercase;color:var(--gold2)}
.rc-cap span{color:#8f8a80;letter-spacing:0;text-transform:none;font-weight:300;font-size:14px}
.rc-p{margin:16px 54px 30px;padding:16px 20px;background:#141416;border-left:2px solid var(--gold)}
.rc-p .lbl{font:500 11px/1 'Inter';letter-spacing:.24em;text-transform:uppercase;color:var(--gold);margin-bottom:8px}
.rc-p code{font:400 15px/1.55 ui-monospace,Menlo,monospace;color:#d9d4c8;white-space:pre-wrap;display:block}
"""


def esc(s):
    return html.escape(s or "", quote=False)


S, n = [], 0


def add(s):
    global n
    n += 1
    S.append(s.replace("__ID__", f"s{n:02d}"))


def recipe(title, kick, src, src_cap, src_sub, out, out_cap, out_sub, lbl, code):
    add(f"""<section class="slide rc" id="__ID__">
  <div class="rc-h"><div class="rc-t">{esc(title)}</div><span class="kick d">{esc(kick)}</span></div>
  <div class="rc-imgs">
    <div class="rc-cell"><div class="rc-frame"><img src="{src}" alt=""></div>
      <div class="rc-cap">{esc(src_cap)} · <span>{esc(src_sub)}</span></div></div>
    <div class="rc-cell"><div class="rc-frame"><img src="{out}" alt=""></div>
      <div class="rc-cap">{esc(out_cap)} · <span>{esc(out_sub)}</span></div></div>
  </div>
  <div class="rc-p"><div class="lbl">{esc(lbl)}</div><code>{esc(code)}</code></div>
</section>""")


# ---------- 1. обложка
add("""<section class="slide dark" id="__ID__" style="grid-template-columns:1fr 1fr">
  <div style="display:flex;flex-direction:column;justify-content:space-between;padding:54px 20px 54px 58px">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:134px;width:auto;object-fit:contain;filter:brightness(0) invert(1);align-self:flex-start">
    <div>
      <div class="kick d" style="margin-bottom:20px">Внутренний стандарт · Как мы собираем деки</div>
      <h1 class="serif" style="font-weight:300;font-size:58px;line-height:1.05;color:var(--ivory)">Канон Stargift:<br>формат и кухня</h1>
      <p style="font:300 19px/1.58 'Inter';color:#b8b2a6;margin-top:20px;max-width:40ch">Каждый разворот показан дважды: сначала слайд,
      каким его видит клиент, затем — исходное фото продавца, промпт или команда и результат.</p>
    </div>
    <div class="kick" style="letter-spacing:.24em">август 2026</div>
  </div>
  <div style="display:flex;flex-direction:column;justify-content:center;padding:0 58px;border-left:1px solid rgba(169,133,69,.28)">
    <div class="serif" style="font-weight:300;font-size:126px;line-height:.92;color:var(--gold);opacity:.9">4</div>
    <div class="rule" style="width:76px;margin:24px 0"></div>
    <p style="font:300 20px/1.55 'Inter';color:#b8b2a6;max-width:27ch">способа получить чистый кадр: nano banana pro,
    геометрическое выравнивание, отбеливание фона и честные макро-фрагменты.</p>
    <p style="font:300 20px/1.55 'Inter';color:#b8b2a6;max-width:27ch;margin-top:22px">Один промпт на все предметы.
    Ни одного перерисованного автографа.</p>
  </div>
</section>""")

# ---------- 2. пример: слайд лота, обработка nano
add("""<section class="slide white solo" id="__ID__">
  <div class="ph"><img src="img_mj/halfslide/clean_thriller.jpg" alt=""></div>
  <div class="side">
    <div class="kick">Формат · Слайд лота</div>
    <div class="nm" style="margin-top:13px">Альбом Thriller с автографом Майкла Джексона</div>
    <div class="hist"><div class="era">Epic Records · 1982</div>
      <div class="histt">Самый продаваемый альбом в истории музыки. Подпись синим маркером
      по лаковому конверту первого пресса.</div></div>
    <div class="tx">Фото занимает ровно половину слайда, текст стоит на воздухе справа:
    название, контекст первым абзацем, цена золотом. Кегли — от 18 px, дека читается с телефона.</div>
    <div class="pr">1 500 000&nbsp;₽</div>
    <div class="ct">PSA/DNA</div>
  </div>
</section>""")

# ---------- 3. рецепт nano
recipe("Кухня: белая студия одним промптом", "Higgsfield · nano banana pro · 2k",
       "img_canon/r_thriller_src.jpg", "Было", "фото продавца: стол, тень, завал, наклейка",
       "img_canon/r_thriller_out.jpg", "Стало", "фронтально, белая студия, автограф 1-в-1",
       "Промпт — один и тот же для любого предмета. Имён и сюжета в нём нет: модель может выдумать только то, что упомянуто",
       NANO)

# ---------- 4. пример: слайд лота, геометрия
add("""<section class="slide white solo" id="__ID__">
  <div class="ph"><img src="img_box/half/orig_hof96_22.jpg" alt=""></div>
  <div class="side">
    <div class="kick">Формат · Слайд лота</div>
    <div class="nm" style="margin-top:13px">Программа Зала боксёрской славы, 1996 год, 22 автографа</div>
    <div class="hist"><div class="era">Канастота · 9 июня 1996</div>
      <div class="histt">Плоский лот, весь смысл которого — подписи. Такому генерация
      противопоказана: ракурс исправлен геометрией, пиксели настоящие.</div></div>
    <div class="tx">Внешне слайд не отличается от соседнего — и не должен: клиент видит один
    стандарт подачи, каким бы путём ни был получен кадр.</div>
    <div class="pr">700 000&nbsp;₽</div>
    <div class="ct">JSA</div>
  </div>
</section>""")

# ---------- 5. рецепт flatten
recipe("Кухня: ракурс правится без нейросети", "tools_flatten.py · перспективный варп",
       "img_canon/r_hof_src.jpg", "Было", "тёмная ткань продавца, наклон, перспектива",
       "img_canon/r_hof_out.jpg", "Стало", "те же пиксели, развёрнутые фронтально",
       "Команда вместо промпта: находим четыре угла листа и разворачиваем. Подписи не перерисовываются в принципе",
       "python3 tools_flatten.py --mode=bright --out=img_box/flat img_box/orig_hof96_22.jpg\n"
       "python3 tools_halfslide.py --out=img_box/half img_box/flat/orig_hof96_22.jpg")

# ---------- 6. пример: слайд лота, отбеливание
add("""<section class="slide white solo" id="__ID__">
  <div class="ph"><img src="img_box/half/orig_glove5.jpg" alt=""></div>
  <div class="side">
    <div class="kick">Формат · Слайд лота</div>
    <div class="nm" style="margin-top:13px">Пара перчаток Everlast: Тайсон, Льюис, Леонард, Хирнс, Дюран</div>
    <div class="hist"><div class="era">Состаренная кожа · пара</div>
      <div class="histt">Объёмный предмет на сером фоне продавца. Вырезать нельзя —
      жёсткая маска рвёт кромку. Фон уведён в белый без границы.</div></div>
    <div class="tx">Трое из пяти подписавших — «Четыре короля» восьмидесятых. Пара на подставке —
    объект, а не сувенир.</div>
    <div class="pr">550 000&nbsp;₽</div>
    <div class="ct">Beckett</div>
  </div>
</section>""")

# ---------- 7. рецепт whiten
recipe("Кухня: фон в белый, границы нет", "tools_whiten.py · без вырезания",
       "img_canon/r_glove_src.jpg", "Было", "перчатка Али лежит на столе у стены",
       "img_canon/r_glove_out.jpg", "Стало", "стоит, как выставляют; фон чистый белый",
       "Фон опознаётся как светлое и бесцветное и плавно уводится в белый; --rot ставит предмет так, как его выставляют",
       "python3 tools_whiten.py --rot=90 --out=img_box/wht img_box/orig_glove_ali.jpg\n"
       "python3 tools_halfslide.py --out=img_box/half img_box/wht/orig_glove_ali.jpg")

# ---------- 8. пример: подписи крупно
add("""<section class="slide white" id="__ID__" style="grid-template-rows:auto 1fr auto">
  <div style="padding:30px 58px 0;display:flex;justify-content:space-between;align-items:baseline;gap:30px">
    <div class="serif" style="font-weight:500;font-size:32px;line-height:1.1;color:var(--ink)">Подписи крупно</div>
    <span class="kick" style="white-space:nowrap">Формат · Второй слайд лота</span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;padding:20px 58px 0">
    <div style="background:#F7F5F1;display:flex;align-items:center;justify-content:center;overflow:hidden;height:100%"><img src="img_canon/r_det_a.jpg" alt="" style="max-width:100%;max-height:100%;object-fit:contain"></div>
    <div style="background:#F7F5F1;display:flex;align-items:center;justify-content:center;overflow:hidden;height:100%"><img src="img_canon/r_det_b.jpg" alt="" style="max-width:100%;max-height:100%;object-fit:contain"></div>
  </div>
  <div style="padding:18px 58px 30px">
    <div style="font:300 18px/1.5 'Inter';color:#4a4a4a">Арчи Мур · Флойд Паттерсон · Кармен Базилио · Карлос Ортис · Боб Фостер · Кристи Мартин</div>
    <div style="font:300 14px/1.5 'Inter';color:#8d8880;margin-top:8px">Когда у лота одно фото объявления, вторые ракурсы не выдумываются — режутся из того же кадра.</div>
  </div>
</section>""")

# ---------- 9. рецепт details
recipe("Кухня: макро без выдумки", "tools_box_details.py · фрагменты того же листа",
       "img_canon/r_hof_src2.jpg", "Было", "один кадр объявления на весь лот",
       "img_canon/r_det_a2.jpg", "Стало", "фрагмент 1:1 под пропорцию ячейки слайда",
       "Центр и ширина фрагмента задаются в долях предмета; границы предмета инструмент находит сам",
       'SPEC = {"hof96_22": [(0.31, 0.22, 0.62), (0.69, 0.79, 0.62)]}  # (cx, cy, ширина)\n'
       "python3 tools_box_details.py")

# ---------- 10. пример: тексты — было/стало
add("""<section class="slide dark" id="__ID__" style="grid-template-rows:auto 1fr">
  <div style="padding:42px 62px 0">
    <div class="kick d" style="margin-bottom:12px">Формат · Тексты лотов</div>
    <h2 class="serif" style="font-weight:300;font-size:40px;line-height:1.06;color:var(--ivory)">Из строки выгрузки — в голос дома</h2>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1.25fr;gap:44px;padding:28px 62px 48px;align-content:center">
    <div>
      <div class="rc-cap" style="margin-bottom:10px">Было · строка CSV</div>
      <p style="font:400 16px/1.6 ui-monospace,Menlo,monospace;color:#8f8a80">Boxing Greats Multi Signed Autographed Robe 51 Sigs Hearns Lewis BAS AC49467. Международная сертификация подлинности: Beckett/BAS.</p>
    </div>
    <div>
      <div class="rc-cap" style="margin-bottom:10px">Стало · текст в деке</div>
      <p style="font:300 19px/1.55 'Inter';color:#d9d4c8">Пятьдесят один росчерк серебром по синему атласу. Среди подписавших — Томас Хирнс и Леннокс Льюис. Предмет читается с другого конца комнаты, а масштаб понятен сразу: столько имён на одной вещи случайно не собирается. Для большой стены — кабинет, клубная комната, лестничный пролёт.</p>
      <p style="font:300 15px/1.55 'Inter';color:#8f8a80;margin-top:14px">Формула: факт → в чём особенность → кому подойдёт. Слова «подлинность» нет ни в одном тексте; сертификатор — мелкой строкой, только Beckett · JSA · PSA/DNA.</p>
    </div>
  </div>
</section>""")

# ---------- 11. финал: свод правил
add("""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="padding:0 66px;display:flex;flex-direction:column;justify-content:center">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:120px;width:auto;object-fit:contain;filter:brightness(0) invert(1);align-self:flex-start">
    <h2 class="serif" style="font-weight:300;font-size:40px;line-height:1.15;color:var(--ivory);margin-top:30px;max-width:44ch">Пять правил, которые держат всё: одно фото — один слайд; фото лота не кропать; кегли не уменьшать; про подлинность не писать; автограф не перерисовывать.</h2>
  </div>
  <div style="padding:24px 66px 40px;border-top:1px solid rgba(169,133,69,.3);display:flex;justify-content:space-between">
    <span class="kick" style="letter-spacing:.24em;color:var(--gold2)">stargift.ru</span>
    <span class="kick" style="letter-spacing:.24em">PHOTO_RULES.md · CLAUDE.md</span>
  </div>
</section>""")

doc = f"""<meta charset="utf-8">
<title>Stargift · Канон: формат и кухня</title>
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
open(f"{R}/deck_canon.html", "w", encoding="utf-8").write(doc)
print(f"deck_canon.html: {n} слайдов")
