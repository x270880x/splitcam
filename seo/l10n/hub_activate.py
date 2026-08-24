#!/usr/bin/env python3
"""Turn a "Soon" card on a /for/ hub into a live link, in one locale.

The hub card for an audience ships as an inert <div class="hub-card soon"> with a
"Soon" tag. When that audience's page goes live the card must become a link — in
EVERY locale, or a localized hub keeps advertising a page it never links to.

The "Open the guide →" label is NOT translated here: it is copied from a card that
is already active in the same locale, so the wording matches what that locale uses.

Usage:  python3 hub_activate.py <locale> <hub_file> <icon> [--dry]
"""
import re
import sys


def _card_end(html, open_pos):
    """Index just past the <div class="hub-card soon"> that starts at open_pos.

    Counted by nesting depth, not by a lazy regex: a card contains nested <div>s
    (hub-ico, hub-meta), so matching to the first </div> silently cuts the card in
    half and orphans its <p> — which is exactly what a first attempt here did.
    """
    depth = 0
    for m in re.finditer(r"<div\b[^>]*>|</div>", html[open_pos:]):
        depth += 1 if m.group(0).startswith("<div") else -1
        if depth == 0:
            return open_pos + m.end()
    raise ValueError("unbalanced <div> in hub card")


def activate(html, locale, icon):
    """Replace the inert card carrying `icon` with a link to that locale's page."""
    start = None
    for m in re.finditer(r'<div class="hub-card soon">', html):
        end = _card_end(html, m.start())
        if f'<div class="hub-ico">{icon}</div>' in html[m.start():end]:
            start, stop = m.start(), end
            break
    if start is None:
        return None, "карточка не найдена (уже активна или другой значок)"

    card = html[start:stop]
    inner = re.sub(r'<span class="tag-soon">[^<]*</span>\s*', "", card)
    inner = inner[inner.index(">") + 1:]                 # drop the opening <div ...>
    inner = inner[:inner.rindex("</div>")].rstrip()      # drop the matching </div>

    go = re.search(r'<div class="hub-go">([^<]*)</div>', html)
    if not go:
        return None, "не найдена активная карточка-образец с hub-go"

    prefix = f"https://splitcam.com/{locale}/" if locale != "en" else "https://splitcam.com/"
    new_card = (f'<a class="hub-card" href="{prefix}for/educators">\n'
                f'{inner}\n'
                f'      <div class="hub-go">{go.group(1)}</div>\n'
                f'    </a>')
    return html[:start] + new_card + html[stop:], None


def main():
    locale, path, icon = sys.argv[1], sys.argv[2], sys.argv[3]
    dry = "--dry" in sys.argv
    html = open(path, encoding="utf-8").read()
    out, err = activate(html, locale, icon)
    if err:
        print(f"{locale}: SKIP — {err}")
        return
    if not dry:
        open(path, "w", encoding="utf-8").write(out)
    print(f"{locale}: карточка активирована{' (dry)' if dry else ''}")


if __name__ == "__main__":
    main()
