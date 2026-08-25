# -*- coding: utf-8 -*-
"""Собирает локализованную /for/educators/: обрамление от локальной /for/churches/,
содержимое и стили — от английского оригинала, тексты — из перевода."""
import re, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from for_extract import inject
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGE = "for/educators"

def regions(h):
    b = h.find("<body>"); bc = h.find('<div class="breadcrumbs">'); ft = h.find("<footer")
    assert 0 < b < bc < ft, "структура неожиданная"
    return b, bc, ft

def build(loc, tr):
    src   = os.path.join(ROOT, PAGE, "index.html")
    donor = os.path.join(ROOT, loc, "for", "churches", "index.html")
    assert os.path.isfile(donor), f"нет донора {donor}"
    D = open(donor, encoding="utf-8").read()
    content_tr = {k: v for k, v in tr.items() if "#" in k and not k.startswith(("meta#", "ld#"))}
    S_tr = inject(src, content_tr)
    sb, sbc, sft = regions(S_tr); db, dbc, dft = regions(D)
    head, chrome1, content, chrome2 = S_tr[:sb], D[db:dbc], S_tr[sbc:sft], D[dft:]
    head = re.sub(r'<html[^>]*>', re.search(r'<html[^>]*>', D).group(0), head, count=1)
    url = f"https://splitcam.com/{loc}/{PAGE}"
    def setm(pat, val, s):
        s2, n = re.subn(pat, lambda m: m.group(1) + val + m.group(3), s, count=1, flags=re.S)
        assert n == 1, f"мета не заменена: {pat[:40]}"
        return s2
    esc = lambda x: x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    T, DESC = tr["meta#title"], tr["meta#description"]
    for pat, val in ((r'(<title>)(.*?)(</title>)', esc(T)),
                     (r'(<meta name="description" content=")(.*?)(")', esc(DESC)),
                     (r'(<meta name="keywords" content=")(.*?)(")', esc(tr["meta#keywords"])),
                     (r'(<link rel="canonical" href=")(.*?)(")', url),
                     (r'(<meta property="og:url" content=")(.*?)(")', url),
                     (r'(<meta property="og:title" content=")(.*?)(")', esc(T)),
                     (r'(<meta property="og:description" content=")(.*?)(")', esc(DESC)),
                     (r'(<meta name="twitter:title" content=")(.*?)(")', esc(T)),
                     (r'(<meta name="twitter:description" content=")(.*?)(")', esc(DESC))):
        head = setm(pat, val, head)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', head, re.S)
    g = json.loads(m.group(1))["@graph"]
    strip = lambda s: re.sub(r'\s+', ' ', re.sub(r'<[^>]*>', '', s)).strip()
    steps = [(tr[f"step_a#{i}"], tr[f"stepp#{i}"]) for i in range(5)]
    nfaq = sum(1 for k in tr if k.startswith("faqq#"))
    faq = [(tr[f"faqq#{i}"], tr[f"faqa#{i}"]) for i in range(nfaq)]
    for n in g:
        t = n["@type"]
        if t == "BreadcrumbList":
            it = n["itemListElement"]
            it[0]["item"] = f"https://splitcam.com/{loc}/"; it[0]["name"] = strip(tr.get("crumb_a#0", it[0]["name"]))
            it[1]["item"] = f"https://splitcam.com/{loc}/for"; it[1]["name"] = strip(tr.get("crumb_b#0", it[1]["name"]))
            it[2]["item"] = url; it[2]["name"] = strip(tr.get("crumb_c#0", it[2]["name"]))
        elif t == "HowTo":
            n["name"] = tr["ld#howto_name"]; n["description"] = tr["ld#howto_desc"]
            for k, st in enumerate(n.get("step", [])):
                if k < len(steps): st["name"] = strip(steps[k][0]); st["text"] = strip(steps[k][1])
        elif t == "SoftwareApplication":
            n["description"] = tr["ld#app_desc"]; n["url"] = url
        elif t == "FAQPage":
            n["mainEntity"] = [{"@type": "Question", "name": strip(q),
                                "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faq]
    head = head[:m.start()] + '<script type="application/ld+json">\n' + \
           json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, indent=2) + \
           '\n</script>' + head[m.end():]
    content = content.replace('href="https://splitcam.com/"', f'href="https://splitcam.com/{loc}/"')
    for sib in ("for/churches", "for/youtubers", "virtual-camera", "features", "products", "multistreaming", "for"):
        if os.path.isfile(os.path.join(ROOT, loc, sib, "index.html")):
            content = content.replace(f'href="https://splitcam.com/{sib}"', f'href="https://splitcam.com/{loc}/{sib}"')
    dst = os.path.join(ROOT, loc, PAGE); os.makedirs(dst, exist_ok=True)
    out = head + chrome1 + content + chrome2
    open(os.path.join(dst, "index.html"), "w", encoding="utf-8").write(out)
    return len(out)
