#!/usr/bin/env python3
"""
Ahrefs SEO data collector for SplitCam project.

Usage:
    export AHREFS_TOKEN='your_token_here'
    python3 ahrefs.py [--targets-only | --keywords-only]

Reads:
    targets.txt    — domains to analyze (one per line)
    keywords.txt   — keywords to research (one per line)

Writes:
    data/<domain>-overview.json     — DR, organic traffic, ahrefs rank
    data/<domain>-keywords.json     — top 50 organic keywords driving traffic
    data/keywords-research.json     — volume/KD/CPC for our target keywords
    data/_usage.json                — Ahrefs credits used in this run
"""

import os
import sys
import json
import time
from pathlib import Path
import requests

TOKEN = os.environ.get("AHREFS_TOKEN")
if not TOKEN:
    print("ERROR: Set AHREFS_TOKEN env var first.\n  export AHREFS_TOKEN='your_token'")
    sys.exit(1)

BASE = "https://api.ahrefs.com/v3"
SEO_DIR = Path(__file__).parent
DATA_DIR = SEO_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
TODAY = time.strftime("%Y-%m-%d")
COUNTRY = "us"  # Change to "world" for global, or specific country codes


def api(path: str, params: dict) -> dict:
    """Make a GET request to Ahrefs API v3."""
    url = f"{BASE}/{path}"
    headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        if r.status_code != 200:
            return {"_error": True, "status": r.status_code, "body": r.text[:500]}
        return r.json()
    except requests.RequestException as e:
        return {"_error": True, "body": str(e)}


def read_list(filename: str) -> list[str]:
    """Read non-empty, non-comment lines from a file."""
    path = SEO_DIR / filename
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def analyze_domain(domain: str) -> dict:
    """Pull overview + top keywords for one domain."""
    print(f"\n=== {domain} ===")
    result = {"domain": domain, "fetched_at": TODAY, "country": COUNTRY}

    # 1) Domain rating + Ahrefs rank
    dr = api("site-explorer/domain-rating", {"target": domain, "date": TODAY})
    if "_error" not in dr:
        result["domain_rating"] = dr.get("domain_rating", {})
        print(f"  Domain Rating: {dr.get('domain_rating', {}).get('domain_rating', '?')}")

    # 2) Organic traffic metrics
    metrics = api("site-explorer/metrics", {"target": domain, "date": TODAY, "country": COUNTRY})
    if "_error" not in metrics:
        result["metrics"] = metrics.get("metrics", {})
        org = metrics.get("metrics", {}).get("org_traffic", "?")
        print(f"  Organic traffic (US): {org}")

    # 3) Top 50 organic keywords (what drives traffic)
    kw = api("site-explorer/organic-keywords", {
        "target": domain,
        "country": COUNTRY,
        "date": TODAY,
        "limit": 50,
        "order_by": "sum_traffic:desc",
        "select": "keyword,volume,keyword_difficulty,cpc,best_position,sum_traffic,serp_features",
    })
    if "_error" not in kw:
        kws = kw.get("keywords", [])
        result["top_keywords"] = kws
        print(f"  Top keywords: {len(kws)} pulled")
        if kws:
            print(f"  #1 by traffic: '{kws[0].get('keyword')}' (vol {kws[0].get('volume')}, pos {kws[0].get('best_position')})")
    else:
        result["top_keywords_error"] = kw

    return result


def research_keywords(keywords: list[str]) -> dict:
    """Get volume, difficulty, CPC for our target keywords."""
    print(f"\n=== Keywords research ({len(keywords)} keywords) ===")
    if not keywords:
        return {}

    # Smaller batch to keep URL length safe + simpler select
    BATCH = 20
    all_results = []
    for i in range(0, len(keywords), BATCH):
        batch = keywords[i:i+BATCH]
        kw_csv = ",".join(batch)
        res = api("keywords-explorer/overview", {
            "keywords": kw_csv,
            "country": COUNTRY,
            "select": "keyword,volume,difficulty,cpc",
        })
        if "_error" in res:
            print(f"  Batch {i}-{i+len(batch)}: ERROR {res.get('status')} - {res.get('body', '')[:200]}")
            continue
        items = res.get("keywords", [])
        all_results.extend(items)
        print(f"  Batch {i}-{i+len(batch)}: {len(items)} keywords")

    return {"fetched_at": TODAY, "country": COUNTRY, "keywords": all_results}


def usage_snapshot() -> dict:
    return api("subscription-info/limits-and-usage", {})


def safe_filename(domain: str) -> str:
    return domain.replace("/", "_").replace(":", "_")


def main():
    do_targets = "--keywords-only" not in sys.argv
    do_keywords = "--targets-only" not in sys.argv

    usage_before = usage_snapshot()
    print(f"Plan: {usage_before.get('limits_and_usage', {}).get('subscription', '?')}")
    print(f"Units used: {usage_before.get('limits_and_usage', {}).get('units_usage_workspace', '?')} / "
          f"{usage_before.get('limits_and_usage', {}).get('units_limit_workspace', '?')}")

    if do_targets:
        targets = read_list("targets.txt")
        print(f"\nAnalyzing {len(targets)} domains...")
        for domain in targets:
            data = analyze_domain(domain)
            out = DATA_DIR / f"{safe_filename(domain)}.json"
            out.write_text(json.dumps(data, indent=2, ensure_ascii=False))
            print(f"  → saved {out.name}")

    if do_keywords:
        keywords = read_list("keywords.txt")
        kw_data = research_keywords(keywords)
        out = DATA_DIR / "keywords-research.json"
        out.write_text(json.dumps(kw_data, indent=2, ensure_ascii=False))
        print(f"\n  → saved {out.name}")

    usage_after = usage_snapshot()
    delta = (usage_after.get("limits_and_usage", {}).get("units_usage_workspace", 0) -
             usage_before.get("limits_and_usage", {}).get("units_usage_workspace", 0))
    print(f"\n=== Done. Units consumed this run: {delta} ===")
    (DATA_DIR / "_usage.json").write_text(json.dumps({"before": usage_before, "after": usage_after, "delta": delta}, indent=2))


if __name__ == "__main__":
    main()
