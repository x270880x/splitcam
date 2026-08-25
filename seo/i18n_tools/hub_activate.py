# -*- coding: utf-8 -*-
"""Превращает карточку «Soon» в хабе /for/ в живую ссылку.
Все строки берутся из самой локали — новых переводов не требуется.
Запуск:  python3 seo/i18n_tools/hub_activate.py 🎓 educators [--dry]
"""
import re, os, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def activate(path, emoji, slug, dry=False):
    h = open(path, encoding="utf-8").read()
    loc = os.path.relpath(path, ROOT).split("/")[0]
    loc = "" if loc == "for" else loc + "/"
    href = f"https://splitcam.com/{loc}for/{slug}"
    if href in h: return f"SKIP {path}: уже активна"
    i = h.find(emoji)
    if i < 0: return f"FAIL {path}: карточка с {emoji} не найдена"
    s = h.rfind('<div class="hub-card soon">', 0, i)
    if s < 0: return f"FAIL {path}: карточка не помечена soon"
    p_end = h.find("</p>", h.find("<p>", i))
    if p_end < 0: return f"FAIL {path}: нет <p> в карточке"
    e = h.find("</div>", p_end)
    if e < 0: return f"FAIL {path}: конец карточки не найден"
    card = h[s:e + 6]
    go = re.search(r'<div class="hub-go">([^<]*)</div>', h)
    if not go: return f"FAIL {path}: нет образца hub-go"
    new = card.replace('<div class="hub-card soon">', f'<a class="hub-card" href="{href}">', 1)
    new = re.sub(r'\s*<span class="tag-soon">[^<]*</span>', '', new, count=1)
    tail = new.rstrip()
    assert tail.endswith("</div>")
    new = tail[:-6].rstrip() + f'\n      <div class="hub-go">{go.group(1)}</div>\n    </a>'
    if dry: return f"DRY  {path}\n{new}"
    open(path, "w", encoding="utf-8").write(h[:s] + new + h[e + 6:])
    return f"OK   {path}"

if __name__ == "__main__":
    emoji, slug = sys.argv[1], sys.argv[2]
    dry = "--dry" in sys.argv
    files = [os.path.join(ROOT, "for/index.html")] + sorted(glob.glob(os.path.join(ROOT, "*/for/index.html")))
    ok = fail = skip = 0
    for f in files:
        r = activate(f, emoji, slug, dry)
        if dry: print(r); continue
        ok += r.startswith("OK"); skip += r.startswith("SKIP"); fail += r.startswith("FAIL")
        if r.startswith("FAIL"): print("  ⚠", r)
    if not dry: print(f"  активировано: {ok} · пропущено: {skip} · ошибок: {fail}")
