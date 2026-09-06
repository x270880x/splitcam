# -*- coding: utf-8 -*-
"""Выпуск подготовленной страницы /alternatives/<slug>/ из скрытого состояния в живое.

   python3 seo/release_page.py <slug> <hub_cards.json> [--dry]

Страницы собираются заранее и лежат закрытыми (noindex, без карточки в хабе, вне PAGE_PATHS
и карты сайта). Этот скрипт открывает одну страницу целиком и во всех 35 локалях сразу —
чтобы выпуск нельзя было сделать наполовину, как это уже случалось: карточки хаба однажды
включили до того, как появились страницы локалей, и получилось 34 битые ссылки.

Что делает, по порядку:
  1. снимает noindex со всех 35 файлов, возвращая обычное значение robots;
  2. вставляет карточку в хаб /alternatives/ во всех 35 локалях, текст берётся из json;
  3. добавляет путь в PAGE_PATHS (seo/i18n_wire.py);
  4. запускает i18n_wire.py — hreflang, переключатель языков, карта сайта;
  5. синхронизирует крошки и FAQ-разметку;
  6. прогоняет page_audit и linkcheck и ОТКАЗЫВАЕТСЯ считать выпуск состоявшимся при 🔴.
Деплой намеренно НЕ делает: это отдельный осознанный шаг по скиллу splitcam-deploy.
"""
import re, os, sys, json, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT); sys.path.insert(0, os.path.join(ROOT, "seo"))
from i18n import LANG_ORDER, LANG_PATH

ROBOTS = "index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"
esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def hub_path(loc):
    return os.path.join(LANG_PATH[loc], "alternatives", "index.html")

def page_path(loc, slug):
    return os.path.join(LANG_PATH[loc], "alternatives", slug, "index.html")

def card_html(loc, slug, c):
    href = f"https://splitcam.com/{LANG_PATH[loc]}alternatives/{slug}"
    return (f'<a class="hub-card" href="{href}">\n'
            f'      <div class="hub-ico vs">vs</div>\n'
            f'      <h3>{esc(c["h3"])}</h3>\n'
            f'      <div class="hub-meta">{esc(c["meta"])}</div>\n'
            f'      <p>{esc(c["p"])}</p>\n'
            f'      <div class="hub-go">{esc(c["go"])}</div>\n'
            f'    </a>')

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    slug, cards_file = args[0], args[1]
    cards = json.load(open(cards_file, encoding="utf-8"))          # {loc: {h3, meta, p, go}}
    key = slug.replace("-", "_")
    problems, opened, carded = [], 0, 0

    # 0. предполётная проверка: страница обязана существовать во всех 35 локалях
    missing = [L for L in LANG_ORDER if not os.path.exists(page_path(L, slug))]
    if missing:
        print(f"  🔴 страницы нет в локалях: {missing}"); raise SystemExit(1)
    if "en" not in cards and not all(L in cards for L in LANG_ORDER if L != "en"):
        miss = [L for L in LANG_ORDER if L != "en" and L not in cards]
        print(f"  🔴 нет текста карточки для локалей: {miss}"); raise SystemExit(1)

    # 1. снять noindex
    for L in LANG_ORDER:
        p = page_path(L, slug); h = open(p, encoding="utf-8").read()
        if "noindex" not in h: continue
        nh = re.sub(r'(<meta name="robots" content=")[^"]*(")', lambda m: m.group(1) + ROBOTS + m.group(2), h, count=1)
        nh = re.sub(r'<!-- HOLD:.*?-->\n', '', nh, flags=re.S)
        if not dry: open(p, "w", encoding="utf-8").write(nh)
        opened += 1

    # 2. карточка в хаб
    for L in LANG_ORDER:
        hp = hub_path(L); h = open(hp, encoding="utf-8").read()
        if f"alternatives/{slug}" in h: continue
        i = h.find('<div class="hub-grid">')
        if i < 0: problems.append((L, "нет сетки хаба")); continue
        end = h.find("</section>", i)
        last = h.rfind("</a>", i, end)
        if last < 0: problems.append((L, "нет ни одной карточки")); continue
        c = cards["en"] if L == "en" and "en" in cards else cards.get(L)
        if not c: problems.append((L, "нет текста карточки")); continue
        ins = last + len("</a>")
        nh = h[:ins] + "\n\n    " + card_html(L, slug, c) + h[ins:]
        if not dry: open(hp, "w", encoding="utf-8").write(nh)
        carded += 1

    # 3. PAGE_PATHS
    wp = os.path.join(ROOT, "seo", "i18n_wire.py"); w = open(wp, encoding="utf-8").read()
    entry = f'"alternatives/{slug}/"'
    if entry not in w:
        w2 = w.replace('"alternatives/vmix/",', f'"alternatives/vmix/", {entry},', 1)
        if w2 == w: problems.append(("PAGE_PATHS", "не нашёл якорь для вставки"))
        elif not dry: open(wp, "w", encoding="utf-8").write(w2)

    print(f"  {'(dry) ' if dry else ''}снят noindex: {opened} · карточек добавлено: {carded} · проблем: {len(problems)}")
    for p in problems: print("   🔴", p)
    if dry or problems:
        if problems: raise SystemExit(1)
        return

    # 4-6. обвязка и проверки
    for step, cmd in (("i18n_wire", "python3 seo/i18n_wire.py"),
                      ("крошки",     f"python3 seo/crumb_sync.py --fix alternatives/{slug}/"),
                      ("FAQ",        f"python3 seo/faq_sync.py --fix alternatives/{slug}/"),
                      ("аудит",      "python3 seo/page_audit.py --quiet"),
                      ("ссылки",     "python3 seo/linkcheck.py --no-network")):
        code, out = run(cmd)
        tail = [l for l in out.strip().splitlines() if l.strip()][-1:] or [""]
        red = "🔴" in out or (step == "аудит" and code != 0)
        print(f"  {'🔴' if red else '✅'} {step}: {tail[0][:110]}")
        if red: problems.append((step, "красные находки"))
    # карточки в сетке по три: остаток 1 оставляет сироту в последнем ряду
    n = len(re.findall(r'<a class="hub-card"', open(hub_path("en"), encoding="utf-8").read()))
    if n % 3 == 1: print(f"  ⚠ карточек в хабе {n}: последний ряд с одной сиротой, сетка repeat(3,1fr)")
    print("\n  " + ("🔴 ВЫПУСК НЕ СОСТОЯЛСЯ — сначала исправить" if problems
                    else f"✅ /alternatives/{slug}/ открыта во всех 35 локалях. Осталось: деплой по скиллу splitcam-deploy."))
    raise SystemExit(1 if problems else 0)

if __name__ == "__main__":
    main()
