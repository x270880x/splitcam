# -*- coding: utf-8 -*-
"""Извлекает переводимые строки страниц /alternatives/<slug>/ в JSON.

   python3 seo/i18n_tools/alt_extract.py <файл.json> <slug> [<slug> …]

🔴 ЛОВУШКА, которая уже стоила повреждённого исходника (2026-09-03):
класс "eyebrow" есть и в шапке страницы, и в карточках related. Шаблон
    <span class="eyebrow">(.*?)</span>\\s*<h4>…
с флагом re.S откатывается от шапки и поглощает ПОЛСТРАНИЦЫ: в строку попадает
9 тысяч символов вместо тридцати. Ошибка не видна ни глазом, ни по числу групп —
групп ровно 3, как и ожидалось. Ловится только проверкой ДЛИН.
Поэтому: якорь на родительский элемент + [^<]* вместо (.*?) + контроль длины.
"""
import re, json, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAXLEN = 1200          # ни одна осмысленная строка страницы не длиннее

def extract(slug, base="alternatives"):
    path = os.path.join(ROOT, base, slug, "index.html") if base else os.path.join(ROOT, slug, "index.html")
    h = open(path, encoding="utf-8").read()
    b = h[h.find('<div class="breadcrumbs">'):h.find("<footer")]
    d = {}
    d["title"]       = re.search(r'<title>(.*?)</title>', h, re.S).group(1)
    d["description"] = re.search(r'<meta name="description" content="(.*?)"', h, re.S).group(1)
    d["keywords"]    = re.search(r'<meta name="keywords" content="(.*?)"', h, re.S).group(1)
    d["h1"]      = re.search(r'<h1[^>]*>(.*?)</h1>', b, re.S).group(1)
    # eyebrow шапки: только ПЕРВЫЙ, и без пересечения тегов
    d["eyebrow"] = re.search(r'<span class="eyebrow">([^<]*)</span>', b).group(1)
    d["sub"]     = re.search(r'<p class="sub">(.*?)</p>', b, re.S).group(1)
    d["badges"]  = re.findall(r'<span class="h-badge">([^<]*)</span>', b)
    d["qa_h"]    = re.search(r'<div class="qa-h">(.*?)</div>', b, re.S).group(1)
    d["qa"]      = re.findall(r'<li>(.*?)</li>', b, re.S)
    d["sec_h"]   = re.findall(r'<h2 class="sec-h">(.*?)</h2>', b, re.S)
    d["sec_p"]   = re.findall(r'<p class="sec-p">(.*?)</p>', b, re.S)
    d["cards"]   = [[m.group(1), m.group(2)] for m in
                    re.finditer(r'<div class="reason">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', b, re.S)]
    d["table_head"] = re.findall(r'<th>([^<]*)</th>', b)
    d["rows"]    = [re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)
                    for r in re.findall(r'<tr>(.*?)</tr>', b, re.S) if "<td" in r]
    d["faq"]     = [[m.group(1), m.group(2)] for m in
                    re.finditer(r'<summary>(.*?)</summary>\s*<p>(.*?)</p>', b, re.S)]
    # ЯКОРЬ на related-card — см. предупреждение в шапке файла
    d["related"] = [[m.group(1), m.group(2), m.group(3)] for m in
                    re.finditer(r'<a class="related-card"[^>]*>\s*<span class="eyebrow">([^<]*)</span>'
                                r'\s*<h4>([^<]*)</h4>\s*<p>([^<]*)</p>', b)]
    # Анимированный блок live-look (появился на snap-camera 2026-09-06). Без этих ключей
    # его текст молча остался бы английским во всех 34 локалях — ровно тот случай, о котором
    # предупреждает комментарий про <h4> на странице Restream.
    d["sec_eyebrow"] = re.findall(r'<span class="sec-eyebrow">([^<]*)</span>', b)
    d["steps"]       = re.findall(r'<div class="sc-step"><span>(.*?)</span></div>', b, re.S)
    d["demo_out"]    = re.findall(r'<p class="sc-out"><span>(.*?)</span>', b, re.S)
    d["demo_alt"]    = re.findall(r'<svg[^>]*aria-label="([^"]*)"', b)
    # Схема-конвейер (появилась на nvidia-broadcast 2026-09-06)
    d["pipe_cap"]  = re.findall(r'<div class="nb-cap">([^<]*)</div>', b)
    d["pipe_p"]    = re.findall(r'<div class="nb-box[^"]*">\s*<div class="nb-cap">[^<]*</div>\s*<p>(.*?)</p>', b, re.S)
    d["pipe_src"]  = re.findall(r'<span class="nb-src">(?:<svg.*?</svg>)?([^<]*)</span>', b, re.S)
    d["pipe_gate"] = re.findall(r'<span class="nb-gate">([^<]*)</span>', b)
    d["pipe_out"]  = re.findall(r'<span class="nb-out">([^<]*)</span>', b)
    d["pipe_note"] = re.findall(r'<p class="nb-note">(.*?)</p>', b, re.S)
    d["cta"]     = [re.search(r'<section class="cta-block">\s*<h2>(.*?)</h2>', b, re.S).group(1),
                    re.search(r'<section class="cta-block">.*?<p>(.*?)</p>', b, re.S).group(1)]
    return d

# Строки, которые НЕ извлекаются намеренно: кнопки, заголовок related и подпись LIVE берутся
# сборщиком локали у страницы-донора и уже переведены там; названия площадок и продуктов
# одинаковы во всех языках.
DONOR_OR_BRAND = re.compile(
    r'^(Free Download|See the table|Jump to comparison|Related guides|LIVE|YouTube|Twitch|Facebook|Kick|Zoom|Teams|'
    r'Microsoft Teams|Google Meet|Meet|Discord|OBS|SplitCam|Snapchat|Snap Camera|Lens Studio|'
    r'NVIDIA Broadcast|NVIDIA|Windows|macOS|Mac)$')

BASELINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coverage_baseline.json")

def _baseline():
    try: return json.load(open(BASELINE, encoding="utf-8"))
    except Exception: return {}

def coverage(slug, d, base="alternatives"):
    """Что на странице видно, но не извлеклось. Ловит ЛЮБОЙ новый блок, а не только известные.

    Появилось 2026-09-06: две подряд собранные страницы получили собственные секции
    (анимированный кадр камеры, схема-конвейер), и текст обеих извлекатель не видел —
    он остался бы английским во всех 34 локалях, ничем себя не выдав."""
    path = os.path.join(ROOT, base, slug, "index.html") if base else os.path.join(ROOT, slug, "index.html")
    h = open(path, encoding="utf-8").read()
    b = h[h.find('<div class="breadcrumbs">'):h.find("<footer")]
    b = re.sub(r'<script.*?</script>|<style.*?</style>', '', b, flags=re.S)
    b = re.sub(r'<details class="lang[^"]*".*?</details>', '', b, flags=re.S)
    norm = lambda s: re.sub(r'\s+', ' ', re.sub('<[^>]*>', ' ', s)).strip()
    covered = " ".join(norm(x) for x in re.findall(r'"([^"]*)"', json.dumps(d, ensure_ascii=False)))
    out, seen = [], set()
    for m in re.finditer(r'>([^<>]{4,})<', b):
        t = norm(m.group(1))
        if len(re.findall(r"[A-Za-z]", t)) < 4: continue      # значки, числа, разделители
        # стрелки и значки в подписях кнопок («⬇ Free Download», «See the table ↓») — не текст
        bare = re.sub(r'^[^\w(]+|[^\w).]+$', '', t).strip()
        if t in covered or DONOR_OR_BRAND.match(bare): continue
        if t not in seen: seen.add(t); out.append(t)
    # Храповик: строки, уже принятые для этой страницы, не считаются. Страницы, собранные до
    # появления проверки (obs — рукописный шаблон, manycam), переведены другим путём: проверено
    # 2026-09-06, в локалях этот текст НЕ английский. Новое непокрытие падает.
    known = set(_baseline().get(slug, []))
    return [t for t in out if t not in known]

def check(slug, d):
    """Контроль длин — единственное, что ловит «съевшую полстраницы» регулярку."""
    bad = []
    def walk(key, v):
        if isinstance(v, str):
            if len(v) > MAXLEN: bad.append(f"{key}: {len(v)} симв.")
        elif isinstance(v, list):
            for i, x in enumerate(v): walk(f"{key}[{i}]", x)
    for k, v in d.items(): walk(k, v)
    if not d["related"]: bad.append("related: пусто — якорь не сработал")
    if len(d["rows"]) < 3: bad.append(f"rows: всего {len(d['rows'])}")
    # Пустой список — тихая потеря целого блока текста. Страница Restream писалась
    # вручную и использовала <h4> в карточках вместо <h3>: извлеклось 0 карточек,
    # и текст остался бы английским во всех 34 локалях, никак себя не выдав.
    waived = set(_baseline().get("_waive_checks", {}).get(slug, []))
    for key in ("cards", "faq", "badges", "qa", "sec_h", "sec_p", "table_head", "cta"):
        if key in waived: continue
        if not d.get(key): bad.append(f"{key}: ПУСТО — блок не извлёкся")
    # блок live-look есть не на всех страницах; если он есть — обязан извлечься целиком
    src = open(os.path.join(ROOT, "alternatives", slug, "index.html"), encoding="utf-8").read()
    if "sc-step" in src:
        for key, want in (("steps", 4), ("demo_out", 1), ("demo_alt", 1), ("sec_eyebrow", 1)):
            if len(d.get(key, [])) < want: bad.append(f"{key}: извлечено {len(d.get(key, []))}, ожидалось {want}")
    if "nb-cap" in src:
        for key in ("pipe_cap", "pipe_p", "pipe_src", "pipe_gate", "pipe_out", "pipe_note"):
            if not d.get(key): bad.append(f"{key}: ПУСТО — схема-конвейер не извлеклась")
    left = coverage(slug, d)
    if left:
        bad.append(f"НЕ ПОКРЫТО извлечением ({len(left)}): " + " | ".join(x[:52] for x in left[:4])
                   + f"  → если это законно, внеси в {os.path.basename(BASELINE)}")
    return bad

if __name__ == "__main__":
    out, slugs = sys.argv[1], sys.argv[2:]
    # slug вида "root:phone-as-webcam" означает страницу в корне сайта
    def split(sl): return (sl[5:], "") if sl.startswith("root:") else (sl, "alternatives")
    res = {}
    fail = False
    for s in slugs:
        s, base = split(s)
        d = extract(s, base)
        bad = check(s, d)
        n = sum(1 for _ in json.dumps(d))
        mx = max(len(x) for x in re.findall(r'"([^"]*)"', json.dumps(d, ensure_ascii=False)))
        if bad:
            print(f"  🔴 {s}: {'; '.join(bad)}"); fail = True
        else:
            print(f"  ✓ {s}: cards={len(d['cards'])} rows={len(d['rows'])} faq={len(d['faq'])} "
                  f"badges={len(d['badges'])} qa={len(d['qa'])} sec_h={len(d['sec_h'])} "
                  f"related={len(d['related'])} · макс. строка {mx}")
        res[s] = d
    if fail: raise SystemExit("извлечение отклонено")
    json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"  → {out}")
