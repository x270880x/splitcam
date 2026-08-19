#!/usr/bin/env python3
"""Замер кластера «virtual camera» в Search Console — снимок и сравнение.

Задача: главная (/) перехватывала generic-запрос «virtual camera» у профильной
страницы /virtual-camera, потому что термин стоял в тайтле главной. Термин убран
2026-08-20. Этот скрипт фиксирует, что было, и показывает, что стало.

  снимок:    seo/.gscvenv/bin/python seo/vc_cluster.py --save seo/vc-baseline.json
  сравнение: seo/.gscvenv/bin/python seo/vc_cluster.py --compare seo/vc-baseline.json
"""
import datetime, json, sys, argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY  = "/Users/splitcam/.gsc_service_account.json"
SITE = "sc-domain:splitcam.com"
# кластер: всё, что про виртуальную камеру/вебкамеру, без брендовых вариантов
TERMS = ["virtual camera", "virtual cam", "virtual webcam", "vitual camera", "virtualcam"]

def svc():
    c = service_account.Credentials.from_service_account_file(
        KEY, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    return build("searchconsole", "v1", credentials=c, cache_discovery=False)

def snapshot(days=28):
    s = svc()
    end = datetime.date.today() - datetime.timedelta(days=3)
    start = end - datetime.timedelta(days=days - 1)
    def q(dims, filters=None, n=200):
        b = {"startDate": str(start), "endDate": str(end), "dimensions": dims, "rowLimit": n}
        if filters: b["dimensionFilterGroups"] = [{"filters": filters}]
        return s.searchanalytics().query(siteUrl=SITE, body=b).execute().get("rows", [])

    queries, pages = {}, {}
    for t in TERMS:
        for r in q(["query"], [{"dimension": "query", "operator": "contains", "expression": t}]):
            k = r["keys"][0]
            if "splitcam" in k.lower().replace(" ", ""):   # брендовые не считаем
                continue
            queries[k] = {"impressions": r["impressions"], "clicks": r["clicks"],
                          "position": round(r["position"], 1), "ctr": round(r["ctr"] * 100, 2)}
    # кто отвечает по главному запросу
    for r in q(["page"], [{"dimension": "query", "operator": "equals", "expression": "virtual camera"}]):
        pages[r["keys"][0].replace("https://splitcam.com", "") or "/"] = {
            "impressions": r["impressions"], "clicks": r["clicks"], "position": round(r["position"], 1)}
    tot = {"impressions": sum(v["impressions"] for v in queries.values()),
           "clicks": sum(v["clicks"] for v in queries.values()),
           "queries": len(queries)}
    return {"from": str(start), "to": str(end), "days": days,
            "total": tot, "queries": queries, "pages_for_virtual_camera": pages}

def show(s, label="СНИМОК"):
    t = s["total"]
    print(f"=== {label}: {s['from']} … {s['to']} ===")
    print(f"  запросов в кластере: {t['queries']} · показы {t['impressions']} · клики {t['clicks']}")
    print(f"\n  кто отвечает по «virtual camera»:")
    for p, v in sorted(s["pages_for_virtual_camera"].items(), key=lambda x: -x[1]["impressions"])[:6]:
        print(f"    {p[:44]:46} показы {v['impressions']:>5}  клики {v['clicks']:>4}  поз {v['position']:>5.1f}")
    print(f"\n  топ запросов:")
    for k, v in sorted(s["queries"].items(), key=lambda x: -x[1]["impressions"])[:12]:
        print(f"    {k[:40]:42} показы {v['impressions']:>5}  клики {v['clicks']:>4}  поз {v['position']:>5.1f}  CTR {v['ctr']:>5.2f}%")

def compare(base, now):
    print(f"=== СРАВНЕНИЕ ===")
    print(f"  было: {base['from']} … {base['to']}")
    print(f"  стало: {now['from']} … {now['to']}\n")
    b, n = base["total"], now["total"]
    for f in ("impressions", "clicks"):
        d = n[f] - b[f]; pct = (d / b[f] * 100) if b[f] else 0
        print(f"  {f:12} {b[f]:>7} → {n[f]:>7}   {d:+6} ({pct:+.1f}%)")
    print("\n  кто отвечает по «virtual camera»:")
    keys = set(base["pages_for_virtual_camera"]) | set(now["pages_for_virtual_camera"])
    for p in sorted(keys):
        bb = base["pages_for_virtual_camera"].get(p, {}); nn = now["pages_for_virtual_camera"].get(p, {})
        print(f"    {p[:40]:42} показы {bb.get('impressions',0):>5} → {nn.get('impressions',0):<5}"
              f"  поз {bb.get('position','—')} → {nn.get('position','—')}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--save"); ap.add_argument("--compare"); ap.add_argument("--days", type=int, default=28)
    a = ap.parse_args()
    now = snapshot(a.days)
    if a.compare:
        compare(json.load(open(a.compare, encoding="utf-8")), now); show(now, "СЕЙЧАС")
    else:
        show(now)
        if a.save:
            json.dump(now, open(a.save, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(f"\n  снимок сохранён: {a.save}")
