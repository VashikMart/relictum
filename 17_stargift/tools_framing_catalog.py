#!/usr/bin/env python3
"""«База оформления Stargift» — каталог форматов, 1280×720.

    python3 tools_framing_catalog.py     # → deck_framing.html

Каталог собирается из img_framing/: у каждой категории берётся мастер-лист
и текст правила. Добавил новую категорию — допиши сюда строку, пересобери.
"""
import html, os

R = os.path.dirname(os.path.abspath(__file__))
F = "img_framing"


def esc(s):
    return html.escape(s or "", quote=False)


# (папка, мастер, заголовок, кикер, абзац, подписи-колонки)
CATS = [
 (f"{F}/frames_photo/master_frames_photo.jpg", "Фотографии и постеры", "8 форматов",
  "Самодостаточный экспонат: кадр объясняет себя сам, второй элемент не нужен. "
  "Работает и обратный ход — два кадра в одной раме, когда хочется показать "
  "героя и его сцену.",
  [("Бархат", "бордо · уголь · красный · синий"),
   ("Особые", "перламутровое серебро, кованое золото, «парящее стекло»"),
   ("Табличка", "PERSONALLY SIGNED BY")]),

 (f"{F}/frames_doc/master_frames_doc.jpg", "Документы, письма, журналы", "8 форматов",
  "Здесь второй элемент обязателен: документ без портрета не читается. "
  "Портрет может стоять слева или справа; для крупных фигур — триптих: "
  "портрет, документ и третий предмет эпохи.",
  [("Рама по эпохе", "резное золото — XIX век · серебро — наука и космос · красное дерево — политика"),
   ("Паспарту", "синий — основной регистр, зелёный и красный — исключения"),
   ("Табличка", "русская для русских героев")]),

 (f"{F}/frames_script/master_frames_script.jpg", "Киносценарии", "6 форматов",
  "Формат жёсткий: слева титульный лист в собственном золотом багете, справа "
  "постер фильма. Латунные брадсы переплёта видны и не убираются — это признак "
  "настоящего съёмочного экземпляра.",
  [("Военное кино", "серый дуб + угольный бархат"),
   ("Культовое кино 90-х", "тёмно-серая рама + красный"),
   ("Сериалы и ретро-ТВ", "бронза + зелёный")]),

 (f"{F}/frames_vinyl/master_frames_vinyl.jpg", "Пластинки", "3 формата",
  "Главный формат — раскрывающийся диптих на латунных петлях: закрытым он "
  "показывает конверт, открытым — конверт и сам диск в глубокой нише. "
  "Если подписан только винил, берём квадрат с диском на красном бархате.",
  [("Диптих", "бордовый бархат в обеих панелях"),
   ("Только диск", "чёрная фактурная рама + красный"),
   ("Только конверт", "золото + бордо или орех + синий")]),

 (f"{F}/instruments_guitar/master_guitar.jpg", "Гитары", "накладка → инструмент",
  "Дом покупает подписанную накладку, а гитару подбирает под неё. "
  "Белая и кремовая накладка — чёрный Stratocaster или Telecaster, реже "
  "винтажно-белый. Черепаховая и белая «капля» — санбёрст-акустика.",
  [("Подача", "чёрная напольная стойка, съёмка в зале"),
   ("Без рамы", "инструмент показываем целиком"),
   ("Заказные", "пурпурный «спарклевый» Telecaster под белую накладку")]),

 (f"{F}/instruments_drum/master_drum.jpg", "Барабаны", "пластик → малый барабан",
  "Та же логика: покупается подписанный пластик, дом ставит его на настоящий "
  "хромированный малый барабан на стойке. Для группового лота на обод крепится "
  "шеврон группы.",
  [("Два состояния", "голый пластик «как куплен» и собранный барабан"),
   ("Шеврон", "Iron Maiden, Black Sabbath — по группе"),
   ("Подача", "барабан на стойке, вид сверху под углом")]),

 (f"{F}/frames_shirt/master_frames_shirt.jpg", "Футболки и джерси", "3 формата",
  "Паспарту берёт клубные цвета: «Барселона» — бордо, сборная Бразилии — "
  "зелёный, белая форма — светло-серое. По бокам таблички ставят два шеврона "
  "клуба.",
  [("Рама", "чёрная или золотая, широкое паспарту"),
   ("Линия", "тонкая золотая по периметру окна"),
   ("Табличка", "латунь, по центру нижнего поля")]),

 (f"{F}/frames_poster/master_frames_poster.jpg", "Постеры и афиши", "4 формата",
  "Паспарту подбирается под палитру афиши. Крупный формат допускает белое "
  "паспарту без бархата — плакату нужен воздух, а не бархат.",
  [("Тёплые афиши", "золото + бордо"),
   ("Современные", "серебро + белое"),
   ("Классика", "тёмная рама + белое, крупный формат")]),

 (f"{F}/frames_card/master_frames_card.jpg", "Карточки и слабы", "3 формата",
  "Маленький предмет требует контекста сильнее прочих: к карточке почти всегда "
  "добавляют фотографию героя, иначе в раме остаётся пустое поле.",
  [("Паспарту", "красный или синий бархат"),
   ("Пара", "карточка + фото героя"),
   ("Группа", "чёрное паспарту под коллективный кадр")]),

 (f"{F}/frames_book/master_frames_book.jpg", "Книги", "2 формата",
  "Либо подписанная страница плоско рядом с портретом автора, либо сама книга "
  "раскрытой в глубоком боксе. Большинство книг в каталоге сняты «как есть» — "
  "рама добавляется под заказ.",
  [("Плоско", "тёмная рама + красный бархат + портрет"),
   ("Глубокий бокс", "красное дерево + зелёный, книга раскрыта"),
   ("Табличка", "имя автора")]),

 (f"{F}/stands_ball/master_stands_ball.jpg", "Мячи", "акриловый куб",
  "Прозрачный куб на квадратном основании, латунная табличка на передней грани. "
  "Куб выше и уже, чем бокс под бутсу: мяч стоит по центру и не касается стенок.",
  [("Основания", "красное дерево · белый, зелёный, чёрный мрамор"),
   ("Подбор", "винтажная кожа — дерево и зелёный, белый мяч — чёрный мрамор"),
   ("Табличка", "мяч команды — клуб и сезон, а не имя")]),

 (f"{F}/stands_boot/master_stands.jpg", "Бутсы и объёмные вещи", "6 оснований",
  "Вытянутый акриловый бокс на каменном или деревянном основании. Основание "
  "подбирается под цвет предмета, а не под вид спорта.",
  [("Основания", "красное дерево ×3 · белый, чёрный, зелёный мрамор"),
   ("Шайбы", "тот же формат, куб меньшего размера"),
   ("Табличка", "PERSONALLY SIGNED BY")]),
]

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
.div-rule{height:1px;width:70px;background:rgba(169,133,69,.55)}

/* разворот категории: мастер сверху, правило снизу */
.cat{grid-template-rows:auto 1fr auto}
.cat-head{display:flex;justify-content:space-between;align-items:baseline;padding:26px 56px 0}
.cat-name{font-family:'Cormorant Garamond';font-weight:500;font-size:29px;color:var(--ink)}
.cat-sheet{padding:16px 56px 0;display:flex;align-items:center;justify-content:center}
.cat-sheet img{max-width:100%;max-height:100%;object-fit:contain}
.cat-foot{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:30px;
  padding:16px 56px 26px;align-items:start}
.cat-text{font:300 13.5px/1.6 'Inter';color:#4a4a4a}
.cell-k{font:500 9.5px/1 'Inter';letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:7px}
.cell-v{font:300 12.5px/1.55 'Inter';color:#5a5a5a}

/* пример генерации: кадр на полслайда */
.ex{grid-template-columns:1.15fr .85fr}
.ex-ph{height:720px;overflow:hidden;background:#fff}
.ex-ph img{width:100%;height:100%;object-fit:contain}
.ex-side{display:flex;flex-direction:column;justify-content:center;padding:50px 56px 50px 30px}
.ex-name{font-family:'Cormorant Garamond';font-weight:500;font-size:28px;line-height:1.15;color:var(--ink)}
.ex-text{font:300 15px/1.64 'Inter';color:#4a4a4a;margin-top:14px}
.ex-note{font:300 12.5px/1.55 'Inter';color:#7a7a7a;margin-top:18px;
  border-top:1px solid rgba(169,133,69,.3);padding-top:14px}

.rules{grid-template-rows:auto 1fr}
.rule{display:grid;grid-template-columns:52px 1fr;gap:22px;padding:18px 0;
  border-bottom:1px solid rgba(169,133,69,.22)}
.rule-n{font-family:'Cormorant Garamond';font-weight:300;font-size:38px;line-height:1;color:var(--gold)}
.rule-h{font-family:'Cormorant Garamond';font-weight:500;font-size:22px;color:var(--ivory)}
.rule-t{font:300 14px/1.62 'Inter';color:#b8b2a6;margin-top:7px;max-width:96ch}
"""

RULES = [
 ("Экспонат почти никогда не идёт один",
  "Если предмет сам по себе не объясняет, кто это и откуда, в раму добавляется второй "
  "элемент: портрет героя, постер фильма, обложка, кадр с матча. Документ, письмо, книга, "
  "сценарий, журнал и карточка идут парой практически всегда. Фотография и футболка обычно "
  "самодостаточны. Критерий один: гость должен понять экспонат, не читая подпись."),
 ("Цвет паспарту берётся у предмета",
  "Бордовый — тёплые и красные кадры. Зелёный — жёлтые, природные, ретро-ТВ. Тёмно-синий — "
  "документы, наука, космос, чёрно-белая хроника. Угольный — военное и современное кино. "
  "Красный — культовое кино и советская эпоха. Для клубной вещи паспарту берёт клубные цвета."),
 ("Рама попадает в эпоху",
  "Резное золото и багет с орнаментом — XIX век и раньше. Матовое серебро и брашированный "
  "металл — космос, наука, XX век. Красное дерево — политика и классика. Серый дуб — военное "
  "кино и современность. Чёрное и венге — рок и современный спорт. Один и тот же документ "
  "в золотом багете и в сером дубе читается как разные вещи."),
 ("Накладку покупаем — инструмент подбираем",
  "У гитар и барабанов подписан не инструмент, а съёмная часть: пикгард или пластик. "
  "Инструмент дом подбирает под неё по цвету и типу, и это отдельное решение, "
  "а не техническая сборка."),
]


def main():
    S, n = [], 0

    def add(s):
        nonlocal n
        n += 1
        S.append(s.replace("__ID__", f"s{n:02d}"))

    # обложка
    add(f"""<section class="slide dark on" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="padding:74px 66px 0;display:flex;flex-direction:column;justify-content:center">
    <img src="img/stargift_logo.png" alt="Stargift" style="height:132px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.97;align-self:flex-start">
    <div class="kick d" style="margin-top:40px;margin-bottom:20px">Внутренний стандарт дома</div>
    <h1 class="serif" style="font-weight:300;font-size:62px;line-height:1.04;color:var(--ivory)">База оформления</h1>
    <p style="font:300 16px/1.66 'Inter';color:#b8b2a6;margin-top:22px;max-width:56ch">Форматы рам, подставок и сборки инструментов,
    снятые с готовых лотов. {len(CATS)} категорий, правила подбора рамы, паспарту и второго элемента.</p>
  </div>
  <div style="padding:24px 66px 40px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.24em;color:var(--gold2)">17_stargift/img_framing</span>
  </div>
</section>""")

    # правила
    rows = "".join(
        f'<div class="rule"><div class="rule-n">{i}</div>'
        f'<div><div class="rule-h">{esc(h)}</div><div class="rule-t">{esc(t)}</div></div></div>'
        for i, (h, t) in enumerate(RULES, 1))
    add(f"""<section class="slide dark rules" id="__ID__">
  <div style="padding:40px 62px 0">
    <div class="kick d" style="margin-bottom:12px">Что общего у всех категорий</div>
    <h2 class="serif" style="font-weight:300;font-size:40px;line-height:1;color:var(--ivory)">Четыре правила</h2>
  </div>
  <div style="padding:14px 62px 30px">{rows}</div>
</section>""")

    # категории
    for i, (sheet, name, kick, text, cells) in enumerate(CATS, 1):
        if not os.path.exists(os.path.join(R, sheet)):
            print(f"  пропуск: нет {sheet}")
            continue
        cc = "".join(f'<div><div class="cell-k">{esc(k)}</div>'
                     f'<div class="cell-v">{esc(v)}</div></div>' for k, v in cells)
        add(f"""<section class="slide white cat" id="__ID__">
  <div class="cat-head">
    <div class="cat-name">{esc(name)}</div>
    <span class="kick">{esc(kick)}</span>
  </div>
  <div class="cat-sheet"><img src="{sheet}" alt=""></div>
  <div class="cat-foot"><div class="cat-text">{esc(text)}</div>{cc}</div>
</section>""")

    # примеры генераций
    EX = [
     (f"{F}/generated/bocelli_vinyl_open_diptych.jpg",
      "Раскрывающаяся рама · Андреа Бочелли",
      "Собрано из двух настоящих кадров лота: подписанный конверт и сам диск. "
      "Модель получила мастер-лист категории первым референсом, конверт вторым, "
      "диск третьим — и сложила их в формат дома.",
      "Макет формата. В клиентский каталог ставим фотографию собранной рамы."),
     (f"{F}/generated/rock_mag_photo_dark_navy.jpg",
      "Обложка и портрет · Дуэйн Джонсон",
      "Экспонат из презентации по Скале: подписанная обложка Rolling Stone. "
      "К ней добавлен второй элемент — ринговый кадр эпохи Rocky Maivia. "
      "Две эпохи одного человека в одной раме.",
      "Крупные надписи и подписи сохранены точно; мелкий шрифт обложки модель "
      "перерисовывает — ещё одна причина показывать клиенту фото готовой рамы."),
    ]
    for path, name, text, note in EX:
        if not os.path.exists(os.path.join(R, path)):
            continue
        add(f"""<section class="slide white ex" id="__ID__">
  <div class="ex-ph"><img src="{path}" alt=""></div>
  <div class="ex-side">
    <div class="kick" style="margin-bottom:14px">Пример сборки</div>
    <div class="ex-name">{esc(name)}</div>
    <div class="ex-text">{esc(text)}</div>
    <div class="ex-note">{esc(note)}</div>
  </div>
</section>""")

    # финал
    add("""<section class="slide dark" id="__ID__" style="grid-template-rows:1fr auto">
  <div style="padding:76px 66px 0;display:flex;flex-direction:column;justify-content:center">
    <h2 class="serif" style="font-weight:300;font-size:42px;line-height:1.16;color:var(--ivory);max-width:34ch">Новая категория — четыре шага</h2>
    <div class="div-rule" style="margin:26px 0"></div>
    <p style="font:300 15px/1.7 'Inter';color:#b8b2a6;max-width:62ch">Отобрать 6–8 готовых лотов категории с сайта и увидеть,
    чем они отличаются. Сложить мастер-лист с подписями: <span style="color:var(--gold2)">tools_master_sheet.py</span>.
    Записать правило в README рядом с картинками. Проверить генерацией на реальном предмете — и только потом
    считать категорию освоенной.</p>
  </div>
  <div style="padding:24px 66px 40px;border-top:1px solid rgba(169,133,69,.3)">
    <span class="kick" style="letter-spacing:.24em;color:var(--gold2)">stargift.ru</span>
  </div>
</section>""")

    doc = f"""<meta charset="utf-8">
<title>Stargift · База оформления</title>
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
    open(f"{R}/deck_framing.html", "w", encoding="utf-8").write(doc)
    print(f"deck_framing.html: {n} слайдов")


if __name__ == "__main__":
    main()
