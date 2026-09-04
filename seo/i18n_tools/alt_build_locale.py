# -*- coding: utf-8 -*-
"""Собирает /<loc>/alternatives/<slug>/ — обрамление от донора той же локали,
содержимое от EN-страницы, тексты из перевода.

   python3 seo/i18n_tools/alt_build_locale.py <slug> <переводы.json>

переводы.json: [{"loc":"ru","strings":{...}}, …] — ключи как в alt_strings.json.

Донор: <loc>/alternatives/obs/ — та же глубина вложенности, поэтому относительные
пути, меню, подвал и <html lang/dir> гарантированно настоящие.
"""
import re, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def chrome_of(path):
    """Возвращает (head_до_body, шапка, подвал_и_хвост) страницы-донора."""
    h = open(path, encoding="utf-8").read()
    b = h.find("<body>")
    bc = h.find('<div class="breadcrumbs">')
    ft = h.find("<footer")
    if not (0 < b < bc < ft):
        raise SystemExit(f"донор нестандартной структуры: {path}")
    return h[:b], h[b:bc], h[ft:]

def build(slug, loc, S, base="alternatives", donor_page="alternatives/obs"):
    # донор ОБЯЗАН быть той же глубины вложенности, что и собираемая страница:
    # относительные пути, меню и подвал зависят от глубины.
    donor = os.path.join(ROOT, loc, donor_page, "index.html")
    en    = os.path.join(ROOT, base, slug, "index.html") if base else os.path.join(ROOT, slug, "index.html")
    if not os.path.exists(donor):
        return None, f"нет донора {loc}/{donor_page}/"
    head, top, tail = chrome_of(donor)
    ehead, _, _ = chrome_of(en)
    eh = open(en, encoding="utf-8").read()
    body = eh[eh.find('<div class="breadcrumbs">'):eh.find("<footer")]

    URL = f"https://splitcam.com/{loc}/{base}/{slug}" if base else f"https://splitcam.com/{loc}/{slug}"
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    # ── head: берём EN-head (там уже вся структура страницы) и локализуем
    nh = ehead
    def setm(pat, val, s):
        s2, n = re.subn(pat, lambda m: m.group(1) + val + m.group(3), s, count=1, flags=re.S)
        return s2 if n else s
    for pat, key in ((r'(<title>)(.*?)(</title>)', "title"),
                     (r'(<meta name="description" content=")(.*?)(")', "description"),
                     (r'(<meta name="keywords" content=")(.*?)(")', "keywords"),
                     (r'(<meta property="og:title" content=")(.*?)(")', "title"),
                     (r'(<meta property="og:description" content=")(.*?)(")', "description"),
                     (r'(<meta name="twitter:title" content=")(.*?)(")', "title"),
                     (r'(<meta name="twitter:description" content=")(.*?)(")', "description")):
        if key in S:
            nh = setm(pat, esc(re.sub(r'\s+', ' ', S[key]).strip()), nh)
    for pat in (r'(<link rel="canonical" href=")(.*?)(")',
                r'(<meta property="og:url" content=")(.*?)(")'):
        nh = setm(pat, URL, nh)
    # <html lang/dir> — от донора
    dm = re.search(r'<html[^>]*>', head)
    if dm:
        nh = re.sub(r'<html[^>]*>', dm.group(0), nh, count=1)
    # hreflang: пока локалей у страницы нет — только self + x-default (см. CLAUDE.md)
    nh = re.sub(r'[ \t]*<link rel="alternate" hreflang="(?!x-default")[^"]+" href="[^"]*"\s*/?>\n?', '', nh)
    nh = re.sub(r'(<link rel="alternate" hreflang="x-default" href=")[^"]*(")',
                r'\g<1>https://splitcam.com/' + (base + '/' if base else '') + slug + r'\g<2>', nh)

    # ── тело: подставляем переводы по позициям
    nb = body
    def rep_all(pattern, values, s):
        it = iter(values)
        def r(m):
            try: v = next(it)
            except StopIteration: return m.group(0)
            return m.group(1) + v + m.group(3)
        return re.sub(pattern, r, s, flags=re.S)

    if "h1" in S:      nb = setm(r'(<h1[^>]*>)(.*?)(</h1>)', S["h1"], nb)
    if "eyebrow" in S: nb = setm(r'(<span class="eyebrow">)(.*?)(</span>)', S["eyebrow"], nb)
    if "sub" in S:     nb = setm(r'(<p class="sub">)(.*?)(</p>)', S["sub"], nb)
    if "qa_h" in S:    nb = setm(r'(<div class="qa-h">)(.*?)(</div>)', S["qa_h"], nb)
    for key, pat in (("badges", r'(<span class="h-badge">)(.*?)(</span>)'),
                     ("qa",     r'(<li>)(.*?)(</li>)'),
                     ("sec_h",  r'(<h2 class="sec-h">)(.*?)(</h2>)'),
                     ("sec_p",  r'(<p class="sec-p">)(.*?)(</p>)'),
                     ("table_head", r'(<th>)(.*?)(</th>)')):
        if key in S: nb = rep_all(pat, S[key], nb)
    if "cards" in S:
        it = iter(S["cards"])
        def rc(m):
            try: t, p = next(it)
            except StopIteration: return m.group(0)
            return f'<div class="reason">\n        <h3>{t}</h3>\n        <p>{p}</p>'
        nb = re.sub(r'<div class="reason">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', rc, nb, flags=re.S)
    if "rows" in S:
        it = iter(S["rows"])
        def rr(m):
            try: cells = next(it)
            except StopIteration: return m.group(0)
            tds = re.findall(r'<td([^>]*)>(.*?)</td>', m.group(1), re.S)
            if len(tds) != len(cells): return m.group(0)
            inner = "".join(f'<td{a}>{c}</td>' for (a, _), c in zip(tds, cells))
            return f'<tr>{inner}</tr>'
        nb = re.sub(r'<tr>((?:(?!</tr>).)*?<td.*?)</tr>', rr, nb, flags=re.S)
    if "faq" in S:
        it = iter(S["faq"])
        def rf(m):
            try: q, a = next(it)
            except StopIteration: return m.group(0)
            return f'<summary>{q}</summary>\n        <p>{a}</p>'
        nb = re.sub(r'<summary>(.*?)</summary>\s*<p>(.*?)</p>', rf, nb, flags=re.S)
    if "related" in S:
        it = iter(S["related"])
        def rl(m):
            try: e, t, p = next(it)
            except StopIteration: return m.group(0)
            return m.group(1) + e + m.group(2) + t + m.group(3) + p + m.group(4)
        # ЯКОРЬ на related-card обязателен: класс eyebrow есть и в шапке страницы,
        # а '(.*?)' с re.S откатывается и съедает всё между ними. Так уже терялась страница.
        nb = re.sub(r'(<a class="related-card"[^>]*>\s*<span class="eyebrow">)[^<]*(</span>\s*<h4>)[^<]*(</h4>\s*<p>)[^<]*(</p>)',
                    rl, nb)
    if "cta" in S and len(S["cta"]) == 2:
        nb = re.sub(r'(<section class="cta-block">\s*<h2>)(.*?)(</h2>)',
                    lambda m: m.group(1) + S["cta"][0] + m.group(3), nb, count=1, flags=re.S)
        nb = re.sub(r'(<section class="cta-block">.*?<p>)(.*?)(</p>)',
                    lambda m: m.group(1) + S["cta"][1] + m.group(3), nb, count=1, flags=re.S)
    # ── кнопки и хлебные крошки: берём готовый перевод у донора, а не у переводчика.
    # Эти строки одинаковы на всех страницах рубрики, и в локали они уже выверены.
    dh = open(donor, encoding="utf-8").read()
    db = dh[dh.find('<div class="breadcrumbs">'):dh.find("<footer")]
    for cls in ("btn-primary", "btn-ghost"):
        em = re.search(r'<a[^>]*class="[^"]*' + cls + r'[^"]*"[^>]*>([^<]*)</a>', body)
        dm = re.search(r'<a[^>]*class="[^"]*' + cls + r'[^"]*"[^>]*>([^<]*)</a>', db)
        if em and dm and em.group(1) != dm.group(1):
            nb = nb.replace(">" + em.group(1) + "</a>", ">" + dm.group(1) + "</a>")
    # заголовок блока «Related guides» — тоже у донора («Гайды по теме» и т.п.).
    # В извлекаемые строки он не попадает: там только содержимое карточек.
    er = re.search(r'(<h3[^>]*>)([^<]*)(</h3>\s*<div class="related-grid")', body)
    dr = re.search(r'<h3[^>]*>([^<]*)</h3>\s*<div class="related-grid"', db)
    if not dr:
        # у донора нет блока related (корневые страницы) — берём заголовок
        # у /alternatives/obs/ той же локали, там он переведён гарантированно
        alt = os.path.join(ROOT, loc, "alternatives", "obs", "index.html")
        if os.path.exists(alt):
            ah = open(alt, encoding="utf-8").read()
            dr = re.search(r'<h3[^>]*>([^<]*)</h3>\s*<div class="related-grid"',
                           ah[ah.find('<div class="breadcrumbs">'):ah.find("<footer")])
    if er and dr and er.group(2) != dr.group(1):
        nb = nb.replace(er.group(1) + er.group(2) + "</h3>", er.group(1) + dr.group(1) + "</h3>", 1)

    # хлебные крошки: структура донора, последний элемент — имя нашего конкурента
    ec = re.search(r'<div class="breadcrumbs">(.*?)</div>', body, re.S)
    dc = re.search(r'<div class="breadcrumbs">(.*?)</div>', db, re.S)
    if ec and dc:
        rival = re.findall(r'<span>([^<]*)</span>', ec.group(1))
        new_c = re.sub(r'(<span>)[^<]*(</span>\s*)$', r'\g<1>' + (rival[-1] if rival else slug) + r'\g<2>',
                       dc.group(1))
        nb = nb.replace(ec.group(0), '<div class="breadcrumbs">' + new_c + '</div>', 1)

    # внутренние ссылки страницы — на локальные версии
    # Префикс локали ставим ТОЛЬКО там, где локализованная страница реально есть.
    # /download локализованной версии не имеет — он один на весь сайт, и слепое
    # добавление префикса давало 68 битых ссылок (по 2 на каждую из 34 локалей).
    def localize_href(m):
        path = m.group(1)
        if not path:
            return m.group(0)
        if os.path.exists(os.path.join(ROOT, loc, path.rstrip("/"), "index.html")):
            return f'href="https://splitcam.com/{loc}/{path}"'
        return m.group(0)
    nb = re.sub(r'href="https://splitcam\.com/(?!' + loc + r'/)([a-z0-9/-]*)"', localize_href, nb)
    # JSON-LD: переносим локализованные заголовки/описание/FAQ
    def fix_ld(m):
        try: g = json.loads(m.group(1))
        except Exception: return m.group(0)
        strip = lambda s: re.sub(r'\s+', ' ', re.sub('<[^>]*>', '', s)).strip()
        for node in g.get("@graph", []):
            if node.get("@type") == "SoftwareApplication":
                node["url"] = URL
                if "description" in S: node["description"] = strip(S["description"])
            if node.get("@type") == "BreadcrumbList":
                for li in node.get("itemListElement", []):
                    if li.get("position") == 3: li["item"] = URL
            if node.get("@type") == "FAQPage" and "faq" in S:
                for q, (nq, na) in zip(node.get("mainEntity", []), S["faq"]):
                    q["name"] = strip(nq)
                    q.setdefault("acceptedAnswer", {})["text"] = strip(na)
        return '<script type="application/ld+json">\n' + json.dumps(g, ensure_ascii=False, indent=2) + '\n</script>'
    nh = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_ld, nh, count=1, flags=re.S)

    # Защита от «съеденного» тела. Сравнивать ДЛИНУ нельзя: японский, корейский и
    # китайский короче английского в разы, и порог по символам их ложно забракует
    # (проверено — ja/ko/zh дали 6700–7700 против 10153 при полностью верной странице).
    # Инвариант, не зависящий от языка, — СТРУКТУРА: число элементов каждого типа.
    STRUCT = (r'<td[^>]*>', r'<summary>', r'<h-?badge|h-badge', r'<h2 class="sec-h">',
              r'<div class="reason">', r'<h4>', r'<tr>', r'<span class="h-badge">')
    for pat in STRUCT:
        want, got = len(re.findall(pat, body)), len(re.findall(pat, nb))
        if want != got:
            return None, (f"структура нарушена: {pat} — {got} против {want} в оригинале; "
                          f"страница НЕ записана")
    dst = os.path.join(ROOT, loc, base, slug) if base else os.path.join(ROOT, loc, slug)
    os.makedirs(dst, exist_ok=True)
    open(os.path.join(dst, "index.html"), "w", encoding="utf-8").write(nh + top + nb + tail)
    return os.path.join(loc, "alternatives", slug, "index.html"), None

if __name__ == "__main__":
    slug, tf = sys.argv[1], sys.argv[2]
    base = sys.argv[3] if len(sys.argv) > 3 else "alternatives"
    donor_page = sys.argv[4] if len(sys.argv) > 4 else "alternatives/obs"
    data = json.load(open(tf, encoding="utf-8"))
    ok = err = 0
    for item in data:
        p, e = build(slug, item["loc"], item["strings"], base, donor_page)
        if e: print(f"  🔴 {item['loc']}: {e}"); err += 1
        else: ok += 1
    print(f"  собрано: {ok}, ошибок: {err}")
