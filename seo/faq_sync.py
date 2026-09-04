# -*- coding: utf-8 -*-
"""Приводит разметку FAQPage в соответствие видимому тексту страницы.

   python3 seo/faq_sync.py --check          показать расхождения по всему сайту
   python3 seo/faq_sync.py --fix <путь> …   починить указанные страницы (и все их локали)

ЗАЧЕМ. Google требует, чтобы содержимое FAQPage было видно на странице. Если в
разметке текст отличается от видимого — или вопросов там меньше, чем на странице, —
расширенный сниппет могут снять. Найдено 2026-09-04: на 7 английских страницах
(включая главную и /multistreaming/) ответы в разметке расходились с видимыми, а на
/virtual-audio-mac/ в разметке было 6 вопросов против 8 на странице.

Источник истины — ВИДИМЫЙ текст: его читает человек, разметка обязана его повторять.
Правка механическая и не зависит от языка: берём текст локали и кладём в её же разметку.
"""
import re, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
strip = lambda s: re.sub(r'\s+', ' ', re.sub('<[^>]*>', '', s)).strip()

def visible_faq(html):
    vis = [(strip(m.group(1)), strip(m.group(2)))
           for m in re.finditer(r'<summary>(.*?)</summary>\s*<p>(.*?)</p>', html, re.S)]
    if not vis:                                   # /features/: FAQ свёрстан карточками connect-step h4/p
        sec = re.search(r'<section[^>]*id="faq"[^>]*>(.*?)</section>', html, re.S)
        if sec:
            vis = [(strip(q), strip(a)) for q, a in
                   re.findall(r'<div class="connect-step"><h4>(.*?)</h4><p>(.*?)</p>', sec.group(1), re.S)]
    return vis

def audit(path):
    h = open(path, encoding="utf-8").read()
    vis = visible_faq(h)
    if not vis:
        return None
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            g = json.loads(m.group(1))
        except Exception:
            continue
        for n in (g.get("@graph") or [g]):
            if n.get("@type") == "FAQPage":
                ent = n.get("mainEntity", [])
                dq = sum(1 for (vq, _), j in zip(vis, ent) if strip(j.get("name", "")) != vq)
                da = sum(1 for (_, va), j in zip(vis, ent)
                         if strip(j.get("acceptedAnswer", {}).get("text", "")) != va)
                return len(vis), len(ent), dq, da
    return None

def fix(path):
    h = open(path, encoding="utf-8").read()
    vis = visible_faq(h)
    if not vis:
        return "нет видимого FAQ"
    changed = [False]

    def repl(m):
        try:
            g = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        nodes = g.get("@graph") or [g]
        hit = False
        for n in nodes:
            if n.get("@type") != "FAQPage":
                continue
            hit = True
            n["mainEntity"] = [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in vis]
        if not hit:
            return m.group(0)
        changed[0] = True
        return ('<script type="application/ld+json">\n'
                + json.dumps(g, ensure_ascii=False, indent=2) + '\n</script>')

    h2 = re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, h, flags=re.S)
    if not changed[0]:
        return "FAQPage в разметке не найден"
    open(path, "w", encoding="utf-8").write(h2)
    return None

LOCS = "ru es de fr pt tr fil uk it vi id nl ro hi ja ms bg ar ko th pl hu sv zh el cs he sr hr da fi no sk fa".split()

if __name__ == "__main__":
    if "--check" in sys.argv:
        bad = 0
        for dp, dn, fn in os.walk(ROOT):
            if "/.git" in dp or "/seo" in dp:
                continue
            if "index.html" not in fn:
                continue
            p = os.path.join(dp, "index.html")
            r = audit(p)
            if r and (r[0] != r[1] or r[2] or r[3]):
                bad += 1
                rel = os.path.relpath(p, ROOT)
                print(f"  🔴 {rel}: видимо {r[0]}, в разметке {r[1]}, вопросов≠ {r[2]}, ответов≠ {r[3]}")
        print(f"\n  страниц с расхождением: {bad}")
    elif "--fix" in sys.argv:
        pages = [a for a in sys.argv[1:] if a != "--fix"]
        n = err = 0
        for page in pages:
            for loc in [""] + LOCS:
                p = os.path.join(ROOT, loc, page, "index.html") if loc else os.path.join(ROOT, page, "index.html")
                if not os.path.exists(p):
                    continue
                e = fix(p)
                if e:
                    err += 1
                else:
                    n += 1
        print(f"  исправлено файлов: {n}, пропущено: {err}")
