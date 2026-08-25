# -*- coding: utf-8 -*-
"""Извлекает/вставляет переводимые строки страниц семейства /for/.
🔴 Гарантия — round-trip: вставка исходных строк обязана дать исходный файл байт в байт.
Запуск проверки:  python3 seo/i18n_tools/for_extract.py for/educators/index.html
"""
import re, json, sys

BLOCKS = [
 (r'<span class="eyebrow">(.*?)</span>',   'eyebrow'),
 (r'<h1 class="h1">(.*?)</h1>',            'h1'),
 (r'<p class="sub">(.*?)</p>',             'sub'),
 (r'<span class="h-badge">(.*?)</span>',   'badge'),
 (r'<div class="qa-h">(.*?)</div>',        'qah'),
 (r'<h2 class="sec-h">(.*?)</h2>',         'sech'),
 (r'<p class="sec-p">(.*?)</p>',           'secp'),
 (r'<p class="step-p">(.*?)</p>',          'stepp'),
 (r'<div class="tip-card-h">(.*?)</div>',  'tiph'),
 (r'<p class="tip-card-p">(.*?)</p>',      'tipp'),
 (r'<summary>(.*?)</summary>',             'faqq'),
 (r'<div class="edu-l s\d">(.*?)</div>',   'vis'),
 (r'<div class="edu-out">(.*?)</div>',     'visout'),
]
SINGLES = [
 (r'(<div class="breadcrumbs">\s*<a[^>]*>)([^<]*)(</a><span class="sep">/</span><a[^>]*>)([^<]*)(</a><span class="sep">/</span><span>)([^<]*)(</span>)', 'crumb3'),
 (r'(<div class="step-h">)(.*?)(<span class="step-time">)(.*?)(</span></div>)', 'step'),
 (r'(<div class="hw-card">\s*<h4>)(.*?)(</h4>\s*<p>)(.*?)(</p>)', 'hw'),
 (r'(</summary>\s*<p>)(.*?)(</p>)', 'faqa'),
 (r'(<a href="[^"]*" class="btn-primary btn-lg"[^>]*>)(.*?)(</a>)', 'btnp'),
 (r'(<a href="[^"]*" class="btn-ghost btn-lg">)(.*?)(</a>)', 'btng'),
 (r'(<div class="related">\s*<h3[^>]*>)(.*?)(</h3>)', 'relh'),
 (r'(<a class="related-card" href="[^"]*">\s*<span class="eyebrow">)(.*?)(</span>\s*<h4>)(.*?)(</h4>\s*<p>)(.*?)(</p>)', 'rel3'),
 (r'(<section class="cta-block">\s*<h2>)(.*?)(</h2>\s*<p>)(.*?)(</p>)', 'cta'),
 (r'(<span class="edu-apps"><span>|<div class="edu-apps">)(.*?)(</div>)', 'apps'),
 (r'(<li>)(.*?)(</li>)', 'li'),
]

def region(h):
    i = h.find('<div class="breadcrumbs">'); j = h.find("<footer")
    assert i > 0 and j > i, "границы не найдены"
    return i, j

def extract(path):
    h = open(path, encoding="utf-8").read()
    i, j = region(h); body = h[i:j]
    out, order, used = {}, [], []
    def key(t):
        n = sum(1 for k in order if k.startswith(t + "#")); k = f"{t}#{n}"; order.append(k); return k
    for pat, tag in SINGLES:
        for m in re.finditer(pat, body, re.S):
            g = m.groups()
            if tag == 'crumb3':
                out[key('crumb_a')] = g[1]; out[key('crumb_b')] = g[3]; out[key('crumb_c')] = g[5]
            elif tag == 'rel3':
                out[key('rel_e')] = g[1]; out[key('rel_h')] = g[3]; out[key('rel_p')] = g[5]
            elif tag in ('step', 'hw', 'cta'):
                out[key(tag + '_a')] = g[1]; out[key(tag + '_b')] = g[3]
            else:
                out[key(tag)] = g[1]
            used.append((m.start(), m.end()))
    for pat, tag in BLOCKS:
        for m in re.finditer(pat, body, re.S):
            if any(s <= m.start() < e for s, e in used): continue
            out[key(tag)] = m.group(1)
    return h, i, j, out

def inject(path, tr):
    """Вставляет переводы. Защищённые участки (SINGLES) заменяются на токены ДО
    обработки BLOCKS — иначе правки сдвигают позиции и BLOCKS попадают не туда.
    Именно на этом сломалась предыдущая версия: проверка round-trip подставляет
    строки той же длины, смещений не возникает, и ошибка не проявлялась."""
    h = open(path, encoding="utf-8").read()
    i, j = region(h); body = h[i:j]
    cnt = {}
    def nxt(t):
        cnt[t] = cnt.get(t, -1) + 1; return f"{t}#{cnt[t]}"

    # 1) SINGLES → готовый текст, спрятанный за токен
    stash = []
    for pat, tag in SINGLES:
        def rs(m, tag=tag):
            g = m.groups()
            if tag == 'crumb3':
                out = g[0]+tr.get(nxt('crumb_a'),g[1])+g[2]+tr.get(nxt('crumb_b'),g[3])+g[4]+tr.get(nxt('crumb_c'),g[5])+g[6]
            elif tag == 'rel3':
                out = g[0]+tr.get(nxt('rel_e'),g[1])+g[2]+tr.get(nxt('rel_h'),g[3])+g[4]+tr.get(nxt('rel_p'),g[5])+g[6]
            elif tag in ('step','hw','cta'):
                out = g[0]+tr.get(nxt(tag+'_a'),g[1])+g[2]+tr.get(nxt(tag+'_b'),g[3])+g[4]
            else:
                out = g[0]+tr.get(nxt(tag),g[1])+g[2]
            stash.append(out)
            return f"\x00{len(stash)-1}\x00"
        body = re.sub(pat, rs, body, flags=re.S)

    # 2) BLOCKS — токены им уже не мешают
    for pat, tag in BLOCKS:
        def rb(m, tag=tag):
            v = tr.get(nxt(tag))
            return m.group(0).replace(m.group(1), v, 1) if v is not None else m.group(0)
        body = re.sub(pat, rb, body, flags=re.S)

    # 3) возвращаем спрятанное
    body = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], body)
    return h[:i] + body + h[j:]

if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "for/educators/index.html"
    h, i, j, dd = extract(p)
    ok = inject(p, dd) == h
    print(f"  {p}: строк {len(dd)} · round-trip {'✓' if ok else '🔴 РАСХОЖДЕНИЕ'}")
