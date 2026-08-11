#!/bin/bash
# Дек → редактируемый PPTX одной командой, с проверками до и после.
#   ./tools_pptx.sh deck_museum.html STARGIFT_Muzey_futbola.pptx
set -e
DECK="$1"; OUT="$2"
[ -z "$OUT" ] && { echo "usage: $0 deck.html out.pptx"; exit 1; }
D=$(cd "$(dirname "$0")" && pwd)
B="$D/build/$(basename "$DECK" .html)"

# до сборки: контент не уходит за срез и одно фото не стоит на двух слайдах
python3 "$D/tools_deck_check.py" "$DECK"
python3 "$D/tools_deck_extract.py" "$DECK" --out "$B"
python3 "$D/tools_deck_to_pptx.py" "$B" --out "$OUT" --root "$D"
# после сборки: та ли картинка легла на тот слайд
python3 "$D/tools_pptx_verify.py" "$B" "$OUT"
