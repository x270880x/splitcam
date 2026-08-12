# Апелляции — готовые тексты под вставку

Составлено 2026-08-12. Обоснование, порядок и что убивает заявку —
в [REPUTATION-DELISTING.md](REPUTATION-DELISTING.md). Здесь только то, что копируется.

**Перед отправкой заменить во всех текстах:** `<ВАШЕ ИМЯ>`, `<ДОЛЖНОСТЬ>`,
`<you@splitcam.com>`, `<ТЕЛЕФОН>`. Почта — **только на домене splitcam.com**, она же
доказательство владения; gmail — причина молчаливого отказа у CRDF, AlphaSOC и Fortinet.

## Статус подачи

| Вендор | Статус | Когда | Как проверять результат | Когда напоминать |
|---|---|---|---|---|
| **Fortinet** | ✅ подана | 12.08.2026 | `https://www.fortiguard.com/webfilter` (POST со страницы, прямой GET отдаёт 403) | не напоминать — rate-limit; обещают сутки |
| **MalwareURL** | ✅ отправлено письмом на `team@malwareurl.com` с `support@splitcam.com` | 12.08.2026 | `https://www.malwareurl.com/listing-urls.php` | письмом через неделю, если тишина |
| **AlphaSOC** | ✅ отправлено письмом на `virustotal@alphasoc.com` с `support@splitcam.com` | 12.08.2026 | только VirusTotal, публичного lookup нет | вежливый follow-up через 10–14 дней |
| **CRDF** | ⏳ форма заполнена, не отправлена | — | `https://threatcenter.crdf.fr/check.html` — отдельно apex, `www`, `http://77.83.100.153` | ответ ~24 ч, решение до 5 рабочих дней |
| **ThreatFox** | ⏳ ждёт аккаунт abuse.ch | — | сама карточка `https://threatfox.abuse.ch/ioc/1861022/` | — |
| **Malwarebytes** | ⏳ ждёт аккаунт + скриншот от Morgan | — | публичной проверки нет, только Browser Guard | staff отвечает за часы–48 ч |
| Gridinsoft | подавать последним | — | `https://gridinsoft.com/online-virus-scanner/` | только если через 2–3 недели держится |

Fortinet и AlphaSOC подтверждений не присылают вообще — тишина там норма, а не отказ.
Общий индикатор успеха — счётчик на VirusTotal: сейчас 4 из 91, цель 0.

---

🔴 **Проверено на практике 12.08.2026: подать эти формы из автоматизированного
браузера нельзя.** Форма Fortinet была заполнена корректно (URL, категория, имя,
почта, компания, комментарий, `contact_me`, пройденные ALTCHA и картиночная капча) —
POST на `https://www.fortiguard.com/faq/wfratingsubmit` вернул **403 Forbidden**, и
страницу перебросило на главную. Это отбил их антибот-слой, а не валидация полей.
Подбирать обходы никто не будет. **Все формы подаёт человек в обычном браузере.**

Реквизиты для всех форм (согласованы с владельцем 12.08.2026):

    Name:    Anatoly Smelkov
    Email:   support@splitcam.com
    Company: SplitCam Labs

Подавать **строго в этом порядке**: ThreatFox первым. Остальные, судя по всему, тянут
вердикт оттуда, и снятие ниже по течению не удержится, пока жив первоисточник.

---

## 0. ThreatFox — первоисточник. Начинать отсюда

**Куда:** `https://threatfox.abuse.ch/ioc/1861022/` → меню `Actions` → `Report False Positive`
**Нужен аккаунт abuse.ch** (бесплатный, Auth0). Регистрация: `https://auth.abuse.ch/`

> This entry reports splitcam.com as ClearFake / payload_delivery. I am the domain owner,
> and I am asking for it to be withdrawn on the following grounds.
>
> The site this entry describes no longer existed when the entry was filed.
>
> This IOC was submitted 2026-07-27 19:57:13 UTC. By that date the site had already been
> a static HTML/CSS/JS build for at least nine days — no CMS, no plugins, one PHP file in
> the document root — on a different server. The Internet Archive snapshot from
> 2026-07-18 is 144122 bytes, exactly the size of the page served today; it contains no
> injected script and loads no external script host other than www.googletagmanager.com.
>
> An earlier WordPress installation of this domain WAS compromised, and I am not
> disputing detections from that period — they were correct. What I am disputing is an
> entry filed three weeks after that installation was destroyed and replaced.
>
> The entry itself carries: confidence 50%, no reference or evidence link, and
> "last seen: never" — it has not been re-observed by anyone in the two weeks since.
>
> Verification performed on 2026-08-12:
>
> - The homepage returns a byte-identical response with an identical SHA-256 across four
>   different user agents and with a Google referer, so nothing is being served
>   conditionally.
> - The Cloudflare layer was audited over the API: the only Worker on the zone is a
>   redirect map (path lookup, 301, otherwise pass through) with no HTMLRewriter, no
>   eval, and no user-agent or referer branching, so HTML injection is not possible
>   there. No subdomain points at any previous server. The cache was purged in full.
> - VirusTotal: Google Safe Browsing, Kaspersky, BitDefender, ESET, Sophos, Dr.Web,
>   Emsisoft, G-Data, Forcepoint and Netcraft all report the domain clean.
> - Sucuri SiteCheck: no malware, no blacklisting.
> - AbuseIPDB for the origin 77.83.100.153: 3% confidence, one unrelated port-scan report.
> - All WordPress paths (wp-login.php, xmlrpc.php, wp-admin/, wp-content/, wp-includes/,
>   wp-json/, readme.html) return 404.
>
> If the reporter has evidence from 2026-07-27 specifically, I would genuinely like to
> see it — if something was still reachable on that date I need to find it. But as the
> entry stands there is nothing attached to it, and it is being consumed downstream by
> several vendors who now block the domain.
>
> — <ВАШЕ ИМЯ>, <ДОЛЖНОСТЬ>, <you@splitcam.com>

---

## 1. Fortinet (FortiGuard Web Filter) — наибольший охват

**Куда:** `https://www.fortiguard.com/faq/wfratingsubmit`
Аккаунт не нужен. Проверка результата: `https://www.fortiguard.com/webfilter`

| Поле | Что вписать |
|---|---|
| URL | `splitcam.com` |
| Suggest a category | **`Freeware and Software Downloads`** ← обязательно, без выбранной категории заявку отклоняют |
| Name / Email / Company | заполнить полностью, почта на splitcam.com |
| ☑ contact_me | **отметить**, иначе ответа не будет вообще |

> splitcam.com is the site of SplitCam, free streaming and virtual-camera software for
> Windows and macOS. The domain was registered in 2005. It is currently rated Malware;
> I am asking for a re-rating to Freeware and Software Downloads.
>
> An earlier WordPress installation of this site was compromised, and detections from
> that period were correct. That installation no longer exists. Since 2026-07-18 at the
> latest the site is static HTML/CSS/JS with no CMS and no plugins — a single PHP file in
> the document root — on a different server (origin 77.83.100.153, served through
> Cloudflare at 104.21.39.190 / 172.67.148.86).
>
> The current classification appears to trace to ThreatFox IOC 1861022, filed
> 2026-07-27, malware ClearFake. That entry was filed nine days after the site had
> already been replaced; it carries confidence 50%, no evidence reference, and its
> "last seen" field is "never". I have submitted a false-positive report there as well.
>
> Independent checks, 2026-08-12: VirusTotal reports the domain clean for Google Safe
> Browsing, Kaspersky, BitDefender, ESET, Sophos, Dr.Web, Emsisoft, G-Data, Forcepoint
> and Netcraft, and rates https://splitcam.com/win-download/SplitCamSetup_x64.msi clean.
> Sucuri SiteCheck finds no malware and no blacklisting. AbuseIPDB scores the origin IP
> at 3% with one unrelated port-scan report. The homepage returns a byte-identical
> response across four user agents and with a Google referer, so no cloaked content is
> being served. All WordPress paths return 404.
>
> Please re-scan and re-categorise. If your verdict is inherited from a third-party feed
> rather than your own crawl, please tell me which source.
>
> <ВАШЕ ИМЯ>, <ДОЛЖНОСТЬ>, <you@splitcam.com>, <ТЕЛЕФОН>

---

## 2. Malwarebytes — единственная подтверждённая блокировка у живого пользователя

**Куда:** `https://forums.malwarebytes.com/forum/123-website-blocking/?do=add`
**Нужен бесплатный аккаунт:** `https://forums.malwarebytes.com/register/`

⚠️ **Ждать скриншот от Morgan Sands.** Их закреплённые правила требуют логи и скриншот
блокировки; без них тема встаёт намертво. Мы запросили у него точный адрес, имя детекта
и скриншот 12.08 — пока ответа нет. Если через неделю тишина, подавать без скриншота,
явно написав, что блокировку сообщил пользователь и своего скриншота у нас нет.

**Заголовок темы:** `False positive website block: splitcam.com`

**Домен и IP вставлять ТОЛЬКО в Code Block** (кнопка `<>` на панели редактора) —
кликабельная ссылка нарушает их правила.

> A user reported to our support address that Malwarebytes blocks our site as a Trojan.
> I am the domain owner.
>
> Domain and addresses:
>
> ```
> splitcam.com
> origin IP 77.83.100.153
> Cloudflare 104.21.39.190 / 172.67.148.86
> ```
>
> Checked before posting, per the pinned instructions: no existing report for this domain
> in this forum in the past 6 months; AbuseIPDB for the origin IP scores 3% confidence
> with a single unrelated port-scan report.
>
> An earlier WordPress installation of this site was compromised and detections from that
> period were correct. It no longer exists. Since 2026-07-18 at the latest the site is
> static HTML/CSS/JS — no CMS, no plugins, one PHP file in the document root — on a
> different server. The Internet Archive snapshot of 2026-07-18 is 144122 bytes, exactly
> the size of the page served today, with no injected script.
>
> The block most likely traces to ThreatFox IOC 1861022, filed 2026-07-27 (ClearFake,
> confidence 50%, no evidence reference, "last seen: never") — nine days after the site
> had already been replaced. A false-positive report has been filed there too.
>
> As of 2026-08-12: VirusTotal reports the domain clean for Google Safe Browsing,
> Kaspersky, BitDefender, ESET, Sophos, Dr.Web, Emsisoft, G-Data, Forcepoint and
> Netcraft; Sucuri SiteCheck finds no malware and no blacklisting; the homepage is
> byte-identical across four user agents and with a Google referer; all WordPress paths
> return 404; the Cloudflare layer was audited and its only Worker is a redirect map with
> no ability to modify HTML.
>
> Could you please re-scan and remove the block — and, given the history, **add the
> domain to the whitelist** rather than only unblocking it? I have seen reports here of
> domains slipping back through the feed after removal.
>
> User-side details, as reported to us: <адрес блокировки>, detection name
> <имя детекта>, module <Browser Guard v… / Web Protection v…>. Screenshot attached.

---

## 3. CRDF Threat Center

**Куда:** `https://threatcenter.crdf.fr/false_positive.html`
Аккаунт не нужен. Проверка: `https://threatcenter.crdf.fr/check.html` — отдельно apex,
`www` и `http://77.83.100.153`

- `domainName` = `https://splitcam.com` — **со схемой**, голое `splitcam.com` не пройдёт
  валидацию.
- Через `multiple_urls` добавить `https://www.splitcam.com` (до 5 URL).
- Отметить `tos_ag` и `not_robot`.
- **Поле `motivations` — жёсткий лимит 1000 символов**, поэтому текст ниже сжат
  специально. Не расширять.

> I own splitcam.com (SplitCam, free streaming/virtual-camera software, domain from 2005).
> An earlier WordPress install was compromised; those detections were correct. It is gone.
> Since 2026-07-18 the site is static HTML/CSS/JS, no CMS, no plugins, on a new server
> (origin 77.83.100.153, via Cloudflare). The listing appears to come from ThreatFox IOC
> 1861022, filed 2026-07-27 — nine days AFTER the rebuild — confidence 50%, no evidence
> reference, last seen: never. On 2026-08-12 VirusTotal shows the domain clean for Google
> Safe Browsing, Kaspersky, BitDefender and ESET, and rates our installer URL clean;
> Sucuri finds nothing; AbuseIPDB scores the IP 3%; the homepage is byte-identical across
> four user agents and with a Google referer; all WordPress paths 404. Our installers
> bundle no third-party offers; EULA and Privacy Policy are linked from the download page.
> Please re-scan and delist. If the verdict is inherited from a feed, please say which.
>
> <ВАШЕ ИМЯ>, <you@splitcam.com>

*(Посчитано с подстановкой имени и адреса: **989 знаков**, запас 11. Ничего не дописывать — при 1001 форма молча обрежет текст.)*

---

## 4. MalwareURL

**Куда:** `https://www.malwareurl.com/contact-us.php`, продублировать письмом на
`team@malwareurl.com`

🔴 **Ни в коем случае не `https://www.malwareurl.com/submit.php`** — эта форма
**добавляет** URL в блоклист, и ссылка на неё подсовывается прямо из результата проверки.

Поле `info` — минимум 25 символов, отдельных полей под домен и категорию нет, всё текстом.

> Your database currently lists splitcam.com with the security category
> `Trojan JS ClearFake`. I am the domain owner and I am asking for a re-scan.
>
> The ClearFake injection was present on a previous WordPress installation of this
> domain. That installation was destroyed, not cleaned: since 2026-07-18 the site is
> static HTML/CSS/JS with no CMS and no plugins, one PHP file in the document root, on a
> different server.
>
> Please note you are scanning our Cloudflare addresses (104.21.39.190 / 172.67.148.86);
> the origin behind them is 77.83.100.153. Both now serve the same static build. The
> Cloudflare cache was purged in full on 2026-08-12 and the site re-checked through the
> CDN afterwards, so no stale cached object remains.
>
> The upstream source appears to be ThreatFox IOC 1861022, filed 2026-07-27 — nine days
> after the rebuild — with confidence 50%, no evidence reference, and "last seen: never".
> A false-positive report has been filed there.
>
> As of 2026-08-12 VirusTotal reports the domain clean for Google Safe Browsing,
> Kaspersky, BitDefender, ESET, Sophos, Dr.Web, Emsisoft, G-Data, Forcepoint and
> Netcraft, and rates our installer URL clean. Sucuri SiteCheck finds no malware.
>
> <ВАШЕ ИМЯ>, <ДОЛЖНОСТЬ>, <you@splitcam.com>

---

## 5. AlphaSOC

**Куда:** `https://alphasoc.com/contact/`, и параллельно письмом на
**`virustotal@alphasoc.com`** (этот адрес указан на официальной странице FP-контактов
VirusTotal — предпочтительный канал).

- Дропдаун «How can we help?» переключить с `Sales / general enquiry` на
  **`Threat indicator review`** — иначе заявка уедет в продажи.
- Company заполнить, почта рабочая на splitcam.com.
- Приложить пермалинк на отчёт VirusTotal по домену.

> Your feed currently classifies splitcam.com as Malware on VirusTotal. I am the domain
> owner and am asking for the indicator to be reviewed.
>
> An earlier WordPress installation of this site was compromised; that installation no
> longer exists. Since 2026-07-18 the site is static HTML/CSS/JS with no CMS and no
> plugins, on a different server (origin 77.83.100.153, via Cloudflare).
>
> The likely upstream is ThreatFox IOC 1861022, filed 2026-07-27 — nine days after the
> rebuild — ClearFake, confidence 50%, no evidence reference, "last seen: never".
>
> As of 2026-08-12: 4 of 91 vendors on VirusTotal flag the domain; Google Safe Browsing,
> Kaspersky, BitDefender, ESET, Sophos, Dr.Web, Emsisoft, G-Data, Forcepoint and Netcraft
> report it clean. Sucuri SiteCheck finds no malware. The homepage is byte-identical
> across four user agents and with a Google referer. All WordPress paths return 404.
>
> **Which indicator source produced this listing?** If it is inherited rather than your
> own observation, knowing the source lets me address it upstream instead of asking every
> downstream consumer separately.
>
> VirusTotal report: <пермалинк>
>
> <ВАШЕ ИМЯ>, <ДОЛЖНОСТЬ>, <you@splitcam.com>

---

## 6. Gridinsoft — подавать последним, скорее всего снимется само

Их оценка производна: в отчёте ровно два негативных сигнала — «предупреждения
поставщиков безопасности» и «обнаружения в нескольких блоклистах (4)». Снимутся
четыре — снимется и этот. Подавать только если через 2–3 недели после остальных
вердикт держится.

**Куда:** форма обратной связи на странице проверки домена в
`https://gridinsoft.com/online-virus-scanner/`

> Trust Score for splitcam.com is currently 35/100 with the note "Listed by Gridinsoft".
> The report cites two negative signals: security-provider warnings and blacklist
> detections. Those listings have since been withdrawn — please re-evaluate.
>
> Background: an earlier WordPress installation was compromised and is gone; since
> 2026-07-18 the site is static HTML/CSS/JS on a different server. As of <дата>,
> VirusTotal shows <N>/91 detections.
>
> <ВАШЕ ИМЯ>, <you@splitcam.com>

---

## После подачи

- Ничего не дублировать: у Fortinet повторная заявка ловит rate-limit, у Malwarebytes
  дубликат за 6 месяцев закрывают.
- Fortinet и AlphaSOC подтверждений не присылают вообще — тишина это норма, результат
  меряется по `https://www.fortiguard.com/webfilter` и по VirusTotal.
- Проверять раз в несколько дней и записывать даты сюда же, чтобы знать, когда пора
  напоминать (AlphaSOC — вежливый follow-up через 10–14 дней, MalwareURL — через неделю
  письмом).
- Когда VirusTotal покажет 0 детектов — снять задачу в `REMINDERS.md` и убрать
  соответствующий пункт отсюда.
