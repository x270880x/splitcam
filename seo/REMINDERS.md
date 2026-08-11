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
| — | ⏳ открыто | **Отчёт о состоянии SEO** — данные есть, отчёт не написан. См. ниже |
| когда выйдет Android Remote | ⏳ триггер | Вернуть обычную ссылку на Play вместо CTA тестировщика; переоткрыть решение по `/products/remote/`. Детали: `seo/ANDROID-TESTER-CTA.md` |

Закрытые пункты расписания (Play Store, Week 1/2 checks, Wave 2, tester CTA)
перенесены в [REMINDERS-LOG.md](REMINDERS-LOG.md).

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

**WEB и ПОЧТА — оба на DirectAdmin** `185.67.3.44`
(`lwanngbs@185.67.3.44`, креды `~/.hostsila_da_ssh`, панель API :2222).
Cloudflare спереди для веба (apex/www → CF), почта напрямую.

Проверено по DNS 2026-07-19:
`MX → mail.splitcam.com → 185.67.3.44`, `webmail → 185.67.3.44`, порт 465 отвечает.

🔴 **ПОЧТА УЕХАЛА С `185.67.3.44` (перепроверено по DNS 2026-08-12).** Сейчас:
`MX → mail.splitcam.com → 77.83.100.153`, `webmail → 77.83.100.153`. Адрес
`77.83.100.153` не упомянут больше нигде в доках — когда и зачем переносили,
по репозиторию не восстановить. **Строчка выше про `185.67.3.44` для почты
устарела; для веба не проверялась.**

Ловушка при проверке: `185.67.3.44`, `77.83.100.153`, `77.83.100.124` и
`91.223.223.113` — все четыре отвечают Dovecot по IMAPS 993 и все четыре отдают
сайт по HTTP 200 одинакового размера (проверено `curl --resolve`). «Сервер
отвечает» не доказывает ничего. Смотреть строго по MX; какой сервер origin для
веба — снаружи не определить, Cloudflare закрывает, нужен CF-токен или доступ
на сервер.

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

Снаружи 2026-08-12: IMAPS 993 отвечает штатно, а SMTP 25/587/465 принимают TCP
и молча закрывают без баннера. Похоже на фильтрацию по IP клиента, но с одной
точки не различить — проверить до настройки алиаса, иначе Google не сможет
доставить код подтверждения и настройка тихо не пройдёт.

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
| splitcam.com | `485c229ee85ee55f1967363aabec7e9a` | 527 |
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
