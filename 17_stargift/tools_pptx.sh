#!/bin/bash
# Дек → редактируемый PPTX одной командой.
#   ./tools_pptx.sh deck_museum.html STARGIFT_Muzey_futbola.pptx
set -e
DECK="$1"; OUT="$2"
[ -z "$OUT" ] && { echo "usage: $0 deck.html out.pptx"; exit 1; }
D=$(cd "$(dirname "$0")" && pwd)
B="$D/build/$(basename "$DECK" .html)"
python3 "$D/tools_deck_check.py" "$DECK"          # контент не должен уходить за срез
python3 "$D/tools_deck_extract.py" "$DECK" --out "$B"
python3 "$D/tools_deck_to_pptx.py" "$B" --out "$OUT" --root "$D"
python3 /root/.claude/skills/pptx/scripts/office/validate.py "$OUT" 2>&1 | tail -2
