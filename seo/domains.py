#!/usr/bin/env python3
"""
Domain weight checker (Ahrefs API v3) — for evaluating domains to buy/use.

Usage:
    export AHREFS_TOKEN='your_token_here'
    python3 domains.py domain1.com domain2.io ...

Reports per domain: Domain Rating, organic traffic/keywords, total
backlinks + referring domains, and top organic keywords.
"""
import os
import sys
import json
import time
import requests

TOKEN = os.environ.get("AHREFS_TOKEN")
if not TOKEN:
    print("ERROR: set AHREFS_TOKEN")
    sys.exit(1)

BASE = "https://api.ahrefs.com/v3"
TODAY = time.strftime("%Y-%m-%d")
COUNTRY = "us"
DOMAINS = sys.argv[1:] or ["multi-stream.io", "split.cam", "splitstrem.com"]


def api(path, params):
    headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}
    try:
        r = requests.get(f"{BASE}/{path}", headers=headers, params=params, timeout=45)
        if r.status_code != 200:
            return {"_error": True, "status": r.status_code, "body": r.text[:400]}
        return r.json()
    except requests.RequestException as e:
        return {"_error": True, "body": str(e)}


def check(domain):
    print(f"\n========== {domain} ==========")
    out = {"domain": domain}

    dr = api("site-explorer/domain-rating", {"target": domain, "date": TODAY})
    dr_val = dr.get("domain_rating", {}).get("domain_rating") if "_error" not in dr else None
    out["domain_rating"] = dr_val
    print(f"  Domain Rating : {dr_val if dr_val is not None else '— (error/no data)'}")

    bs = api("site-explorer/backlinks-stats", {"target": domain, "mode": "domain", "date": TODAY})
    if "_error" not in bs:
        m = bs.get("metrics", bs)
        out["backlinks"] = m.get("live")
        out["refdomains"] = m.get("live_refdomains")
        print(f"  Backlinks     : {m.get('live', '?')}")
        print(f"  Ref. domains  : {m.get('live_refdomains', '?')}")
    else:
        print(f"  Backlinks     : error {bs.get('status')} {bs.get('body','')[:160]}")
        out["backlinks_error"] = bs

    me = api("site-explorer/metrics", {"target": domain, "date": TODAY, "country": COUNTRY})
    if "_error" not in me:
        m = me.get("metrics", me)
        out["org_traffic"] = m.get("org_traffic")
        out["org_keywords"] = m.get("org_keywords")
        print(f"  Org. traffic  : {m.get('org_traffic', '?')} (US)")
        print(f"  Org. keywords : {m.get('org_keywords', '?')} (US)")
    else:
        print(f"  Metrics       : error {me.get('status')} {me.get('body','')[:160]}")

    kw = api("site-explorer/organic-keywords", {
        "target": domain, "country": COUNTRY, "date": TODAY, "limit": 10,
        "order_by": "sum_traffic:desc",
        "select": "keyword,volume,best_position,sum_traffic",
    })
    if "_error" not in kw:
        rows = kw.get("keywords", [])
        out["top_keywords"] = rows
        if rows:
            print(f"  Top keywords  :")
            for r in rows[:10]:
                print(f"     pos {r.get('best_position','?'):>3}  "
                      f"vol {r.get('volume','?'):>6}  {r.get('keyword','')}")
        else:
            print(f"  Top keywords  : none (domain ranks for nothing)")
    return out


def main():
    u0 = api("subscription-info/limits-and-usage", {}).get("limits_and_usage", {}).get("units_usage_workspace", 0)
    results = [check(d) for d in DOMAINS]
    u1 = api("subscription-info/limits-and-usage", {}).get("limits_and_usage", {}).get("units_usage_workspace", 0)
    print(f"\n=== Units used this run: {u1 - u0} ===")
    print("\n--- SUMMARY ---")
    for r in results:
        print(f"  {r['domain']:<22} DR={r.get('domain_rating','—')}  "
              f"refdomains={r.get('refdomains','—')}  org_traffic={r.get('org_traffic','—')}")


if __name__ == "__main__":
    main()
