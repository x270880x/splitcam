# -*- coding: utf-8 -*-
"""Мёртвые адреса, за которые мы всё ещё платим показами. Источник — Search Console.

   python3 seo/deadlinks.py                 90 дней, адреса с показами ≥5
   python3 seo/deadlinks.py --min 1         вообще все
   python3 seo/deadlinks.py --days 28
   python3 seo/deadlinks.py --json out.json

ЗАЧЕМ. `linkcheck.py` проверяет ссылки ВНУТРИ сайта — он видит только то, на что мы сами ссылаемся.
Он принципиально не видит адреса, которые Google до сих пор показывает людям, а сервер на них
отвечает 404: старые файлы, снесённые разделы, ссылки с чужих сайтов. Такой адрес не выдаёт себя
ничем, кроме потерянных показов. Так в сентябре 2026 нашлись 85 мёртвых адресов справки со
137 530 показами за 90 дней — их закрыли перенаправлениями.

Проверяет ещё и КУДА ведёт перенаправление: 301 на несуществующую страницу выглядит здоровым в
любом отчёте, а для человека это тот же тупик.
"""
import sys, os, json, subprocess, collections, concurrent.futures as cf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "seo"))
import gsc_lite

SITE = "sc-domain:splitcam.com"

def status(url, timeout=15):
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code} %{redirect_url}",
                        "--max-time", str(timeout), url], capture_output=True, text=True).stdout
    parts = r.split(" ", 1)
    return parts[0], (parts[1].strip() if len(parts) > 1 else "")

def main():
    a = sys.argv[1:]
    days = int(a[a.index("--days") + 1]) if "--days" in a else 90
    minimp = int(a[a.index("--min") + 1]) if "--min" in a else 5
    out_json = a[a.index("--json") + 1] if "--json" in a else None
    import datetime as dt
    end = dt.date.today() - dt.timedelta(days=2)          # консоль отстаёт на пару дней
    start = end - dt.timedelta(days=days)
    rows = gsc_lite.query(["page"], start.isoformat(), end.isoformat(), None, 25000)
    rows = [r for r in rows if r["impressions"] >= minimp]
    print(f"  окно {start}…{end} · адресов с показами ≥{minimp}: {len(rows)}")

    def check(r):
        u = r["keys"][0]
        code, dest = status(u)
        dcode = ""
        if code.startswith("3") and dest:
            dcode, _ = status(dest)
        return dict(url=u, impressions=r["impressions"], clicks=r["clicks"],
                    position=round(r.get("position", 0), 1), code=code, dest=dest, dest_code=dcode)
    res = []
    with cf.ThreadPoolExecutor(12) as ex:
        for x in ex.map(check, rows):
            res.append(x)

    by = collections.Counter(x["code"] for x in res)
    print("  коды ответа:", dict(sorted(by.items())))
    dead = [x for x in res if x["code"] in ("404", "410", "000")]
    broken_redirect = [x for x in res if x["code"].startswith("3") and x["dest_code"] in ("404", "410", "000")]
    forbidden = [x for x in res if x["code"] == "403"]

    def section(title, items):
        if not items:
            print(f"\n  ✅ {title}: нет"); return
        print(f"\n  🔴 {title}: {len(items)} адресов, показов {sum(i['impressions'] for i in items)}, "
              f"кликов {sum(i['clicks'] for i in items)}")
        for i in sorted(items, key=lambda x: -x["impressions"])[:15]:
            u = i["url"].replace("https://splitcam.com", "")
            extra = f"  → {i['dest'].replace('https://splitcam.com','')} [{i['dest_code']}]" if i["dest"] else ""
            print(f"   {i['impressions']:>7} показов, {i['clicks']:>4} кликов, поз. {i['position']:>5}  {u[:78]}{extra}")
        if len(items) > 15: print(f"   … и ещё {len(items)-15}")
    section("Отдают 404 при живых показах", dead)
    section("Перенаправление ведёт в никуда", broken_redirect)
    section("Отдают 403", forbidden)

    if out_json:
        json.dump(res, open(out_json, "w"), ensure_ascii=False, indent=1)
        print(f"\n  полный список → {out_json}")
    lost = sum(i["impressions"] for i in dead + broken_redirect)
    print(f"\n  показов уходит в тупик: {lost}")
    sys.exit(1 if dead or broken_redirect else 0)

if __name__ == "__main__":
    main()
