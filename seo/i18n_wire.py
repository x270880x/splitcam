#!/usr/bin/env python3
"""Wire the language system across every page (no build step).

Run after translating new locale pages. For every existing <locale>/<page>/index.html
it rebuilds — idempotently, via <!--MARKER--> regions — the cross-cutting i18n bits so
they only ever list locales where THAT page actually exists on disk:

  * the language dropdown (replaces the legacy 3-button .lang-sw switcher), nav + burger
  * the hreflang alternates block (+ keeps the per-locale canonical untouched)
  * the browser-language auto-redirect JS (per-page locale list → never 404s)
  * the dropdown CSS (once per page <style>)
  * sitemap.xml (per-page xhtml:link alternates)

Usage:  python3 seo/i18n_wire.py            # wire + rewrite sitemap
        python3 seo/i18n_wire.py --check     # report only, no writes
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = "--check" in sys.argv

# Page paths that participate in the locale system (translatable set).
PAGE_PATHS = ["", "products/", "virtual-camera/", "multistreaming/", "alternatives/",
              "alternatives/obs/", "for/", "for/youtubers/", "for/churches/", "help/",
              "changelog/", "privacy-policy/", "license-agreement/"]
# changelog/privacy/license sit at priority 0.6/0.3; rest from i18n weighting.
PRIO = {"": "1.0", "multistreaming/": "0.9", "virtual-camera/": "0.9", "products/": "0.9",
        "changelog/": "0.6", "help/": "0.6", "privacy-policy/": "0.3", "license-agreement/": "0.3"}
FREQ = {"": "weekly", "changelog/": "weekly", "privacy-policy/": "yearly", "license-agreement/": "yearly"}
LASTMOD = "2026-06-13"


def file_for(locale, page):
    pre = "" if locale == "en" else f"{locale}/"
    return os.path.join(ROOT, f"{pre}{page}index.html")


def exists(locale, page):
    return os.path.isfile(file_for(locale, page))


def available(page):
    return [L for L in i18n.LANG_ORDER if exists(L, page)]


def depth_prefix(locale, page):
    segs = (0 if locale == "en" else 1) + page.count("/")
    return "../" * segs


def region(marker, body):
    return f"<!--{marker}-->{body}<!--/{marker}-->"


def sub_region(s, marker, body, legacy_pat):
    """Replace a marked region if present, else the first legacy match. Returns (s, n)."""
    m = re.compile(rf"<!--{marker}-->.*?<!--/{marker}-->", re.DOTALL)
    if m.search(s):
        return m.sub(lambda _: region(marker, body), s), m.subn(lambda _: "", s)[1]
    if legacy_pat is not None:
        new, n = legacy_pat.subn(lambda _: region(marker, body), s, count=1)
        return new, n
    return s, 0


LEGACY_SW = re.compile(r'<div class="lang-sw"[^>]*>.*?</div>', re.DOTALL)
LEGACY_HL = re.compile(r'(?:[ \t]*<link rel="alternate" hreflang="[^"]*"[^>]*>\s*)+')
AD_MARK = re.compile(r"<!--AD-->.*?<!--/AD-->", re.DOTALL)


def wire_file(locale, page, avail):
    fn = file_for(locale, page)
    s = open(fn, encoding="utf-8").read()
    orig = s
    depth = depth_prefix(locale, page)

    # 0. normalize <html> direction (RTL locales -> dir="rtl", LTR -> none). Idempotent.
    dir_attr = ' dir="rtl"' if i18n.is_rtl(locale) else ''
    s = re.sub(rf'<html lang="{re.escape(locale)}"[^>]*>',
               f'<html lang="{locale}"{dir_attr}>', s, count=1)

    # 1. dropdown switcher — both nav-right and #nav-mobile copies
    dd = i18n.dropdown(locale, avail, page, depth)
    # marked replacement (rerun) first
    if re.search(r"<!--LD-->.*?<!--/LD-->", s, re.DOTALL):
        s = re.sub(r"<!--LD-->.*?<!--/LD-->", lambda _: region("LD", dd), s, flags=re.DOTALL)
    else:
        s = LEGACY_SW.sub(lambda _: region("LD", dd), s)  # replaces all (nav + burger)

    # 2. hreflang block
    hl = i18n.hreflang_block(page, avail)
    s, _ = sub_region(s, "HL", "\n" + hl + "\n", LEGACY_HL)

    # 3. auto-detect JS (per-page locale list) before </body>
    ad = i18n.AUTO_DETECT_JS.replace("__LANG_LIST__", "[" + ",".join(f'"{L}"' for L in avail) + "]")
    if AD_MARK.search(s):
        s = AD_MARK.sub(lambda _: region("AD", ad), s)
    else:
        s = s.replace("</body>", region("AD", ad) + "\n</body>", 1)

    # 4. dropdown CSS once
    if ".lang-dl{position" not in s:
        s = s.replace("</style>", "\n" + i18n.DROPDOWN_CSS + "\n</style>", 1)

    # 5. partial-wave link safety (any page): a localized sibling link points to the
    # localized page if it exists, else falls back to the EN page so nothing 404s.
    # From /L/<page>/, an in-locale sibling link uses prefix `../`*n (n = page depth);
    # the EN fallback is one level higher (`../`*(n+1)). Longest sibling first so
    # 'for/youtubers/' is handled before 'for/'.
    if locale != "en":
        n = page.count("/")
        loc_pre, en_pre = "../" * n, "../" * (n + 1)
        for S in sorted([p for p in PAGE_PATHS if p and p != page], key=len, reverse=True):
            if exists(locale, S):
                s = s.replace(f'href="{en_pre}{S}', f'href="{loc_pre}{S}')   # localize
            else:
                s = s.replace(f'href="{loc_pre}{S}', f'href="{en_pre}{S}')   # EN fallback

    if s != orig and not CHECK:
        open(fn, "w", encoding="utf-8").write(s)
    return s != orig


def build_sitemap():
    B = i18n.SITE + "/"
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for page in PAGE_PATHS:
        avail = available(page)
        if not avail:
            continue
        alts = "".join(
            f'    <xhtml:link rel="alternate" hreflang="{L}" href="{B}{i18n.LANG_PATH[L]}{page}"/>\n'
            for L in avail) + f'    <xhtml:link rel="alternate" hreflang="x-default" href="{B}{page}"/>\n'
        for L in avail:
            loc = f"{B}{i18n.LANG_PATH[L]}{page}"
            out.append(f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n'
                       f'    <changefreq>{FREQ.get(page, "monthly")}</changefreq>\n'
                       f'    <priority>{PRIO.get(page, "0.7")}</priority>\n{alts}  </url>')
    out.append("</urlset>")
    if not CHECK:
        open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(out) + "\n")
    return sum(len(available(p)) for p in PAGE_PATHS if available(p))


def main():
    changed = 0
    summary = []
    for page in PAGE_PATHS:
        avail = available(page)
        if not avail:
            continue
        summary.append(f"  {page or '/':22} {len(avail):2} locales: {' '.join(avail)}")
        for L in avail:
            if wire_file(L, page, avail):
                changed += 1
    n_urls = build_sitemap()
    print("PAGES × LOCALES:")
    print("\n".join(summary))
    print(f"\n{'(check) ' if CHECK else ''}files wired: {changed} · sitemap urls: {n_urls}")


if __name__ == "__main__":
    main()
