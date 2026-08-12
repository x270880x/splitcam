# splitcam.com — репутация домена и снятие блокировок

**Заведено 2026-08-12.** Повод: пользователь (Morgan Sands, `morgansands@verizon.net`)
написал 28.07 на `support@`, что Malwarebytes определяет сайт как троян. Письмо
пролежало две недели; 12.08 ответили с `support@splitcam.com`, копия в `.Sent`,
попросили точный адрес блокировки, имя детекта и скриншот. Ждём ответа.

Проверка показала, что дело не в одном антивирусе.

---

## 🔴 Срочное, к репутации отношения не имеет: MySQL открыт в интернет

Проверено лично, живым подключением с рабочего мака 12.08.2026: `77.83.100.153:3306`
отвечает рукопожатием **MariaDB 10.6.27**. Порт доступен из интернета кому угодно.

Полная картина открытых портов (тем же способом):

    21   Pure-FTPd    открыт, баннер отдаётся
    22   OpenSSH 8.0  открыт
    25   Exim         открыт
    110  Dovecot POP3 открыт
    143  Dovecot IMAP открыт
    2222 DirectAdmin  открыт
    3306 MariaDB      ОТКРЫТ  ← закрыть
    8887 / 8888       открыты, без баннера
    8889              открыт, отвечает "Your connection to this server has been blocked"

Сайт статический, база ему не нужна вообще. Действия: убедиться, что старая база
WordPress удалена (а не просто отключена), в DirectAdmin убрать все хосты удалённого
доступа к MySQL, и запросить у hostsila закрытие 3306 на файрволе — на shared-хостинге
это их сторона. Заодно OpenSSH 8.0 старый; парольную аутентификацию отключить в пользу
ключей (сейчас вход по паролю, ключей на машине нет).

---

## Что подтверждено мной лично

| Что | Как проверено |
|---|---|
| 4 вендора помечают домен: AlphaSOC, CRDF, Fortinet, MalwareURL + Gridinsoft «suspicious» | VirusTotal, веб-интерфейс, 12.08.2026. Остальные ~86 чисто, включая Google Safe Browsing, Kaspersky, BitDefender, ESET, Dr.Web, Emsisoft |
| Malwarebytes **не является** вендором VirusTotal | там же — его вердикт оттуда не виден в принципе |
| MySQL 3306 открыт наружу | прямое TCP-подключение, получено рукопожатие MariaDB |
| Боевой установщик: 490 226 688 байт (467,5 МБ), Last-Modified 29.06.2026 | `curl -I` |
| Требования Malwarebytes к заявке | прочитана их закреплённая тема (после того, как проверку Cloudflare прошёл пользователь) |

**Что проверить не смог:** AbuseIPDB (бот-защита Cloudflare), ThreatFox и URLhaus
(CAPTCHA + требуется auth-key), поиск по форуму Malwarebytes (требует входа).
Бот-защиту не обхожу, аккаунты не создаю — эти шаги за человеком.

---

# splitcam.com — план снятия блокировок

**Статус форензики: живого заражения не найдено.** Клоакинга нет (4 разных UA + Google-referer дают побайтово идентичный ответ, один SHA-256), инлайн-скрипты чистые, WordPress вычищен под ноль, Sucuri SiteCheck 12.08.2026 — чисто. Флаг стоит на **домене целиком**, а не на путях: CRDF и Fortinet одновременно помечают хост как Malicious/Malware, а `https://splitcam.com/win-download/SplitCamSetup_x64.msi` — как **Clean**. Так бывает только при доменной записи в блоклисте.

Но подавать заявки **прямо сейчас нельзя**. Сначала — блок 0.

---

## Блок 0. Сделать ДО подачи любой заявки (1–3 дня)

Каждый пункт — либо дыра в доказательной базе, либо то, что вернёт флаг обратно.

### 0.1. Проверить сайт через Cloudflare, а не с origin — **обязательно**
MalwareURL записал домен на IP `172.67.148.86` (Cloudflare, AS13335), а **не** на ваш origin `77.83.100.153`. Локальный ClamAV по файлам origin не исключает ни протухший объект в кэше Cloudflare, ни JS, отдаваемый условно.

- Открыть сайт с **реальной Windows-машины, Chrome, жилой IP**, 2–3 разных гео (минимум US + EU), с `Referer: https://www.google.com/`. Смотреть DevTools → Network на предмет фальшивых «обновлений браузера» / ClickFix-оверлеев.
- Cloudflare → Caching → **Purge Everything**. Затем перепроверить.
- Проверить Cloudflare Workers / Page Rules / injected scripts (Zaraz, Apps) — их ClamAV на origin не видит в принципе.
- Если что-то ClearFake-подобное всплывает — **стоп, заявки не подавать**, листинг корректен.

### 0.2. Закрыть вопрос по ThreatFox IOC 1861022 — самый высокий рычаг

> ⚠️ **Реквизиты этого IOC никем не подтверждены.** Страница
> `https://threatfox.abuse.ch/ioc/1861022/` закрыта интерактивной CAPTCHA, а
> `threatfox-api.abuse.ch` без auth-key отдаёт `{"error":"Unauthorized"}` —
> проверено дважды, 12.08.2026. Номер IOC, дата публикации и уровень confidence
> взяты из вторичных источников и **могут быть неверны**. Что подтверждено
> независимо: MalwareURL 12.08.2026 держит splitcam.com с категорией
> `Trojan JS ClearFake` — то есть связь листинга с ClearFake реальна.
> Первое действие: завести бесплатный аккаунт abuse.ch, получить ключ и
> посмотреть карточку IOC глазами.
Единственный датируемый след: IOC `splitcam.com`, malware=**ClearFake**, threat_type=payload_delivery, confidence=**50%**, опубликован ~28.07.2026 — то есть примерно на **10 дней позже** перестройки сайта (Wayback: статика встала 18.07.2026). ThreatFox бесплатен и потребляется десятками фидов — **это вероятный первоисточник вердиктов AlphaSOC, MalwareURL и, через них, Gridinsoft**. Снимать блокировки ниже по течению, пока жив upstream — значит получить их обратно на следующем обновлении фида.

- Зарегистрировать бесплатный аккаунт abuse.ch (Auth0) → получить `Auth-Key` → запросить `https://threatfox-api.abuse.ch/api/v1/` по IOC id 1861022 и вытащить **first_seen, reporter, reference**.
- Если `first_seen` ≥ 18.07.2026 или reference пустой — подать в ThreatFox запрос на удаление IOC как FP (через аккаунт / `#abusech` в их канале), приложив Wayback-хронологию.
- Если `first_seen` < 18.07.2026 — версия «остаточная репутация» подтверждена документально, это лучший аргумент во все шесть заявок.

### 0.3. Починить подписи инсталляторов
Все три свежих MSI на VirusTotal имеют тег `signed` **и** `invalid-signature` одновременно — подпись есть, но невалидна (истёкший сертификат / сломанная контрасигнатура / битая цепочка). Для репутационных движков это прямой множитель риска и вероятная часть причины, почему вас держат в списках, независимо от взлома.

- Перевыпустить/перепроверить сертификат, пересобрать и подписать **с RFC-3161 timestamp**.
- Проверить: `signtool verify /pa /v /all SplitCamSetup_x64.msi` — должно быть без ошибок.
- Только после этого писать в заявках «installers are code-signed».

### 0.4. Загрузить на VT текущую живую сборку
Живой x64 весит **490 226 688 байт** (Last-Modified 29.06.2026), и **ни один образец на VT такого размера не найден** — самый свежий сэмпл (327,26 МБ, 29.07.2026) это другая сборка. Пока это так, «наш инсталлятор 0/92» — утверждение про чужой файл.

- Скачать оба текущих MSI с собственного сервера, посчитать SHA-256, залить на virustotal.com, сохранить пермалинки. Их и вставлять в заявки.
- Единственный ожидаемый детект — VBA32 `BScope.Trojan.Inject` (одна эвристика одного второстепенного вендора на больших MSI, классический FP). Отдельно в VBA32 писать не нужно, на доменную репутацию не влияет.

### 0.5. Закрыть поверхность на сервере (иначе повторный взлом обнулит всё)
`77.83.100.153` — **shared-хостинг** (соседи: `vabi.pl`, `mail.angar.org.ua`, реверс `pl-rocket-da3.hostsila.org`). Сам IP нигде не листится (VT 0/91, Spamhaus ZEN / Barracuda / SpamCop / SORBS — чисто), причиной флагов он быть не может. Но наружу открыты 21, 22, 25, 80, 110, 143, 443, 465, 587, 995, 2222, 3306, 8887, 8888, 8889.

- **3306 (MariaDB 10.6.27) торчит в интернет** — закрыть файрволом, bind на 127.0.0.1.
- OpenSSH 8.0 — обновить (Shodan сопоставляет 26 CVE, включая CVE-2023-38408, CVE-2023-48795, CVE-2025-26465). Отключить парольную аутентификацию.
- Закрыть/ограничить 2222, 8887–8889, 21 (Pure-FTPd).

### 0.6. Проверить критерии CRDF до подачи (не только «мы вычистили взлом»)
`https://threatcenter.crdf.fr/criteria.html` перечисляет **не-малварные** основания для листинга: бандлинг adware/PUP, распространение через сторонних аффилиатов, установка без явного согласия, отсутствие внятного EULA или доступной privacy policy. Если листинг стоит по этой линии, рассказ про WordPress его не сдвинет.

- Убедиться, что инсталляторы не несут сторонних офферов, а EULA и Privacy Policy заметно слинкованы со страницы загрузки.
- Отдельно: в графе VT к домену привязан **`ICReinstall_file.exe`** (SHA-256 `25e8da91…3726c`, 36/70, 1,14 МБ, 2022 г., InstallCore adware). Это **не ваш** файл — сторонний загрузчик-обёртка с download-портала, который тянет SplitCam с вашего домена. Многолетний независимый источник порчи репутации. Действия: разослать порталам-нарушителям требование убрать обёртку, на странице загрузки явно указать «official build only from splitcam.com», и **упомянуть этот файл в заявках** как чужой — иначе аналитик найдёт его сам и решит иначе.

---

## Общая заготовка текста (EN) — вставлять во все формы

> Subject: False positive / re-review request: splitcam.com
>
> I am the owner of splitcam.com (SplitCam — free streaming and virtual-camera software; domain registered 2005).
>
> The previous WordPress installation of this site was compromised. It has been completely removed. Since 2026-07-18 the site is static HTML/CSS/JS with no CMS and no plugins (a single PHP file in the document root), on a different server: origin IP 77.83.100.153. Public traffic is served through Cloudflare (currently 104.21.39.190 / 172.67.148.86).
>
> Remediation evidence:
> - ClamAV 1.5.2, July 2026: 529 pages and 24 Windows installers scanned — zero detections.
> - All WordPress paths (wp-login.php, xmlrpc.php, wp-admin/, wp-content/, wp-includes/, wp-json/, readme.html) now return 404.
> - Sucuri SiteCheck, 2026-08-12: no malware found, no blacklisting, security 6/6.
> - VirusTotal, 2026-08-12: Google Safe Browsing, Kaspersky, BitDefender, ESET, Sophos, Dr.Web, Emsisoft, G-Data, Forcepoint and Netcraft all report the domain clean. The installer URL https://splitcam.com/win-download/SplitCamSetup_x64.msi is 0/92.
> - Installers are code-signed; current VirusTotal reports: <ссылки из п. 0.4>.
>
> Note: a file named ICReinstall_file.exe (SHA-256 25e8da914f31f72777198acc739bce98039e037442d2df5317fe6a3e26e3726c) is associated with our domain in third-party graphs. It is NOT our software — it is a third-party InstallCore download wrapper redistributed by download portals. Our official builds are served only from splitcam.com.
>
> Request: please re-scan splitcam.com and remove the current classification. If your verdict originates from a third-party feed, please tell me which source, so that I can address it there as well.
>
> Contact: <имя>, <должность>, <you@splitcam.com>, <телефон>

**Почту указывать только на домене splitcam.com** — она же служит доказательством владения. Gmail/одноразовые адреса — прямая причина молчаливого отклонения у CRDF, AlphaSOC и Fortinet.

---

## Вендоры — по убыванию отдачи

Все шесть заявок подаются **человеком в обычном браузере**. Ни одну нельзя подать скриптом: везде либо CAPTCHA/ALTCHA/Turnstile/reCAPTCHA, либо React-форма без HTML-fallback, либо требуется аккаунт. У CRDF автоматизированная подача прямо указана в ToS как основание для отказа.

### 1. Fortinet (FortiGuard Web Filter) — максимальный охват

FortiGate стоит в корпоративных периметрах; это блокировка, которая реально режет трафик и продажи.

| | |
|---|---|
| URL | `https://www.fortiguard.com/faq/wfratingsubmit` |
| Аккаунт | не нужен |
| Кто подаёт | **лично, вручную** (ALTCHA proof-of-work) |
| Срок | «within 24 hours» по их же странице; на практике до нескольких дней + кэш на устройствах |
| Проверка результата | `https://www.fortiguard.com/webfilter` (только POST со страницы; прямые GET-ссылки отдают 403) |

**Что вставить:** URL = `splitcam.com`. **Suggest a category = `Freeware and Software Downloads`** (запасные: `Information Technology`, `Streaming Media and Download`). Name / Email / Company — заполнить полностью. Comment — общая заготовка. **Отметить чекбокс `contact_me`** — иначе ответа не будет вообще.

**Что убивает заявку:** заявка без выбранной конкретной категории («просто снимите Malicious»); пустые/мусорные Name/Email/Company; одноразовая почта; скриншот >2 МБ. Форма **не выдаёт номер тикета и не присылает подтверждение** — тишина это норма, повторно не дублировать (rate-limit). Если флагаются ещё и конкретные глубокие URL (`www`, страницы загрузки) — подавать их **отдельными заявками**. Детекты Fortinet по файлам — другая подсистема (`submitvirus`), эта форма их не закрывает.

---

### 2. Malwarebytes — единственная подтверждённая реальная блокировка у пользователя

Быстрее всех и с прямым эффектом на конечных пользователей.

| | |
|---|---|
| URL | `https://forums.malwarebytes.com/forum/123-website-blocking/?do=add` |
| Аккаунт | **нужен**, бесплатный: `https://forums.malwarebytes.com/register/` (reCAPTCHA + CleanTalk + подтверждение почты) |
| Кто подаёт | **только лично** — гость не может ни писать, ни искать по форуму |
| Срок | часы — 48 ч. Staff отвечает реально и быстро |
| Проверка результата | публичного сервиса **нет** — только поставить Browser Guard и открыть сайт |

**Порядок:**
1. Зарегистрироваться, подтвердить почту.
2. Перед публикацией — поиск по форуму **отдельно по домену и отдельно по IP**, фильтр «This Forum» + «past 6 months». Дубликат закроют. (На 12.08.2026 тем про splitcam.com не найдено.)
3. Проверить `77.83.100.153` на `abuseipdb.com` и приложить результат.
4. Заголовок: `False positive website block: splitcam.com`.
5. **Домен и URL — только внутри Code Block** (`<>` на панели редактора). Кликабельная ссылка = нарушение закреплённых правил.
6. Обязательно указать: домен **и** IP `77.83.100.153` **и** Cloudflare-адреса; тип блокировки с экрана (Trojan/Malware/…); модуль и версию (Browser Guard v3.3.2 или Web Protection в Malwarebytes v5); Detection ID / версию базы со страницы блокировки.
7. **Приложить скриншот экрана блокировки** и/или экспорт «Malwarebytes Website Blocked Report ….txt». Без него тема встаёт намертво.
8. Явно попросить не только снять блок, но и **добавить домен в whitelist** — зафиксирован случай, когда разблокированный домен «slipped through the feed to be re-blocked».

**Что убивает заявку:** нет скриншота; кликабельная ссылка; дубликат за 6 месяцев; пост в форум 252 (Browser Guard) вместо 123 (Website Blocking); попытка идти через AI-чат поддержки (он выдаёт ссылку на несуществующую страницу «False Positive Submission»); support.threatdown.com (это B2B). Кнопка «Continue to this website» — обход для себя, на решение staff не влияет. Форум **публичный и индексируется** — историю компрометации скрывать не надо (staff видит причину блока), но формулировать аккуратно. Если флагаются и сами инсталляторы — это **отдельный** репорт в `https://forums.malwarebytes.com/forum/42-file-detections/` с файлом в zip.

---

### 3. CRDF Threat Center — фид, который потребляют другие

| | |
|---|---|
| URL | `https://threatcenter.crdf.fr/false_positive.html` |
| Аккаунт | не нужен |
| Кто подаёт | **лично** (собственная бот-проверка `crdfcaptcha`; ToS §9 прямо называет «automated» основанием для отказа) |
| Срок | ответ ~24 ч, решение до 5 рабочих дней (в FAQ гарантии сняты) |
| Проверка результата | `https://threatcenter.crdf.fr/check.html` — 10 секунд вручную. Проверить **отдельно** apex, `www`, и `http://77.83.100.153` |

**Что вставить:** `domainName` = `https://splitcam.com` — **со схемой**, голое `splitcam.com` не пройдёт валидацию `type=url`. Через чекбокс `multiple_urls` можно добавить `https://www.splitcam.com` (максимум 5 URL за раз). Отметить `tos_ag` и `not_robot`.

**Поле `motivations` — жёсткий лимит 1000 символов.** Сжатая версия:

> Owner of splitcam.com (SplitCam, free streaming/virtual-camera software, domain since 2005). The old WordPress site was compromised and has been fully removed. Since 2026-07-18 the site is static HTML/CSS/JS, no CMS, no plugins, one PHP file, new server (origin 77.83.100.153, Cloudflare-fronted). Evidence: ClamAV 1.5.2 (July 2026) over 529 pages + 24 installers = 0 detections; all wp-* paths return 404; Sucuri SiteCheck 2026-08-12 clean, 6/6; Google Safe Browsing, Kaspersky, BitDefender, ESET, Sophos, Dr.Web, Emsisoft clean. Installers are code-signed and carry no bundled offers; EULA and privacy policy are linked from the download page. Please re-scan and remove the classification.

**Что убивает заявку:** любой канал кроме портала («any other request will be ignored» — `contact.html` не использовать); **повторная заявка при открытой** («another request for this domain is already being processed») — дополнять надо внутри защищённого треда, а не новой формой; одноразовая почта; отсутствие схемы в URL; вопрос «а что именно у вас сработало» — запросы «designed to reveal detection methods» отклоняются, CRDF никогда не объясняет причину. Решение действует **только на точное поданное значение** — apex не чистит `www`, поддомены, пути и IP. Отставание VirusTotal после очистки — ожидаемо и **не повод** открывать второй тикет. Сохранить письмо с reference и ссылкой на тред; тред не публиковать.

---

### 4. MalwareURL — активный листинг с конкретной категорией

Подтверждено 12.08.2026: **«This web site is a known security risk», Security Category: `Trojan JS ClearFake`**, IP `172.67.148.86`, AS13335. Контроль (`example.com` → «not currently listed») показывает, что это реальный хит базы, а не дефолт. Дат first/last seen они не публикуют. B2B-фид, который перепродаётся другим вендорам — снятие имеет каскадный эффект, но процесса для владельцев сайтов у них нет.

| | |
|---|---|
| URL | `https://www.malwareurl.com/contact-us.php` (выделенной FP-формы **не существует**) |
| Дублировать письмом | `team@malwareurl.com` |
| Аккаунт | не нужен (портал `/login.php` — только для платных клиентов) |
| Кто подаёт | **лично** (Cloudflare Turnstile) |
| Срок | не публикуется. Если через ~неделю тишина — писать на почту |
| Проверка результата | `https://www.malwareurl.com/listing-urls.php` (детальная страница открывается только переходом из результата в той же сессии) |

**Что вставить** (поля: name, email, phone — опционально, info; минимум 25 символов; домена/категории отдельных полей нет — всё в текст): общая заготовка **плюс обязательно**:
- явное упоминание их категории: *«Your database currently lists splitcam.com as `Trojan JS ClearFake`. The ClearFake injection was present on the previous compromised WordPress installation, which has been entirely replaced»*;
- **оба адреса**: Cloudflare `172.67.148.86` / `104.21.39.190` (то, что сканируете вы) и origin `77.83.100.153`;
- указание, что кэш Cloudflare продут <дата> и сайт перепроверен через CDN.

**Что убивает заявку:** **ни в коем случае не `https://www.malwareurl.com/submit.php`** — эта форма **добавляет** URL в блоклист, и ссылка на неё («please submit it for rating») подсовывается прямо из результата проверки. Сообщение <25 символов блокируется валидацией. Скриптовый POST без токена Turnstile → «Wrong captcha», тихо в мусор. Указать только origin → пересканируют не то. Подавать, пока хоть один ClearFake-артефакт достижим через кэш CDN → отказ и ужесточение листинга.

---

### 5. AlphaSOC — низкий пользовательский эффект, но нужен для счётчика VT

B2B-телеметрия, не потребительский AV; конечных пользователей почти не блокирует, но держит один из 4 голосов на VirusTotal.

| | |
|---|---|
| URL | `https://alphasoc.com/contact/` |
| Параллельно и предпочтительно | письмо на **`virustotal@alphasoc.com`** — этот адрес указан на официальной странице FP-контактов VirusTotal |
| Аккаунт | не нужен |
| Кто подаёт | **лично** — форма на Next.js/React, без `action`/`method`, без HTML-fallback: curl и headless «отправляют» в никуда |
| Срок | не публикуется, SLA нет. Планировать вежливый follow-up через 10–14 дней |
| Проверка результата | только VirusTotal — публичного lookup у AlphaSOC нет вообще |

**Что вставить:** Full name / Work email (**@splitcam.com**) / Company. **Дропдаун «How can we help?» переключить с дефолтного `Sales / general enquiry` на `Threat indicator review`** — иначе заявка уедет в отдел продаж и умрёт. Message — общая заготовка + пермалинк на VT-отчёт домена + прямой вопрос: *«Which indicator source produced this listing?»* (в письме на `virustotal@alphasoc.com` — то же самое; VT требует прикладывать пермалинк).

**Что убивает заявку:** дефолтный дропдаун; отправка с gmail и пустой Company (читается как lead-gen бот); `support@alphasoc.com` (это техподдержка клиентов, не тот queue); голое «уберите нас, мы чистые» без доказательств. Подтверждения не будет — тикета, статуса и письма не предусмотрено; успех меряется по VT, а не по ответу. **Кнопка «Reanalyze» на VirusTotal бесполезна** — она переспрашивает вендоров по их же текущим данным. Главный риск: если вердикт унаследован из чужого фида (вероятно — ThreatFox, см. 0.2), снятие у AlphaSOC не удержится; поэтому вопрос про источник — не вежливость, а рабочая необходимость.

---

### 6. Gridinsoft — делать **последним**, скорее всего снимется само

Вердикт 12.08.2026: «Suspicious Website», Trust Score 35/100, «Listed by Gridinsoft». Но негативных сигналов в отчёте ровно два: «security-provider warnings» и «multiple blacklist detections (4)» — то есть их оценка **производна от тех же четырёх блоклистов**. Три независимых контентных сканера в их же панели (Sucuri, Quttera, URLhaus) — Clean. Скор пересчитывается автоматически, поэтому заявка, поданная раньше остальных, будет отменена следующим пересчётом.

| | |
|---|---|
| URL | `https://portal.gridinsoft.com/false-positive` |
| Резерв | `legal@gridinsoft.com` (только если портал недоступен) |
| Аккаунт | не нужен (но `portal.gridinsoft.com/register` позволяет «claim» профиль домена — рекомендуется при оспаривании скора) |
| Кто подаёт | **лично** (невидимая reCAPTCHA v3, score-based) |
| Срок | нигде не документирован |
| Проверка результата | `https://gridinsoft.com/website-reputation-checker`, пермалинк `https://gridinsoft.com/online-virus-scanner/url/splitcam-com` |

**Что вставить:** `reporter_role` = «I represent this domain»; имя/фамилия; email; domain = `splitcam.com`; message (мин. 20 симв.) — общая заготовка + список уже поданных заявок к Fortinet/CRDF/MalwareURL/AlphaSOC с датами.

**Что убивает заявку:** **двойное подтверждение по почте** — после отправки тикет ещё НЕ создан, надо кликнуть ссылку из письма («Until then, our team cannot review or reply to it»). Письмо часто в спаме; на странице есть кнопка повторной отправки. Второй убийца — **не тот канал**: доменные кейсы нельзя вести через `support.gridinsoft.com/portal/en/newticket`, дубликат закроют. Ссылки `gridinsoft.com/incorrect-detection` и `anti-malware.gridinsoft.com/false-detect/`, которые до сих пор гуляют по статьям про блоклисты, — **мёртвые редиректы на документацию**, форм там нет. reCAPTCHA v3 без взаимодействия: подавать из обычного десктопного браузера с JS, без VPN/Tor и агрессивных блокировщиков — иначе низкий score и тихий отказ. Из URL вычистить пароли, токены и session id. **Платить нельзя никому**: «We never charge website owners for reviews or reconsideration requests».

**Отдельно эскалирую:** в их отчёте есть строка о «license-restricted partner security signal», чьё имя и вердикт не раскрываются публично. Это скрытый негативный вход, который нельзя ни увидеть, ни адресовать напрямую — и **правдоподобное место, где живёт тот самый вердикт Malwarebytes**. В заявке стоит спросить прямо, что это за сигнал.

---

## Порядок и сроки

| День | Действие |
|---|---|
| 0–1 | Блок 0: проверка через Cloudflare с жилого Windows-IP, purge cache, закрыть 3306, обновить OpenSSH |
| 1–2 | Получить Auth-Key abuse.ch, вытащить `first_seen` IOC 1861022, при необходимости подать FP в ThreatFox |
| 1–3 | Перевыпустить подпись инсталляторов, залить текущие сборки на VT, сохранить пермалинки |
| 3 | Подать: **Fortinet**, **Malwarebytes** (после регистрации), **CRDF** |
| 3–4 | Подать: **MalwareURL** (форма + письмо), **AlphaSOC** (форма + `virustotal@alphasoc.com`) |
| 5–7 | Дождаться первых снятий → подать **Gridinsoft** |
| +7 | Проверить: FortiGuard webfilter, CRDF check.html, MalwareURL listing-urls.php, Gridinsoft checker, VT-отчёт домена |
| +14 | Follow-up: AlphaSOC (письмо), MalwareURL (`team@malwareurl.com`). CRDF — **только внутри существующего треда**, новую форму не подавать |

Вести таблицу: вендор / дата подачи / канал / reference (если есть) / дата ответа / текущий вердикт.

---

## Что проверить не удалось и чем это закрывается

| Не проверено | Почему | Что закроет вопрос |
|---|---|---|
| **`first_seen` ThreatFox IOC 1861022** — до или после перестройки 18.07.2026 | страница за интерактивной CAPTCHA; API без `Auth-Key` → `{"error":"Unauthorized"}` | Бесплатный аккаунт abuse.ch → API-ключ. **Самый значимый пробел: это единственная слабая точка версии «остаточная репутация»** |
| История листингов URLhaus по домену и по IP | тот же `Unauthorized` без ключа | тот же ключ abuse.ch |
| Полный список «detected URLs» под доменом в VT | нет API-ключа VT; `/ui/` требует reCAPTCHA. Проверены только корень, оба инсталлятора, поддомены, passive DNS | ключ VT API v3 (даже бесплатный) |
| Соответствие живой x64-сборки (490 226 688 байт) хоть какому-то образцу на VT | инсталляторы не скачивались; ни одного сэмпла такого размера на VT нет | п. 0.4 — залить файл самому |
| 32-битный файл сопоставлен с образцом `splitcam-4496.msi` (0/48) **по точному совпадению размера в байтах**, а не по хешу | файл не скачивался | посчитать SHA-256 живого файла локально |
| Вердикт Malwarebytes | они не участвуют в доменной репутации VT, публичного lookup нет, тем на форуме про splitcam.com нет | поставить Browser Guard, открыть сайт, снять скриншот (он же нужен для заявки) |
| Текущий вердикт Fortinet напрямую | форма lookup только POST + ALTCHA; старые GET-ссылки → 403 | вручную на `https://www.fortiguard.com/webfilter` |
| Текущий вердикт CRDF напрямую | `check.html` за их бот-проверкой; API-скоуп `lookup` только для платных | вручную, 10 секунд |
| Причина вердикта Gridinsoft и скрытый «partner signal» | страница отдала 403 / имя провайдера не раскрывается по лицензии | спросить в заявке напрямую |
| **Клоакинг по гео/ASN/referer** | сайт смотрелся из песочницы через egress-прокси, а не как реальный Windows-браузер с жилого IP. 4 UA + Google-referer — хорошая, но не исчерпывающая проверка. ClearFake исторически применял именно такой клоакинг | п. 0.1: жилые IP, 2–3 гео, реальный Chrome. Плюс логи Cloudflare за июль на аномальные ответы |
| Состав ресурсов в сохранённых сканах urlscan.io (28.07, 29.07, 01.08) | result API теперь требует логина; доступны только метаданные (200, Cloudflare, 19–32 запроса) | бесплатный аккаунт urlscan.io |
| Опирается ли листинг CRDF на бандлинг/аффилиатов/EULA, а не на взлом | их критерии этого не раскрывают, и CRDF принципиально не объясняет причину | п. 0.6 — привести инсталляторы и юр. страницы в соответствие **до** подачи |

**Главное, что нельзя замалчивать перед вендорами:** IOC про ClearFake опубликован ~28.07.2026, примерно через 10 дней после перестройки. Это не доказательство живого заражения (ThreatFox часто вносит записи ретроспективно, confidence=50% указывает на автоматическую заявку низкой достоверности), но и опровергнуть это без `first_seen` невозможно. Если п. 0.2 покажет, что IOC описывает послемиграционную активность — **вся кампания по снятию блокировок останавливается**, и сначала ищется, что именно отдаётся и кому.