#!/usr/bin/env python3
"""Страница /data-deletion/ и раздел «вход через площадки» в /privacy-policy/ — для App Review Meta.

Строки локали — data_deletion/<loc>.json (ключи как в en.json). Страница удаления строится из
политики той же локали: те же шапка, стили, меню языков и подвал, меняются мета, крошки, H1 и
текст. Раздел политики встаёт перед третьим <h2> (после «Information Collection»). Ссылка
«Удаление данных» добавляется в подвал политики, лицензии и помощи — это три входящих ссылки.

Идемпотентно: повторный запуск ничего не дублирует.
    python3 seo/i18n_tools/data_deletion/assemble.py en ru ...
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
MARK = "<!--dd-section-->"


def page(loc, slug):
    return ROOT / (f"{slug}/index.html" if loc == "en" else f"{loc}/{slug}/index.html")


def url(loc, slug):
    return f"https://splitcam.com/{slug}" if loc == "en" else f"https://splitcam.com/{loc}/{slug}"


def attr(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def add_footer_link(html, loc, label):
    dd = url(loc, "data-deletion")
    if f'href="{dd}"' in html.split('<div class="footer-links">', 1)[-1]:
        return html
    pp = re.escape(url(loc, "privacy-policy"))
    m = re.search(rf'(<div class="footer-links">.*?<a href="{pp}"[^>]*>[^<]*</a>)', html, re.S)
    if not m:
        raise SystemExit(f"{loc}: нет ссылки на политику в подвале")
    return html[:m.end()] + f'\n      <a href="{dd}">{label}</a>' + html[m.end():]


def build(loc):
    t = json.loads((HERE / f"{loc}.json").read_text())
    pp_url, dd_url = url(loc, "privacy-policy"), url(loc, "data-deletion")
    src = page(loc, "privacy-policy").read_text()

    # --- Страница удаления: из политики той же локали, до правок политики.
    base = re.sub(r"\s*" + re.escape(MARK) + r".*?" + re.escape(MARK), "", src, flags=re.S)
    card_a = base.index('<div class="legal-card">') + len('<div class="legal-card">')
    card_b = base.index("</div>\n</section>", card_a)
    foot_a = base.index("<footer")
    foot_b = base.index("</footer>") + len("</footer>")
    head, card, mid, foot, tail = base[:card_a], base[card_a:card_b], base[card_b:foot_a], base[foot_a:foot_b], base[foot_b:]
    head = head.replace("/privacy-policy", "/data-deletion")
    mid = mid.replace("/privacy-policy", "/data-deletion")
    tail = tail.replace("/privacy-policy", "/data-deletion")

    head = re.sub(r"<title>.*?</title>", f"<title>{t['dd_title']}</title>", head, count=1, flags=re.S)
    for name in ("description", "og:description", "twitter:description"):
        head = re.sub(rf'(<meta (?:name|property)="{name}" content=")[^"]*', lambda m: m.group(1) + attr(t["dd_desc"]), head, count=1)
    for name in ("og:title", "twitter:title"):
        head = re.sub(rf'(<meta (?:name|property)="{name}" content=")[^"]*', lambda m: m.group(1) + attr(t["dd_title"]), head, count=1)
    head = re.sub(r'(<meta name="keywords" content=")[^"]*', lambda m: m.group(1) + attr(t["dd_keywords"]), head, count=1)
    # Видимая крошка; BreadcrumbList подгоняет crumb_sync.py --fix.
    head = re.sub(r'(<div class="breadcrumbs">.*?<span class="sep">/</span><span>)[^<]*(</span>)',
                  lambda m: m.group(1) + t["dd_crumb"] + m.group(2), head, count=1, flags=re.S)
    # Пробел перед выделенной частью — как в H1 политики той же локали: в ja/zh/th его нет.
    h1_src = re.search(r'<h1 class="h1">(.*?)<span class="accent">', base, re.S)
    gap = " " if h1_src and h1_src.group(1).endswith(" ") else ""
    head = re.sub(r'<h1 class="h1">.*?</h1>',
                  f'<h1 class="h1">{t["dd_h1_plain"]}{gap}<span class="accent">{t["dd_h1_accent"]}</span></h1>', head, count=1, flags=re.S)
    head = re.sub(r'(<p class="sub">).*?(</p>)', lambda m: m.group(1) + t["dd_sub"] + m.group(2), head, count=1, flags=re.S)
    card = "\n\n    " + t["dd_body"].replace("{PRIVACY_URL}", pp_url) + "\n\n  "
    foot = foot.replace(' class="active"', "")
    foot = add_footer_link(foot, loc, t["footer_label"]).replace(
        f'<a href="{dd_url}">', f'<a href="{dd_url}" class="active">', 1)
    out = page(loc, "data-deletion")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head + card + mid + foot + tail)

    # --- Раздел в политику: перед третьим <h2> карточки.
    pp = src
    if MARK not in pp:
        a = pp.index('<div class="legal-card">')
        h2s = [m.start() for m in re.finditer(r"<h2>", pp[a:])]
        at = a + h2s[2]
        # Политика fil и hi на сайте написана по-английски — раздел в неё тоже английский,
        # чтобы не смешивать два языка на одной странице.
        pp_t = t
        if "We gather information like IP addresses" in pp:
            pp_t = json.loads((HERE / "en.json").read_text())
        section = pp_t["pp_section"].replace("{DD_URL}", dd_url).rstrip()
        pp = pp[:at] + f"{MARK}\n    {section}\n    {MARK}\n\n    " + pp[at:]
    pp = add_footer_link(pp, loc, t["footer_label"])
    page(loc, "privacy-policy").write_text(pp)

    for slug in ("license-agreement", "help"):
        p = page(loc, slug)
        p.write_text(add_footer_link(p.read_text(), loc, t["footer_label"]))
    print(f"{loc}: ok")


if __name__ == "__main__":
    for loc in sys.argv[1:]:
        build(loc)
