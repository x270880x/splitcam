#!/usr/bin/env python3
"""Site-wide link & interlinking audit for the SplitCam static site.

Checks:
  1. Internal links resolve to real files (incl. #anchors, trailing slashes).
  2. Resource refs (img/script/css/video/poster) resolve.
  3. External links respond (GET, browser UA, 8 threads). 403/429 -> WARN.
  4. Internal link graph: contextual (body) vs nav/footer/breadcrumb links,
     inlink/outlink counts, click depth from homepage, orphans.
  5. sitemap.xml vs indexable pages on disk.

Usage:  python3 seo/linkcheck.py [--no-network]
"""
import os, re, sys, json, posixpath, subprocess
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', '.claude', 'node_modules', 'seo'}
ARCHIVED_PREFIXES = ('v2/',)          # checked for broken links, excluded from graph
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')

def rel(p):  # repo-relative posix path
    return os.path.relpath(p, ROOT).replace(os.sep, '/')

# ---------------------------------------------------------------- collect ---
pages = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for f in sorted(filenames):
        if f.endswith('.html'):
            pages.append(os.path.join(dirpath, f))

# ------------------------------------------------------------------ parse ---
class Audit(HTMLParser):
    """Collect <a> links (with context + anchor text), resource refs, ids."""
    RES_ATTRS = {'img': 'src', 'script': 'src', 'source': 'src',
                 'video': 'src', 'audio': 'src', 'iframe': 'src'}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.resources, self.ids = [], [], set()
        self.ctx = []           # stack of 'nav'/'footer'/'breadcrumb'
        self.a_stack = []       # [href, text-accumulator, context]
        self.noindex = False
    def context(self):
        if 'breadcrumb' in self.ctx: return 'breadcrumb'
        if 'footer' in self.ctx: return 'footer'
        if 'nav' in self.ctx: return 'nav'
        return 'body'
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        cls = a.get('class', '')
        if (tag in ('nav', 'footer') or 'breadcrumb' in cls
                or 'nav-mobile' in cls or a.get('id') == 'nav-mobile'):
            self.ctx.append('breadcrumb' if 'breadcrumb' in cls
                            else ('footer' if tag == 'footer' else 'nav'))
            setattr(self, f'_open_{len(self.ctx)}', tag)
        if tag == 'meta' and a.get('name') == 'robots' and 'noindex' in a.get('content', ''):
            self.noindex = True
        if tag == 'a' and a.get('href'):
            self.a_stack.append([a['href'], [], self.context()])
        if tag in self.RES_ATTRS and a.get(self.RES_ATTRS[tag]):
            self.resources.append(a[self.RES_ATTRS[tag]])
        if tag == 'video' and a.get('poster'):
            self.resources.append(a['poster'])
        if tag == 'link' and a.get('href') and any(
                r in a.get('rel', '') for r in ('stylesheet', 'icon', 'manifest', 'preload')):
            self.resources.append(a['href'])
    def handle_endtag(self, tag):
        if self.ctx and getattr(self, f'_open_{len(self.ctx)}', None) == tag:
            self.ctx.pop()
        if tag == 'a' and self.a_stack:
            href, text, ctx = self.a_stack.pop()
            self.links.append((href, ' '.join(''.join(text).split())[:80], ctx))
    def handle_data(self, data):
        for a in self.a_stack: a[1].append(data)

parsed = {}
for p in pages:
    with open(p, encoding='utf-8', errors='replace') as fh:
        a = Audit(); a.feed(fh.read())
    parsed[rel(p)] = a

# --------------------------------------------------------------- resolve ---
def canon_page(path):
    """foo/index.html -> foo/ ; index.html -> '' (site-root-relative key)."""
    return path[:-len('index.html')] if path.endswith('index.html') else path

broken_internal, missing_slash, broken_anchor, broken_res = [], [], [], []
external = {}           # url -> [(page, context), ...]
splitcam_links = {}     # links to the live splitcam.com site
graph = []              # (src_page, dst_page, context, anchor_text)

def resolve(page, href, kind, anchor_text='', ctx='body'):
    base = posixpath.dirname(page)
    raw = href.strip()
    if raw.startswith(('mailto:', 'tel:', 'javascript:', 'data:')): return
    if raw.startswith('#'):
        if raw[1:] and raw[1:] not in parsed[page].ids:
            broken_anchor.append((page, raw, '(self)'))
        return
    if raw.startswith(('http://', 'https://')):
        host_path = re.sub(r'^https?://', '', raw)
        if host_path.startswith('x270880x.github.io/splitcam'):
            broken_internal.append((page, href, 'absolute staging URL — make relative'))
            return
        target = splitcam_links if host_path.startswith(('splitcam.com', 'www.splitcam.com')) else external
        target.setdefault(raw.split('#')[0], []).append((page, ctx))
        return
    path, _, frag = raw.partition('#')
    path = path.split('?')[0]
    if not path:  # pure fragment handled above
        return
    full = posixpath.normpath(posixpath.join(base, path))
    if full.startswith('..'):
        broken_internal.append((page, href, 'escapes site root')); return
    full = '' if full == '.' else full
    fs = os.path.join(ROOT, full.replace('/', os.sep))
    resolved = None
    if path.endswith('/') or full == '':
        idx = posixpath.join(full, 'index.html')
        if os.path.isfile(os.path.join(ROOT, idx)): resolved = idx
    elif os.path.isfile(fs):
        resolved = full
    elif os.path.isdir(fs):
        idx = posixpath.join(full, 'index.html')
        if os.path.isfile(os.path.join(ROOT, idx)):
            resolved = idx
            if kind == 'link': missing_slash.append((page, href))
    if resolved is None:
        (broken_internal if kind == 'link' else broken_res).append((page, href, 'target not found'))
        return
    if kind == 'link':
        if frag and resolved in parsed and frag not in parsed[resolved].ids:
            broken_anchor.append((page, href, resolved))
        graph.append((page, resolved, ctx, anchor_text))

for page, a in parsed.items():
    for href, text, ctx in a.links: resolve(page, href, 'link', text, ctx)
    for src in a.resources:        resolve(page, src, 'res')

# ---------------------------------------------------------------- network ---
def check_url(url):
    # curl uses the system trust store (python.org Python often lacks certs)
    r = subprocess.run(
        ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-L',
         '--max-time', '25', '-A', UA, url],
        capture_output=True, text=True)
    code = r.stdout.strip()
    if code.isdigit() and code != '000':
        return url, int(code), ''
    return url, None, f'curl exit {r.returncode} (DNS/conn/timeout)'

net_results = {}
if '--no-network' not in sys.argv:
    urls = sorted(set(external) | set(splitcam_links))
    with ThreadPoolExecutor(8) as ex:
        for url, code, err in ex.map(check_url, urls):
            net_results[url] = (code, err)

# ------------------------------------------------------------------ graph ---
public = {canon_page(p) for p in parsed
          if not p.startswith(ARCHIVED_PREFIXES) and not parsed[p].noindex}
inl, outl = {}, {}
for src, dst, ctx, text in graph:
    s, d = canon_page(src), canon_page(dst)
    if s.startswith(ARCHIVED_PREFIXES) or d.startswith(ARCHIVED_PREFIXES): continue
    if s == d: continue
    inl.setdefault(d, []).append((s, ctx, text))
    outl.setdefault(s, []).append((d, ctx, text))

# click depth from homepage over all internal links
depth, frontier = {'': 0}, ['']
while frontier:
    nxt = []
    for s in frontier:
        for d, _, _ in outl.get(s, []):
            if d not in depth:
                depth[d] = depth[s] + 1; nxt.append(d)
    frontier = nxt

# ---------------------------------------------------------------- sitemap ---
sitemap_urls = set()
sm = os.path.join(ROOT, 'sitemap.xml')
if os.path.isfile(sm):
    sitemap_urls = {m.group(1).strip() for m in
        re.finditer(r'<loc>\s*(.*?)\s*</loc>', open(sm, encoding='utf-8').read())}
sitemap_paths = {re.sub(r'^https?://(www\.)?splitcam\.com/', '', u) for u in sitemap_urls}
indexable = {p for p in public if canon_page(p) == p or True}
page_keys = {canon_page(p) for p in parsed if not p.startswith(ARCHIVED_PREFIXES)}
noindex_pages = {canon_page(p) for p in parsed if parsed[p].noindex}

# ----------------------------------------------------------------- report ---
print('=' * 72); print('PAGES SCANNED:', len(parsed))
print('noindex pages:', sorted(noindex_pages) or '—')

def section(title, rows, fmt=lambda r: ' | '.join(map(str, r))):
    print(f'\n--- {title} ({len(rows)}) ---')
    for r in rows: print(' ', fmt(r))

section('BROKEN internal links', broken_internal)
section('BROKEN anchors (#fragment missing)', broken_anchor)
section('BROKEN resources (img/css/js/video)', broken_res)
section('Links missing trailing slash (301 hop)', missing_slash)

bad_ext = {u: rc for u, rc in net_results.items()
           if rc[0] is None or rc[0] >= 400}
warn = {u: rc for u, rc in bad_ext.items() if rc[0] in (403, 429, 999)}
hard = {u: rc for u, rc in bad_ext.items() if u not in warn}
section('EXTERNAL hard failures', sorted(hard.items()),
        lambda kv: f'{kv[1][0] or kv[1][1]}  {kv[0]}  <- ' +
                   ', '.join(sorted({p for p, _ in (external | splitcam_links)[kv[0]]})))
section('EXTERNAL bot-blocked (verify by hand)', sorted(warn.items()),
        lambda kv: f'{kv[1][0]}  {kv[0]}')
print('\nexternal OK:', sum(1 for u, rc in net_results.items()
                            if rc[0] and rc[0] < 400), '/', len(net_results))

print('\n--- INTERNAL LINK GRAPH (public, nav/footer vs contextual) ---')
hdr = f'{"page":34} {"depth":>5} {"in:body":>7} {"in:nav":>6} {"in:foot":>7} {"in:bc":>5} {"out:body":>8}'
print(hdr); print('-' * len(hdr))
for p in sorted(public, key=lambda x: (depth.get(x, 99), x)):
    i = inl.get(p, [])
    print(f'{p or "/":34} {depth.get(p, "∞"):>5} '
          f'{sum(1 for s, c, t in i if c == "body"):>7} '
          f'{sum(1 for s, c, t in i if c == "nav"):>6} '
          f'{sum(1 for s, c, t in i if c == "footer"):>7} '
          f'{sum(1 for s, c, t in i if c == "breadcrumb"):>5} '
          f'{sum(1 for d, c, t in outl.get(p, []) if c == "body"):>8}')

print('\n--- CONTEXTUAL (body) INLINKS DETAIL ---')
for p in sorted(public):
    rows = [(s, t) for s, c, t in inl.get(p, []) if c == 'body']
    print(f'\n{p or "/"} <- {len(rows)} body links')
    for s, t in sorted(rows): print(f'   from {s or "/":30} anchor: "{t}"')

print('\n--- SITEMAP vs DISK ---')
print('in sitemap, no matching page on disk:',
      sorted(sitemap_paths - page_keys) or '—')
print('page on disk, not in sitemap (excl. noindex):',
      sorted((page_keys - noindex_pages) - sitemap_paths) or '—')
print('noindex pages listed in sitemap (bad):',
      sorted(sitemap_paths & noindex_pages) or '—')

print('\n--- LINKS TO LIVE splitcam.com (will need rewrite at migration) ---')
for u in sorted(splitcam_links):
    code = net_results.get(u, ('skip',))[0]
    print(f'  [{code}] {u}  <- {", ".join(sorted({p for p, _ in splitcam_links[u]}))}')
