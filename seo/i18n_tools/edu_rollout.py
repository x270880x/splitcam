# -*- coding: utf-8 -*-
"""Проверяет переводы educators, собирает 34 страницы, активирует карточки в хабах.
Запуск:  python3 seo/i18n_tools/edu_rollout.py <переводы.json> [--force]
"""
import json, os, sys, glob, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from edu_build_locale import build
from hub_activate import activate
ROOT = os.path.dirname(os.path.dirname(HERE))
SRCJSON = os.path.join(HERE, "src_for-educators.json")
TAGS = ["<strong>", "</strong>", "<b>", "</b>", '<span class="accent">', "</span>", "<br>", "<code>", "</code>"]
PLAT = re.compile(r'Windows|macOS')

def validate(tr_all):
    src = json.load(open(SRCJSON, encoding="utf-8"))
    probs = []
    for t in tr_all:
        loc, d = t["loc"], t.get("strings") or {}
        miss = [k for k in src if k not in d]
        if miss:  probs.append(f"{loc}: нет ключей {len(miss)} {miss[:4]}")
        extra = [k for k in d if k not in src]
        if extra: probs.append(f"{loc}: лишние {extra[:4]}")
        for k, v in d.items():
            if k not in src: continue
            o = src[k]
            for tag in TAGS:
                if o.count(tag) != v.count(tag):
                    probs.append(f"{loc}/{k}: тег {tag} {o.count(tag)}→{v.count(tag)}")
            if not v.strip(): probs.append(f"{loc}/{k}: пусто")
            if k.startswith("hw_a#") and PLAT.search(o) and not PLAT.search(v):
                probs.append(f"{loc}/{k}: потерян ярлык платформы «{o[-24:]}»")
        T, D_ = d.get("meta#title", ""), d.get("meta#description", "")
        if T and len(T) > 70: probs.append(f"{loc}: title {len(T)}")
        if D_ and not (110 <= len(D_) <= 185): probs.append(f"{loc}: description {len(D_)}")
    return probs

if __name__ == "__main__":
    tr = json.load(open(sys.argv[1], encoding="utf-8"))
    probs = validate(tr)
    print(f"=== ПРОВЕРКА ({len(tr)} локалей) ===")
    if probs:
        for p in probs[:40]: print("  ⚠", p)
        print(f"  всего: {len(probs)}")
        if "--force" not in sys.argv:
            print("\n  сборка не выполнена. --force, если замечания приемлемы."); sys.exit(1)
    else:
        print("  замечаний нет ✓")
    src = json.load(open(SRCJSON, encoding="utf-8"))
    good = [t for t in tr if not [k for k in src if k not in (t.get("strings") or {})]]
    bad  = [t["loc"] for t in tr if t not in good]
    n = 0
    for t in good: build(t["loc"], t["strings"]); n += 1
    print(f"\n=== СБОРКА ===\n  собрано: {n}")
    if bad: print(f"  🔴 пропущены (нужен повторный перевод): {', '.join(bad)}")
    print("\n=== КАРТОЧКИ В ХАБАХ ===")
    print("  (включаем только там, где страница существует)")
    ok = fail = skip = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "*/for/index.html"))):
        loc = os.path.relpath(f, ROOT).split("/")[0]
        if not os.path.isfile(os.path.join(ROOT, loc, "for", "educators", "index.html")):
            continue
        r = activate(f, "🎓", "educators")
        ok += r.startswith("OK"); skip += r.startswith("SKIP"); fail += r.startswith("FAIL")
        if r.startswith("FAIL"): print("  ⚠", r)
    print(f"  активировано: {ok} · пропущено: {skip} · ошибок: {fail}")
