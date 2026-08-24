#!/usr/bin/env python3
"""Extract translatable strings from a SplitCam page into a keyed dict, and inject them back.

Replaces the throwaway `scratchpad/va_extract.py` used for the virtual-audio rollout
(2026-08-20), which was not kept and had to be rewritten for /for/educators.

Guarantee: `inject(html, extract(html)) == html`, byte for byte. Run --selftest.
That round-trip is what catches pattern bugs — on the previous rollout a greedy FAQ
pattern swallowed its own <summary>, so FAQ questions were silently never extracted
and would have shipped in English.

Units are "leaf block" elements: a block-level element with no block-level child.
Its innerHTML travels as one string, so inline markup (<b>, <a>, <span>) stays inside
the translated sentence instead of chopping it into fragments a translator cannot reorder.

Usage:
    python3 seo/l10n/extract.py --selftest  <file>
    python3 seo/l10n/extract.py --dump      <file> > strings.json
    python3 seo/l10n/extract.py --inject    <file> strings.json > out.html
"""
import json
import re
import sys
from html.parser import HTMLParser

BLOCK = {
    "html", "head", "body", "div", "section", "article", "aside", "nav", "header",
    "footer", "main", "ul", "ol", "li", "dl", "dt", "dd", "p", "h1", "h2", "h3",
    "h4", "h5", "h6", "details", "table", "thead", "tbody", "tr", "td", "th",
    "form", "figure", "figcaption", "blockquote", "script", "style", "svg", "picture",
    "summary",
}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}

# Attributes worth translating, per tag.
ATTRS = {
    "img": ("alt",),
    "a": ("aria-label", "title"),
    "summary": ("aria-label",),
    "button": ("aria-label", "title"),
    "input": ("placeholder", "aria-label"),
}
# <meta> name/property values whose content= is translatable.
META_KEYS = {
    "description", "keywords",
    "og:title", "og:description",
    "twitter:title", "twitter:description",
}


def _raw_attr_span(raw, attr):
    """Byte span of attr's value inside a raw start tag, exactly as written in the file.

    Matching the RAW text matters: HTMLParser hands back decoded values, so a title
    containing &amp; would never be found by searching for the decoded form.
    """
    m = re.search(r'\b' + re.escape(attr) + r'\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', raw)
    if not m:
        return None
    g = 1 if m.group(1) is not None else 2
    return m.start(g), m.end(g)


class Collector(HTMLParser):
    """Records byte spans of translatable text: leaf-block innerHTML, <title>, meta content."""

    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.stack = []          # (tag, inner_start, had_block_child)
        self.spans = []          # (start, end, kind, label)
        self._line_starts = [0]
        for i, ch in enumerate(src):
            if ch == "\n":
                self._line_starts.append(i + 1)

    def _pos(self):
        line, off = self.getpos()
        return self._line_starts[line - 1] + off

    def handle_starttag(self, tag, attrs):
        start = self._pos()
        raw = self.get_starttag_text() or ""
        inner_start = start + len(raw)
        d = dict(attrs)

        # translatable attribute values
        for a in ATTRS.get(tag, ()):
            if a in d and d[a] and d[a].strip():
                span = _raw_attr_span(raw, a)
                if span:
                    vs, ve = span
                    self.spans.append((start + vs, start + ve, "attr", f"{tag}@{a}"))

        if tag == "meta":
            key = d.get("name") or d.get("property") or ""
            if key in META_KEYS and "content" in d:
                span = _raw_attr_span(raw, "content")
                if span:
                    vs, ve = span
                    self.spans.append((start + vs, start + ve, "meta", key))

        if tag in VOID or raw.endswith("/>"):
            return
        if tag in BLOCK and self.stack:
            self.stack[-1][2].append(True)          # mark parent as having a block child
        self.stack.append([tag, inner_start, []])

    def handle_endtag(self, tag):
        end = self._pos()
        while self.stack:
            t, inner_start, blocks = self.stack.pop()
            if t != tag:
                continue                            # unclosed inline tag; skip
            if t in ("script", "style"):
                break
            inner = self.src[inner_start:end]
            if t == "title":
                if inner.strip():
                    self.spans.append((inner_start, end, "title", "title"))
                break
            if t in BLOCK and not blocks and inner.strip():
                self.spans.append((inner_start, end, "block", t))
            break


def collect(html):
    c = Collector(html)
    c.feed(html)
    c.close()
    spans = sorted(set(c.spans))
    # drop spans nested inside another kept span (keeps the outermost unit)
    out, last_end = [], -1
    for s in spans:
        if s[0] >= last_end:
            out.append(s)
            last_end = s[1]
    return out


def extract(html):
    """-> {key: text} in document order. Keys are stable: kind/label/index."""
    d, seen = {}, {}
    for start, end, kind, label in collect(html):
        base = f"{kind}:{label}"
        n = seen.get(base, 0)
        seen[base] = n + 1
        d[f"{base}#{n}"] = html[start:end]
    return d


def inject(html, strings):
    """Rebuild the page with translated values. Unknown/missing keys keep the original."""
    pieces, prev = [], 0
    seen = {}
    for start, end, kind, label in collect(html):
        base = f"{kind}:{label}"
        n = seen.get(base, 0)
        seen[base] = n + 1
        key = f"{base}#{n}"
        pieces.append(html[prev:start])
        pieces.append(strings.get(key, html[start:end]))
        prev = end
    pieces.append(html[prev:])
    return "".join(pieces)


def main():
    mode, path = sys.argv[1], sys.argv[2]
    html = open(path, encoding="utf-8").read()
    if mode == "--selftest":
        s = extract(html)
        back = inject(html, s)
        ok = back == html
        print(f"strings: {len(s)}")
        print(f"round-trip: {'OK — byte identical' if ok else 'FAILED'}")
        if not ok:
            for i, (a, b) in enumerate(zip(html, back)):
                if a != b:
                    print(f"first diff at byte {i}: {html[i-60:i+60]!r} != {back[i-60:i+60]!r}")
                    break
            print(f"len {len(html)} -> {len(back)}")
            sys.exit(1)
    elif mode == "--dump":
        json.dump(extract(html), sys.stdout, ensure_ascii=False, indent=1)
    elif mode == "--inject":
        strings = json.load(open(sys.argv[3], encoding="utf-8"))
        sys.stdout.write(inject(html, strings))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
