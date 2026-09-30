# -*- coding: utf-8 -*-
"""Inject reviewed What's-new strings into the 34 locale homepages (used for v11.0.11, 2026-09-30).
The translator + native-reviewer output is in seo/l10n/whats-new-11.0.11.json; agents never edit the pages.
usage: python3 inject_whats_new.py results.json [--check]
results.json: [{code, rv:{sec_p, cards:[{h,p}x4]}}]
"""
import html, json, re, sys
REPO = "/Users/splitcam/Documents/Проекты/SplitCam/SplitCam сайт/splitcam"
sys.path.insert(0, REPO + "/seo")
from i18n import LANG_PATH

GLOSS_OPEN = '<span style="color:var(--text-sub);font-weight:500">'
ICO_RESTREAM = '<rect width="20" height="8" x="2" y="2" rx="2"/>'
ICO_VCANVAS = '<rect width="12" height="20" x="6" y="2" rx="2"/><path d="M12 7v10"/>'

en = open(REPO + "/index.html", encoding="utf-8").read()
en_new = re.findall(r'      <div class="new-card">\n.*?\n      </div>\n', en[en.index('<div class="new-grid">'):], re.S)[:4]
EN_ICONS = [re.search(r'<div class="new-ico" aria-hidden="true">.*?</div>', c, re.S).group(0) for c in en_new]
assert len(EN_ICONS) == 4

esc = lambda t: html.escape(t, quote=False)

ALLOWED_OPEN = set()   # gloss <span …> openings that this locale's block already uses (filled per locale)

def title_html(h):
    m = re.match(r'^([^<]*)(<span style="[^"]*">)([^<]*)</span>\s*$', h)
    if m:
        assert m.group(2) in ALLOWED_OPEN, ("gloss span not used by this locale before", m.group(2))
        return esc(m.group(1)) + m.group(2) + esc(m.group(3)) + "</span>"
    assert "<" not in h and ">" not in h, ("unexpected markup in title", h)
    return esc(h)

def card(badge, icon, h, p):
    return (f'      <div class="new-card">\n        <span class="new-badge">{badge}</span>\n        {icon}\n'
            f'        <div class="new-h">{title_html(h)}</div>\n        <p class="new-p">{esc(p)}</p>\n      </div>\n')

def build(code, rv, s):
    i = s.index('id="whats-new"'); g = s.index('<div class="new-grid">\n', i); gi = g + len('<div class="new-grid">\n')
    ge = s.index('    </div>\n  </div>\n</section>', gi)
    cards = re.findall(r'      <div class="new-card">\n.*?\n      </div>\n', s[gi:ge], re.S)
    assert len(cards) == 6 and "".join(cards) == s[gi:ge], (code, "grid shape")
    restream = [c for c in cards if ICO_RESTREAM in c]; vcanvas = [c for c in cards if ICO_VCANVAS in c]
    assert len(restream) == 1 and len(vcanvas) == 1, (code, "kept cards not found")
    ALLOWED_OPEN.clear(); ALLOWED_OPEN.update(re.findall(r'<div class="new-h">[^<]*(<span style="[^"]*">)', s[gi:ge]))
    badges = set(re.findall(r'<span class="new-badge">([^<]*)</span>', s[gi:ge]))
    assert len(badges) == 1, (code, badges)
    new_word = badges.pop()
    grid = "".join(card(new_word, EN_ICONS[k], rv["cards"][k]["h"], rv["cards"][k]["p"]) for k in range(4))
    for c in (vcanvas[0], restream[0]):
        c2 = c.replace(f'<span class="new-badge">{new_word}</span>', '<span class="new-badge">v10.9.2</span>', 1)
        assert c2 != c; grid += c2
    s = s[:gi] + grid + s[ge:]
    m = re.compile(r'(<section class="section" id="whats-new">.*?<p class="sec-p">)([^<]*)(</p>)', re.S).search(s)
    assert m and "10.9.2" in m.group(2), (code, "sec-p")
    s = s[:m.start(2)] + esc(rv["sec_p"]) + s[m.end(2):]
    f = re.compile(r'(<li><a href="#whats-new">[^<]*?)v10\.9\.2(</a>)')
    s, n = f.subn(lambda mm: mm.group(1) + "v11.0.11" + mm.group(2), s)
    assert n == 1, (code, "footer link", n)
    return s, new_word

def main():
    res = json.load(open(sys.argv[1], encoding="utf-8"))
    check = "--check" in sys.argv
    seen = set()
    for r in res:
        code, rv = r["code"], r["rv"]
        assert code not in seen; seen.add(code)
        assert len(rv["cards"]) == 4 and "v11.0.11" in rv["sec_p"] and "10.9.2" in rv["sec_p"], (code, "sec_p/cards")
        p = REPO + "/" + LANG_PATH[code] + "index.html"
        s = open(p, encoding="utf-8").read()
        if re.search(r'<li><a href="#whats-new">[^<]*v11\.0\.11</a>', s):
            print(f"{code:4} already injected — skipped"); continue
        out, word = build(code, rv, s)
        if not check:
            open(p, "w", encoding="utf-8").write(out)
        print(f"{code:4} ok  badge={word}")
    print("locales:", len(seen))

if __name__ == "__main__":
    main()
