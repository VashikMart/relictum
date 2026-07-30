# База оформления Stargift

Реальные форматы дома. Всё, что генерируем через nano banana, опирается только
на эти референсы: мастер-лист + чистое фото предмета → белая студийная съёмка.

```
img_framing/
├── frames_photo/    рамы — ТОЛЬКО для фотографий, постеров, плакатов
├── stands_boot/     акриловый бокс на основании — для бутс и объёмных вещей
└── generated/       результаты генераций (примеры для показа клиенту)
```

## frames_photo · рамы для фотографий

| файл | формат | под какую категорию |
|---|---|---|
| `frame_jolie_red_velvet.jpg` | золотая рама, бордовый бархат, латунная табличка | кино, экшн, тёплые и красные кадры |
| `frame_tarantino_green_velvet.jpg` | бронзовая рама, зелёный бархат, золотая рамка вокруг фото | кино, два автографа на одном кадре, жёлтые/зелёные кадры |
| `frame_pacino_dark_noMat.jpg` | тёмная состаренная рама, без паспарту, фото во всю площадь | классика кино, тёмные и ночные кадры, крупный формат 41×51 |
| `frame_eminem_float_glass.jpg` | золотая рама, «парящее» фото между стёкол, без паспарту | музыка, современные и светлые кадры |
| `master_frames.jpg` | 2×2 все четыре | **мастер-референс для nano** |

Цвет бархата подбираем под кадр: бордовый — тёплые тона, зелёный — жёлтые
и природные, тёмная рама без паспарту — чёрно-белое и ночное.
Табличка всегда: `PERSONALLY SIGNED BY <ИМЯ>`.

## stands_boot · подставки для бутс

| файл | основание |
|---|---|
| `stand_wood_black.jpg` | красное дерево, чёрная бутса |
| `stand_wood_f50_top.jpg` | красное дерево, вид сверху |
| `stand_wood_copa.jpg` | красное дерево, ракурс три четверти |
| `stand_marble_white.jpg` | белый каррарский мрамор |
| `stand_marble_black.jpg` | чёрный мрамор |
| `stand_marble_green.jpg` | зелёный мрамор |
| `master_stands.jpg` | 3×2 все шесть — **мастер-референс для nano** |

Основание подбираем под цвет предмета: белая бутса — красное дерево или зелёный
мрамор, красная и чёрная — чёрный мрамор, светлая пёстрая — белый мрамор.

## generated · примеры готовых оформлений

| файл | что |
|---|---|
| `cr7_red_marble_black.jpg` | красная Mercurial CR7, чёрный мрамор |
| `cr7_dreamspeed_marble_white.jpg` | Dream Speed, белый мрамор |
| `cr7_lisbon_wood.jpg` | белая Mercurial (Лиссабон-2018), красное дерево |
| `cr7_victory_marble_green.jpg` | Mercurial Victory, зелёный мрамор |
| `rock_maivia_gold_red_velvet.jpg` | фото Rocky Maivia, золотая рама + бордовый бархат |

## Как генерировать

1. Фото предмета сначала прогнать через nano на чистую белую студию.
2. Загрузить в Higgsfield мастер-референс нужной категории
   (`master_frames.jpg` или `master_stands.jpg`).
3. Промпт: «Using the framing/display style from the first reference image …,
   place the item from the second reference …, brass plaque reading
   PERSONALLY SIGNED BY <ИМЯ>. Clean white studio background. Do not change
   the item itself: keep … and the handwritten signature exactly as in the reference.»
4. Проверить глазами: предмет не перерисован, подпись на месте, табличка без
   выдуманного текста.
