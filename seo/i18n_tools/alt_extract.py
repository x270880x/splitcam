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

def extract(slug):
    h = open(os.path.join(ROOT, "alternatives", slug, "index.html"), encoding="utf-8").read()
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
    d["cta"]     = [re.search(r'<section class="cta-block">\s*<h2>(.*?)</h2>', b, re.S).group(1),
                    re.search(r'<section class="cta-block">.*?<p>(.*?)</p>', b, re.S).group(1)]
    return d

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
    return bad

if __name__ == "__main__":
    out, slugs = sys.argv[1], sys.argv[2:]
    res = {}
    fail = False
    for s in slugs:
        d = extract(s)
        bad = check(s, d)
        n = sum(1 for _ in json.dumps(d))
        mx = max(len(x) for x in re.findall(r'"([^"]*)"', json.dumps(d, ensure_ascii=False)))
        if bad:
            print(f"  🔴 {s}: {'; '.join(bad)}"); fail = True
        else:
            print(f"  ✓ {s}: related={len(d['related'])}, rows={len(d['rows'])}, "
                  f"faq={len(d['faq'])}, самая длинная строка {mx} симв.")
        res[s] = d
    if fail: raise SystemExit("извлечение отклонено")
    json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"  → {out}")
