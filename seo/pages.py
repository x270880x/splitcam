#!/usr/bin/env python3
"""
Per-page SEO weight collector for splitcam.com (Ahrefs API v3).

Pulls, for every page that has any SEO weight:
  - organic traffic + traffic value + ranking keyword count  (top-pages)
  - backlinks + referring domains per URL                    (best-by-external-links)

Usage:
    export AHREFS_TOKEN='your_token_here'
    python3 pages.py [domain]        # default domain: splitcam.com

Writes:
    data/<domain>-pages.json   — merged per-URL weight table
    data/<domain>-pages-raw.json — raw API responses (for debugging)
"""

import os
import sys
import json
import time
from pathlib import Path
import requests

TOKEN = os.environ.get("AHREFS_TOKEN")
if not TOKEN:
    print("ERROR: Set AHREFS_TOKEN env var first.")
    sys.exit(1)

BASE = "https://api.ahrefs.com/v3"
SEO_DIR = Path(__file__).parent
DATA_DIR = SEO_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
TODAY = time.strftime("%Y-%m-%d")
COUNTRY = "us"
DOMAIN = sys.argv[1] if len(sys.argv) > 1 else "splitcam.com"


def api(path: str, params: dict) -> dict:
    url = f"{BASE}/{path}"
    headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=60)
        if r.status_code != 200:
            return {"_error": True, "status": r.status_code, "body": r.text[:600]}
        return r.json()
    except requests.RequestException as e:
        return {"_error": True, "body": str(e)}


def first_list(resp: dict):
    """Return the first list value in an API response (the rows), plus its key."""
    for k, v in resp.items():
        if isinstance(v, list):
            return k, v
    return None, []


def main():
    raw = {}
    usage_before = api("subscription-info/limits-and-usage", {})
    units0 = usage_before.get("limits_and_usage", {}).get("units_usage_workspace", 0)
    print(f"Domain: {DOMAIN}  |  units used so far: {units0}")

    # ---- 1) TOP PAGES BY TRAFFIC ----
    print("\n[1/2] top-pages by organic traffic...")
    tp = api("site-explorer/top-pages", {
        "target": DOMAIN,
        "country": COUNTRY,
        "date": TODAY,
        "limit": 1000,
        "order_by": "sum_traffic:desc",
        "select": "url,sum_traffic,value,keywords,top_keyword,top_keyword_volume,top_keyword_best_position",
    })
    if "_error" in tp:
        print(f"  ERROR {tp.get('status')}: {tp.get('body','')}")
        # retry with a minimal select
        tp = api("site-explorer/top-pages", {
            "target": DOMAIN, "country": COUNTRY, "date": TODAY,
            "limit": 1000, "order_by": "sum_traffic:desc",
            "select": "url,sum_traffic,keywords",
        })
        if "_error" in tp:
            print(f"  retry ERROR {tp.get('status')}: {tp.get('body','')}")
    raw["top_pages"] = tp
    tp_key, tp_rows = first_list(tp) if "_error" not in tp else (None, [])
    print(f"  pages with traffic: {len(tp_rows)}")

    # ---- 2) PAGES BY BACKLINKS ----
    print("\n[2/2] best-by-external-links (backlinks per page)...")
    bl = api("site-explorer/best-by-external-links", {
        "target": DOMAIN,
        "mode": "subdomains",
        "limit": 500,
        "order_by": "refdomains_target:desc",
        "select": "url_to,refdomains_target,links_to_target,dofollow_to_target,url_rating_target,http_code_target",
    })
    if "_error" in bl:
        print(f"  ERROR {bl.get('status')}: {bl.get('body','')}")
        bl = api("site-explorer/best-by-external-links", {
            "target": DOMAIN, "mode": "subdomains", "limit": 500,
            "order_by": "refdomains_target:desc", "select": "url_to,refdomains_target",
        })
        if "_error" in bl:
            print(f"  retry ERROR {bl.get('status')}: {bl.get('body','')}")
    raw["backlinks"] = bl
    bl_key, bl_rows = first_list(bl) if "_error" not in bl else (None, [])
    print(f"  pages with backlinks: {len(bl_rows)}")

    # ---- MERGE INTO ONE PER-URL TABLE ----
    def norm(u):
        return (u or "").rstrip("/").split("?")[0].lower()

    table = {}
    for r in tp_rows:
        u = norm(r.get("url"))
        if not u:
            continue
        table.setdefault(u, {"url": r.get("url")})
        table[u].update({
            "traffic": r.get("sum_traffic", 0),
            "traffic_value": r.get("value", 0),
            "keywords": r.get("keywords", 0),
            "top_keyword": r.get("top_keyword"),
            "top_keyword_volume": r.get("top_keyword_volume"),
            "top_keyword_position": r.get("top_keyword_best_position"),
        })
    for r in bl_rows:
        u = norm(r.get("url_to") or r.get("url"))
        if not u:
            continue
        table.setdefault(u, {"url": r.get("url_to") or r.get("url")})
        table[u].update({
            "refdomains": r.get("refdomains_target", 0),
            "external_links": r.get("links_to_target", 0),
            "dofollow_refdomains": r.get("dofollow_to_target"),
            "url_rating": r.get("url_rating_target"),
            "http_code": r.get("http_code_target"),
        })

    merged = sorted(
        table.values(),
        key=lambda x: (x.get("traffic", 0) or 0, x.get("refdomains", 0) or 0),
        reverse=True,
    )

    out = {
        "domain": DOMAIN, "fetched_at": TODAY, "country": COUNTRY,
        "page_count": len(merged), "pages": merged,
    }
    (DATA_DIR / f"{DOMAIN}-pages.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    (DATA_DIR / f"{DOMAIN}-pages-raw.json").write_text(json.dumps(raw, indent=2, ensure_ascii=False))

    usage_after = api("subscription-info/limits-and-usage", {})
    units1 = usage_after.get("limits_and_usage", {}).get("units_usage_workspace", 0)
    print(f"\n=== Done. {len(merged)} unique URLs. Units this run: {units1 - units0} ===")
    print(f"Saved: data/{DOMAIN}-pages.json")

    # quick top-15 console preview
    print(f"\nTop 15 pages by traffic:")
    for p in merged[:15]:
        print(f"  {p.get('traffic',0):>6}  rd={p.get('refdomains','-'):>4}  "
              f"kw={p.get('keywords','-'):>4}  {p.get('url','')}")


if __name__ == "__main__":
    main()
