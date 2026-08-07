#!/usr/bin/env python3
"""SplitCam Remote — читает заявки тестеров из общей таблицы ответов, без браузера.

Все 35 локализованных форм пишут в ОДНУ таблицу (по вкладке на язык). Скрипт
собирает все строки, показывает итог и заявки за последние N дней.

Разовая настройка владельцем (bpgroup@gmail.com):
  1. Включить Sheets API в проекте splitcam-macos:
     https://console.developers.google.com/apis/api/sheets.googleapis.com/overview?project=257789627798
  2. Расшарить таблицу сервисному аккаунту (Viewer):
     gsc-reader@splitcam-macos.iam.gserviceaccount.com

Запуск:  seo/.gscvenv/bin/python seo/tester_signups.py [--days 7] [--all]
"""
import sys, datetime, argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SHEET_ID = "1qEGIHXiwP0od9o8RXmZ_VGQ6ObeFszZBOMDOJttfm5o"
KEY = "/Users/splitcam/.gsc_service_account.json"

def parse_ts(s):
    s = (s or "").strip()
    for fmt in ("%m/%d/%Y %H:%M:%S", "%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S",
                "%m/%d/%Y %H:%M", "%d.%m.%Y %H:%M:%S", "%d.%m.%Y %H:%M"):
        try: return datetime.datetime.strptime(s, fmt)
        except ValueError: pass
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--all", action="store_true", help="показать ВСЕ заявки, не только за окно")
    args = ap.parse_args()

    creds = service_account.Credentials.from_service_account_file(
        KEY, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    try:
        svc = build("sheets", "v4", credentials=creds, cache_discovery=False)
        meta = svc.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    except HttpError as e:
        print(f"HTTP {e.resp.status}: {e._get_reason()}")
        if "has not been used" in str(e) or "disabled" in str(e):
            print("→ включи Sheets API: https://console.developers.google.com/apis/api/sheets.googleapis.com/overview?project=257789627798")
        elif e.resp.status in (403, 404):
            print("→ расшарь таблицу сервисному аккаунту gsc-reader@splitcam-macos.iam.gserviceaccount.com (Viewer)")
        sys.exit(1)

    import re
    EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.I)
    print("Таблица:", meta.get("properties", {}).get("title"))
    tabs = [s["properties"]["title"] for s in meta.get("sheets", [])]
    cutoff = datetime.datetime.now() - datetime.timedelta(days=args.days)

    # ТОЛЬКО вкладки "Form Responses*" = реальные отправки формы.
    # "FORM URLS" (ссылки) и "Тестеры — чистка" (ручной рабочий лист) — служебные, не заявки.
    rows = []          # (ts, ts_raw, tab, email_field)
    clean_list = 0
    for t in tabs:
        try:
            vals = svc.spreadsheets().values().get(
                spreadsheetId=SHEET_ID, range=f"'{t}'!A2:D3000").execute().get("values", [])
        except HttpError:
            vals = []
        if t.lower().startswith("form responses"):
            for r in vals:
                rows.append((parse_ts(r[0] if r else ""), r[0] if r else "", t,
                             (r[1].strip() if len(r) > 1 else "")))
        elif "чистка" in t.lower():
            clean_list = len([r for r in vals if r and any(c.strip() for c in r)])

    valid = [r for r in rows if EMAIL.match(r[3])]
    uniq = sorted({r[3].lower() for r in valid})
    junk = [r for r in rows if not EMAIL.match(r[3])]
    recent = [r for r in rows if r[0] and r[0] >= cutoff]

    print(f"\n=== ЗАЯВКИ НА ТЕСТ SplitCam Remote ===")
    print(f"  Всего отправок формы:        {len(rows)}")
    print(f"  С валидным e-mail:           {len(valid)}")
    print(f"  Уникальных e-mail:           {len(uniq)}")
    print(f"  Мусорных ответов (не email): {len(junk)}")
    print(f"  За последние {args.days} дней:          {len(recent)}")
    if clean_list:
        print(f"  Рабочий лист 'Тестеры — чистка': {clean_list} строк")
    show = rows if args.all else recent
    if show:
        print(f"\n  {'все' if args.all else 'свежие'} заявки:")
        for ts, raw, tab, email in sorted(show, key=lambda x: (x[0] or datetime.datetime.min), reverse=True):
            mark = "" if EMAIL.match(email) else "  ⚠ не email"
            print(f"   {raw:22} {email}{mark}")

if __name__ == "__main__":
    main()
