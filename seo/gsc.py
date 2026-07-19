#!/usr/bin/env python3
"""Google Search Console data for splitcam.com / camstreamguide.com.

Set up 2026-07-19. Service account `gsc-reader@splitcam-macos.iam.gserviceaccount.com`
(project splitcam-macos, owner bpgroup@gmail.com) was added as a full user on the
Search Console property. Key: ~/.gsc_service_account.json (chmod 600, NOT in git).

Both properties live under bpgroup@gmail.com together with mydocs.co.il and
gimnastika.zp.ua. splitcameramail@gmail.com is a second verified owner — that is
where the alert e-mails land, but the console itself is reachable from either.

Usage:
    python3 gsc.py                    # 28-day summary for splitcam.com
    python3 gsc.py --days 7
    python3 gsc.py --site camstreamguide.com
    python3 gsc.py --locales          # per-locale breakdown
    python3 gsc.py --pages 20         # top pages
    python3 gsc.py --queries 20       # top queries
    python3 gsc.py --json             # machine-readable, for scheduled tasks

Requires: google-auth google-api-python-client
    python3 -m venv seo/.gscvenv
    seo/.gscvenv/bin/pip install google-auth google-api-python-client
"""

import argparse
import json
import re
import sys
from datetime import date, timedelta

KEY = "/Users/splitcam/.gsc_service_account.json"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

# Locale prefixes actually used on the site (EN lives at the root).
LOCALES = ("ru es de fr pt tr fil uk it vi id nl ro hi ja ms bg ar ko th "
           "pl hu sv zh el cs he sr hr da fi no sk fa").split()
LOC_RE = re.compile(r"https://[^/]+/(" + "|".join(LOCALES) + r")(/|$)")


def service():
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        sys.exit("Missing deps. Run:\n"
                 "  python3 -m venv seo/.gscvenv\n"
                 "  seo/.gscvenv/bin/pip install google-auth google-api-python-client\n"
                 "then call this script with seo/.gscvenv/bin/python")
    creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
    return build("searchconsole", "v1", credentials=creds)


def query(svc, site, start, end, dimensions=None, limit=25000):
    body = {"startDate": str(start), "endDate": str(end),
            "dimensions": dimensions or [], "rowLimit": limit}
    return svc.searchanalytics().query(siteUrl=site, body=body).execute().get("rows", [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="splitcam.com")
    ap.add_argument("--days", type=int, default=28)
    ap.add_argument("--locales", action="store_true")
    ap.add_argument("--pages", type=int, metavar="N")
    ap.add_argument("--queries", type=int, metavar="N")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    site = a.site if a.site.startswith("sc-domain:") else f"sc-domain:{a.site}"
    svc = service()

    # GSC data lags ~2 days; yesterday is the safest end date.
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=a.days - 1)

    rows = query(svc, site, start, end)
    t = rows[0] if rows else {}
    out = {
        "site": site,
        "from": str(start), "to": str(end),
        "clicks": round(t.get("clicks", 0)),
        "impressions": round(t.get("impressions", 0)),
        "ctr": round(t.get("ctr", 0) * 100, 2),
        "position": round(t.get("position", 0), 1),
    }

    pages = query(svc, site, start, end, ["page"])
    loc_rows = [p for p in pages if LOC_RE.match(p["keys"][0])]
    out["urls_with_impressions"] = len(pages)
    out["localized_urls"] = len(loc_rows)
    out["localized_impressions"] = round(sum(p["impressions"] for p in loc_rows))

    if a.locales:
        per = {}
        for p in loc_rows:
            m = LOC_RE.match(p["keys"][0])
            k = m.group(1)
            d = per.setdefault(k, {"urls": 0, "impressions": 0, "clicks": 0})
            d["urls"] += 1
            d["impressions"] += p["impressions"]
            d["clicks"] += p["clicks"]
        out["per_locale"] = {k: {kk: round(vv) for kk, vv in v.items()}
                             for k, v in sorted(per.items(),
                                                key=lambda x: -x[1]["impressions"])}

    if a.pages:
        out["top_pages"] = [
            {"url": p["keys"][0].replace("https://splitcam.com", ""),
             "impressions": round(p["impressions"]), "clicks": round(p["clicks"]),
             "ctr": round(p["ctr"] * 100, 2), "position": round(p["position"], 1)}
            for p in sorted(pages, key=lambda x: -x["impressions"])[:a.pages]]

    if a.queries:
        qs = query(svc, site, start, end, ["query"], limit=a.queries)
        out["top_queries"] = [
            {"query": q["keys"][0], "impressions": round(q["impressions"]),
             "clicks": round(q["clicks"]), "position": round(q["position"], 1)}
            for q in sorted(qs, key=lambda x: -x["impressions"])]

    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    print(f"{out['site']}   {out['from']} … {out['to']}")
    print(f"  clicks {out['clicks']:,} · impressions {out['impressions']:,} · "
          f"CTR {out['ctr']}% · position {out['position']}")
    print(f"  URLs with impressions: {out['urls_with_impressions']} "
          f"(localized: {out['localized_urls']}, "
          f"{out['localized_impressions']:,} impressions)")

    if a.locales and out.get("per_locale"):
        print("\n  locale   urls  impressions  clicks")
        for k, v in out["per_locale"].items():
            print(f"  {k:<7} {v['urls']:>5} {v['impressions']:>12,} {v['clicks']:>7,}")

    if a.pages:
        print("\n  impressions  clicks    CTR   pos  page")
        for p in out["top_pages"]:
            print(f"  {p['impressions']:>11,} {p['clicks']:>7,} {p['ctr']:>6}% "
                  f"{p['position']:>5}  {p['url'][:48]}")

    if a.queries:
        print("\n  impressions  clicks   pos  query")
        for q in out["top_queries"]:
            print(f"  {q['impressions']:>11,} {q['clicks']:>7,} {q['position']:>5}  "
                  f"{q['query'][:48]}")


if __name__ == "__main__":
    main()
