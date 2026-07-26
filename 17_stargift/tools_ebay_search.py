#!/usr/bin/env python3
"""
Поиск лотов на eBay через официальное Browse API → CSV в формате каталога Stargift.

Ключи НИКОГДА не хранятся в репозитории. Берутся из переменных окружения
EBAY_CLIENT_ID / EBAY_CLIENT_SECRET, либо из файла, путь к которому лежит
в EBAY_ENV_FILE (по умолчанию ~/.ebay.env, формат KEY=VALUE построчно).

Примеры:
    python3 tools_ebay_search.py "Lionel Messi signed" --limit 40 --out messi.csv
    python3 tools_ebay_search.py "Maradona signed jersey" --min 500 --max 6000 --no-frame
    python3 tools_ebay_search.py "Mike Tyson signed glove" --group БОКС --details

Что делает:
  • только фиксированная цена (аукционы не берём — нужна финальная цена, а не ставки);
  • --details подтягивает карточку лота: все фото в s-l1600, характеристики, описание;
  • сертификатор распознаётся и приводится к трём разрешённым (Beckett / JSA / PSA-DNA),
    всё остальное → пустая строка (правило дома: других имён в презентациях не пишем);
  • лоты в раме помечаются, --no-frame их выкидывает (приоритет — без рамы);
  • колонка «Цена» остаётся ПУСТОЙ: рублёвую цену ставит человек, формулы тут нет.
"""

import argparse, base64, csv, json, os, re, sys, time, urllib.parse, urllib.request

API = "https://api.ebay.com"
TOKEN_CACHE = "/tmp/.ebay_token.json"

# ---------------------------------------------------------------- credentials

def creds():
    cid, sec = os.environ.get("EBAY_CLIENT_ID"), os.environ.get("EBAY_CLIENT_SECRET")
    if cid and sec:
        return cid, sec
    path = os.environ.get("EBAY_ENV_FILE", os.path.expanduser("~/.ebay.env"))
    if os.path.exists(path):
        env = {}
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
        cid, sec = env.get("EBAY_CLIENT_ID"), env.get("EBAY_CLIENT_SECRET")
    if not (cid and sec):
        sys.exit("Нет ключей eBay. Задай EBAY_CLIENT_ID и EBAY_CLIENT_SECRET "
                 "или положи их в файл из EBAY_ENV_FILE.")
    return cid, sec


def token():
    if os.path.exists(TOKEN_CACHE):
        try:
            c = json.load(open(TOKEN_CACHE))
            if c["exp"] > time.time() + 120:
                return c["token"]
        except Exception:
            pass
    cid, sec = creds()
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope",
    }).encode()
    req = urllib.request.Request(
        API + "/identity/v1/oauth2/token", data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "Authorization": "Basic " + base64.b64encode(f"{cid}:{sec}".encode()).decode()})
    d = json.load(urllib.request.urlopen(req, timeout=40))
    tok = d["access_token"]
    json.dump({"token": tok, "exp": time.time() + int(d.get("expires_in", 7200))},
              open(TOKEN_CACHE, "w"))
    os.chmod(TOKEN_CACHE, 0o600)
    return tok


def get(path, params, tok, market="EBAY_US"):
    url = API + path + ("?" + urllib.parse.urlencode(params, doseq=True) if params else "")
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + tok,
        "X-EBAY-C-MARKETPLACE-ID": market,
        "Accept": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=60))

# ------------------------------------------------------------------ разбор лота

# только три имени, разрешённые в презентациях
CERTS = [
    (r"\bPSA\s*/?\s*DNA\b|\bPSA\b(?!.{0,12}\bgrade)", "PSA/DNA"),
    (r"\bBeckett\b|\bBAS\b(?![A-Za-z])",              "Beckett"),
    (r"\bJSA\b|\bJames\s+Spence\b",                    "JSA"),
]
FRAME_RE = re.compile(r"\bframed?\b|\bframe\b|\bshadow\s*box\b|в\s*раме", re.I)


def certifier(*texts):
    blob = " ".join(t or "" for t in texts)
    for pat, name in CERTS:
        if re.search(pat, blob, re.I):
            return name
    return ""            # Icons, Fanatics, COA магазина и т.п. — не показываем


def hi(url):
    """миниатюра eBay → максимальное разрешение"""
    return re.sub(r"/s-l\d+\.(jpg|jpeg|png|webp)", r"/s-l1600.\1", url or "")


def summarize(it):
    title = it.get("title", "")
    price = (it.get("price") or {}).get("value")
    return {
        "title":  title,
        "usd":    float(price) if price else None,
        "cur":    (it.get("price") or {}).get("currency", "USD"),
        "id":     it.get("legacyItemId") or "",
        "url":    it.get("itemWebUrl", ""),
        "img":    hi((it.get("image") or {}).get("imageUrl", "")),
        "seller": (it.get("seller") or {}).get("username", ""),
        "cond":   it.get("condition") or "",
        "cert":   certifier(title),
        "framed": bool(FRAME_RE.search(title)),
        "photos": [],
        "aspects": {},
        "desc":   "",
        "rest_id": it.get("itemId", ""),
    }


def enrich(row, tok):
    """карточка лота: все фото, характеристики, описание"""
    try:
        d = get("/buy/browse/v1/item/" + urllib.parse.quote(row["rest_id"], safe=""), None, tok)
    except Exception as e:
        print(f"  ! карточка {row['id']}: {e}", file=sys.stderr)
        return row
    imgs = [d.get("image") or {}] + (d.get("additionalImages") or [])
    row["photos"] = [hi(i.get("imageUrl", "")) for i in imgs if i.get("imageUrl")]
    if row["photos"]:
        row["img"] = row["photos"][0]
    row["aspects"] = {a["name"]: a["value"] for a in (d.get("localizedAspects") or [])}
    desc = re.sub(r"<[^>]+>", " ", d.get("description") or "")
    row["desc"] = re.sub(r"\s+", " ", desc).strip()
    row["cert"] = certifier(row["title"], row["desc"], json.dumps(row["aspects"], ensure_ascii=False))
    row["framed"] = row["framed"] or bool(FRAME_RE.search(row["desc"][:400]))
    return row

# ------------------------------------------------------------------------ вывод

COLS = ["Название", "Краткое описание", "Полное описание", "Цена", "Валюта", "Сертификат",
        "Группа", "URL на сайте", "URL главного фото", "Закупка USD", "eBay URL",
        "Комментарий к фото"]


def write_csv(rows, path, group):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(COLS)
        for r in rows:
            extra = " | ".join(r["photos"][1:6])
            w.writerow([
                r["title"], "", r["desc"][:900], "", "RUB", r["cert"], group, "",
                r["img"], f"{r['usd']:.2f}" if r["usd"] else "", r["url"],
                (f"фото всего: {len(r['photos'])}. Ещё ракурсы: {extra}" if extra else ""),
            ])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--min", type=float, default=None, help="цена от, USD")
    p.add_argument("--max", type=float, default=None, help="цена до, USD")
    p.add_argument("--group", default="")
    p.add_argument("--market", default="EBAY_US")
    p.add_argument("--no-frame", action="store_true", help="выкинуть лоты в раме")
    p.add_argument("--certified", action="store_true", help="только Beckett / JSA / PSA-DNA")
    p.add_argument("--details", action="store_true", help="тянуть карточку каждого лота")
    p.add_argument("--sort", default="", help="price | -price | newlyListed; пусто = релевантность")
    p.add_argument("--out", default="ebay_found.csv")
    a = p.parse_args()

    tok = token()
    filt = ["buyingOptions:{FIXED_PRICE}"]
    if a.min is not None or a.max is not None:
        filt.append("price:[%s..%s]" % (a.min if a.min is not None else "",
                                        a.max if a.max is not None else ""))
        filt.append("priceCurrency:USD")

    rows, offset = [], 0
    while len(rows) < a.limit:
        params = {"q": a.query, "filter": ",".join(filt),
                  "limit": min(200, a.limit - len(rows)), "offset": offset}
        if a.sort:
            params["sort"] = a.sort
        d = get("/buy/browse/v1/item_summary/search", params, tok, a.market)
        batch = d.get("itemSummaries") or []
        if not batch:
            break
        rows += [summarize(i) for i in batch]
        offset += len(batch)
        if offset >= int(d.get("total", 0)):
            break
    print(f"найдено всего: {d.get('total', '?')}, взято: {len(rows)}")

    if a.no_frame:
        n = len(rows); rows = [r for r in rows if not r["framed"]]
        print(f"без рамы: {len(rows)} (отсеяно {n - len(rows)})")

    if a.details:
        for i, r in enumerate(rows, 1):
            enrich(r, tok)
            print(f"  [{i}/{len(rows)}] {r['title'][:58]} · фото {len(r['photos'])} · {r['cert'] or '—'}")

    if a.certified:
        n = len(rows); rows = [r for r in rows if r["cert"]]
        print(f"с Beckett/JSA/PSA-DNA: {len(rows)} (отсеяно {n - len(rows)})")

    write_csv(rows, a.out, a.group)
    print(f"\n→ {a.out} ({len(rows)} лотов). Колонка «Цена» пустая — рублёвую ставим руками.")


if __name__ == "__main__":
    main()
