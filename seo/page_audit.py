# -*- coding: utf-8 -*-
"""SEO-аудит страницы во всех 35 локалях — обязательный шаг перед коммитом любой страницы.

   python3 seo/page_audit.py                       весь сайт (PAGE_PATHS × 35 локалей)
   python3 seo/page_audit.py stream-deck/ for/churches/    только эти страницы
   python3 seo/page_audit.py --locales ru,de stream-deck/  только эти локали
   python3 seo/page_audit.py --quiet                только сводка и 🔴
   python3 seo/page_audit.py --json out.json        полный список находок в JSON

Правило владельца (2026-09-05): каждая страница на каждом языке рождается сразу с правильными
title, description, тегами, H1, перелинковкой и хлебными крошками — полностью по правилам SEO —
и всё это проверяется автоматически, а не на глаз. Код выхода 1, если есть хоть одно 🔴.

Правила (id · уровень · что проверяется):
  T01 🔴 <title> есть, ≤60 символов (🟡 61–65), содержит «SplitCam», уникален в своей локали
  T02 🔴 description есть, 140–160 символов (🟡 120–139 / 161–165, 🔴 <120 или >165), уникален
  T03 🔴 ровно один <h1>, непустой
  T04 🔴 canonical = единственный URL страницы (без слеша в конце), og:url совпадает
  T05 🔴 hreflang: 35 локалей + x-default, каждый ведёт на существующий файл, обратная ссылка есть,
         своя локаль указана
  T06 🔴 <html lang> = локали (pt → pt-BR), dir="rtl" только у ar/he/fa
  T07 🟡 og:title/og:description/og:image, twitter:card/title/description; 🔴 og:image нет на диске
  T08 🟡 <meta keywords> есть и не пуст
  T09 🔴 robots не содержит noindex; есть viewport и charset
  T10 🔴 JSON-LD парсится, без aggregateRating
  T11 🔴 хлебные крошки: видимые ↔ BreadcrumbList (число, последнее имя, URL существуют,
         первый = корень локали); нет ни того, ни другого — допустимо только для главной
  T12 🔴 FAQ: видимые вопросы/ответы = FAQPage (число и текст)
  T13 🔴 Google Analytics G-S1THLDP1XV: gtag('config') ровно один раз
  T14 🔴 URL есть в sitemap.xml, путь есть в i18n_wire.PAGE_PATHS
  T15 🔴 входящие ссылки: ≥1 с других страниц той же локали (🟡 <3); хаб обязан ссылаться:
         alternatives/* ← /alternatives/, for/* ← /for/, feature-страницы ← /features/
  T16 🔴 все внутренние ссылки ведут на существующие файлы; 🟡 ссылка из локали на EN-версию
         страницы, у которой есть локальная версия
  T17 🔴 запрещённые фразы: «peer-to-peer» / «P2P» в видимом тексте (правило владельца)
  T18 🔴 скрипт автоопределения языка: location.replace только под guard «explicit»
  T19 🔴 структура локали = EN (порядок блочных тегов, ≥3 расхождений); changelog не сверяем
  T20 🟡 <img> без alt; 🔴 локальный src без файла
  T21 🟡 английские служебные слова в тексте локали (утечка перевода); fil/hi не считаем
  T22 🔴 title или description локали дословно = EN (не локализовано); fil/hi — исключение
  T23 🟡 RTL-локаль без блока <!--RTLCSS-->
  T24 🔴 H1 локали дословно = EN H1 (fil/hi — исключение)
  T25 🔴 комментарии в <head> не врут о странице: «SEO targeting» перечисляет ключи, которых нет
  T26 🔴 FAQ локали: вопрос дословно равен английскому при переведённом ответе, либо два одинаковых
         вопроса на странице. Найдено 2026-09-05: на virtual-audio-* в 31 локали 190 вопросов остались
         английскими при переведённых ответах, а часть переведённых стояла НЕ В СВОИХ слотах —
         `faq_sync` этого не видит, потому что подгоняет разметку под видимый текст, а испорчен был он.
  T27 🟡 строка JSON-LD дословно равна английской в поле, которое обязано переводиться
         (name/description/featureList/keywords/text) — непереведённая структурированная разметка
         ни в keywords локали, ни в EN (хвост шаблона, с которого страницу копировали);
         «Schema.org: …» перечисляет не те @type, что реально лежат в JSON-LD
"""
import re, os, sys, json, difflib, html as _html
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "seo"))
from i18n import LANG_ORDER, LANG_PATH, RTL_LANGS, page_url, SITE
from i18n_wire import PAGE_PATHS

LOCS = [L for L in LANG_ORDER]                      # en first
ENGLISH_TECH = {"fil", "hi"}                          # ищут технику по-английски (I18N-PLAN)
HUB_OF = {}                                           # страница → хаб, который обязан ссылаться
for _p in PAGE_PATHS:
    if _p.startswith("alternatives/") and _p != "alternatives/":
        HUB_OF[_p] = "alternatives/"
    elif _p.startswith("for/") and _p != "for/":
        HUB_OF[_p] = "for/"
    elif _p in ("virtual-camera/", "multistreaming/", "phone-as-webcam/", "multi-camera/",
                "stream-deck/", "virtual-audio-mac/", "virtual-audio-windows/"):
        HUB_OF[_p] = "features/"
EN_ONLY = {"download/"}                               # по замыслу только EN (CLAUDE.md: EN-only /download landing)
HOST_MANAGED = ("win-download/", "mac-download/", "ver.txt", "ver.php", ".well-known/")   # вне git, живут на хосте
CJK = {"ja", "zh", "ko"}                              # полноширинные символы: в сниппет входит вдвое меньше
GA = "G-S1THLDP1XV"
SCHEMA_TYPES = {"BreadcrumbList", "SoftwareApplication", "FAQPage", "HowTo", "ItemList", "WebPage",
                "WebSite", "Organization", "ContactPage", "TechArticle", "VideoObject", "Product",
                "Article", "Review", "AggregateRating", "Person", "ImageObject"}
FORBIDDEN = [re.compile(r"peer[\s-]*to[\s-]*peer", re.I), re.compile(r"\bP2P\b")]
EN_WORDS = re.compile(r"\b(the|and|with|your|from|this|that|which|when|without|into)\b")
BLOCK = {'div','section','table','thead','tbody','tr','td','th','ul','ol','li','h1','h2','h3','h4',
         'details','summary','p','article','nav','footer','header','main'}
SKIPR = re.compile(r'<!--(LD|HL|AD|RTLCSS)-->.*?<!--/\1-->', re.S)

strip = lambda s: _html.unescape(re.sub(r'\s+', ' ', re.sub('<[^>]*>', '', s))).strip()

LD_TRANSLATABLE = {"name", "description", "featureList", "keywords", "text"}

def _ld_strings(h):
    """Строки JSON-LD в полях, которые обязаны переводиться. Названия продуктов и версий
       (alternateName, softwareVersion, …) сюда не попадают — они одинаковы во всех языках."""
    out = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            g = json.loads(m.group(1))
        except Exception:
            continue
        def walk(o, k=""):
            if isinstance(o, dict):
                for kk, v in o.items(): walk(v, kk)
            elif isinstance(o, list):
                for v in o: walk(v, k)
            elif isinstance(o, str):
                v = re.sub(r'\s+', ' ', o).strip()
                if (k in LD_TRANSLATABLE and len(v) > 25 and not v.startswith("http")
                        and re.search(r"[A-Za-z]", v)
                        and not (k == "name" and v.startswith("SplitCam") and len(v) < 60)):
                    out.append((k, v))                    # имя продукта «SplitCam … for iOS» одинаково во всех языках
        walk(g)
    return out

def fpath(loc, page):
    return os.path.join(ROOT, LANG_PATH[loc], page, "index.html") if page else os.path.join(ROOT, LANG_PATH[loc], "index.html")

def url_of(loc, page):
    return page_url(LANG_PATH[loc], page)

def to_file(href, cur_loc):
    """internal href → repo file path or None (external/anchor/mail)."""
    if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
        return None
    if href.startswith("http"):
        if not href.startswith(SITE):
            return None
        href = href[len(SITE):] or "/"
    if not href.startswith("/"):
        return None                                   # относительные не используем
    href = href.split("#")[0].split("?")[0]
    p = href.strip("/")
    if p.startswith(HOST_MANAGED) or p in {h.strip("/") for h in HOST_MANAGED}:
        return None
    if re.search(r'\.(png|jpg|jpeg|webp|svg|gif|ico|css|js|xml|txt|pdf|mp4|webm|zip|dmg|exe|json|woff2?)$', p, re.I):
        return os.path.join(ROOT, p)
    return os.path.join(ROOT, p, "index.html") if p else os.path.join(ROOT, "index.html")

class Page:
    def __init__(self, loc, page):
        self.loc, self.page = loc, page
        self.path = fpath(loc, page)
        self.exists = os.path.exists(self.path)
        if not self.exists:
            return
        h = open(self.path, encoding="utf-8").read()
        self.h = h
        head = h[:h.find("<body")] if "<body" in h else h
        self.head = head
        self.body = h[h.find("<body"):] if "<body" in h else ""
        g = lambda rx, s=head: (re.search(rx, s, re.S) or [None, None])[1]
        self.title = strip(g(r"<title>(.*?)</title>") or "")
        self.desc = _html.unescape(g(r'<meta name="description" content="([^"]*)"') or "")
        self.kw = g(r'<meta name="keywords" content="([^"]*)"') or ""
        self.robots = g(r'<meta name="robots" content="([^"]*)"') or ""
        self.canonical = g(r'<link rel="canonical" href="([^"]*)"') or ""
        self.lang = g(r'<html[^>]*\blang="([^"]*)"', h[:400]) or ""
        self.dir = g(r'<html[^>]*\bdir="([^"]*)"', h[:400]) or ""
        self.hreflang = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', head))
        self.og = dict(re.findall(r'<meta property="og:([a-z_:]+)" content="([^"]*)"', head))
        self.tw = dict(re.findall(r'<meta name="twitter:([a-z_]+)" content="([^"]*)"', head))
        self.viewport = 'name="viewport"' in head
        self.charset = "charset=" in head.lower()
        self.h1 = [strip(x) for x in re.findall(r"<h1[^>]*>(.*?)</h1>", self.body, re.S)]
        self.ga_config = len(re.findall(r"gtag\('config',\s*'" + GA + "'", h))
        self.ld, self.ld_err = [], None
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            try:
                d = json.loads(m.group(1)); self.ld += d.get("@graph") or [d]
            except Exception as e:
                self.ld_err = str(e)[:60]
        bc = re.search(r'<div class="breadcrumbs">(.*?)</div>', self.body, re.S)
        self.crumbs = None
        if bc:
            self.crumbs = [strip(x) for x in re.findall(r'(?:<a[^>]*>|<span>)(.*?)(?:</a>|</span>)', bc.group(1), re.S)]
            self.crumbs = [c for c in self.crumbs if c and c != "/"]
        self.faq = [(strip(q), strip(a)) for q, a in re.findall(r'<summary>(.*?)</summary>\s*<p>(.*?)</p>', self.body, re.S)]
        if not self.faq:                              # /features/: FAQ свёрстан карточками connect-step h4/p
            sec = re.search(r'<section[^>]*id="faq"[^>]*>(.*?)</section>', self.body, re.S)
            if sec:
                self.faq = [(strip(q), strip(a)) for q, a in re.findall(r'<div class="connect-step"><h4>(.*?)</h4><p>(.*?)</p>', sec.group(1), re.S)]
        body_links = self.body
        body_links = SKIPR.sub("", body_links)
        self.links = re.findall(r'<a\s[^>]*href="([^"]+)"', body_links)
        self.imgs = re.findall(r'<img\b[^>]*>', self.body)
        # видимый текст
        t = SKIPR.sub("", self.body)
        t = re.sub(r'<script.*?</script>|<style.*?</style>', "", t, flags=re.S)
        self.text = strip(t)
        self.ad_ok = ("location.replace" not in h) or ("explicit" in h)

    def bseq(self):
        b = SKIPR.sub("", self.body)
        b = re.sub(r'<script.*?</script>|<style.*?</style>', "", b, flags=re.S)
        b = re.sub(r'<details class="lang[^"]*".*?</details>', "", b, flags=re.S)
        return [m.group(1).lower() for m in re.finditer(r'<(/?[a-zA-Z][a-zA-Z0-9]*)', b) if m.group(1).lower().lstrip('/') in BLOCK]

def audit(pages, locs, quiet=False):
    sitemap = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read() if os.path.exists(os.path.join(ROOT, "sitemap.xml")) else ""
    # граф входящих ссылок по всей локали (по всем PAGE_PATHS, не только по проверяемым)
    cache = {}
    def P(loc, page):
        k = (loc, page)
        if k not in cache:
            cache[k] = Page(loc, page)
        return cache[k]
    inbound = defaultdict(set)      # (loc, url) → {source page}
    for loc in locs:
        for pg in PAGE_PATHS:
            src = P(loc, pg)
            if not src.exists:
                continue
            for href in src.links:
                u = href if href.startswith("http") else (SITE + href if href.startswith("/") else None)
                if u:
                    u = u if u.endswith("/") and u.count("/") <= 4 else u.rstrip("/")
                    inbound[u].add(pg)
    findings = []                    # (sev, loc, page, rule, msg)
    F = lambda sev, loc, page, rule, msg: findings.append((sev, loc, page, rule, msg))
    for page in pages:
        en = P("en", page)
        titles, descs = defaultdict(list), defaultdict(list)
        for loc in locs:
            p = P(loc, page)
            if not p.exists:
                if loc != "en" and page in EN_ONLY: continue
                F("🔴", loc, page, "T00", "файла нет"); continue
            tmax, tyel = (32, 36) if loc in CJK else (60, 65)
            dlo, dhi, dred_lo, dred_hi = (70, 100, 50, 110) if loc in CJK else (140, 160, 120, 165)
            url = url_of(loc, page)
            # T01
            if not p.title: F("🔴", loc, page, "T01", "нет <title>")
            else:
                n = len(p.title)
                if n > tyel: F("🔴", loc, page, "T01", f"title {n} символов (>{tyel})")
                elif n > tmax: F("🟡", loc, page, "T01", f"title {n} символов ({tmax+1}–{tyel})")
                if "splitcam" not in p.title.lower(): F("🟡", loc, page, "T01", "в title нет «SplitCam»")
            # T02
            n = len(p.desc)
            if not p.desc: F("🔴", loc, page, "T02", "нет description")
            elif n < dred_lo or n > dred_hi: F("🔴", loc, page, "T02", f"description {n} символов (норма {dlo}–{dhi})")
            elif n < dlo or n > dhi: F("🟡", loc, page, "T02", f"description {n} символов (норма {dlo}–{dhi})")
            # T03
            if len(p.h1) != 1: F("🔴", loc, page, "T03", f"<h1> ×{len(p.h1)}")
            elif not p.h1[0]: F("🔴", loc, page, "T03", "пустой <h1>")
            # T04
            if p.canonical != url: F("🔴", loc, page, "T04", f"canonical «{p.canonical}» ≠ «{url}»")
            if p.og.get("url") and p.og["url"] != url: F("🔴", loc, page, "T04", f"og:url «{p.og['url']}» ≠ canonical")
            # T05
            exp = {L for L in LANG_ORDER if P(L, page).exists} | {"x-default"}
            have = set(p.hreflang)
            if have != exp:
                F("🔴", loc, page, "T05", f"hreflang {len(have)} вместо {len(exp)}: нет {sorted(exp-have)[:5]} лишние {sorted(have-exp)[:5]}")
            if p.hreflang.get(loc) != url: F("🔴", loc, page, "T05", f"своя hreflang «{p.hreflang.get(loc)}» ≠ «{url}»")
            if p.hreflang.get("x-default") != url_of("en", page): F("🔴", loc, page, "T05", "x-default не на EN")
            for L, href in p.hreflang.items():
                if L == "x-default": continue
                tf = to_file(href, loc)
                if not tf or not os.path.exists(tf): F("🔴", loc, page, "T05", f"hreflang {L} → {href}: файла нет")
                elif L in locs or L == "en":
                    back = P(L, page)
                    if back.exists and back.hreflang.get(loc) != url:
                        F("🔴", loc, page, "T05", f"{L} не ссылается обратно на {loc}")
            # T06
            want_lang = "pt-BR" if loc == "pt" else loc
            if p.lang != want_lang: F("🔴", loc, page, "T06", f"lang=«{p.lang}», ожидалось «{want_lang}»")
            if (loc in RTL_LANGS) != (p.dir == "rtl"): F("🔴", loc, page, "T06", f"dir=«{p.dir}» для {loc}")
            # T07
            for k in ("title", "description", "image"):
                if not p.og.get(k): F("🟡", loc, page, "T07", f"нет og:{k}")
            for k in ("card", "title", "description"):
                if not p.tw.get(k): F("🟡", loc, page, "T07", f"нет twitter:{k}")
            if p.og.get("image"):
                tf = to_file(p.og["image"], loc)
                if tf and not os.path.exists(tf): F("🔴", loc, page, "T07", f"og:image нет на диске: {p.og['image']}")
            if p.og.get("title") and p.og["title"] != p.title and _html.unescape(p.og["title"]) != p.title:
                F("🟡", loc, page, "T07", "og:title ≠ title")
            # T08
            if not p.kw.strip(): F("🟡", loc, page, "T08", "нет keywords")
            # T09
            if "noindex" in p.robots: F("🔴", loc, page, "T09", "robots noindex")
            if not p.viewport: F("🔴", loc, page, "T09", "нет viewport")
            if not p.charset: F("🟡", loc, page, "T09", "нет charset")
            # T10
            if p.ld_err: F("🔴", loc, page, "T10", f"JSON-LD не парсится: {p.ld_err}")
            if "aggregateRating" in p.h: F("🔴", loc, page, "T10", "aggregateRating запрещён")
            # T11
            bl = [x for x in p.ld if x.get("@type") == "BreadcrumbList"]
            if p.crumbs is None and not bl:
                if page != "": F("🔴", loc, page, "T11", "нет хлебных крошек (видимых и BreadcrumbList)")
            elif p.crumbs is None or not bl:
                F("🔴", loc, page, "T11", "крошки есть только " + ("в разметке" if not p.crumbs else "видимые"))
            else:
                items = bl[0].get("itemListElement", [])
                names = [strip(i.get("name", "")) for i in items]
                if len(items) != len(p.crumbs): F("🔴", loc, page, "T11", f"крошек видимых {len(p.crumbs)}, в BreadcrumbList {len(items)}")
                elif names[-1] != p.crumbs[-1]:
                    a, b = names[-1].lower(), p.crumbs[-1].lower()
                    F("🟡" if (a in b or b in a) else "🔴", loc, page, "T11", f"последняя крошка «{p.crumbs[-1]}» ≠ «{names[-1]}» в BreadcrumbList")
                for i in items:
                    it = i.get("item") or ""
                    tf = to_file(it, loc)
                    if it and tf and not os.path.exists(tf): F("🔴", loc, page, "T11", f"крошка → {it}: файла нет")
                if items and (items[0].get("item") or "").rstrip("/") != url_of(loc, "").rstrip("/"):
                    F("🔴", loc, page, "T11", f"первая крошка «{items[0].get('item')}» ≠ корень локали")
            # T12
            fq = [x for x in p.ld if x.get("@type") == "FAQPage"]
            if p.faq and not fq: F("🔴", loc, page, "T12", "видимый FAQ без FAQPage")
            elif fq and not p.faq: F("🔴", loc, page, "T12", "FAQPage без видимого FAQ")
            elif fq:
                ent = fq[0].get("mainEntity", [])
                if len(ent) != len(p.faq): F("🔴", loc, page, "T12", f"FAQ видимых {len(p.faq)}, в разметке {len(ent)}")
                else:
                    dq = sum(1 for (q, _), j in zip(p.faq, ent) if strip(j.get("name", "")) != q)
                    da = sum(1 for (_, a), j in zip(p.faq, ent) if strip(j.get("acceptedAnswer", {}).get("text", "")) != a)
                    if dq or da: F("🔴", loc, page, "T12", f"FAQ расходится: вопросов {dq}, ответов {da}")
            # T13
            if p.ga_config != 1: F("🔴", loc, page, "T13", f"gtag config ×{p.ga_config}")
            # T14
            if f"<loc>{url}</loc>" not in sitemap: F("🔴", loc, page, "T14", "нет в sitemap.xml")
            if page not in PAGE_PATHS: F("🔴", loc, page, "T14", "нет в i18n_wire.PAGE_PATHS")
            # T15
            key = url if page == "" else url.rstrip("/")
            srcs = {s for s in inbound.get(key, set()) if s != page}
            if page != "":
                if not srcs: F("🔴", loc, page, "T15", "0 входящих ссылок в локали")
                elif len(srcs) < 3: F("🟡", loc, page, "T15", f"входящих ссылок {len(srcs)}: {sorted(srcs)}")
                hub = HUB_OF.get(page)
                if hub and hub not in srcs: F("🔴", loc, page, "T15", f"хаб /{hub} не ссылается на страницу")
            # T16
            for href in p.links:
                tf = to_file(href, loc)
                if tf is None: continue
                if not os.path.exists(tf): F("🔴", loc, page, "T16", f"битая ссылка {href}")
                elif loc != "en" and href.startswith(SITE + "/") and not re.match(SITE + r"/([a-z]{2,3})/", href):
                    rel_ = href[len(SITE):].strip("/")
                    if rel_ and not re.search(r'\.\w{2,5}$', rel_) and os.path.exists(os.path.join(ROOT, loc, rel_, "index.html")):
                        F("🟡", loc, page, "T16", f"ссылка на EN {href}, хотя есть /{loc}/{rel_}")
            # T17
            for rx in FORBIDDEN:
                m = rx.search(p.text)
                if m: F("🔴", loc, page, "T17", f"запрещённая фраза «{m.group(0)}»")
            # T18
            if not p.ad_ok: F("🔴", loc, page, "T18", "location.replace без guard explicit")
            # T19
            if loc != "en" and en.exists and page != "changelog/":
                es, ls = en.bseq(), p.bseq()
                if es != ls:
                    ops = [o for o in difflib.SequenceMatcher(None, es, ls, autojunk=False).get_opcodes() if o[0] != "equal"]
                    if len(ops) >= 3:
                        o = ops[0]
                        F("🔴", loc, page, "T19", f"структура ≠ EN: {len(ops)} правок; первая {o[0]} EN[{o[1]}:{o[2]}]={' '.join(es[o[1]:o[2]][:4])}")
            # T20
            noalt = sum(1 for i in p.imgs if not re.search(r'\balt="', i))
            if noalt: F("🟡", loc, page, "T20", f"<img> без alt ×{noalt}")
            for i in p.imgs:
                s = re.search(r'\bsrc="([^"]+)"', i)
                if s:
                    tf = to_file(s.group(1), loc)
                    if tf and not os.path.exists(tf): F("🔴", loc, page, "T20", f"картинки нет: {s.group(1)}")
            # T21
            if loc != "en" and loc not in ENGLISH_TECH and page != "changelog/":
                n = len(EN_WORDS.findall(p.text))
                if n >= 12: F("🟡", loc, page, "T21", f"английских служебных слов в тексте: {n}")
            # T22 / T24
            if loc != "en" and en.exists and loc not in ENGLISH_TECH:
                if p.title == en.title: F("🔴", loc, page, "T22", "title = EN (не локализован)")
                if p.desc == en.desc: F("🔴", loc, page, "T22", "description = EN (не локализован)")
                if p.h1 and en.h1 and p.h1[0] == en.h1[0]: F("🔴", loc, page, "T24", "H1 = EN (не локализован)")
            # T23
            if loc in RTL_LANGS and "<!--RTLCSS-->" not in p.h: F("🟡", loc, page, "T23", "нет блока RTLCSS")
            # T25 — комментарии в <head> сверяются со страницей, а не с шаблоном, с которого её копировали
            cm = re.search(r'<!--\s*SEO targeting:(.*?)-->', p.head, re.S)
            if cm:
                keys = re.findall(r'"([^"]+)"', cm.group(1))
                kws = (p.kw + " " + (en.kw if en.exists else "")).lower()
                if keys and not any(k.lower() in kws for k in keys):
                    F("🔴", loc, page, "T25", f"комментарий SEO targeting не про эту страницу: {keys[:3]} нет в keywords")
            cm = re.search(r'<!--\s*Schema\.org:([^>]*?)-->', p.head)
            if cm:
                real = {x.get("@type") for x in p.ld if x.get("@type")}
                voc = real | SCHEMA_TYPES
                claimed = {t for t in voc if re.search(r'\b' + re.escape(t) + r'\b', cm.group(1))}
                if claimed != real:
                    F("🔴", loc, page, "T25", f"комментарий Schema.org: заявлено {sorted(claimed)}, в JSON-LD {sorted(real)}")
            # T26 — вопрос FAQ против английского и против соседей по странице
            if loc != "en" and en.exists and loc not in ENGLISH_TECH and p.faq:
                en_q = {q for q, _ in en.faq}
                for i, (q, a) in enumerate(p.faq, 1):
                    if q in en_q and i <= len(en.faq) and a != en.faq[i - 1][1]:
                        F("🔴", loc, page, "T26", f"вопрос {i} остался английским при переведённом ответе: «{q[:55]}»")
                dup = [q for q, n in Counter(q for q, _ in p.faq).items() if n > 1]
                if dup: F("🔴", loc, page, "T26", f"вопрос повторяется на странице: «{dup[0][:55]}»")
            # T27 — непереведённая структурированная разметка
            if loc != "en" and en.exists and loc not in ENGLISH_TECH:
                en_ld = {v for _, v in _ld_strings(en.h)}
                same = [(k, v) for k, v in _ld_strings(p.h) if v in en_ld]
                if same:
                    F("🟡", loc, page, "T27", f"строк JSON-LD не переведено: {len(same)}, первая — {same[0][0]}: «{same[0][1][:55]}»")
            titles[loc].append(p.title); descs[loc].append(p.desc)
    # уникальность title/description внутри локали по всему сайту
    for loc in locs:
        seen_t, seen_d = defaultdict(list), defaultdict(list)
        for pg in PAGE_PATHS:
            q = P(loc, pg)
            if q.exists:
                seen_t[q.title].append(pg); seen_d[q.desc].append(pg)
        for t, pgs in seen_t.items():
            if len(pgs) > 1 and any(x in pages for x in pgs): F("🔴", loc, pgs[0], "T01", f"дубликат title на {pgs}")
        for d, pgs in seen_d.items():
            if d and len(pgs) > 1 and any(x in pages for x in pgs): F("🔴", loc, pgs[0], "T02", f"дубликат description на {pgs}")
    return findings

def main():
    args = sys.argv[1:]
    quiet = "--quiet" in args; args = [a for a in args if a != "--quiet"]
    jout = None
    if "--json" in args:
        i = args.index("--json"); jout = args[i + 1]; del args[i:i + 2]
    locs = LOCS
    if "--locales" in args:
        i = args.index("--locales"); locs = ["en"] + [l for l in args[i + 1].split(",") if l != "en"]; del args[i:i + 2]
    pages = [a.strip("/") + "/" if a.strip("/") else "" for a in args] or list(PAGE_PATHS)
    fs = audit(pages, locs, quiet)
    red = [f for f in fs if f[0] == "🔴"]; yel = [f for f in fs if f[0] == "🟡"]
    if jout:
        json.dump([dict(sev=a, loc=b, page=c, rule=d, msg=e) for a, b, c, d, e in fs], open(jout, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    per = defaultdict(lambda: [0, 0])
    for s, loc, page, rule, msg in fs:
        per[page][0 if s == "🔴" else 1] += 1
    print(f"page_audit: страниц {len(pages)} × локалей {len(locs)}  →  🔴 {len(red)}  🟡 {len(yel)}")
    for page in pages:
        r, y = per[page]
        print(f"  {'/' + page:<28} 🔴 {r:<4} 🟡 {y}")
    shown = red if quiet else fs
    byrule = defaultdict(list)
    for f in shown: byrule[f[3]].append(f)
    for rule in sorted(byrule):
        rows = byrule[rule]
        print(f"\n--- {rule} ({len(rows)}) ---")
        for s, loc, page, _, msg in rows[:40 if not quiet else 15]:
            print(f"  {s} {loc:<3} /{page:<24} {msg}")
        if len(rows) > (40 if not quiet else 15): print(f"  … и ещё {len(rows) - (40 if not quiet else 15)}")
    sys.exit(1 if red else 0)

if __name__ == "__main__":
    main()
