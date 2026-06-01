# ВЕРСТКА-products.md — глубокий аудит страницы /products/

Полный пообъектный пробег по [products/index.html](../products/index.html)
— 556 строк / 37KB. Сопровождает [ВЕРСТКА.md](ВЕРСТКА.md) (главная) и
[ВЕРСТКА-pages.md](ВЕРСТКА-pages.md) (компактный обзор остальных страниц).

Дата снимка: 2026-06-01. Версия SplitCam Windows v10.9.2, macOS v1.19.

---

## Блочная структура

```
HEAD (meta + Schema.org)
NAV (fixed, 60px) + nav-mobile
BREADCRUMBS (SplitCam / Products)
HERO (centered, "Download SplitCam — on every screen you own")
SECTION 1 — Stream from any device (4 product-card 2×2)
SECTION 2 — Companion app: SplitCam Remote (2-col + phone-mock)
SECTION 3 — How it works: Pair in three steps (3 connect-step)
CTA — Pick the SplitCam you need
FOOTER (1-row footer-lite)
```

Высота на 1440px: 3557px. На 390px: ~6500px. Горизонтального скролла нет.

---

## 1. HEAD / Meta / Schema.org

### 1.1 Title и meta
- **Title:** «Download SplitCam — Windows, Mac, iOS & Android | SplitCam»
  → SEO-keyword «Download SplitCam» вынесен вперёд. Хорошо.
- **Description:** конкретика про 4 платформы + Remote, упоминание «no
  watermark». Хорошо.
- **Keywords meta:** есть (legacy, мало вреда).
- **Robots:** `index, follow, max-snippet:-1` — расширенное.

### 1.2 Open Graph / Twitter Card
- Полный набор (og:type/url/title/description/image, twitter:card),
  идентичный title/description с основными meta.

### 1.3 Schema.org
- **BreadcrumbList** ✓
- **SoftwareApplication** (brand-level, добавил недавно): name + alternateName
  + softwareVersion `10.9.2` + datePublished `2003-01-01` + AggregateRating
  `4.5/357` + Offer 0$ ✓
- **ItemList** из 5 элементов: Win / Mac / iOS / Android / Remote — каждый
  как `SoftwareApplication` или `MobileApplication` со своим
  applicationCategory + operatingSystem + Offer ✓

**Замечание:** Mac в Schema.org `operatingSystem: "macOS 13+"` (отвечает
реальности), iOS — `iOS 16.6+`. **Согласовано** с product-platform строкой в
HTML.

### 1.4 Favicon набор
Win/Mac путь правильный — `../favicon-*.png`.

---

## 2. NAV (фиксированная шапка)

### 2.1 Структура
- 60px высота, fixed top, backdrop-blur, нижний border
- Логотип + текст «splitcam»
- 6 ссылок: Products (.active) / Virtual Camera / Multistreaming /
  Alternatives / Use Cases / Help
- Кнопка Download + гамбургер

### 2.2 Найдено
- ✅ Active state на Products
- ✅ Гамбургер работает на <900px (после P0 NAV-fix)
- ✅ scroll-padding-top: 60px (после ВЕРСТКА P1 #9)
- ✅ Mobile menu без Download дубля (после недавней правки)

### 2.3 Замечаний нет.

---

## 3. BREADCRUMBS

Минимальный: «SplitCam / Products». Совпадает с Schema.org BreadcrumbList.
Без замечаний.

---

## 4. HERO

### 4.1 Структура
- Eyebrow: «Products» (синий blue-dim pill)
- H1: «**Download SplitCam** — on every screen you own.»
  («Download SplitCam» с gradient .accent текстом синий→пурпур)
- Sub: упоминает Windows/macOS/iOS/Android + SplitCam Remote + "no
  watermark, no subscription"
- 4 badges: ✓ Free forever / ✓ No watermark / ✓ Peer-to-peer multistream /
  ✓ Built since 2003

### 4.2 Найдено
- **Сильно: H1 SEO-keyword «Download SplitCam» вынесен вперёд** + gradient
  делает его магистральным элементом
- **Badges «Built since 2003»** — то же что footer copyright. Минор-дубль
  (как было на главной с stats-strip 2003).
- **«Peer-to-peer multistream»** — приходит как пред-объяснение для
  технически-грамотного юзера. На /products/ это норм.
- **H1 max-width 820, sub max-width 680** — типографически читаемая ширина.
- Hero на 1440px не имеет app-window (как на главной), просто центрированный
  текст + badges. Это правильно для хаб-страницы.

### 4.3 Замечаний: нет.

---

## 5. SECTION «Stream from any device» — 4 product-cards

### 5.1 Структура
- Eyebrow: «Live streaming»
- H2: «Stream from any device»
- Sub: «desktop and mobile builds share the same multistreaming engine,
  the same scene-and-source model, the same zero cost»
- Grid 2×2 из 4 `.product` карточек:
  - **Windows** (win) — gradient blue icon, v10.9.2, 5 features, Download
    + Changelog
  - **macOS** (mac) — gradient purple icon, tag-new v1.19, 5 features, Mac
    App Store + Changelog
  - **iOS** (ios) — black gradient icon, tag-beta, 5 features (2 marked
    «in development»), App Store
  - **Android** (android) — green Android icon, tag-beta, 5 features,
    Google Play

### 5.2 Найдено
- **🔥 4 product-card — все `<div>`, не `<a>`.** Карточки выглядят как
  кликабельные, но клик ничего не делает. (Hover transform-lift был убран
  в коммите [0401aac](https://github.com/x270880x/splitcam/commit/0401aac)
  — это смягчило проблему.) Download-кнопка внутри карточки работает.
- **«Hardware encoding: NVENC · QuickSync · AMF»** в Win, но в Mac упомянуто
  только «VideoToolbox» в описании. Согласовано с реальностью.
- **iOS: 2 фичи помечены «in development»** (`Real-time AR filters and
  visual effects` + `Picture-in-picture`) — честность по CLAUDE.md ✓
- **Android tag-beta** есть, но в product-features нет «in development»
  бейджей. CLAUDE.md только iOS упоминает «in development». Возможно
  Android фичи реальные — норм.
- **Changelog link** есть у Win/Mac, не у iOS/Android. Логично — у Win/Mac
  есть version (v10.9.2/v1.19), у iOS/Android только tag-beta.
- **«SplitCam for macOS v1.19»** — Schema.org для macOS не упоминает версию
  v1.19, только operating-system. Можно добавить `softwareVersion: "1.19"`
  в Schema item.

### 5.3 Контейнер
- product-grid 2×2 на 1100px секции. На 1440px viewport секция вписана в
  1100px = 170px пустоты по каждой стороне.

---

## 6. SECTION «Companion app: SplitCam Remote»

### 6.1 Структура
- Eyebrow: «Companion app»
- H2: «SplitCam Remote — your stream, in your hand»
- Sub: phone controls desktop SplitCam, switch scenes / volumes / pause
  without keyboard
- `.remote-feature` — gradient panel с purple/blue glow, border 1px purple
  - Left: h3 + paragraph + 6-bullet features list + 2 store buttons
    («App Store Coming soon», «Google Play Coming soon», disabled) +
    compat-note
  - Right: `.phone-mock` — phone-img + brand-pill (SplitCam Remote) +
    LIVE stop button

### 6.2 Найдено
- **«One tap. No awkward reach for the keyboard.»** — ритмичный slogan c
  .accent gradient на второй части.
- **6 features** перечислены с purple bullet-dot. Все realistic фичи,
  никаких маркетинговых натяжек.
- **2 store buttons disabled** — `opacity:.55, cursor:not-allowed,
  aria-disabled` — кнопки честно показывают что ещё не выпущено. Хорошо.
- **Compat-note блок** — Win 10/11 + macOS 13+ + same Wi-Fi requirement
  + «no cloud middleman, no monthly fee» + «sub-100ms latency».
- **phone-mock 280px** — в правой колонке `.remote-visual`. CSS включает
  position:relative + custom border-radius 34px + box-shadow + 1px
  white-tint outline. Внутри: phone-img + phone-brand pill (gradient
  background, blur) + phone-stop (red square with red glow).
- **🔥 Подсветка картинки (что просили):** до моей правки phone-mock имел
  только dark shadow + 1px outline. Теперь добавил сине-пурпурную auro:
  - `box-shadow` дополнен `0 0 90px rgba(40,120,252,.32), 0 0 140px
    rgba(156,91,255,.25)` — двойной colored glow
  - `::before` pseudo-element с radial-gradient blur 28px вокруг phone —
    soft halo, расширяет свечение
  - `overflow: visible` (было hidden), `phone-img` получил собственный
    border-radius 34px чтобы скруглённые углы остались

### 6.3 Замечаний нет (после подсветки).

---

## 7. SECTION «How it works: Pair in three steps»

### 7.1 Структура
- Eyebrow: «How it works»
- H2: «Pair in three steps»
- Sub: «auto-discovers your desktop on the local network — or scan QR»
- 3 `.connect-step` карточек:
  - Step 01 — «Run SplitCam on your computer» (Enable Remote control)
  - Step 02 — «Install SplitCam Remote on your phone» (same Wi-Fi)
  - Step 03 — «Tap to pair, then control» (auto-discover / QR)

### 7.2 Найдено
- **Чисто:** короткие steps, без воды. Шаги дают полное представление
  как работает связка.
- **HowTo Schema.org нет.** Можно добавить как на /alternatives/obs/,
  /for/youtubers/, /for/churches/. SEO польза для «how to pair splitcam
  remote» / «how to control splitcam from phone» queries.
- **`.connect-step` cards** — `<div>`, не кликабельны. Hover был раньше
  (не помню точно), сейчас нет (правил рамку текущего CSS — `.connect-step
  { background:var(--app-panel); border-radius:12px }` без `:hover` правила).
  ✓ Чисто.

### 7.3 Можно добавить HowTo Schema:
```json
{
  "@type": "HowTo",
  "name": "How to pair SplitCam Remote with desktop SplitCam",
  "totalTime": "PT3M",
  "step": [...3 шага из секции...]
}
```

---

## 8. CTA

### 8.1 Структура
- H2: «Pick the SplitCam you need»
- Sub: «Start with the desktop or mobile build — add SplitCam Remote
  later when you want phone control»
- Одна Download кнопка (btn-primary btn-lg)

### 8.2 Найдено
- **Простой 1-CTA блок** — без дополнительных ссылок (типа
  «Explore features»). Минималистично, фокус на скачивании.
- **Sub-копия** настраивает: «mobile build тоже доступен», «Remote
  добавляется позже». Снимает «нужно установить всё сразу» страх.

### 8.3 Замечаний нет.

---

## 9. FOOTER

### 9.1 Структура (footer-lite — 1 строка)
- © 2026 SplitCam · Free streaming software since 2003
- 11 ссылок: Home / Multistreaming / Virtual Camera / Products /
  Alternatives / Use Cases / FAQ / Help / Changelog / License / Privacy

### 9.2 Найдено
- ✅ **/products/ ссылка ведёт на текущую страницу (`./`).** Несколько
  лишне но окей.
- ✅ **Help, Changelog добавлены** — соответствует пост-ВЕРСТКА состоянию.
- ❌ **Нет Telegram / Forum ссылок** (которые есть на главной в Support
  колонке). Если пришёл из Google прямо на /products/ — он не видит social
  channels. Та же претензия что в ВЕРСТКА-pages.md sec 2.5.
- **Сравнение:** главная имеет 4-колоночный footer с Brand · Product ·
  **Support** · Company. На /products/ — 1-row упрощённый. Решение
  «footer-rich vs lite» которое ещё ждёт ответа.

### 9.3 Решение по footer:
Висит — нужно твоё решение (см. ВЕРСТКА-pages.md sec 3 footer вопрос).

---

## 10. Контейнерные ширины (P2 «лестница»)

Замер на 1440px:
- Hero `.hero` — **1100px** (max-width на hero)
- Breadcrumbs — **1100px**
- Section grid `.section` — **1100px**
- Remote-feature panel inside section — **1020px**
- Remote-inner grid columns — text col + 380px phone col, gap 40
- CTA `.cta-block` — **1440px** (full width inside section but content centered)
- Footer-inner — **1100px**

**Найдены 4 уровня:** 1440 / 1100 / 1020 / 938 (по данным eval).

Не катастрофа на эту страницу — отклонения уровня ~80px (1100 vs 1020),
не как на главной с 1440 vs 800.

---

## 11. Mobile (390px)

### 11.1 Поведение
- Все секции схлопываются в 1-column
- product-grid 2x2 → 1×4
- connect grid 3×1 → 1×3
- remote-inner 1fr 380px → 1fr 1fr (gap 28)
- phone-mock 280 → 230 (явная правка в @media)
- nav-burger включается, nav-links скрываются
- footer-inner → flex-direction:column

### 11.2 Найдено
- ✅ Mobile media query учитывает phone-mock, .remote-feature, footer
- ✅ Гамбургер работает (после общей правки)

### 11.3 Замечаний нет.

---

## Сводка приоритетов

### 🔥 Закрыто этой сессией
- **Phone-mock подсветка** — добавлена blue + purple aura (box-shadow
  layers + pseudo-element halo). Картинка теперь visually pops на тёмном
  фоне в гармонии с Remote-section purple gradient.

### ⚠️ Открыто (требует решения)
- **Product cards 4 шт. — `<div>` not `<a>`** (hover transform убран,
  но карточки всё равно выглядят как кликабельные). Если хочется
  закрыть до конца — сделать каждую карточку ссылкой:
  - Windows → `https://splitcam.com/download` (или Win Store)
  - macOS → `https://apps.apple.com/.../id6479984191`
  - iOS → `https://apps.apple.com/.../id1543666414`
  - Android → `https://play.google.com/store/apps/details?id=com.splitcam`
- **macOS Schema.org softwareVersion: "1.19"** — добавить в ItemList элемент
- **HowTo Schema.org** на «Pair in three steps» — для SEO snippet
- **Footer-rich vs lite** — общее решение по сайту, не специфично для
  /products/

### 🔧 P2 hygiene
- **«Built since 2003» в hero-badges** дублирует footer copyright (минор)
- **Контейнерные ширины 1440/1100/1020/938** — мелкая «лестница»,
  не катастрофическая

---

## Что выглядит сильно

- Hero H1 с gradient «Download SplitCam» — отличная SEO+visual
- 5 SoftwareApplication в Schema.org с честными OS-versions
- iOS «in development» бейджи — честность по CLAUDE.md
- 2 store buttons «Coming soon» disabled — без обмана
- Compat-note с «no cloud middleman, no monthly fee, sub-100ms latency»
  — конкретика
- Phone-mock с brand pill «Remote» + LIVE stop overlay — кастомный
  product-shot, не stock photo
- Иконки в брендовых gradient-кругах (синий Win, фиолетовый Mac, чёрный
  iOS, зелёный Android) — мгновенно опознаваемо

## Что слабее

- Product cards — div-and-hover паттерн (cosmetics после убрания lift)
- Footer-lite vs main page rich — разрыв опыта
- HowTo Schema на pair steps — недополучен SEO buff
