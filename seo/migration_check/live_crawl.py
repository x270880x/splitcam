#!/usr/bin/env python3
"""Post-migration live audit of splitcam.com (2026-09-18).
Every target is fetched 3 ways: via Cloudflare (-L), NEW origin raw, OLD origin raw.
Targets = live sitemap + every internal href/src found on every crawled HTML page (BFS)
          + host-managed files on the server + real paths requested via CF yesterday
          + injected probes (blind-spot check: a missing URL MUST be flagged)."""
import subprocess, hashlib, json, re, sys, os, random, threading
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, urlunsplit
from concurrent.futures import ThreadPoolExecutor

import argparse
_ap = argparse.ArgumentParser(description="Post-migration live audit: every URL via Cloudflare + NEW origin + OLD origin")
_ap.add_argument("workdir", help="dir with host_managed.txt and cf_paths_<day>_paths.json; results go here")
_ap.add_argument("--new", required=True, help="NEW origin IP")
_ap.add_argument("--old", required=True, help="OLD origin IP (still up)")
_ap.add_argument("--cf-paths", default="cf_paths_0917_paths.json", help="real requested paths from CF (json list)")
_a = _ap.parse_args()
S = _a.workdir
NEW, OLD = _a.new, _a.old
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
BIG = re.compile(r"\.(msi|dmg|pkg|exe|zip|tar\.gz|bin|mp4|webm|mov)$", re.I)
TMP = os.path.join(S, "crawl_tmp"); os.makedirs(TMP, exist_ok=True)
lock = threading.Lock()

def curl(url, via, follow=False, head=False):
    f = os.path.join(TMP, f"{threading.get_ident()}_{via}.bin")
    a = ["curl", "-s", "-A", UA, "--max-time", "60", "-o", f,
         "-w", "%{http_code}\t%{size_download}\t%{num_redirects}\t%{url_effective}\t%{content_type}\t%{redirect_url}"]
    if follow: a.append("-L")
    if head: a.append("-I")
    if via in ("new", "old"):
        a += ["-k", "--resolve", f"splitcam.com:443:{NEW if via=='new' else OLD}"]
    a.append(url)
    r = subprocess.run(a, capture_output=True, text=True)
    parts = (r.stdout.split("\t") + [""] * 6)[:6]
    code, size, hops, eff, ctype, loc = parts
    body = b""
    try:
        body = open(f, "rb").read()
    except Exception:
        pass
    if head:  # hash the relevant headers instead of a body we did not download
        h = {}
        for line in body.decode("latin1").splitlines():
            k, _, v = line.partition(":")
            if k.lower() in ("content-length", "last-modified", "etag"): h[k.lower()] = v.strip()
        sig = hashlib.sha1(json.dumps(h, sort_keys=True).encode()).hexdigest()[:12]
        return dict(code=code, size=h.get("content-length", "?"), hops=hops, eff=eff, ctype=ctype, loc=loc, sig=sig, body=b"")
    return dict(code=code, size=size, hops=hops, eff=eff, ctype=ctype, loc=loc,
                sig=hashlib.sha1(body).hexdigest()[:12], body=body if "html" in ctype else b"")

class Links(HTMLParser):
    ATTRS = {"a": ["href"], "link": ["href"], "script": ["src"], "img": ["src", "srcset"], "source": ["src", "srcset"],
             "video": ["src", "poster"], "audio": ["src"], "iframe": ["src"], "form": ["action"]}
    def __init__(self): super().__init__(); self.out = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for a in self.ATTRS.get(tag, []):
            v = d.get(a)
            if not v: continue
            if a == "srcset":
                self.out += [p.strip().split(" ")[0] for p in v.split(",") if p.strip()]
            else:
                self.out.append(v)
        if tag == "meta" and (d.get("property") in ("og:image", "og:url") or d.get("name") in ("twitter:image",)):
            if d.get("content"): self.out.append(d["content"])

def norm(u, base):
    u = urljoin(base, u.strip())
    s = urlsplit(u)
    if s.scheme not in ("http", "https"): return None, None
    host = s.netloc.lower()
    clean = urlunsplit(("https", host, s.path or "/", s.query, ""))
    return (clean if host in ("splitcam.com", "www.splitcam.com") else None), (u if host not in ("splitcam.com", "www.splitcam.com") else None)

# ---- seed targets
seeds = {}  # url -> source
sm = curl(f"https://splitcam.com/sitemap.xml?cb={random.randint(1,10**9)}", "cf")
smbody = open(os.path.join(TMP, f"{threading.get_ident()}_cf.bin"), "rb").read().decode()
for loc in re.findall(r"<loc>([^<]+)</loc>", smbody): seeds[loc.strip()] = "sitemap"
n_sitemap = len(seeds)
for line in open(os.path.join(S, "host_managed.txt")):
    p = line.strip()
    if p: seeds.setdefault("https://splitcam.com/" + p, "host")
for p in json.load(open(os.path.join(S, _a.cf_paths))):
    if p.startswith("/cdn-cgi/"): continue
    seeds.setdefault("https://splitcam.com" + p, "cf-traffic")
for p in ["/win-download/images/images.xml", "/ingests/proxy.cfg", "/ver.php", "/images.xml", "/apple-app-site-association", "/.well-known/apple-app-site-association"]:
    seeds.setdefault("https://splitcam.com" + p, "app-endpoint")
PROBES = [f"https://splitcam.com/__migration_probe_{random.randint(10**6,10**7)}.html",
          f"https://splitcam.com/assets/__probe_{random.randint(10**6,10**7)}.png"]
for p in PROBES: seeds[p] = "PROBE"

results, external, seen = {}, {}, set()
queue = list(seeds.items())

def check(url, src):
    head = bool(BIG.search(urlsplit(url).path))
    cf = curl(url, "cf", follow=True, head=head)
    nw = curl(url, "new", head=head)
    od = curl(url, "old", head=head)
    rec = dict(url=url, src=src, cf_code=cf["code"], cf_hops=cf["hops"], cf_final=cf["eff"],
               new_code=nw["code"], new_loc=nw["loc"], new_sig=nw["sig"], new_size=nw["size"],
               old_code=od["code"], old_loc=od["loc"], old_sig=od["sig"], old_size=od["size"],
               ctype=nw["ctype"], links=0)
    found_int, found_ext = [], []
    if nw["body"] and nw["code"] == "200" and "html" in nw["ctype"]:
        lp = Links()
        try: lp.feed(nw["body"].decode("utf-8", "replace"))
        except Exception: pass
        rec["links"] = len(lp.out)
        for l in lp.out:
            i, e = norm(l, url)
            if i: found_int.append(i)
            if e: found_ext.append(e)
    return rec, found_int, found_ext

with ThreadPoolExecutor(12) as ex:
    while queue:
        batch = [(u, s) for u, s in queue if u not in seen]
        queue = []
        for u, _ in batch: seen.add(u)
        for rec, fi, fe in ex.map(lambda t: check(*t), batch):
            results[rec["url"]] = rec
            for e in fe: external.setdefault(e, rec["url"])
            for i in fi:
                if i not in seen and len(seen) + len(queue) < 8000:
                    queue.append((i, "link-from:" + rec["url"]))
        print(f"  проверено {len(results)}, в очереди {len(queue)}", file=sys.stderr, flush=True)

json.dump(dict(results=results, external=external, n_sitemap=n_sitemap, probes=PROBES),
          open(os.path.join(S, "live_crawl.json"), "w"), ensure_ascii=False)
print("DONE", len(results), "targets;", len(external), "external links")
