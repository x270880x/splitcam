#!/usr/bin/env python3
"""Assemble a localized page from the EN reference + a translation dict.

Replaces the throwaway `scratchpad/va_build_locale.py` (2026-08-20), which was not kept.

What comes from where:
  * head SEO, page CSS, content markup -> EN reference (with translations injected)
  * <html> tag, nav, mobile menu, footer, scripts -> the SAME LOCALE's donor page,
    so the chrome is genuinely localized instead of hand-translated
  * JSON-LD -> rebuilt from the finished localized DOM, so structured data can never
    drift from the visible text
  * breadcrumbs -> donor's own trail, with the last crumb swapped for this page

Usage:
    python3 build_locale.py <locale> <en_page> <translations.json> <donor_page> <out_page>
"""
import html as htmllib
import json
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import inject  # noqa: E402

RTL = {"ar", "he", "fa"}
CONTENT_START = "<!-- BREADCRUMBS -->"
CONTENT_END = "<!-- FOOTER -->"
BODY = "<body>"


def zone(text, start_marker, end_marker):
    a = text.index(start_marker)
    b = text.index(end_marker)
    return a, b


def strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s)
    return htmllib.unescape(s).strip()


def collapse(s):
    return re.sub(r"\s+", " ", s).strip()


def build(locale, en_html, tr, donor_html, page_path):
    url = f"https://splitcam.com/{locale}/{page_path}"

    # 1. translations into the EN reference
    out = inject(en_html, tr)

    # 2. <html> tag from the donor (carries lang and, for ar/he/fa, dir="rtl")
    donor_html_tag = re.search(r"<html[^>]*>", donor_html).group(0)
    out = re.sub(r"<html[^>]*>", donor_html_tag, out, count=1)

    # 3. self-referencing URLs
    out = out.replace('<link rel="canonical" href="https://splitcam.com/for/educators">',
                      f'<link rel="canonical" href="{url}">')
    out = out.replace('<meta property="og:url" content="https://splitcam.com/for/educators">',
                      f'<meta property="og:url" content="{url}">')
    # hreflang block is rewritten wholesale by i18n_wire.py; point it at this page meanwhile
    out = re.sub(r"<!--HL-->.*?<!--/HL-->",
                 f'<!--HL-->\n<link rel="alternate" hreflang="{locale}" href="{url}">\n<!--/HL-->',
                 out, flags=re.S)

    # 4. chrome transplant: nav + mobile menu
    d_a, d_b = zone(donor_html, BODY, CONTENT_START)
    o_a, o_b = zone(out, BODY, CONTENT_START)
    out = out[:o_a] + donor_html[d_a:d_b] + out[o_b:]

    # 5. chrome transplant: footer + scripts + </body></html>
    out = out[:out.index(CONTENT_END)] + donor_html[donor_html.index(CONTENT_END):]

    # 6. breadcrumbs: donor's trail, last crumb replaced
    d_crumbs = re.search(r"<div class=\"breadcrumbs\">.*?</div>", donor_html, re.S).group(0)
    last = tr.get("x:breadcrumb_last")
    if not last:
        raise SystemExit(f"{locale}: missing x:breadcrumb_last")
    new_crumbs = re.sub(r"<span>[^<]*</span>\s*$", f"<span>{last}</span>",
                        d_crumbs.rstrip()[:-len("</div>")].rstrip()) + "\n</div>"
    out = re.sub(r"<div class=\"breadcrumbs\">.*?</div>", lambda _m: new_crumbs, out, count=1, flags=re.S)

    # 7. JSON-LD rebuilt from the finished localized DOM
    out = re.sub(r'(<script type="application/ld\+json">\n).*?(\n</script>)',
                 lambda m: m.group(1) + build_jsonld(out, locale, url, new_crumbs) + m.group(2),
                 out, count=1, flags=re.S)
    return out


def build_jsonld(page, locale, url, crumbs_html):
    # breadcrumbs -> ListItem names, in document order
    names = [strip_tags(x) for x in re.findall(r"<(?:a|span)(?: [^>]*)?>(.*?)</(?:a|span)>", crumbs_html)]
    names = [n for n in names if n and n != "/"]
    items = []
    hrefs = re.findall(r'<a href="([^"]+)"', crumbs_html)
    for i, n in enumerate(names):
        item = hrefs[i] if i < len(hrefs) else url
        items.append({"@type": "ListItem", "position": i + 1, "name": n, "item": item})

    desc = re.search(r'<meta name="description" content="([^"]*)"', page).group(1)
    desc = htmllib.unescape(desc)

    howto_name = strip_tags(re.search(r'<section class="section" id="steps">\s*<h2[^>]*>(.*?)</h2>',
                                      page, re.S).group(1))
    steps = []
    for i, m in enumerate(re.finditer(r'<div class="step-h">(.*?)</div>\s*<p class="step-p">(.*?)</p>',
                                      page, re.S), 1):
        name = re.sub(r'<span class="step-time">.*?</span>', "", m.group(1), flags=re.S)
        steps.append({"@type": "HowToStep", "position": i,
                      "name": collapse(strip_tags(name)), "text": collapse(strip_tags(m.group(2)))})

    faqs = []
    for m in re.finditer(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", page, re.S):
        faqs.append({"@type": "Question", "name": collapse(strip_tags(m.group(1))),
                     "acceptedAnswer": {"@type": "Answer", "text": collapse(strip_tags(m.group(2)))}})

    sw_desc = SOFTWARE_DESC.get(locale) or desc
    graph = [
        {"@type": "BreadcrumbList", "itemListElement": items},
        {"@type": "HowTo", "name": howto_name, "description": desc, "totalTime": "PT10M",
         "step": steps},
        {"@type": "SoftwareApplication", "name": "SplitCam",
         "operatingSystem": "Windows 10, Windows 11, macOS 13",
         "applicationCategory": "MultimediaApplication", "description": sw_desc,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "url": url},
        {"@type": "FAQPage", "mainEntity": faqs},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, indent=2)


SOFTWARE_DESC = {}   # filled per-locale from translations if provided


def main():
    locale, en_p, tr_p, donor_p, out_p = sys.argv[1:6]
    en_html = open(en_p, encoding="utf-8").read()
    donor = open(donor_p, encoding="utf-8").read()
    tr = json.load(open(tr_p, encoding="utf-8"))
    if "x:software_desc" in tr:
        SOFTWARE_DESC[locale] = tr["x:software_desc"]
    out = build(locale, en_html, tr, donor, "for/educators")
    os.makedirs(os.path.dirname(out_p), exist_ok=True)
    open(out_p, "w", encoding="utf-8").write(out)
    print(f"{locale}: {len(out)} bytes -> {out_p}")


if __name__ == "__main__":
    main()
