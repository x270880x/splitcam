# ВЕРСТКА-pages.md — аудит остальных страниц сайта

Дополнение к [ВЕРСТКА.md](ВЕРСТКА.md) (главная). Это компактный аудит 10
страниц с навигацией — не пообъектный 15-блочный пробег как у главной, а
выжимка по каждой странице + сквозные паттерны в конце.

Скоп: `/products/`, `/multistreaming/`, `/virtual-camera/`,
`/alternatives/`, `/alternatives/obs/`, `/for/`, `/for/youtubers/`,
`/for/churches/`, `/changelog/`, `/help/`. Legal boilerplate
(`/privacy-policy/`, `/license-agreement/`) пропущен.

Методика: статический анализ HTML/CSS + замеры через headless Chrome.
Дата снимка: 2026-06-01.

---

## Раздел 1. Аудит по страницам

### 1.1 `/products/` — продуктовый хаб

[products/index.html](../products/index.html) · 538 строк · 37KB

**Что:** Хаб всех продуктов SplitCam — десктопные сборки (Win/Mac),
мобильные (iOS/Android), Remote-приложение. Карточки + companion-блок
для Remote + 3-шаговая инструкция «Pair in three steps».

**Структура:** Hero (центр-выравнивание) → «Stream from any device»
(product-grid 2×2: Win/Mac/iOS/Android) → «SplitCam Remote — your stream
in your hand» (remote-feature с phone-mock) → «How it works» (3 шага) →
CTA.

**Schema.org:** BreadcrumbList + ItemList + 4× SoftwareApplication +
MobileApplication. ❌ Нет AggregateRating, нет FAQPage. По CLAUDE.md
рекомендуется добавить хотя бы AggregateRating (4.5/357 для бренда) на
самой важной продуктовой странице.

**H1:** «One SplitCam family — on every screen you own.» — сильный.

**Находки:**

1. **🔥 4 продуктовых карточки `.product` — все `<div>`, не `<a>`.**
   `.product:hover { border-color: ...; transform: translateY(-2px) }` —
   обещают клик, не дают. Можно либо сделать ссылками (на download URL
   платформы / на /changelog/), либо убрать transform.
2. **«Pair in three steps» (`.connect-step`) — 3 шага в карточках с
   `:hover`** — тоже не кликабельны. Меньшая боль чем product cards.
3. **Контейнерные ширины:** 1100 / 900 / 820 / 680 (4 разных). У хаба
   нет такой острой надобности в нескольких уровнях, можно
   унифицировать.
4. **Footer-inner у этой страницы простой** (одна строка с linklist),
   тогда как на главной — 4-колоночный с Support блоком. Несогласовано
   через сайт. Лучше синхронизировать.
5. **Версия в карточке macOS** — `v1.19` бейдж. Хорошо. Windows
   карточка показывает `v10.9.2`. Согласовано.
6. **iOS / Android карточки имеют `tag-beta` бейджи** + «In development»
   фичи в product-features (см. CLAUDE.md «Iso card honesty»). Хорошо.
7. **macOS «In development» фичи** — стоит проверить, есть ли явные
   `in development` бейджи или только текстовое описание (без проверки
   не утверждаю).

---

### 1.2 `/multistreaming/` — основная feature-страница

[multistreaming/index.html](../multistreaming/index.html) · 886 строк · 65KB

**Что:** Глубокий лендинг про мультистриминг. Hero с анимированной
диаграммой потоков, категоризированный список платформ, описание «How
it works», 9 платформенных «combos» (Twitch + YouTube etc), фичи,
шаги, FAQ.

**Структура (8 секций):** Hero → Platforms by category (Streaming /
Social / Pro) → How it works (диаграмма) → Combo-cards (9 пар
платформ) → Use cases → Features grid → 4-step setup → FAQ → CTA →
Footer.

**Schema.org:** BreadcrumbList + SoftwareApplication + AggregateRating
+ HowTo (5 шагов) + FAQPage. Полный набор — отличная SEO-разметка.

**H1:** «One stream. Every platform. All at once.» — энергичный,
ритмичный, в духе главной.

**Находки:**

1. **🔥 12 неклкабельных карточек с hover:** 6×`.feat-card` (фичи) +
   6×`.uc-card` (use cases). Тот же паттерн что на главной — hover
   transform на не-ссылках.
2. **`.combo-card` × 9 — кликабельны (anchors).** Куда они ведут? Если
   на главную с якорем — норм. Если на стабы — проверить.
3. **6 разных контейнерных ширин: 1100 / 900 / 780 / 760 / 640 / 620.**
   Самый рваный «лестничный» набор из всех 10 страниц. 760 vs 780 —
   практически одно и то же, можно склеить.
4. **6 эмодзи в body:** 🌐 🎮 🎓 🎤 🛍 📸 — видимо в use cases. На
   главной такой же выбор — согласовано.
5. **«How it works» диаграмма с анимированными pulse-полосками** —
   красивый блок, согласован визуально с `bc-rows` на главной.
6. **84+ платформ** — упоминание согласовано с главной (там 84+ тоже).
7. **Возможный дубль с главной:** на главной есть #multi-streaming
   секция, а эта страница — её углублённая версия. CTA с главной ведёт
   сюда. Хорошая иерархия. Но проверить, чтобы copy не повторял главную
   слово-в-слово.

---

### 1.3 `/virtual-camera/` — основная feature-страница

[virtual-camera/index.html](../virtual-camera/index.html) · 771 строка · 61KB

**Что:** Лендинг про виртуальную камеру. Hero с превью «slide PiP»
(аналитика бизнес-метрик в углу), grid из 12 приложений (Zoom/Teams/
Meet/Discord/Telegram/WhatsApp/OBS/etc), использование в OBS-сценарии,
features, шаги, FAQ.

**Структура:** Hero → 12-app grid (`.app-card`) → «How SplitCam works
as a virtual webcam» → Use cases (`.uc-card`) → Features (`.feat-card`)
→ Setup steps → FAQ → CTA → Footer.

**Schema.org:** Полный набор как у multistreaming — HowTo + FAQPage +
AggregateRating. ✅

**H1:** «One stream, every meeting app.» — параллель с «One stream.
Every platform. All at once.» на multistreaming. Хорошая
семья-страниц.

**Находки:**

1. **🔥 24 неклкабельных карточек с hover:** 12×`.app-card` + 6×
   `.feat-card` + 6×`.uc-card`. Самая «плотная» страница по
   обещаниям-без-клика. App-card особенно подозрительный — это
   логотипы приложений, пользователи могут ожидать что клик откроет
   `splitcam in Zoom` гайд.
2. **6 разных контейнерных ширин: 1100 / 900 / 780 / 760 / 640 / 620.**
   Идентично multistreaming.
3. **5 эмодзи: 💼 🎮 🎓 📺 📞** — в use cases. На multistreaming
   были 🌐🎮🎓🎤🛍📸. **6 vs 5 эмодзи разные** между двумя
   feature-страницами, хотя use cases похожи. Несогласованность.
4. **Slide PiP в hero** (Q1-Q4 revenue / +47% users / 67% goal / MRR
   $1.24M) — крутая визуализация, согласована с тем что я видел в
   #virtual-cam секции главной. Та же сцена.
5. **«60+ apps» vs точные 12 + «+ 53 more»** — то же расхождение
   (60+ + 12 = 72+ или 60+ всего?) что на главной. На этой странице
   list более полный (12 не 7), но math всё ещё ambivalent.

---

### 1.4 `/alternatives/` — мини-хаб сравнения

[alternatives/index.html](../alternatives/index.html) · 322 строки · 17KB

**Что:** Маленький хаб со списком сравнений: `vs OBS` (готово), `vs
Streamlabs` / `vs Restream` / `vs StreamYard` / `vs vMix` / `vs
ManyCam` (стабы с «In development» бейджем).

**Структура (3 секции):** Hero → Hub-grid (1 ссылка + 4 стаба) → CTA
→ Footer.

**Schema.org:** только BreadcrumbList + ItemList. ❌ Нет
SoftwareApplication. Минимально, но для хаб-страницы приемлемо.

**H1:** «How SplitCam compares — free, with the extras built in.» —
честно: «extras built in» — намёк на multistreaming/VC прямо в SplitCam.

**Находки:**

1. **5 из 6 hub-карточек — `<div class="hub-card soon">` (бейдж In
   development).** Только `vs OBS` живой. По CLAUDE.md SEO Wave 2/3
   должны добавить остальные.
2. **Hub-card hover есть** (`.a.hub-card:hover` через cascade), но 5
   div'ов наследуют ту же стилистику. Проверить — может на soon-картах
   hover отключён (как на главной с use-case soon).
3. **Контейнерные ширины:** 1100 / 900 / 820 / 680. Стандартный набор.
4. **Honest framing «In development»** — отличное решение vs
   маскированные ссылки. Совпадает с use-cases на главной.
5. **Hub-page компактна** (3 секции) — не пытается быть feature-pages.
   Правильно.

---

### 1.5 `/alternatives/obs/` — SEO landing

[alternatives/obs/index.html](../alternatives/obs/index.html) · 672 строки · 46KB

**Что:** SEO-страница «free OBS alternative». Гайд по миграции с OBS,
сравнительная таблица, FAQ, related links.

**Структура (9 секций):** NAV/BREADCRUMBS/HERO/QUICK ANSWER/STEP-BY-STEP/
BONUS/PRO TIPS/COMPARISON/FAQ/RELATED/CTA/FOOTER — полный SEO-template
из CLAUDE.md.

**Schema.org:** BreadcrumbList + SoftwareApplication + AggregateRating
+ ItemList + FAQPage. ❌ Нет HowTo (хотя есть step-by-step миграция).
Можно добавить HowTo schema для гайда — рост rich-snippet шансов.

**H1:** «The free SplitCam alternative to OBS Studio — easier, with
multistream built-in.» — длинно, но SEO-оптимизировано.

**Находки:**

1. **Контейнерные ширины: 900 / 780 / 720 / 680.** SEO-страницы стоят
   на 900px (от template). Согласовано с /for/youtubers и /for/churches.
2. **5 эмодзи: 📡 🪄 🎥 📱 🔄** — в pro-tips или related-cards.
3. **3 related-card — anchors ✓.** Hover на них корректный.
4. **9 секций** — самая длинная SEO-страница, но укладывается в
   стандартный template. Не раздутая.
5. **Strong vs OBS framing** — «easier» / «multistream built-in» —
   правильные топ-боли пользователей OBS.
6. **FAQ с конкретикой** про migration: OBS scenes import, hotkey
   parity и т.д.

---

### 1.6 `/for/` — мини-хаб use cases

[for/index.html](../for/index.html) · 322 строки · 17KB

**Что:** Хаб гайдов по use cases. Те же 6 use cases что на главной +
дополнительные «In development» стабы.

**Структура (3 секции):** Hero → Hub-grid → CTA → Footer.

**Schema.org:** BreadcrumbList + ItemList. ❌ Минимально.

**H1:** «Set up SplitCam for the way you go live.» — естественная.

**Находки:**

1. **2 hub-card живые** (youtubers, churches) + 4 soon. Тот же паттерн
   что на /alternatives/.
2. **4 эмодзи в body: 📹 🎮 🎓 🎬** — НЕсогласовано с главной (там
   🎮📹🎓⛪✨🎵) и с обоими feature pages.
3. **Контейнерные ширины:** 1100 / 900 / 820 / 680. Стандартно.
4. **Очень короткая страница (322 строки)** — голый хаб, не пытается
   повторить функционал главной. Правильно.

---

### 1.7 `/for/youtubers/` — SEO landing

[for/youtubers/index.html](../for/youtubers/index.html) · 569 строк · 40KB

**Что:** Step-by-step гайд «How to live stream on YouTube» — SEO-таргет
на «how to live stream on youtube» (2700 vol). Эталон SEO-template из
CLAUDE.md.

**Структура:** NAV/BREADCRUMBS/HERO/QUICK ANSWER/STEP-BY-STEP/BONUS/
PRO TIPS/COMPARISON/FAQ/RELATED/CTA/FOOTER — каноничный набор.

**Schema.org:** BreadcrumbList + HowTo + 4× HowToStep + HowToTool +
HowToSupply + SoftwareApplication + AggregateRating + FAQPage.
✅ Максимально нагружено — идеально для SEO.

**H1:** «How to live stream on YouTube — free software, 5-minute setup.»

**Находки:**

1. **5 шагов с timing** (~1 min, ~2 min etc) — повторяет паттерн Quick
   Start главной. Хорошо.
2. **6 эмодзи: 🎙 📡 🔁 💡 📊 🎬** — в pro-tips блоке. Согласован
   с alternatives/obs pro-tips (🪄🎥📱🔄📡 — пересечение через 📡).
3. **3 related-card** — кликабельны ✓.
4. **Контейнерные ширины:** 900 / 780 / 720 / 680. SEO-template
   стандарт.
5. **FAQPage — 7 questions** — solid coverage of YouTube live
   questions.
6. **«SplitCam vs OBS Studio for YouTube»** comparison block — полезно
   для converged search intent.

---

### 1.8 `/for/churches/` — SEO landing

[for/churches/index.html](../for/churches/index.html) · 620 строк · 46KB

**Что:** Аналог /for/youtubers/ но для церквей. SEO-таргет «church
streaming software».

**Структура:** То же SEO-template из CLAUDE.md. 8 секций.

**Schema.org:** Полный набор как у /for/youtubers/. ✅

**H1:** «Free church streaming software — broadcast Sunday service to
every platform.»

**Находки:**

1. **5 эмодзи: 🎤 📺 🎬 📊 📝** — в pro-tips. Иной набор от
   /for/youtubers/.
2. **Контейнерные ширины:** идентично /for/youtubers/.
3. **«vs vMix / vs ProPresenter / vs Resi»** в comparison block —
   правильные конкуренты для церковной аудитории.
4. **«FAQPage» с честными ценами конкурентов** ($60, $1200, $499+,
   $99–$249/mo) — отличная конкретика для SEO.
5. **«Free vMix alternative for church»** в keywords — long-tail
   попадание.
6. **На 50 строк длиннее /for/youtubers/** — за счёт более длинных
   FAQ ответов про hardware и multi-camera. Норма для церковной
   аудитории.

---

### 1.9 `/changelog/` — version history

[changelog/index.html](../changelog/index.html) · 4203 строки · 274KB

**Что:** Полная история версий SplitCam. Табы Windows / macOS / iOS /
Android / Remote. ~50+ Windows релизов с changelog'ом, ~30 macOS, etc.

**Структура:** Hero → 5 табов (platforms) → 5 panel'ей с releases-list
→ CTA → Footer.

**Schema.org:** BreadcrumbList + WebPage. ❌ Скудно. Можно добавить
SoftwareApplication с softwareVersion + datePublished для каждого
релиза, но это раздует HTML.

**H1:** «Every version, every release.»

**Находки:**

1. **274KB HTML — самая тяжёлая страница** в проекте. Все Windows
   релизы (50+) с полным changelog'ом в одной странице. Можно
   lazy-load (load tab data on click) для perf, но это инженерная
   правка не контентная.
2. **5 табов работают через JS** — Win / Mac / iOS / Android /
   Remote. Win активна по умолчанию.
3. **`.release` и `.bin-row` — карточки релизов без anchor.** Hover
   есть. Но и не должны быть кликабельными (это просто данные
   релиза). Стоит убрать hover transform если есть.
4. **Контейнерные ширины:** 1100 / 980 / 900 / 780 / 680 / 600 — 6
   разных. Самый рваный набор после multistreaming/vc.
5. **`scroll-padding-top: 120px`** — пользователь сделал шире чем 60px
   для compensation sticky-табов под навбаром. Хорошее решение.
6. **«Binary-only section»** для интерим-сборок (без changelog) —
   честно, не маскирует пробелы.

---

### 1.10 `/help/` — support page

[help/index.html](../help/index.html) · 366 строк · 20KB

**Что:** Страница помощи. Forum + Telegram + ссылка на FAQ главной +
3 ресурса (FAQ / Changelog / Products).

**Структура (4 секции):** Hero → Channels (Forum + Telegram cards) →
Self-serve (3 resources) → CTA → Footer.

**Schema.org:** BreadcrumbList + ContactPage. ✅ Уникальный
ContactPage type — правильно подобран для этой страницы.

**H1:** «Get help straight from the people who built it.»

**Находки:**

1. **Channels (Forum + Telegram) — кликабельны как `<a>` ✓.**
2. **3 Resources карточки (FAQ / Changelog / Products) — `<a>` ✓.** Все
   кликабельные. **Это единственная страница без hover-on-non-clickable.**
3. **Контейнерные ширины:** 1100 / 900 / 720 / 680 / 600. 5 разных.
4. **Note про FAQ:** «Before you write… check the FAQ on the main
   page first» — мягкий self-service-first nudge.
5. **0 эмодзи в body** — иконки только SVG (#i-cam, #i-pen и т.д.).
   Чисто и согласовано с CLAUDE.md icon style.
6. **Только этот файл был мной написан с нуля** — отчасти поэтому он
   самый «чистый» по audit criteria. Шаблон для будущих служебных
   страниц.

---

## Раздел 2. Сквозные паттерны

### 2.1 «Лестница» контейнерных ширин — повсеместно

Каждая страница использует **4–6 разных max-width** для контейнеров.
Сводная таблица:

| Страница | Кол-во ширин | Все значения |
|---|---|---|
| `/products/` | 4 | 1100, 900, 820, 680 |
| `/multistreaming/` | **6** | 1100, 900, 780, 760, 640, 620 |
| `/virtual-camera/` | **6** | 1100, 900, 780, 760, 640, 620 |
| `/alternatives/` | 4 | 1100, 900, 820, 680 |
| `/alternatives/obs/` | 4 | 900, 780, 720, 680 |
| `/for/` | 4 | 1100, 900, 820, 680 |
| `/for/youtubers/` | 4 | 900, 780, 720, 680 |
| `/for/churches/` | 4 | 900, 780, 720, 680 |
| `/changelog/` | **6** | 1100, 980, 900, 780, 680, 600 |
| `/help/` | 5 | 1100, 900, 720, 680, 600 |
| главная (для сравнения) | 4 | 1440, 1200, 1100, 800 |

**Общие наблюдения:**
- `/alternatives/obs/`, `/for/youtubers/`, `/for/churches/` идентичны —
  900/780/720/680. SEO-template работает.
- `/multistreaming/` и `/virtual-camera/` идентичны (6 значений каждая)
  — feature-page template.
- Хабы (`alternatives/`, `for/`, `products/`) близки но не идентичны.
- 780 vs 760 на feature-pages — практически одно и то же, можно склеить.

**Лестничный эффект** на feature-страницах виден явно: hero 1100 → 780
→ 760 → 640 секции — каждая 2-я секция чуть шире/уже соседа.

### 2.2 Hover на некликабельных карточках — везде

Сводка по типам неклкабельных карточек с hover:

| Страница | Карточки | Кол-во |
|---|---|---|
| `/products/` | `.product` | 4 |
| `/multistreaming/` | `.feat-card` + `.uc-card` | 12 |
| `/virtual-camera/` | `.app-card` + `.feat-card` + `.uc-card` | **24** |
| `/alternatives/` | `.hub-card.soon` | 5 |
| `/alternatives/obs/` | (только `.faq-item`, OK) | 0 |
| `/for/` | `.hub-card.soon` | 4 |
| `/for/youtubers/` | (только `.faq-item`, OK) | 0 |
| `/for/churches/` | (только `.faq-item`, OK) | 0 |
| `/changelog/` | `.release`, `.bin-row` | ~80 |
| `/help/` | (все кликабельны) | **0** ✅ |

`/help/` — единственная страница без hover-on-non-clickable (эталон).
`/virtual-camera/` — лидер по количеству (24 карточки), за счёт
12 app-cards.

### 2.3 Schema.org полнота — разнородно

| Страница | Schema types | Достаточность |
|---|---|---|
| `/multistreaming/` | Full set (HowTo + FAQPage + Rating + SoftwareApp) | ✅ |
| `/virtual-camera/` | Full set | ✅ |
| `/for/youtubers/` | Full set | ✅ |
| `/for/churches/` | Full set | ✅ |
| `/alternatives/obs/` | Minus HowTo | ⚠️ Можно добавить HowTo для migration steps |
| `/products/` | Minus FAQPage, AggregateRating | ⚠️ Стоит добавить AggregateRating |
| `/alternatives/` | Minimal (Breadcrumb + ItemList) | ⚠️ Hub-page, можно оставить |
| `/for/` | Minimal (Breadcrumb + ItemList) | ⚠️ Hub-page, можно оставить |
| `/changelog/` | Minimal (Breadcrumb + WebPage) | ⚠️ Можно добавить SoftwareApplication |
| `/help/` | Minimal + ContactPage type | ✅ Подходит для типа страницы |

### 2.4 Эмодзи в body — несогласовано

В main page после возврата на эмодзи в use cases используются:
🎮 📹 🎓 ⛪ ✨ 🎵.

Другие страницы:

| Страница | Эмодзи | Совпадает с главной? |
|---|---|---|
| `/multistreaming/` | 🌐 🎮 🎓 🎤 🛍 📸 | частично (🎮🎓) |
| `/virtual-camera/` | 💼 🎮 🎓 📺 📞 | частично (🎮🎓) |
| `/alternatives/obs/` | 📡 🪄 🎥 📱 🔄 | нет |
| `/for/` | 📹 🎮 🎓 🎬 | частично (🎮🎓📹) |
| `/for/youtubers/` | 🎙 📡 🔁 💡 📊 🎬 | нет |
| `/for/churches/` | 🎤 📺 🎬 📊 📝 | нет |

Эмодзи **разные на каждой странице** — нет общего «языка иконок».
Особенно странно: главная использует 🎮 для For Streamers, а на
multistreaming/vc там 🎮 — но для другого use case. Нужно либо
утвердить «один эмодзи = одна тема» через сайт, либо смешать обратно
на SVG.

### 2.5 Footer-inner структура — не унифицирована

| Страница | Footer структура |
|---|---|
| Главная | 4 колонки (Brand · Product · Support · Company) + bottom-bar |
| `/products/`, `/multistreaming/`, `/virtual-camera/` и др. | Простая 1-строчная footer-links |
| `/changelog/`, `/help/` | Простая 1-строчная |

Главная имеет богатый футер; **все остальные 10 страниц** —
упрощённый «© SplitCam · линки». Это ОК если так задумано
(footer-lite на внутренних страницах), но если пользователь зашёл
сразу на /for/youtubers/ из SEO — он не видит Support / Telegram /
Forum линков в footer. Может имеет смысл синхронизировать.

### 2.6 Cross-page: H1-стиль

| Страница | H1 |
|---|---|
| Главная | «Go live everywhere. / Your free streaming studio for [cyc].» |
| `/products/` | «One SplitCam family — on every screen you own.» |
| `/multistreaming/` | «One stream. Every platform. All at once.» |
| `/virtual-camera/` | «One stream, every meeting app.» |
| `/alternatives/` | «How SplitCam compares — free, with the extras built in.» |
| `/alternatives/obs/` | «The free SplitCam alternative to OBS Studio — easier, with multistream built-in.» |
| `/for/` | «Set up SplitCam for the way you go live.» |
| `/for/youtubers/` | «How to live stream on YouTube — free software, 5-minute setup.» |
| `/for/churches/` | «Free church streaming software — broadcast Sunday service to every platform.» |
| `/changelog/` | «Every version, every release.» |
| `/help/` | «Get help straight from the people who built it.» |

H1-стиль **в семье**: «One X, every Y» (главная / products /
multistreaming / vc) — узнаваемый брендовый ритм. SEO-страницы
утилитарнее («How to…»). Hub-страницы — нейтральнее. **Согласовано
по смыслу.**

---

## Раздел 3. Приоритеты

### 🔥 P0 — кросс-страничные

1. **24 неклкабельных карточек с hover на `/virtual-camera/`** (12
   app-cards + 6 feat + 6 uc). Самая раздутая страница по «обещаниям
   клика». Либо ссылки (на гайды по приложению — `/help/zoom`), либо
   убрать transform.
2. **12 неклкабельных на `/multistreaming/`** (6 feat + 6 uc) — то же.
3. **4 product-карточки на `/products/`** — `<div>`, не `<a>`. Сделать
   ссылками на соответствующие download URL или на /changelog/.

### ⚠️ P1 — на странице

4. **/products/ нет AggregateRating в Schema** — добавить 4.5/357 как на
   главной.
5. **/alternatives/obs/ нет HowTo Schema** — есть step-by-step migration
   guide который рекурсивно описан в тексте, но не в schema.
6. **/changelog/ нет SoftwareApplication Schema** для версий — можно
   обогатить SEO.
7. **«Лестница» 780 vs 760 на feature-страницах** — близкие значения
   склеить в одно (например, всё 780).

### 🔧 P2 — гигиена

8. **Footer-lite vs footer-rich** — синхронизировать. Если у внутренних
   нужен Support колонка с Telegram/Forum/Help, добавить.
9. **Эмодзи не согласованы между страницами** — утвердить либо «один
   эмодзи = одна тема» (🎮 = Gamer), либо вернуться к SVG.
10. **`/products/` — `.connect-step` hover** — карточки 3 шагов
    «Pair in three steps» с hover. Не критично, но subtle false-promise.

### Чего нет в P-листе и можно добавить (новые правки)

- **`/products/` AggregateRating block** — звёзды/число под H1.
- **Каждая SEO-страница могла бы иметь собственную ContactPage-style
  alternative** если хочется. Пока pop-up «get help → /help/» — норм.
- **Sticky download bar mobile** — тот же запрос что для главной,
  одинаково релевантен для всех страниц.

---

## Краткие выводы

**Что хорошо** по сайту целиком:
- SEO-template отработан и применяется единообразно
  (alternatives/obs, for/youtubers, for/churches идентичны структурно).
- Schema.org покрытие feature-страниц на топ-уровне.
- Hub-страницы делают то что должны — не пытаются стать
  feature-pages.
- `/help/` создан как эталонная страница без hover-debt.

**Что плохо** по сайту целиком:
- **Hover-on-non-clickable** есть на 8 из 10 страниц.
- **Контейнерные ширины** — у каждой страницы свой ласка из 4–6
  значений.
- **Эмодзи-язык** не согласован (на главной утверждены 6, на
  feature-pages совсем другие).
- **Footer-структура** отличается на главной и всех остальных.

**Если делать одну сквозную правку** — починить hover-on-non-clickable
на /virtual-camera/, /multistreaming/, /products/. Это покрывает 40
карточек.

**Если делать одну долгую правку** — унификация контейнерных ширин
сразу для всего сайта. Решение по тройке (Hero 1200, sections 1200,
text-narrow 820) и прокинуть везде. Сделать раз и забыть.
