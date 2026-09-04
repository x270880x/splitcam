# -*- coding: utf-8 -*-
"""BreadcrumbList в JSON-LD := видимые хлебные крошки страницы (источник истины — то, что видит человек).

   python3 seo/crumb_sync.py --check            расхождения по всему сайту
   python3 seo/crumb_sync.py --fix [страницы…]  починить (по умолчанию — весь сайт)

Найдено 2026-09-05 аудитом page_audit (T11): 309 локальных страниц, собранных alt_build_locale.py,
несли АНГЛИЙСКИЙ BreadcrumbList (имена «Alternatives», «ManyCam alternative», корень https://splitcam.com/),
хотя видимые крошки локализованы; ещё 244 страницы имели короткую видимую метку («OBS») при полном имени
в разметке («OBS Alternative»). Google требует, чтобы разметка повторяла видимое — синхронизируем механически.
"""
import re, os, sys, json, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "seo"))
from i18n import LANG_ORDER, LANG_PATH, page_url
from i18n_wire import PAGE_PATHS
strip = lambda s: html.unescape(re.sub(r'\s+', ' ', re.sub('<[^>]*>', '', s))).strip()

def visible(h):
    m = re.search(r'<div class="breadcrumbs">(.*?)</div>', h, re.S)
    if not m: return None
    items = []
    for a in re.finditer(r'<a href="([^"]+)">(.*?)</a>|<span>(.*?)</span>', m.group(1), re.S):
        if a.group(1): items.append((strip(a.group(2)), a.group(1)))
        elif strip(a.group(3)) and strip(a.group(3)) != "/": items.append((strip(a.group(3)), None))
    return items

def sync(path, loc, page, fix):
    h = open(path, encoding="utf-8").read()
    vis = visible(h)
    if not vis: return None
    url = page_url(LANG_PATH[loc], page)
    want = [{"@type": "ListItem", "position": i + 1, "name": n, "item": (u or url)} for i, (n, u) in enumerate(vis)]
    changed = []
    def repl(m):
        try: g = json.loads(m.group(1))
        except Exception: return m.group(0)
        nodes = g.get("@graph") or [g]
        for n in nodes:
            if n.get("@type") != "BreadcrumbList": continue
            have = [{"@type": "ListItem", "position": i.get("position"), "name": i.get("name"), "item": i.get("item")} for i in n.get("itemListElement", [])]
            if have != want:
                changed.append((have, want)); n["itemListElement"] = want
        if not changed: return m.group(0)
        return '<script type="application/ld+json">\n' + json.dumps(g, ensure_ascii=False, indent=2) + '\n</script>'
    nh = re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, h, flags=re.S)
    if changed and fix: open(path, "w", encoding="utf-8").write(nh)
    return changed

if __name__ == "__main__":
    fix = "--fix" in sys.argv
    pages = [a.strip("/") + "/" for a in sys.argv[1:] if not a.startswith("--")] or [p for p in PAGE_PATHS if p]
    n = t = 0
    for page in pages:
        for L in LANG_ORDER:
            p = os.path.join(ROOT, LANG_PATH[L], page, "index.html")
            if not os.path.exists(p): continue
            t += 1; r = sync(p, L, page, fix)
            if r:
                n += 1; have, want = r[0]
                if n <= 6 or not fix: print(f"  {'✎' if fix else '≠'} {L}/{page}: {[i['name'] for i in have]} → {[i['name'] for i in want]}" if n <= 12 else "", end="\n" if n <= 12 else "")
    print(f"\n  страниц проверено {t}, {'исправлено' if fix else 'расходятся'} {n}")
