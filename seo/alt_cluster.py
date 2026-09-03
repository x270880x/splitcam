# -*- coding: utf-8 -*-
"""Замер кластера «alternative» до и после переориентации хаба /alternatives/.
   python3 seo/alt_cluster.py --save      сохранить базовый замер
   python3 seo/alt_cluster.py --compare   сравнить сегодня с базой
Зачем: хаб держал streamyard alternative (поз. 11.8) до появления дочерних страниц.
Переезд запроса на дочернюю страницу должен быть виден, а провал — заметен вовремя.
"""
import json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gsc_lite import query

BASE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alt-baseline.json")
TERMS = ("alternativ", "代わり", " vs ", "vs ")
WATCH = ("streamyard alternative", "restream alternative free", "manycam alternative",
         "obs virtual camera alternative", "alternativas a obs", "alternative zu obs")

def snap(start, end):
    rows = [r for r in query(["query"], start, end) if any(t in r["keys"][0] for t in TERMS)]
    pages = query(["page", "query"], start, end, [{"dimension": "page", "operator": "contains",
                                                   "expression": "/alternatives"}])
    return {"start": start, "end": end,
            "queries": {r["keys"][0]: [r["impressions"], r["clicks"], round(r["position"], 1)] for r in rows},
            "hub": {f'{r["keys"][0].replace("https://splitcam.com","")} | {r["keys"][1]}':
                    [r["impressions"], r["clicks"], round(r["position"], 1)] for r in pages}}

def totals(s):
    v = s["queries"].values()
    return sum(x[0] for x in v), sum(x[1] for x in v), len(s["queries"])

if __name__ == "__main__":
    end   = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()
    start = (datetime.date.today() - datetime.timedelta(days=93)).isoformat()
    cur = snap(start, end)
    i, c, n = totals(cur)
    print(f"  окно {start} … {end}")
    print(f"  кластер «alternative»: {i} показов / {c} кликов / {n} запросов\n")
    print("  ключевые запросы:")
    for w in WATCH:
        v = cur["queries"].get(w)
        print(f"    {w:34} " + (f"{v[0]:5d} показ {v[1]:3d} клик  поз {v[2]:5.1f}" if v else "   —"))
    if "--save" in sys.argv:
        json.dump(cur, open(BASE, "w"), ensure_ascii=False, indent=1)
        print(f"\n  база сохранена → {os.path.basename(BASE)}")
    elif "--compare" in sys.argv:
        b = json.load(open(BASE))
        bi, bc, bn = totals(b)
        print(f"\n  было ({b['start']}…{b['end']}): {bi} показов / {bc} кликов / {bn} запросов")
        print(f"  стало: {i-bi:+d} показов / {c-bc:+d} кликов / {n-bn:+d} запросов")
        print("\n  сдвиг позиций по ключевым:")
        for w in WATCH:
            o, v = b["queries"].get(w), cur["queries"].get(w)
            if o and v:
                d = o[2] - v[2]
                print(f"    {w:34} поз {o[2]:5.1f} → {v[2]:5.1f}  ({d:+.1f}) "
                      + ("🔴 упал" if d < -3 else "✓" if d > 0 else ""))
