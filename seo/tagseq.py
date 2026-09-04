# -*- coding: utf-8 -*-
"""Структурная сверка локали с EN: последовательность тегов <body> должна совпадать.
   python3 seo/tagseq.py            — весь сайт по PAGE_PATHS
   python3 seo/tagseq.py for/churches/ — одна страница
Найдено 2026-09-04: hr/for/churches/ был повреждён агентом — 8 строк разметки
перезаписаны случайными строками того же файла. Перевод цел, теги — нет.
Ловится только сравнением ПОРЯДКА тегов с эталоном: ссылки работают, JSON-LD парсится,
счётчики отдельных тегов могут сходиться.
"""
import re, os, sys, difflib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "seo"))
from i18n_wire import PAGE_PATHS
LOCS = "ru es de fr pt tr fil uk it vi id nl ro hi ja ms bg ar ko th pl hu sv zh el cs he sr hr da fi no sk fa".split()
SKIP = re.compile(r'<!--(LD|HL|AD|RTLCSS)-->.*?<!--/\1-->', re.S)   # регенерируемые регионы

def seq(path):
    h = open(path, encoding="utf-8").read()
    b = h[h.find("<body"):]
    b = SKIP.sub("", b)
    b = re.sub(r'<script.*?</script>', '<script/>', b, flags=re.S)
    b = re.sub(r'<style.*?</style>', '<style/>', b, flags=re.S)
    # языковой переключатель: порядок ссылок в нём законно разный
    b = re.sub(r'<details class="lang[^"]*".*?</details>', '<details lang/>', b, flags=re.S)
    return [m.group(1).lower() for m in re.finditer(r'<(/?[a-zA-Z][a-zA-Z0-9]*)', b)]

def check(page):
    en = os.path.join(ROOT, page, "index.html") if page else os.path.join(ROOT, "index.html")
    if not os.path.exists(en): return []
    es = seq(en); out = []
    for l in LOCS:
        p = os.path.join(ROOT, l, page, "index.html") if page else os.path.join(ROOT, l, "index.html")
        if not os.path.exists(p): continue
        ls = seq(p)
        if ls != es:
            ops = [o for o in difflib.SequenceMatcher(None, es, ls, autojunk=False).get_opcodes() if o[0] != "equal"]
            out.append((l, len(es), len(ls), len(ops), ops[:3]))
    return out

if __name__ == "__main__":
    pages = [a.strip("/") + ("/" if a.strip("/") else "") for a in sys.argv[1:]] or PAGE_PATHS
    total = 0
    for pg in pages:
        r = check(pg.rstrip("/"))
        for l, ne, nl, nops, ops in r:
            total += 1
            print(f"  🔴 {l}/{pg or ''}: тегов EN {ne}, локаль {nl}, расхождений {nops}; первое: {ops[0][0]} EN[{ops[0][1]}:{ops[0][2]}]={ops and ' '.join(seq_en) if False else ''}")
    print(f"\n  страниц с расхождением структуры: {total}")
