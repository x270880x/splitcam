# -*- coding: utf-8 -*-
"""Сообщает поисковикам об изменившихся адресах через IndexNow (Bing, Yandex, Seznam, Naver).

   python3 seo/indexnow.py --new              только страницы, созданные за последние N дней
   python3 seo/indexnow.py --all              все адреса из sitemap.xml
   python3 seo/indexnow.py --urls a b c       конкретные адреса
   python3 seo/indexnow.py --all --dry        показать, что будет отправлено

Ключ уже лежит на хосте: /485c229ee85ee55f1967363aabec7e9a.txt — проверяется перед отправкой,
потому что без него приёмная сторона молча отклонит весь список.

🔴 Google в IndexNow НЕ участвует. У него два пути: карта сайта (уже зарегистрирована, читается
сама) и ручной «Запросить индексирование» в интерфейсе Search Console. Программно отправить
обычную страницу в Google нельзя: Indexing API принимает только вакансии и трансляции, а наш
служебный аккаунт вдобавок имеет доступ только на чтение (scope webmasters.readonly).
"""
import sys, os, re, json, subprocess, urllib.request, urllib.parse, datetime as dt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "splitcam.com"
KEY = "485c229ee85ee55f1967363aabec7e9a"
KEY_URL = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"
BATCH = 10000                      # предел одного запроса по спецификации

def sitemap_urls():
    sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    return re.findall(r"<loc>([^<]+)</loc>", sm)

def new_pages(days=14):
    """Адреса страниц, ФАЙЛЫ которых созданы за последние N дней (по git)."""
    since = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    out = subprocess.run(["git", "-C", ROOT, "log", f"--since={since}", "--diff-filter=A",
                          "--name-only", "--pretty=format:"], capture_output=True, text=True).stdout
    created = {l.strip() for l in out.splitlines() if l.strip().endswith("index.html")}
    urls = []
    for u in sitemap_urls():
        p = u.replace(f"https://{HOST}/", "").rstrip("/")
        f = (p + "/index.html") if p else "index.html"
        if f in created:
            urls.append(u)
    return urls

def check_key():
    code = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "15", KEY_URL],
                          capture_output=True, text=True).stdout.strip()
    body = subprocess.run(["curl", "-s", "--max-time", "15", KEY_URL], capture_output=True, text=True).stdout.strip()
    return code == "200" and body == KEY, code, body[:40]

def submit(urls, dry=False):
    ok, code, body = check_key()
    print(f"  ключ {KEY_URL}: HTTP {code}, содержимое {'совпадает' if body == KEY else repr(body)}")
    if not ok:
        print("  🔴 ключ недоступен или не совпадает — отправлять бессмысленно, отклонят молча")
        return 1
    bad = [u for u in urls if not u.startswith(f"https://{HOST}/")]
    if bad:
        print(f"  🔴 чужие адреса в списке ({len(bad)}): {bad[:3]}"); return 1
    print(f"  адресов к отправке: {len(urls)}")
    if dry:
        for u in urls[:10]: print("   ", u)
        if len(urls) > 10: print(f"    … и ещё {len(urls)-10}")
        return 0
    sent = 0
    for i in range(0, len(urls), BATCH):
        part = urls[i:i + BATCH]
        payload = json.dumps({"host": HOST, "key": KEY, "keyLocation": KEY_URL, "urlList": part}).encode()
        req = urllib.request.Request(ENDPOINT, data=payload,
                                     headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                print(f"  партия {i//BATCH+1}: {len(part)} адресов → HTTP {r.status} {r.reason}")
                sent += len(part)
        except urllib.error.HTTPError as e:
            print(f"  🔴 партия {i//BATCH+1}: HTTP {e.code} {e.reason} — {e.read()[:200]}")
        except Exception as e:
            print(f"  🔴 партия {i//BATCH+1}: {e}")
    print(f"  отправлено: {sent}/{len(urls)}")
    print("  коды: 200 принято · 202 принято, ключ проверяется · 400 некорректный запрос · 403 ключ не совпал")
    return 0

if __name__ == "__main__":
    a = sys.argv[1:]
    dry = "--dry" in a
    if "--urls" in a:
        urls = [x for x in a[a.index("--urls") + 1:] if not x.startswith("--")]
    elif "--all" in a:
        urls = sitemap_urls()
    else:
        days = int(a[a.index("--days") + 1]) if "--days" in a else 14
        urls = new_pages(days)
        print(f"  страницы, созданные за последние {days} дн.")
    sys.exit(submit(urls, dry))
