#!/usr/bin/env python3
"""Split a page's extracted strings into what a translator gets and what is transplanted.

The chrome (nav, mobile menu, footer, scripts, language dropdown) is NOT translated —
it is transplanted from the same locale's own page, so its strings must never reach a
translator. Only the head SEO block and everything between BREADCRUMBS and FOOTER does.
"""
import sys

CONTENT_START = "<!-- BREADCRUMBS -->"
CONTENT_END = "<!-- FOOTER -->"
HEAD_KINDS = ("title:", "meta:")


def content_span(html):
    a = html.index(CONTENT_START)
    b = html.index(CONTENT_END)
    return a, b


def translatable(html, spans_with_keys):
    """-> set of keys inside the head-SEO block or the content zone."""
    a, b = content_span(html)
    out = set()
    for key, start, end in spans_with_keys:
        if key.startswith(HEAD_KINDS) or (a <= start < b):
            out.add(key)
    return out


def keyed_spans(html):
    """-> [(key, start, end)] mirroring extract.collect() key numbering."""
    from extract import collect
    seen, out = {}, []
    for start, end, kind, label in collect(html):
        base = f"{kind}:{label}"
        n = seen.get(base, 0)
        seen[base] = n + 1
        out.append((f"{base}#{n}", start, end))
    return out


if __name__ == "__main__":
    import json
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    html = open(sys.argv[1], encoding="utf-8").read()
    spans = keyed_spans(html)
    keep = translatable(html, spans)
    d = {k: html[s:e] for k, s, e in spans if k in keep}
    json.dump(d, sys.stdout, ensure_ascii=False, indent=1)
