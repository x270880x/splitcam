#!/usr/bin/env python3
"""Рассылка письма тестировщикам SplitCam Remote — каждому на его языке.

Шлёт по SMTP на exim сервера splitcam.com через SSH-туннель. Прямой SMTP с рабочего
мака невозможен: провайдер режет 25/465/587 до ЛЮБОГО хоста (проверено на
smtp.gmail.com и smtp.yandex.ru — ведут себя так же). Туннель обходит это честно:
трафик идёт по SSH на 22-й порт, а на том конце мы приходим на собственный exim
с локалхоста.

  1. Поднять туннель (держать открытым всё время рассылки):
       ssh -N -L 2525:127.0.0.1:25 lwanngbs@77.83.100.153

  2. Прогон вхолостую — ничего не отправляется, только отчёт:
       python3 seo/send_tester_mail.py --list testers.csv --dry-run

  3. Одно пробное письмо себе:
       python3 seo/send_tester_mail.py --list testers.csv --test-to support@splitcam.com

  4. Настоящая рассылка:
       python3 seo/send_tester_mail.py --list testers.csv

СПИСОК (CSV или TSV). Колонки определяются по заголовку, регистр не важен:
  - адрес     — email / e-mail / почта / адрес / "Google account" / "Аккаунт Google"
  - язык      — locale / lang / язык  (если колонки нет — берётся --default-locale)
  - готовность— "added to console" / "добавлен"  (галочка TRUE/да/1/x)

**Без колонки готовности скрипт откажется слать**, если не передать явно
`--no-console-filter`. Причина: opt-in ссылка работает ТОЛЬКО после того, как адрес
добавлен в список тестировщиков в Play Console. Письмо, отправленное раньше,
приведёт человека на «приложение недоступно», и он решит, что приложение сломано.

ЛОГ пишется в --log (по умолчанию `seo/data/tester-mail-log.csv`) и читается при
следующем запуске: повторно на тот же адрес письмо не уйдёт. Файл лежит в
gitignored-каталоге `seo/data/` — **в репозиторий адреса не коммитить**, репозиторий
сайта публичный.
"""
import argparse
import csv
import datetime
import json
import pathlib
import re
import smtplib
import sys
import time
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

ROOT = pathlib.Path(__file__).resolve().parent
COPY_JSON = ROOT / "tester-email-i18n.json"
DEFAULT_LOG = ROOT / "data" / "tester-mail-log.csv"

FROM_ADDR = "support@splitcam.com"
FROM_NAME = "SplitCam"

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.I)
TRUEISH = {"true", "1", "yes", "y", "да", "x", "✓", "v", "+"}

ADDR_KEYS = ("google account", "аккаунт google", "e-mail", "email", "mail", "почта", "адрес")
LOC_KEYS = ("locale", "lang", "language", "язык", "локаль")
READY_KEYS = ("added to console", "добавлен", "console", "готов")

# exim на этом сервере анонсирует LIMITS MAILMAX=100 — переподключаемся заранее
PER_CONNECTION = 90


def canon(addr):
    """Ключ для поиска дублей. Gmail игнорирует точки в имени и всё после «+»,
    поэтому s.rios.vo@gmail.com и sriosvo@gmail.com — один и тот же ящик."""
    addr = addr.strip().lower()
    if "@" not in addr:
        return addr
    local, domain = addr.rsplit("@", 1)
    if domain in ("gmail.com", "googlemail.com"):
        local = local.split("+", 1)[0].replace(".", "")
        domain = "gmail.com"
    return f"{local}@{domain}"


def pick_column(header, keys):
    low = [(h or "").strip().lower() for h in header]
    for i, h in enumerate(low):
        if any(k == h for k in keys):
            return i
    for i, h in enumerate(low):
        if any(k in h for k in keys):
            return i
    return None


def read_list(path, default_locale, allow_no_filter):
    raw = pathlib.Path(path).read_text(encoding="utf-8-sig", errors="replace")
    dialect = csv.Sniffer().sniff(raw[:4096], delimiters=",;\t") if raw.strip() else csv.excel
    rows = list(csv.reader(raw.splitlines(), dialect))
    if not rows:
        sys.exit("список пуст")
    header, body = rows[0], rows[1:]

    ci = pick_column(header, ADDR_KEYS)
    if ci is None:
        ci = 1 if len(header) > 1 else 0   # формы: A=時間, B=единственный вопрос
        print(f"! колонка адреса не опознана по заголовку, беру колонку {ci + 1}")
    li = pick_column(header, LOC_KEYS)
    ri = pick_column(header, READY_KEYS)

    if ri is None and not allow_no_filter:
        sys.exit(
            "В списке нет колонки «Added to Console» — непонятно, кто уже добавлен в\n"
            "Play Console. Письмо тем, кого там нет, приводит на «приложение недоступно».\n"
            "Добавь колонку либо запусти с --no-console-filter, если уверен."
        )

    out, skipped = [], {"плохой адрес": 0, "не добавлен в Console": 0, "дубль": 0}
    seen = set()
    for r in body:
        get = lambda i: (r[i].strip() if i is not None and i < len(r) else "")
        addr = get(ci)
        if not addr and not any(x.strip() for x in r):
            continue
        if not EMAIL_RE.match(addr):
            skipped["плохой адрес"] += 1
            continue
        if ri is not None and not allow_no_filter and get(ri).lower() not in TRUEISH:
            skipped["не добавлен в Console"] += 1
            continue
        key = canon(addr)
        if key in seen:
            skipped["дубль"] += 1
            continue
        seen.add(key)
        out.append({"email": addr, "locale": (get(li) or default_locale).strip() or default_locale})
    return out, skipped


def load_sent(log_path):
    p = pathlib.Path(log_path)
    if not p.exists():
        return set()
    done = set()
    with p.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if (row.get("result") or "").startswith("ok"):
                done.add(canon(row.get("email") or ""))
    return done


class SshSendmail:
    """Отправка через /usr/sbin/sendmail на сервере по SSH.

    Почему не SMTP: exim на 127.0.0.1:25 принимает письма только для локальных
    доменов, наружу отдаёт `550 relay not permitted` — релей требует авторизации,
    а пароля ящика у нас нет. Локальный `sendmail`, запущенный от владельца
    аккаунта, доверенный и шлёт куда угодно. Именно так 12.08 ушли апелляции
    в MalwareURL и AlphaSOC.

    Письмо передаётся base64 внутри команды, чтобы не воевать с экранированием.
    """

    def __init__(self, wrapper, sender):
        self.wrapper = wrapper
        self.sender = sender
        if not pathlib.Path(wrapper).exists():
            sys.exit(f"нет SSH-обёртки: {wrapper}\n"
                     "Это expect-скрипт, который логинится паролем из ~/.hostsila_da_ssh\n"
                     "и выполняет переданную команду. Путь задаётся через --ssh-wrapper.")

    def close(self):
        pass

    def send(self, msg):
        import base64
        import subprocess
        blob = base64.b64encode(bytes(msg)).decode()
        cmd = (f"echo '{blob}' | base64 -d | /usr/sbin/sendmail -t -f {self.sender} "
               f"&& echo SENDMAIL_OK")
        r = subprocess.run([self.wrapper, cmd], capture_output=True, text=True, timeout=120)
        if "SENDMAIL_OK" not in (r.stdout or ""):
            raise RuntimeError((r.stdout or "") .strip()[-200:] or (r.stderr or "").strip()[-200:]
                               or "sendmail не подтвердил отправку")


class SmtpTunnel:
    """SMTP через SSH-туннель. Годится ТОЛЬКО для адресов на splitcam.com:
    наружу exim отвечает `550 relay not permitted`."""

    def __init__(self, host, port):
        self.host, self.port, self.srv, self.n = host, port, None, 0

    def send(self, msg):
        if self.srv is None or self.n >= PER_CONNECTION:
            self.close()
            self.srv = smtplib.SMTP(self.host, self.port, timeout=30)
            self.n = 0
        try:
            self.srv.send_message(msg)
            self.n += 1
        except Exception:
            self.srv = None
            raise

    def close(self):
        if self.srv:
            try: self.srv.quit()
            except Exception: pass
            self.srv = None


def transport(a):
    if a.transport == "smtp":
        return SmtpTunnel(a.host, a.port)
    return SshSendmail(a.ssh_wrapper, FROM_ADDR)


def build(copy, locale, to_addr):
    c = copy.get(locale) or copy.get("EN")
    msg = EmailMessage()
    msg["From"] = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"] = to_addr
    msg["Subject"] = c["subject"]
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="splitcam.com")
    msg["Reply-To"] = FROM_ADDR
    msg["Auto-Submitted"] = "auto-generated"
    msg.set_content(c["body"], subtype="plain", charset="utf-8")
    return msg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", required=True, help="CSV/TSV со списком тестировщиков")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=2525, help="локальный конец SSH-туннеля")
    ap.add_argument("--delay", type=float, default=8.0, help="пауза между письмами, сек")
    ap.add_argument("--limit", type=int, default=0, help="отправить не больше N (0 = все)")
    ap.add_argument("--only-locale", default="", help="только один язык, для проверки")
    ap.add_argument("--default-locale", default="EN")
    ap.add_argument("--log", default=str(DEFAULT_LOG))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--test-to", default="", help="одно письмо на этот адрес и выход")
    ap.add_argument("--no-console-filter", action="store_true")
    ap.add_argument("--transport", choices=["ssh", "smtp"], default="ssh",
                    help="ssh = sendmail на сервере (шлёт наружу); smtp = туннель, только локальные адреса")
    ap.add_argument("--ssh-wrapper", default="", help="expect-обёртка для SSH с паролем")
    a = ap.parse_args()

    copy = json.loads(COPY_JSON.read_text(encoding="utf-8"))

    if a.test_to:
        loc = a.only_locale or a.default_locale
        msg = build(copy, loc, a.test_to)
        print(f"пробное письмо: {a.test_to}, язык {loc}, тема: {msg['Subject']}")
        if a.dry_run:
            return
        transport(a).send(msg)
        print("отправлено")
        return

    people, skipped = read_list(a.list, a.default_locale, a.no_console_filter)
    already = load_sent(a.log)
    queue = [p for p in people if canon(p["email"]) not in already]
    if a.only_locale:
        queue = [p for p in queue if p["locale"] == a.only_locale]
    if a.limit:
        queue = queue[: a.limit]

    by_loc = {}
    missing = set()
    for p in queue:
        by_loc[p["locale"]] = by_loc.get(p["locale"], 0) + 1
        if p["locale"] not in copy:
            missing.add(p["locale"])

    print(f"в списке годных адресов: {len(people)}")
    print(f"  пропущено: " + ", ".join(f"{k} {v}" for k, v in skipped.items() if v) or "  пропущено: нет")
    print(f"  уже писали раньше: {len(people) - len(queue) if not a.limit and not a.only_locale else '—'}")
    print(f"К ОТПРАВКЕ: {len(queue)}")
    print("  по языкам: " + ", ".join(f"{k} {v}" for k, v in sorted(by_loc.items(), key=lambda x: -x[1])))
    if missing:
        print(f"  ! нет текста для локалей {sorted(missing)} — уйдёт английский")
    est = len(queue) * a.delay / 60
    print(f"  расчётное время: ~{est:.0f} мин при паузе {a.delay} с")

    if a.dry_run:
        print("\n--dry-run: ничего не отправлено")
        return
    if not queue:
        print("\nотправлять нечего")
        return

    log_path = pathlib.Path(a.log)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    new_log = not log_path.exists()
    sent = failed = 0
    with log_path.open("a", newline="", encoding="utf-8") as lf:
        w = csv.writer(lf)
        if new_log:
            w.writerow(["ts_utc", "email", "locale", "result"])
        tr = transport(a)
        try:
            for i, p in enumerate(queue, 1):
                ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                try:
                    tr.send(build(copy, p["locale"], p["email"]))
                    w.writerow([ts, p["email"], p["locale"], "ok"]); sent += 1
                    print(f"  [{i}/{len(queue)}] {p['email']} ({p['locale']}) — ok")
                except Exception as e:
                    w.writerow([ts, p["email"], p["locale"], f"FAIL {type(e).__name__}: {e}"])
                    failed += 1
                    print(f"  [{i}/{len(queue)}] {p['email']} — ОШИБКА: {e}")
                lf.flush()
                if i < len(queue):
                    time.sleep(a.delay)
        finally:
            tr.close()

    print(f"\nотправлено {sent}, ошибок {failed}. Лог: {log_path}")


if __name__ == "__main__":
    main()
