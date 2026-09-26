# -*- coding: utf-8 -*-
"""Новая версия SplitCam для Windows на сайте: запись в changelog ×35 + версия по сайту.

   python3 seo/release_windows.py <history.txt> --summary-file s.txt      стабильная
   python3 seo/release_windows.py <history.txt> --beta                    бета: только changelog
   ... --no-installer      номер версии без ссылки (установщика ещё нет на GitHub)
   ... --notes out.md      заодно записать текст релиза для gh release create
   ... --notes out.md --notes-only    только текст релиза, сайт не трогать
   python3 seo/release_windows.py --collapse-only                  только свернуть лишние раскрытые записи

<history.txt> — файл разработчика (https://splitstream.com/splitcam-update/history.txt).
Берётся верхний блок: «SplitCam vX», строка из дефисов, дата «Month D, YYYY», разделы
NEW / UPDATED / FIXED с пунктами «- …» (перенос строки внутри пункта склеивается).
--summary-file — абзац по-английски для JSON-LD releaseNotes последнего релиза
(стиль: «New — …; …. Updated — …. Fixed — ….»). Для беты не нужен.

Что делает (порядок процедуры и проверок — в скилле splitcam-release):
  1. В каждом из 35 changelog вставляет запись над верхней записью панели Windows. Шаблон —
     та же верхняя запись в этой же локали, поэтому подписи разделов остаются местными.
     Заметки — по-английски, дата — по-английски, как во всех локалях.
  2. Счётчик вкладки Windows и числа в шапке («N releases … M releases») ставит равными
     реальному числу записей в панелях Windows и macOS: в fa — персидскими цифрами,
     в ru, uk, pl, hr, sk, ro, ar — с согласованием слова с числом.
  3. Только для стабильной: JSON-LD softwareVersion и запись «SplitCam for Windows vX»,
     затем старая версия меняется на новую на страницах из PAGES: разметка, «Latest vX»,
     метки продукта, текст на virtual-audio-windows, alternatives/restream и в 404.
     Блок «What's new» на главной и ссылку на него в подвале НЕ трогает: карточки там
     описывают прежние функции, а в tr к номеру версии приклеен падежный суффикс.
Не коммитит и не деплоит. После запуска — page_audit, linkcheck, коммит, i18n_wire.py
(lastmod в sitemap берётся из git, поэтому ПОСЛЕ коммита), второй коммит.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT); sys.path.insert(0, os.path.join(ROOT, "seo"))
from i18n import LANG_ORDER, LANG_PATH

PERSIAN = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
GH = "https://github.com/x270880x/splitcam-release/releases/download/v{v}/{v}_x64.msi"
PAGES = ["", "products/", "features/", "donate-us/", "download/", "virtual-audio-windows/", "alternatives/restream/"]
PROSE = ("virtual-audio-windows/", "alternatives/restream/")        # там версия стоит в тексте — меняется целиком
MONTHS = "January February March April May June July August September October November December".split()


def plural_word(loc, n, word):
    """Слово после числа в шапке changelog — для языков, где форма зависит от числа."""
    d, dd = n % 10, n % 100
    slav = lambda one, few, many: one if d == 1 and dd != 11 else few if 2 <= d <= 4 and not 12 <= dd <= 14 else many
    if loc == "ru": return slav("релиз", "релиза", "релизов")
    if loc == "uk": return slav("реліз", "релізи", "релізів")
    if loc == "hr": return slav("izdanje", "izdanja", "izdanja")
    if loc == "pl": return "wydanie" if n == 1 else "wydania" if 2 <= d <= 4 and not 12 <= dd <= 14 else "wydań"
    if loc == "sk": return "vydanie" if n == 1 else "vydania" if 2 <= n <= 4 else "vydaní"
    if loc == "ro": return ("de lansări" if dd == 0 or dd >= 20 else "lansări") if n != 1 else "lansare"
    if loc == "ar": return "إصدارًا" if 11 <= dd <= 99 else "إصدارات" if 3 <= dd <= 10 else "إصدار"
    return word                                                     # остальные: форма от числа не зависит


CHEV = ('<svg class="rel-chev" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>')


def collapse_extra_open(s, keep=3):
    """В панели Windows раскрытыми остаются только верхние `keep` записей (так обещает вводный текст
    «Top 3 expanded by default» во всех локалях). Остальные open-<article> превращаются в <details>
    ровно как это делали выпуски macOS (коммиты 1d6409ac, 2ccd44c1)."""
    pw, pm = s.index('id="panel-win"'), s.index('id="panel-mac"')
    blocks = list(re.finditer(r'<article class="release open" id="win-v[\d.]+">.*?</article>', s[pw:pm], re.S))
    for b in reversed(blocks[keep:]):
        t = b.group(0)
        t = t.replace('<article class="release open"', '<details class="release"', 1)
        t = t.replace('<header class="rel-head">', '<summary class="rel-head">', 1)
        t, n = re.subn(r'\n([ \t]*)</header>', lambda m: f"\n{m.group(1)}  {CHEV}\n{m.group(1)}</summary>", t, count=1)
        assert n == 1
        t = t[: -len("</article>")] + "</details>"
        a, e = pw + b.start(), pw + b.end()
        s = s[:a] + t + s[e:]
    return s, max(0, len(blocks) - keep)


def parse_history(path):
    txt = open(path, encoding="utf-8", errors="replace").read().replace("\r\n", "\n")  # в старых записях есть байт cp1252
    top = re.split(r"\n(?=SplitCam v\d)", txt.lstrip("﻿"))[0]
    assert top.isascii(), "верхний блок history.txt не чистый ASCII — проверить вручную"
    lines = top.split("\n")
    ver = re.fullmatch(r"SplitCam v(\d+(?:\.\d+)+)", lines[0].strip()).group(1)
    date = lines[2].strip()
    mo, day, year = re.fullmatch(r"([A-Z][a-z]+) (\d{1,2}), (\d{4})", date).groups()
    iso = f"{year}-{MONTHS.index(mo) + 1:02d}-{int(day):02d}"
    secs, cur = {"NEW": [], "UPDATED": [], "FIXED": []}, None
    for line in lines[3:]:
        if line.strip() in secs:
            cur = line.strip(); continue
        if not line.strip():
            continue
        if line.startswith("- "):
            secs[cur].append(line[2:].strip())
        elif line.startswith(" ") and cur and secs[cur]:
            secs[cur][-1] += " " + line.strip()
        else:
            raise SystemExit(f"🔴 не разобрана строка history.txt: {line!r}")
    return ver, date, iso, secs


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--collapse-only" in sys.argv:                               # разовая починка без нового релиза
        for loc in LANG_ORDER:
            f = LANG_PATH[loc] + "changelog/index.html"
            t, n = collapse_extra_open(open(f, encoding="utf-8").read())
            if n:
                open(f, "w", encoding="utf-8").write(t)
            print(f"  {loc}: свёрнуто {n}")
        return
    beta, no_inst = "--beta" in sys.argv, "--no-installer" in sys.argv
    ver, date, iso, secs = parse_history(args[0])
    home = open("index.html", encoding="utf-8").read()
    old = re.search(r'"softwareVersion": "([\d.]+)"', home).group(1)
    print(f"v{ver} ({date}) {'BETA' if beta else 'STABLE'}; версия сайта сейчас {old}; "
          + " / ".join(f"{k} {len(v)}" for k, v in secs.items()))
    if "--notes" in sys.argv:                                       # текст релиза для GitHub
        out = ([f"**Beta build.** Not the current stable release — splitcam.com and auto-update stay on {old}.", "", date, ""]
               if beta else [f"**SplitCam {ver}** — released {date}", ""])
        for k in ("NEW", "UPDATED", "FIXED"):
            if secs[k]:
                out += [f"**{k}**"] + [f"- {i}" for i in secs[k]] + [""]
        np = sys.argv[sys.argv.index("--notes") + 1]
        open(np, "w", encoding="utf-8").write("\n".join(out).rstrip() + "\n"); print(f"notes → {np}")
        if "--notes-only" in sys.argv:
            return
    assert ver != old, "эта версия уже стоит на сайте"
    summary = None
    if not beta:
        sf = sys.argv[sys.argv.index("--summary-file") + 1] if "--summary-file" in sys.argv else None
        if not sf:
            raise SystemExit("🔴 стабильной нужен --summary-file (абзац для JSON-LD releaseNotes)")
        summary = open(sf, encoding="utf-8").read().strip()

    li = lambda items: "\n".join(f"        <li>{html.escape(i, quote=True)}</li>" for i in items)
    ver_link = GH.format(v=ver)

    for loc in LANG_ORDER:
        f = LANG_PATH[loc] + "changelog/index.html"
        s = open(f, encoding="utf-8").read()
        assert f'id="win-v{ver}"' not in s, f"{f}: запись v{ver} уже есть"
        pw = s.index('id="panel-win"'); pm = s.index('id="panel-mac"')
        m = re.compile(r'\n([ \t]*)(<article class="release open" id="win-v([\d.]+)">.*?</article>)', re.S).search(s, pw)
        assert m and m.start() < pm, f"{f}: не найдена верхняя запись панели Windows"
        indent, tmpl, tv = m.group(1), m.group(2), m.group(3)
        new = tmpl.replace(f'id="win-v{tv}"', f'id="win-v{ver}"')
        new = re.sub(r'\n[ \t]*<span class="rel-beta">beta</span>', "", new)
        head = re.search(r'<(a|span) class="rel-ver".*?</\1>', new, re.S)
        svg = re.search(r"<svg.*?</svg>", head.group(0), re.S)
        if no_inst:
            rel = f'<span class="rel-ver">v{ver}</span>'
        else:
            t = f"Download v{ver}{' beta' if beta else ''} installer (.msi)"
            rel = (f'<a class="rel-ver" href="{ver_link}" title="{t}" target="_blank" rel="noopener" '
                   f'onclick="event.stopPropagation()">v{ver}{svg.group(0) if svg else ""}</a>')
        if beta:
            ind = re.search(r"\n([ \t]*)<(?:a|span) class=\"rel-ver\"", new).group(1)
            rel += f'\n{ind}<span class="rel-beta">beta</span>'
        new = new[:head.start()] + rel + new[head.end():]
        new, n = re.subn(r'<time class="rel-date">[^<]*</time>', f'<time class="rel-date">{date}</time>', new)
        assert n == 1, (f, "rel-date")
        for cls, key in (("new", "NEW"), ("updated", "UPDATED"), ("fixed", "FIXED")):
            pat = re.compile(r'(\n[ \t]*<div class="rel-sec ' + cls + r'">\s*<h4 class="rel-h"><span class="rel-h-dot"></span>[^<]*</h4>\s*<ul class="rel-ul">\n)(.*?)(\n[ \t]*</ul>\s*</div>)', re.S)
            if secs[key]:
                new, n = pat.subn(lambda mm: mm.group(1) + li(secs[key]) + mm.group(3), new)
                assert n == 1, (f, f"в шаблоне нет раздела {cls} — добавить вручную")
            else:
                new = pat.sub("", new)                              # раздела нет в этом релизе
        assert tv not in new and (beta or "beta" not in new.lower()), (f, "остаток шаблона")
        s = s[:m.start()] + "\n" + indent + new + "\n\n" + indent + tmpl + s[m.end():]
        s, _ = collapse_extra_open(s)                               # раскрытыми остаются 3 верхние

        # счётчики: вкладка Windows + шапка («N releases» для Windows и macOS)
        pw, pm = s.index('id="panel-win"'), s.index('id="panel-mac"')
        pe = s.find('role="tabpanel"', pm + 20); pe = len(s) if pe < 0 else pe
        n_win = len(re.findall(r'<(?:article|details) class="release[" ]', s[pw:pm]))
        n_mac = len(re.findall(r'<(?:article|details) class="release[" ]', s[pm:pe]))
        dig = (lambda x: str(x).translate(PERSIAN)) if loc == "fa" else str
        s, n = re.subn(r'(data-target="panel-win">[^<]*<span class="tab-count">)[^<]*(</span>)',
                       lambda mm: mm.group(1) + dig(n_win) + mm.group(2), s)
        assert n == 1, (f, "tab-count")
        i = s.find("<h1"); hm = re.search(r"<p[^>]*>(.*?)</p>", s[i:], re.S)
        a, b = i + hm.start(1), i + hm.end(1)
        strongs = list(re.finditer(r"<strong>([\d۰-۹]+)(\s*)([^<]*)</strong>", s[a:b]))
        if loc != "sr":                                             # в sr шапка без чисел
            assert len(strongs) == 2, (f, "в шапке ожидалось два <strong>N …</strong>")
            p = s[a:b]
            for sm, cnt in reversed(list(zip(strongs, (n_win, n_mac)))):
                word = plural_word(loc, cnt, sm.group(3))
                p = p[:sm.start()] + f"<strong>{dig(cnt)}{sm.group(2)}{word}</strong>" + p[sm.end():]
            s = s[:a] + p + s[b:]

        if not beta:                                                # JSON-LD
            g = f'"softwareVersion": "{old}",\n      "datePublished": "2003-01-01"'
            assert s.count(g) == 1, (f, "общий softwareVersion")
            s = s.replace(g, g.replace(old, ver))
            bm = re.search(r'"name": "SplitCam for Windows v([\d.]+)",.*?"offers"', s, re.S)
            blk, pv = bm.group(0), bm.group(1)
            blk = blk.replace(f"v{pv}\"", f"v{ver}\"").replace(f"#win-v{pv}\"", f"#win-v{ver}\"")
            blk = re.sub(r'"softwareVersion": "[\d.]+"', f'"softwareVersion": "{ver}"', blk)
            blk = re.sub(r'"datePublished": "[\d-]+"', f'"datePublished": "{iso}"', blk)
            if '"releaseNotes": "https://' not in blk:                 # hr держит ссылку вместо текста
                blk = re.sub(r'"releaseNotes": "(?:[^"\\]|\\.)*"',
                             lambda _: '"releaseNotes": ' + json.dumps(summary, ensure_ascii=False), blk)
            s = s[:bm.start()] + blk + s[bm.end():]
        open(f, "w", encoding="utf-8").write(s)
    print(f"changelog: 35 локалей, Windows {n_win} записей, macOS {n_mac}")

    if beta:
        print("бета: версия сайта, JSON-LD, latest-указатели и ver.txt не тронуты — так и должно быть"); return
    pats = [r'("softwareVersion": ")' + re.escape(old) + r'(")',
            r"(data-dl-ver>[^<]*v)" + re.escape(old) + r"(<)",
            r"(ver: '[^']*v)" + re.escape(old) + r"(')",
            r'(product-tag tag-new">v)' + re.escape(old) + r"(<)",
            r'(pc-ver">v)' + re.escape(old) + r"(<)"]
    for page in PAGES:
        total, files = 0, 0
        for loc in LANG_ORDER:
            f = LANG_PATH[loc] + page + "index.html"
            if not os.path.exists(f):
                continue
            s = open(f, encoding="utf-8").read(); n = 0
            if page in PROSE:
                n = s.count(old); s = s.replace(old, ver)
            else:
                for p in pats:
                    s, k = re.subn(p, lambda mm: mm.group(1) + ver + mm.group(2), s); n += k
            assert n, f"{f}: версия {old} не найдена — разметка поменялась, проверить вручную"
            open(f, "w", encoding="utf-8").write(s); total += n; files += 1
        print(f"  /{page:28} {files:2} файлов, замен {total}")
    for f in ("404.html", "seo/i18n_tools/restream_copy.py"):      # restream_copy — исходник сборщика /alternatives/restream
        s = open(f, encoding="utf-8").read()
        if old in s:
            open(f, "w", encoding="utf-8").write(s.replace(old, ver)); print(f"  {f}")
    sys.stdout.flush()
    print(f"Остались упоминания {old} (ожидаемо: запись {old} в changelog, «What's new» на главной + ссылка в подвале):")
    os.system(f"grep -rl --include='*.html' '{re.escape(old)}' . | grep -vE '^\\./(seo|v2)/' | sed 's#^\\./##' "
              f"| sed -E 's#^[a-z]{{2,3}}/##' | sort | uniq -c")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
