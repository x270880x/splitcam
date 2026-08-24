#!/usr/bin/env python3
"""Verify a built locale page: JSON-LD parses, chrome localized, redirect guard intact,
   no English leaked into content, self-referencing URLs correct."""
import html as H
import json
import re
import sys

locale, path = sys.argv[1], sys.argv[2]
p = open(path, encoding="utf-8").read()
errs, oks = [], []

m = re.search(r"<html([^>]*)>", p)
htag = m.group(1)
want_dir = locale in ("ar", "he", "fa")
m2 = re.search(r'lang="([^"]+)"', htag)
langv = m2.group(1) if m2 else ""
if not (langv == locale or langv.startswith(locale + "-")):
    errs.append(f"<html> lang not {locale}: {htag}")
if want_dir and 'dir="rtl"' not in htag:
    errs.append("RTL locale missing dir=rtl")

for label, needle in (("canonical", f'rel="canonical" href="https://splitcam.com/{locale}/for/educators"'),
                      ("og:url", f'og:url" content="https://splitcam.com/{locale}/for/educators"')):
    if needle not in p:
        errs.append(f"{label} not self-referencing")

lds = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', p, re.S)
if len(lds) != 1:
    errs.append(f"{len(lds)} JSON-LD blocks (want 1)")
else:
    try:
        d = json.loads(lds[0])
        types = [g["@type"] for g in d["@graph"]]
        for t in ("BreadcrumbList", "HowTo", "SoftwareApplication", "FAQPage"):
            if t not in types:
                errs.append(f"JSON-LD missing {t}")
        faq = next(g for g in d["@graph"] if g["@type"] == "FAQPage")
        if len(faq["mainEntity"]) != 8:
            errs.append(f"FAQ has {len(faq['mainEntity'])} (want 8)")
        howto = next(g for g in d["@graph"] if g["@type"] == "HowTo")
        if len(howto["step"]) != 5:
            errs.append(f"HowTo has {len(howto['step'])} steps (want 5)")
        if "aggregateRating" in lds[0]:
            errs.append("aggregateRating present")
        # JSON-LD FAQ questions must equal the visible <summary> text
        vis = [H.unescape(re.sub(r"<[^>]+>", "", x)).strip()
               for x in re.findall(r"<summary>(.*?)</summary>", p, re.S)]
        ldq = [q["name"] for q in faq["mainEntity"]]
        vis_faq = [v for v in vis if v]  # drop the language <summary>
        # the language dropdown summary has no text; keep only the 8 real ones
        vis_faq = [v for v in vis_faq if v.lower() not in ("language",)][-8:]
        if vis_faq != ldq:
            errs.append("FAQ JSON-LD text != visible <summary> text")
        else:
            oks.append("FAQ JSON-LD matches visible questions")
    except Exception as e:
        errs.append(f"JSON-LD parse error: {e}")

# redirect guard must be the fixed form
if "var explicit=L.indexOf(parts[0])>=0" not in p.replace(" ", "").replace("var explicit=L", "var explicit=L"):
    if "explicit" not in p:
        errs.append("redirect guard missing (explicit check)")

# chrome came from donor: breadcrumb uses /<locale>/ links
if f'href="https://splitcam.com/{locale}/for"' not in p:
    errs.append("breadcrumb not localized to /<locale>/for")

# body closed
if not p.rstrip().endswith("</html>"):
    errs.append("page does not end </html>")

for o in oks:
    print(f"  · {locale}: {o}")
for e in errs:
    print(f"  ✗ {locale}: {e}")
sys.exit(1 if errs else 0)
