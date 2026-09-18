import json, sys, collections
S = sys.argv[1]
d = json.load(open(f"{S}/live_crawl.json"))
R = d["results"]; probes = set(d["probes"])
def cat(src):
    return "sitemap" if src == "sitemap" else "link" if src.startswith("link-from") else src
recs = list(R.values())

print("=== 0. ПРОВЕРКА СЛЕПОЙ ЗОНЫ (подсунутые битые адреса) ===")
for p in probes:
    r = R[p]; ok = r["cf_code"] == "404" and r["new_code"] == "404"
    print(f"  {'ПОЙМАН' if ok else '!!! НЕ ПОЙМАН'}: {p.split('/')[-1]}  cf={r['cf_code']} new={r['new_code']}")
html = [r for r in recs if "html" in r["ctype"] and r["new_code"] == "200"]
print(f"  HTML-страниц разобрано: {len(html)}, из них с найденными ссылками: {sum(1 for r in html if r['links']>0)}; ссылок всего: {sum(r['links'] for r in html)}")

real = [r for r in recs if r["url"] not in probes]
by = collections.Counter(cat(r["src"]) for r in real)
print("\n=== 1. ЧТО ПРОВЕРЕНО ===")
for k, v in by.most_common(): print(f"  {k:<14} {v}")
print(f"  ВСЕГО         {len(real)}  (в живой карте сайта {d['n_sitemap']})")

print("\n=== 2. РАСХОЖДЕНИЯ НОВЫЙ vs СТАРЫЙ СЕРВЕР (то, что мог сломать переезд) ===")
drift = [r for r in real if (r["new_code"], r["new_loc"], r["new_sig"]) != (r["old_code"], r["old_loc"], r["old_sig"])]
print(f"  всего: {len(drift)}")
for r in drift[:40]:
    print(f"  {r['url'][20:90]:<70} new={r['new_code']} {r['new_sig']} {r['new_size']} | old={r['old_code']} {r['old_sig']} {r['old_size']} [{cat(r['src'])}]")

print("\n=== 3. ОШИБКИ НОВОГО СЕРВЕРА (5xx / нет ответа) ===")
oe = [r for r in real if r["new_code"] in ("000", "") or r["new_code"].startswith("5")]
print(f"  всего: {len(oe)}")
for r in oe[:30]: print(f"  {r['url'][:100]} new={r['new_code']} cf={r['cf_code']}")

print("\n=== 4. НЕ ОТКРЫВАЕТСЯ ЧЕРЕЗ CLOUDFLARE (итог после редиректов >= 400) ===")
bad = [r for r in real if not r["cf_code"].startswith(("2", "3")) ]
cb = collections.Counter(cat(r["src"]) for r in bad)
print(f"  всего: {len(bad)}  по источникам: {dict(cb)}")
for r in sorted(bad, key=lambda r: cat(r["src"]))[:60]:
    same = "так же и на СТАРОМ" if r["old_code"] == r["new_code"] else f"старый={r['old_code']}"
    print(f"  cf={r['cf_code']:<4} new={r['new_code']:<4} {same:<20} {r['url'][19:95]:<76} [{cat(r['src'])}]")

print("\n=== 5. КАРТА САЙТА: каждая страница должна быть 200 без редиректа ===")
sm = [r for r in real if r["src"] == "sitemap"]
smbad = [r for r in sm if r["cf_code"] != "200" or r["cf_hops"] != "0" or r["new_code"] != "200"]
print(f"  страниц в карте: {len(sm)}, не 200 или с редиректом: {len(smbad)}")
for r in smbad[:20]: print(f"   {r['url']} cf={r['cf_code']} hops={r['cf_hops']} new={r['new_code']}")

print("\n=== 6. ЦЕПОЧКИ РЕДИРЕКТОВ (>1 прыжка через Cloudflare) ===")
ch = [r for r in real if r["cf_hops"].isdigit() and int(r["cf_hops"]) > 1]
print(f"  всего: {len(ch)}")
for r in ch[:25]: print(f"  hops={r['cf_hops']} {r['url'][19:80]:<62} -> {r['cf_final'][19:80]} [{cat(r['src'])}]")

print("\n=== 7. ВНУТРЕННИЕ ССЫЛКИ СО СТРАНИЦ, которые ведут в никуда ===")
lb = [r for r in bad if cat(r["src"]) == "link"]
print(f"  всего: {len(lb)}")
for r in lb[:30]: print(f"  {r['url'][19:]}  cf={r['cf_code']}  <- со страницы {r['src'][10+19:]}")
