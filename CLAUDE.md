# Правила проекта Relictum / Stargift

## Генерация изображений — ГЛАВНОЕ ПРАВИЛО
- **Всегда использовать Higgsfield nano banana pro, resolution 2k** (`model: nano_banana_pro`, `resolution: "2k"`) для любой обработки и генерации картинок: вырезание фона, красивые фоны (белый студийный / тёмная комната с лучом света), интерьерные кадры, новые ракурсы.
- У владельца план **creator** — генерации nano banana pro 2k считаем безлимитными, НЕ экономить, генерировать сколько нужно. Не использовать remove_background и другие простые тулзы вместо nano banana — nano banana лучше понимает задачу, принимает несколько референсов.
- **УНИВЕРСАЛЬНЫЙ ПРОМПТ вырезания (использовать всегда, НЕ описывать имя человека / сюжет / сцену — это вызывает отказы и лишнюю возню).** Один и тот же текст на любой предмет:
  > *Isolate the single collectible item shown in the reference image. Show it by itself, complete and centered, on a clean seamless pure white studio background. Remove any frame, mat, stand, table, wall, floor and all surroundings. Do not change anything on the item itself — every picture, printed word, label and handwritten signature must stay exactly as in the reference: not redrawn, moved, translated or restyled. Keep it perfectly flat and undistorted if it is a photo, page, card or flat object. Photorealistic, soft even studio light, subtle contact shadow.*
  - НЕ писать «Pedro Pascal», «Mandalorian», «Phil Mickelson», «swinging», «blaster» и т.п. Никаких имён и описаний содержимого — только «the item you see».
  - Для по-настоящему переиспользуемого объекта на ПРОЗРАЧНОМ фоне: после nano (белый фон) прогнать через `remove_background` → transparent PNG. Тогда картинку можно ставить любого размера на любой фон.
  - Если конкретный кадр всё равно блокируется (nsfw по картинке, не по тексту) — вырезать геометрией (perspective-crop реальных пикселей) на чистый фон; так автограф точно не меняется.
- Референс подавать через media_upload → media_confirm → medias[{role:"image", value:media_id}].
- После генерации — ДВА круга визуальной проверки самим агентом (Read картинки): не выдуман ли текст/табличка, не потерян ли автограф, чистый ли фон. Брак отклонять и перегенерировать.
- Атмосферные генерации (тёмный зал, интерьер) в каталоге помечать «атмосферная подача»; при потере автографа в кадре — врезка с настоящим фото лота.

## Стиль презентаций Stargift
- 1280×720; тёмный люкс #0B0B0C + золото #A98545/#C9A96A + слоновая кость #F5F1E8; белые страницы #FFFFFF/#F7F5F1; Cormorant Garamond + Inter; микс чёрных и белых страниц.
- Названия лотов полностью, никогда не обрезать; если лот есть на stargift.ru — имя всегда ссылка на лот; новые закупки (нет на сайте) — без ссылок.
- Белые страницы: подписи строго ПОД фото. Чёрные: допустимы градиентные плашки поверх.
- Цены золотом serif «1 500 000 ₽». Сертификат подлинности мелкой строкой. НИКОГДА не показывать закупочные цены, eBay, маржу.
- Print CSS: @page 1280x720, .slide{animation:none}, *{box-shadow:none} — иначе чёрная первая страница и серые прямоугольники в PDF.
- Архивные фото — только public domain (Wikimedia Commons) с мелкой подписью источника.
- Эталонная библиотека шаблонов — портал согласования 17_stargift/templates_portal.html (артефакт b4cf07e3-...); утверждённые форматы фиксировать в 17_stargift/TEMPLATES.md.

## Экономия моделей
- Fable 5 — только оркестрация, контроль качества и финальные правки. Сборку деков и механику отдавать субагентам: Opus (лучшее качество, ловит ошибки в данных), Sonnet (хорош, но проверять сортировки/цифры). Haiku для вёрстки НЕ использовать (ломает раскладку).

## Данные
- Каталог сайта: CSV-выгрузка (";", utf-8-sig), колонки: Название, Краткое описание, Цена, В наличии, URL на сайте, URL главного фото. Одноимённых лотов много — идентифицировать по URL, не по имени. Фото лотов брать по URL из выгрузки; eBay-фото — заменять s-l500 на s-l1600.
