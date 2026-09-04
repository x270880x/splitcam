# SEO Reminders — splitcam.com

> Рабочий файл: живые задачи и действующие правила. Открывать в начале любой
> SEO-сессии.
>
> **История завершённого — в [REMINDERS-LOG.md](REMINDERS-LOG.md).** Разделено
> 2026-07-19: файл разросся до 714 строк, и шесть постоянных правил терялись
> между отчётами о закрытых задачах.

---

## Живые задачи

| Срок | Статус | Задача |
|---|---|---|
| — | ⏳ открыто | **Ротировать токены Cloudflare и Ahrefs** — оба засвечены в переписке, файлы не менялись с 23.05, то есть ключи те же. Панели: Cloudflare → API Tokens → Roll; Ahrefs → Account → API |
| — | ⏳ открыто | **Сменить пароль DirectAdmin** — прислан в переписку 2026-08-12, лежит в `~/.hostsila_da_ssh`. Панель → Password |
| 🔴 срочно | ⏳ открыто | **Закрыть MySQL 3306 на `77.83.100.153`** — порт открыт в интернет, отвечает рукопожатием MariaDB 10.6.27 (проверено 12.08). Сайт статический, база не нужна. Удалить старую базу WordPress, убрать хосты удалённого доступа в DA, запросить у hostsila закрытие порта |
| — | 🔄 в работе | **Снять блокировки домена** — на 12.08 счётчик VirusTotal упал с 4/91 до 2/91: AlphaSOC снят, CRDF оказался не листингом вовсе. Fortinet снят (переклассифицирован в Freeware and Software Downloads через час после заявки), держится MalwareURL (письмо отправлено), Gridinsoft — тикет подан 12.08, владение подтверждено. Отдельно жива запись ThreatFox IOC 1861022, нужен аккаунт abuse.ch. Статусы: `seo/APPEALS-READY.md` |
| — | ⏳ ждём | **Ответ от Morgan Sands (`morgansands@verizon.net`)** — 12.08 ответили с `support@`, спросили точный блокируемый адрес и имя детекта. Без них заявка в Malwarebytes слабая. Переписка в ящике `support@`, копия ответа в `.Sent` |
| 2026-09-24 | 🧪 эксперимент | **Проверить, отдала ли главная запрос «virtual camera»** — 20.08 из тайтла английской главной убрано «& Virtual Camera» (стало `Free Live Streaming Software for PC & Mac | SplitCam`), потому что главная перехватывала generic-запрос у `/virtual-camera`: 1403 показа / поз. 6.7 против 1 показа / поз. 16 у профильной. База замера — `seo/vc-baseline.json` (147 запросов, 4137 показов, 172 клика за 21.07–17.08). Сравнить: `seo/.gscvenv/bin/python seo/vc_cluster.py --compare seo/vc-baseline.json`. Успех = профильная страница поднялась по «virtual camera», клики кластера выросли. 🔴 Если через месяц главная запрос потеряла, а профильная не поднялась — откатить тайтл. Локали НЕ трогали намеренно: там объёмы 1–27 показов и профильная страница и так ранжируется |
| — | ⏳ открыто | **Отчёт о состоянии SEO** — данные есть, отчёт не написан. См. ниже |
| — | ⏳ следить | **Рассылка тестировщикам ушла 12.08** (38 писем, 0 ошибок). Смотреть: отложенные отлупы в `support@`, ответы людей, и сколько реально нажали opt-in — последнее видно только в Play Console, API туда нет |
| когда выйдет Android Remote | ⏳ триггер | Вернуть обычную ссылку на Play вместо CTA тестировщика; переоткрыть решение по `/products/remote/`. Детали: `seo/ANDROID-TESTER-CTA.md` |

Закрытые пункты расписания (Play Store, Week 1/2 checks, Wave 2, tester CTA)
перенесены в [REMINDERS-LOG.md](REMINDERS-LOG.md).

---

## Если Python-скрипты падают с `gaierror` / `Unable to find the server` (2026-08-24)

Симптом: `gsc.py`, `tester_signups.py`, `vc_cluster.py` падают на разрешении имён, при этом
`curl` до тех же хостов работает. Из Python не резолвится **ничего**, даже `splitcam.com`.

Причина — не Python. Mac сидит на **точке доступа телефона** (`192.168.49.x`), а она:
- отвечает по DNS, но на все запросы даёт `REFUSED` → прямого DNS нет вообще;
- пропускает трафик только через HTTP-прокси `192.168.49.1:8181`.

`curl` работает, потому что читает `HTTP_PROXY`/`HTTPS_PROXY` из окружения и отдаёт имя прокси.
`socket.getaddrinfo()` в Python так не умеет — он резолвит сам и упирается в `REFUSED`.

**Лечение (одно из двух):**
1. Перейти на обычную сеть — тогда всё работает без правок. Это предпочтительно.
2. Остаться на точке доступа: в окружении `.gscvenv` должен стоять **`pysocks`**, иначе
   `httplib2.socks is None` и httplib2 молча игнорирует прокси, даже увидев его.
   Поставлено 2026-08-24. Запускать так:
   ```bash
   export http_proxy=http://192.168.49.1:8181
   export https_proxy=http://192.168.49.1:8181
   seo/.gscvenv/bin/python seo/gsc.py --days 7
   ```
   ⚠️ Переменные нужны в **нижнем** регистре — httplib2 читает только их.

⚠️ Отдельная поломка того же происхождения: у `seo/.gscvenv/bin/pip` в shebang остался
**старый путь проекта** (`Documents/Дизайны/SplitCam/SPLITCAM DEV./…`) с переезда папки, и он
не запускается. Ставить пакеты через `seo/.gscvenv/bin/python -m pip install …`, либо
пересоздать окружение.

---

# ПОСТОЯННЫЕ ПРАВИЛА

Шесть правил ниже действуют всегда. Три из них (бета → ver.txt → macOS)
связаны между собой — читать вместе.

---


## Standing rule — link every feature/product page FROM the `/features/` hub (user, 2026-06-28)

`/features/` is the central hub. **Whenever a new feature or product page is built**
(a dedicated AI-background, scenes/layers, effects, audio-mixer, screen-capture, or any
future `/multistreaming/`-type page), add an outbound link from its matching `/features/`
card — the existing pattern is `<a … class="product-changelog">Learn more <svg…></a>`
inside that card's `.product-cta`. **Then mirror the link into all 35 locale `/features/`
pages** (the link text is translated), and rerun `python3 seo/i18n_wire.py` +
`python3 seo/linkcheck.py --no-network` (must be 0).

Currently linked from `/features/`: Virtual Camera → `/virtual-camera/`, Multistreaming →
`/multistreaming/`, OBS Import → `/alternatives/obs/`, Remote → `/products/`. Still
UNLINKED (no dedicated page yet — link them the moment one ships): **AI Background
Removal · Scenes/Sources/Layers · Effects/Filters/Beauty · Audio Mixer · Screen & Window
Capture.** Don't forget.

---


## Standing rule — Hebrew locale: SplitCam is FEMININE (2026-07-02)

In `he/`, the brand **SplitCam takes feminine agreement** (as תוכנה): verbs, adjectives,
pronouns — `SplitCam עובדת / תומכת / חינמית / זמינה`, `היא / אותה`. The whole locale was
unified 2026-07-02 (all 15 pages, JSON-LD included). **Any new or edited `he/` copy must
keep feminine agreement** — don't reintroduce `SplitCam עובד / חינמי / הוא`. Same applies
to SplitCam Remote (אפליקציה). Words agreeing with other subjects (צוות, דרייבר, שידור,
OBS…) keep their own gender.

---


## Релизы: бета, ver.txt, macOS → скилл `splitcam-release`

Полные правила — **в скилле `splitcam-release`**: он загружается, когда ты
публикуешь сборку, то есть ровно тогда, когда они нужны. Там таблица
«Beta vs Stable» построчно: changelog, версионный установщик, latest-указатели,
версия на главной и в JSON-LD, `ver.txt` ×3 / `macver.plist` / `versions.json`.

Суть, чтобы не открывать скилл ради проверки:

- **Бета = только changelog**, каким бы высоким ни был её номер. Latest-указатели,
  версия на главной и автообновление не трогаются никогда.
- **`ver.txt` (все три) бампятся через 10 дней после стабильного релиза**, и
  никогда для беты. Файлы host-managed, вне git.
- **macOS stable**: DMG кладётся под двумя именами (`SplitCam.dmg` + версионное),
  затем `macver.plist` и блок `macOS` в `versions.json`.

Проверено 2026-07-19: на сайте stable `10.9.2`, бета `10.9.4` только в changelog —
правило соблюдается.

## 🔴 Правило: никогда не редиректить с явного `/<locale>/` URL

_Как выяснилось (2026-07-18): собственный JS де-индексировал 512 локализованных страниц._
The 512 locale pages (97% of the 526-URL sitemap) were **not indexed**, and it was NOT crawl
latency. The `<!--AD-->` language auto-redirect ran on EVERY page, including explicit `/xx/` URLs:
on `/ru/features` it compared `document.documentElement.lang` ("ru") against the browser language
and, for any English-language client, did `location.replace('/features')`. **Googlebot crawls with
`en-US`**, so Google was bounced off every localized page onto its English twin and never indexed
them. **Fix:** the redirect now only fires on URLs WITHOUT an explicit locale prefix — an explicit
`/xx/` URL is always respected; a foreign visitor landing on an English page is still forwarded, so
the UX intent survives. Verified 9/9 scenarios in node. Applied to all 526 pages **and to
`seo/i18n.py`** (the generator) so `i18n_wire.py` can't reintroduce it.
**Standing rule: never auto-redirect away from an explicit `/<locale>/` URL.**


---

# ДЕЙСТВУЮЩАЯ ИНФРАСТРУКТУРА

Не история — текущее состояние, которое надо учитывать.

## Хостинг: всё на DirectAdmin (проверено 2026-07-19)

**Почта за 6–14 июля — закрыто, не восстанавливаем (решение 2026-07-19).**
Проверено по заголовкам писем на DA: в `admin@` 1257 писем, июль представлен
только 2 и 3 числа — переписка за 6–14 июля туда не доехала и осталась на
старом cPanel. Старый сервер `91.223.223.113` к тому моменту уже отдавал
только страницу входа с капчей (SSH/IMAP/SMTP закрыты, API отклоняет
сохранённые креды). Пользователь решил эти письма не восстанавливать —
**больше к вопросу не возвращаться, задачу не заводить.**

~~**WEB и ПОЧТА — оба на DirectAdmin** `185.67.3.44` (`lwanngbs@185.67.3.44`,
креды `~/.hostsila_da_ssh`, панель API :2222). Проверено по DNS 2026-07-19:
`MX → mail.splitcam.com → 185.67.3.44`, `webmail → 185.67.3.44`.~~
**УСТАРЕЛО — см. блок ниже.** Cloudflare спереди для веба (apex/www → CF),
почта напрямую — это по-прежнему верно.

🔴 **ПЕРЕЕХАЛ ВЕСЬ СЕРВЕР — и веб, и почта (проверено НА САМОМ СЕРВЕРЕ 2026-08-12).**

    Панель:  https://pl-rocket-da3.hostsila.org:2222/
    SSH:     lwanngbs@77.83.100.153, порт 22, пароль в ~/.hostsila_da_ssh
    Докрут:  /home/lwanngbs/domains/splitcam.com/public_html
    Ящики:   admin, support, pola

Что это боевой сервер, а не staging-копия: в логах доступа свежие запросы с
пограничных IP Cloudflare (`172.69.x`, `172.70.x`, `104.23.x`) на
`www.splitcam.com:443`, порядка 20 МБ сжатого лога в сутки. `MX` и `webmail`
ведут сюда же.

**Всё, что записано про `185.67.3.44` и `rocket-da4`, устарело** — и здесь, и в
`CLAUDE.md`, и в `ONBOARDING.md`.

Ловушка при проверке: `185.67.3.44`, `77.83.100.153`, `77.83.100.124` и
`91.223.223.113` — все четыре отвечают Dovecot по IMAPS 993 и все четыре отдают
сайт по HTTP 200 одинакового размера (проверено `curl --resolve`). «Сервер
отвечает» не доказывает ничего: решают только DNS и логи доступа.

## 🔴 DMARC `p=reject` — правило для любой отправки от @splitcam.com

`_dmarc.splitcam.com` = `v=DMARC1; p=reject` (отчёты идут в Cloudflare).
SPF: `v=spf1 ip4:91.223.223.113 ip4:77.83.100.124 ip4:185.67.0.5
ip4:77.83.100.153 +a +mx +ip4:194.28.87.164 ~all`.

Следствие, о которое легко разбиться: **нельзя слать письма от support@splitcam.com
через чужие серверы.** Если завести адрес алиасом в Gmail и выбрать «отправлять
через Gmail», письма уйдут с IP Google — SPF их не авторизует, DKIM подпишется
доменом `gmail.com`, выравнивания нет, и при `p=reject` получатель обязан
отклонить письмо. Не спам — отказ. Единственный рабочий вариант: алиас с
отправкой **через свой SMTP** `mail.splitcam.com` (тогда исходящий IP —
`77.83.100.153`, который покрыт и `ip4:`, и `+mx`).

**SMTP на сервере исправен — проверено на самой машине 2026-08-12.** Exim 4.99.4
отвечает баннером на 25, 587 и 465 с localhost, входящая почта извне реально
доходит (последние письма от сторонних отправителей — 5 и 7 августа).

Ложная тревога, чтобы её больше не заводить заново: снаружи с рабочего мака
порты 25/587/465 принимают TCP и молча закрываются без баннера, и это выглядит
как блокировка на сервере. **Это блокировка на стороне мака/провайдера, а не
сервера** — `smtp.gmail.com` и `smtp.yandex.ru` с той же машины ведут себя
ровно так же, а уж они исправны. Диагностировать SMTP splitcam.com с этой
машины нельзя в принципе; смотреть изнутри по SSH.

⚠️ **Более ранние записи в этом файле и в логе утверждали, что почта осталась
на cPanel `jntckkaf@91.223.223.113`** — это устарело. Переезд почты завершён,
cPanel в рабочей схеме больше не участвует. Если cPanel-план ещё оплачен —
это вопрос к отмене подписки, а не к инфраструктуре.

Полная история обоих переездов — в [REMINDERS-LOG.md](REMINDERS-LOG.md).


## Деплой: квота DirectAdmin

Полное правило — **в скилле `splitcam-deploy`** (срабатывает в момент деплоя,
когда оно и нужно). Коротко: аккаунт живёт у предела квоты (~11 ГБ, из них
`win-download` ~9.8 ГБ), и tar-деплой при переполнении падает **молча** — вывод
выглядит успешным, а сайт остаётся старым.

**Всегда проверять, что деплой доехал** — по изменившемуся байту на живом
сайте, не по отсутствию ошибок. Каждый новый Mac DMG добавляет ~282 МБ
(latest + версионная копия), запас тает.

# РЕГУЛЯРНЫЕ ПРОЦЕДУРЫ


## IndexNow — submit the full sitemap, both domains (2026-07-19)

Two sites, two keys, both verified serving their key file:

| Domain | Key | URLs |
|---|---|---|
| splitcam.com | `485c229ee85ee55f1967363aabec7e9a` | 598 |
| camstreamguide.com | `1dce1f527c611c22daebaf1b00b0649a` | 2 135 |

Post the **entire sitemap** in chunks of 500 to all three endpoints —
`api.indexnow.org/IndexNow`, `www.bing.com/indexnow`, `yandex.com/indexnow`. 200 or 202 both
mean accepted. There is **no daily quota**; the instinct to ration submissions comes from
GSC's ~10-12 Request-Indexing limit and does not apply here.

⚠️ That GSC limit is **per Google ACCOUNT, not per property** — spending it on splitcam.com
exhausts camstreamguide's allowance the same day. Decide each morning which property needs
it more; splitcam.com is already indexed, camstreamguide is not.

Google's own `google.com/ping?sitemap=` is dead (404, retired 2023). IndexNow reaches only
Bing and Yandex — never Google — but for a young domain those are the realistic first wins.

**Last full run: 2026-08-25 — 598 URLs, 2 chunks (500 + 98), all three endpoints accepted**
(api.indexnow.org 200/200, bing 200/200, yandex 202/200). The run before that was 526 URLs on
2026-07-02; the 2026-08-20 submission was a targeted one for the homepage retitle only, so the
70 Virtual Audio pages and `/for/educators` had never gone out as a full list until now.
Reminder for next time: a targeted submission does NOT replace the full-sitemap run.


---

## Проверка индексации без Search Console

Прямой доступ к GSC появился 2026-07-18, но метод остаётся полезным, если
доступ снова потеряется: проверка через `site:` в разных поисковиках, сверка
с логами сервера, IndexNow-ответы. Полное описание метода и цифры того
прогона — в [REMINDERS-LOG.md](REMINDERS-LOG.md), раздел «Verifying indexing
WITHOUT Search Console access».

---


## Отчёт о состоянии SEO (переформулировано 2026-07-19)

> Раньше значилось как «Month 1 full review» со сроком 2026-06-19 — отсчёт шёл от
> запуска Wave 1 (20.05). К 19.07 прошло два месяца, и название перестало
> соответствовать. Данные Search Console с тех пор получены напрямую (18.07),
> так что собирать заново нужно не всё.
>
> **Писать в `seo/reports/2026-07-status.md`**, не в `month1.md`.

**Goal:** Write a real report on what worked, what didn't, and what Wave 3 should be.

**Data to collect:**

**Google Search Console (all SEO pages):**
- Total impressions / clicks / avg position per page
- Top 20 queries actually driving traffic
- Pages with high impressions but low CTR → title/meta tuning candidates
- Pages with **zero** impressions → need internal link push or content thinning

**Ahrefs (re-run):**
```bash
cd "/Users/splitcam/Documents/Проекты/SplitCam/SplitCam сайт/splitcam/seo"
AHREFS_TOKEN='<token — REGENERATE FIRST>' python3 ahrefs.py
```
Compare DR / ranked keyword count / traffic estimate vs baseline in `seo/reports/`.

**Output:** write `seo/reports/2026-07-status.md` covering:
- What worked (winning pages/keywords)
- What didn't (dead pages — kill or rebuild?)
- Wave 3 recommendation (which clusters to target next)

**Reminder:** the Ahrefs token shared in ONBOARDING.md should have been regenerated by now. If not, regenerate it first.

---

---


## How to use this file

- **Bookmark it** in your editor / browser
- **Open at start of any SEO chat** — Claude can `Read` this file and pick up exactly where things left off
- **Update status** in the live-tasks table as tasks complete. Завершённые разделы переносить в `REMINDERS-LOG.md`, не удалять
- **`CronCreate` для напоминаний не годится** — он session-only, умирает вместе с чатом (проверено в мае 2026). **Но `scheduled-tasks` персистентен** — с 2026-07-19 задача `reminders-overdue-check` читает таблицу выше каждый понедельник и сообщает о просроченном. Этот файл остаётся источником правды о том, ЧТО запланировано.

## 2026-10-01 — замер раздела /alternatives/ после переориентации хаба

Что сделано 2026-09-03: хаб переориентирован с брендовых запросов на общий, четыре
дочерние страницы (ManyCam, Restream, StreamYard, Stream Deck) выкачены на 35 языках.

Базовый замер до изменения — `seo/alt-baseline.json`: 3451 показ / 186 кликов / 276
запросов. Ключевые позиции на момент замера:

    manycam alternative              355 показов  23 клика  поз. 4.7   (отвечала главная)
    streamyard alternative           238 показов   5 кликов поз. 11.8  (отвечал ХАБ)
    restream alternative free         51 показ     2 клика  поз. 15.5  (отвечал ХАБ)
    obs virtual camera alternative    41 показ      6 кликов поз. 3.3

Проверить: `python3 seo/alt_cluster.py --compare`

Что должно произойти: запросы переезжают с хаба и главной на дочерние страницы, позиции
по ним растут. Хаб при этом теряет свои показы по брендовым запросам — это ожидаемо и
не является провалом.

🔴 УСЛОВИЕ ОТКАТА: если через месяц `streamyard alternative` и `restream alternative free`
просели по позиции больше чем на 3 пункта И дочерние страницы их не подхватили —
значит обмен не сработал, и хабу надо вернуть брендовые запросы в title.

Отдельно проверить, подхватила ли дочерняя страница `manycam alternative` (355 показов,
23 клика) у главной: это самый ценный запрос кластера, и до изменения его держала
главная страница с позиции 4.7.

## Пробел локализации: hr/for/churches/ без сравнительной таблицы (найдено 2026-09-04)

На английской `/for/churches/` есть таблица SplitCam vs vMix vs ProPresenter (12 строк).
В хорватской локали `<table>` нет вообще — сравнение туда никогда не переносили.
Всплыло при правке ложных утверждений о vMix: агент исправил FAQ и абзац, а таблицы не
нашёл. Нужно перевести и вставить таблицу (взять структуру из EN, текст перевести).
Проверить остальные страницы с таблицами — см. вывод аудита в журнале за 2026-09-04.

## 2026-10-04 — замер новых страниц vMix и phone-as-webcam

Выкачены 2026-09-04 на 35 языках. Целевые запросы (Ahrefs, US):
  vmix alternative 150/мес слож. 0 · vmix alternatives 80 · vmix vs obs 80
  use iphone as webcam 900 слож. 46 · use phone as webcam 700 слож. 35 · phone as webcam 150
Проверить в Search Console по страницам /alternatives/vmix и /phone-as-webcam: появились ли
показы, по каким запросам, позиции. Телефонная страница — долгая ставка (сложность 35–46,
верхушку держат DroidCam/Iriun), быстрого результата не ждать.

## 2026-10-04 — замер /multi-camera/ (добавить к проверке vMix и phone-as-webcam)

База до страницы (Search Console, 90 дней до 2026-09-02): кластер 1901 показ / 24 клика;
`multi camera live streaming software` 242 показа поз. 14.4 (отвечала главная),
`… software free` 164 показа поз. 4.9 / 10 кликов, `streaming multicamara` 110 поз. 27.8 (es).
Ожидание: запросы переезжают с главной на /multi-camera/, позиции растут; испанский —
на /es/multi-camera/. Проверить по страницам, не по запросам.
