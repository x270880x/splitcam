import json, sys, subprocess, hashlib
from concurrent.futures import ThreadPoolExecutor
S = sys.argv[1]
d = json.load(open(f"{S}/live_crawl.json")); R = d["results"]; probes = set(d["probes"])
drift = [r for r in R.values() if r["url"] not in probes and (r["new_code"], r["new_loc"], r["new_sig"]) != (r["old_code"], r["old_loc"], r["old_sig"])]
IP = {"new": sys.argv[2], "old": sys.argv[3]}  # usage: drift_verify.py <workdir> <NEW_IP> <OLD_IP>
def head(url, v):
    o = subprocess.run(["curl","-skI","--max-time","60","--resolve",f"splitcam.com:443:{IP[v]}",url],capture_output=True,text=True).stdout
    h = {}
    for l in o.splitlines():
        k,_,val = l.partition(":"); k=k.lower()
        if k in ("content-length","last-modified","etag"): h[k]=val.strip()
    return h
def rng(url, v, a, b):
    o = subprocess.run(["curl","-sk","--max-time","120","-r",f"{a}-{b}","--resolve",f"splitcam.com:443:{IP[v]}",url],capture_output=True).stdout
    return hashlib.sha1(o).hexdigest()[:12], len(o)
def full(url, v):
    o = subprocess.run(["curl","-sk","--max-time","120","--resolve",f"splitcam.com:443:{IP[v]}",url],capture_output=True).stdout
    return hashlib.sha1(o).hexdigest()[:12], len(o)
def verify(r):
    u = r["url"]; hn, ho = head(u,"new"), head(u,"old")
    n = int(hn.get("content-length","0") or 0)
    if n and n > 20_000_000:  # огромный файл: размер + дата + начало, середина и конец
        parts = [(0, 1048575), (n//2, n//2+1048575), (n-1048576, n-1)]
        same = all(rng(u,"new",a,b) == rng(u,"old",a,b) for a,b in parts)
        how = "размер+дата+3 куска по 1 МБ"
    else:
        same = full(u,"new") == full(u,"old"); how = "целиком байт в байт"
    meta_same = (hn.get("content-length"), hn.get("last-modified")) == (ho.get("content-length"), ho.get("last-modified"))
    return u, same and meta_same, how, hn.get("etag"), ho.get("etag"), hn.get("last-modified"), ho.get("last-modified")
with ThreadPoolExecutor(6) as ex:
    res = list(ex.map(verify, drift))
okc = sum(1 for x in res if x[1])
print(f"расхождений на перепроверку: {len(res)}; содержимое и дата СОВПАДАЮТ: {okc}; реально разные: {len(res)-okc}")
for u, ok, how, en, eo, ln, lo in res:
    if not ok: print("  РАЗНОЕ:", u, "| new lm:", ln, "| old lm:", lo)
print("примеры — чем отличались (только служебная метка ETag):")
for u, ok, how, en, eo, ln, lo in res[:4]: print(f"  {u[19:60]:<42} {how:<28} ETag new={en} old={eo}")
