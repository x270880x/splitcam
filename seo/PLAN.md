# SplitCam SEO Plan — Two-Section Strategy
*Created 2026-05-20*

---

## 🆕 Разбор кандидатов в /alternatives/ — 2026-09-05

Считано по Semrush **по всем региональным базам**, а не только по US: у нас 35 локалей, и
US-число само по себе вводит в заблуждение (см. Snap Camera ниже — Франция даёт больше США).
Проверено ~100 запросов по смежным категориям: продакшн-софт, виртуальные камеры, эффекты
для вебки, телефон-как-камера, запись экрана, подкаст-сервисы, VTuber-инструменты.

### Итог по кандидатам

| кандидат | рынки | всего/мес | KD | вердикт |
|---|---|---|---|---|
| **Snap Camera** | fr 320 · us 260 · ph 260 · it 140 · de 50 · uk 40 · br 30 + 12 рынков по 20 | **~1350** | 24–30 | **делать первым** |
| **NVIDIA Broadcast** | us 170 · de 110 · остальное по 20 | ~290 | 20–26 | делать вторым |
| DroidCam | us 170 · ru 70 · in 50 · ~20 в 60 рынках | ~900 | 21 | осторожно, см. риск |

Для сравнения, уже построенные: obs 880 (KD 19) · restream 390 (9) · streamyard 320 (8) ·
manycam 50 (18) · vmix 30 (14).

### 🥇 Snap Camera — самый сильный кандидат за всё время после OBS

**Продукт мёртв с 25 января 2023.** Snap отключил серверы авторизации, из-за чего приложение
перестало работать даже у тех, кто уже установил его. Источники:
[TechCrunch](https://techcrunch.com/2023/01/05/snap-is-shutting-down-its-desktop-camera-app-that-allows-users-to-apply-filters-during-video-calls),
[Adweek](https://www.adweek.com/media/snap-camera-desktop-app-to-be-phased-out-jan-25/).

Почему это лучший случай, который вообще бывает:
- спрос осиротел — вендора, который защищал бы выдачу, больше нет;
- совпадение с продуктом точное: ищут виртуальную камеру с фильтрами и эффектами для
  видеозвонков, то есть ровно то, что у нас есть;
- головной запрос `snap camera` — 9900/мес, `snap camera filters` — 320/мес.

⚠️ **Français — крупнейший рынок этой темы (320 против 260 в US), а Филиппины идут вровень
с США.** Это прямая иллюстрация к правилу «таргет из реальных данных, а не из перевода»:
если бы страницу строили от US-числа, приоритет локалей вышел бы неверным. По правилу из
`I18N-PLAN.md` **fil ищет технику по-английски** — значит английская страница обслуживает
филиппинский спрос напрямую, отдельной локали для него не требуется.

### 🥈 NVIDIA Broadcast

Честное отличие: NVIDIA Broadcast требует карту **RTX**, а наше AI-удаление фона работает
без неё. Головной запрос 18100/мес, спрос сосредоточен в US и DE.

🔴 **Перед постройкой требование RTX подтвердить у владельца или в документации NVIDIA.**
Не писать по памяти — правило «писать можно только подтверждённое» уже ловило нас на
утверждениях о чужих продуктах.

### 🥉 DroidCam — с оговоркой

Спрос вширь: ~20/мес в шести десятках рынков, нигде не концентрирован. Главный риск —
**каннибализация собственной `/phone-as-webcam/`**: без чёткого развода по запросам новая
страница съест трафик существующей. Строить только после того, как решено, какой запрос
за какой страницей закреплён.

### Отклонено — и почему именно

Цифры сами по себе не основание: страница обязана быть честной.

| отклонено | vol | причина |
|---|---|---|
| Loom | 480 | асинхронная запись и шаринг ссылок — мы такого не делаем |
| Descript | 210 | AI-монтаж аудио/видео, другая категория |
| Camtasia · Bandicam · ShareX | 90 · 70 · 50 | запись экрана, слабое отличие от нас |
| Wowza | 50 (KD 2!) | сервер трансляций, не наш класс продукта |
| Streamlabs | 90 | отклонялся и раньше; цифра не изменилась |
| Twitch Studio | 20 | закрыт 30.05.2024, но спрос не сошёлся на «alternative» — Twitch опубликовал свой список замен, **SplitCam в него не входит** |
| XSplit · Ecamm · Wirecast · YouCam · ChromaCam · iVCam · Camo · Iriun · Lightstream · Prism · Larix · Riverside · Switcher · Castr · mmhmm · VTube Studio · Animaze | ≤70 | спрос ниже порога окупаемости страницы × 35 локалей |

### Метод, который стоит повторять

Самый ценный признак — **умерший продукт**: спрос остаётся, вендор выдачу не защищает,
а мы предлагаем работающую замену. Так найден Snap Camera. Проверять этот признак стоит
первым, до сравнения объёмов: 260/мес по мёртвому продукту дороже 480/мес по живому
чужому классу.

### 📌 Запланировано владельцем: начать постройку 2026-09-23

Решение от 2026-09-05: сначала только анализ, **через две недели — строить**. Порядок:

1. **Snap Camera** — ✅ **английская версия уже построена 2026-09-06** (коммит `0ddae4f0`),
   придержана под `noindex`, без карточки хаба, вне sitemap и `PAGE_PATHS`. Осталось:
   локализация в 34 локали с вычиткой носителями → снять `noindex` → активировать карточку
   (только ПОСЛЕ локализации, иначе по битой ссылке на локаль) → `i18n_wire` + `linkcheck` → деплой.
2. **NVIDIA Broadcast** — вторым, но сперва подтвердить требование RTX (см. 🔴 выше).
3. **DroidCam** — только после того, как разведены запросы с `/phone-as-webcam/`.

Строить по скиллу `splitcam-new-page`: EN → перелинковка (≥3 входящих, карточка в хабе
`/alternatives/`) → 34 локали → **вычитка носителем-филологом, который сам стримит** →
`page_audit.py` 0 🔴 во всех 35 → `i18n_wire.py` + `linkcheck.py` → деплой + purge.

⚠️ Хаб `/alternatives/` — сетка `repeat(2,1fr)`; сейчас карточек 5, каждая новая меняет
чётность. После добавления проверить, что последняя строка не осталась сиротой.

⚠️ Титулы и описания считать кодом: для CJK (ja/ko/zh) бюджет иной — title ≤32, description
70–100. На vmix этот перелимит пришлось чинить отдельным проходом уже после публикации.


---


## 🆕 Разбор аудиторий и функциональных страниц — 2026-09-06

Считано по Semrush по многим рынкам, затем каждый вывод атакован отдельным скептиком с доступом
к тем же инструментам и к репозиторию. **Скептик отклонил шесть кандидатов из семи и, наоборот,
поднял один.** Это ровно тот случай, ради которого проверка и заводилась: цифры были большие,
а страницы не нужны.

| кандидат | спрос/мес | KD | вердикт | почему |
|---|---|---|---|---|
| `/for/streamers/` | 8764 | 0–91 measured | отклонено | "build_later" is a deferral whose unblocking condition can never be met, because the blocker is structural rather than measurement-dependent: /for/ind |
| `/for/gamers/` | 840 | 12–68 (US database, Ahrefs | **делать** | The decisive blocker is self-inflicted |
| `/ai-background/` | 0 | not measured — no KD retri | отклонено | The decisive measurement was not missing — it was already in the repo, paid for and unmined, and it says reject, not "wait and re-measure |
| `/scenes-and-layers/` | 0 | Not measured — no KD figur | отклонено | The analysis declared the demand question unmeasurable while a working instrument sat unused, and that instrument inverts the one finding that kept th |
| `/effects-and-filters/` | 950 | 28-66 (US database, median | отклонено | STRONGEST OBJECTION: the honest angle and the arriving demand do not overlap, and the colleague's own data proves it |
| `/audio-mixer/` | 0 | Not measured — no KD retri | отклонено | build_later is wrong because it treats missing volume as the only blocker, when the analysis's own findings contain two blockers that no future measur |
| `/screen-capture/` | 77500 | 35-86 measured (US); the f | отклонено | The 77,500 is not a demand pool for this page — it is 91 |

### Что решило дело

**`/for/streamers/` отклонена, несмотря на 8764 запроса в месяц.** Весь этот спрос — уже
объявленная цель ГЛАВНОЙ страницы: её title «Free Live Streaming Software for PC & Mac», а в
`seo/I18N-KEYWORDS.md` обобщённый запрос про «программу для стрима» стоит в строке `/` во всех
волнах и для ru и es прямо помечен «homepage PRIMARY». Строить такую страницу — значит
раздваивать головной запрос сильнейшей страницы домена на 35 локалях. Вдобавок хаб `/for/`
сам озаглавлен «SplitCam for Streamers…», то есть ярлык уже занят. Остаток, который страница
имела бы право таргетировать, измерен в 20 запросов в месяц.

**`/screen-capture/` отклонена, несмотря на 77 500.** Из них 91,6% — один запрос, который
странице таргетировать нельзя, а остаток около 2300 конкурирует с `/for/educators/`, где
раздел про захват экрана уже есть и написан честно.

**`/effects-and-filters/` отклонена по несовпадению намерения.** Спрос за этими запросами —
AR-линзы и Snap Camera, а именно этого у нас нет и заявлять нельзя. Показательно, что тот же
спрос честно обслуживает построенная 2026-09-06 страница `/alternatives/snap-camera/`, где
отсутствие каталога линз прямо проговорено.

**`/ai-background/`, `/scenes-and-layers/`, `/audio-mixer/` отклонены как дубликаты своих же
страниц.** Карточка ИИ-фона уже живёт в `/features/`; `/scenes-and-layers/` — это и есть
`/multi-camera/` под другим URL; аудиомикшер описан внутри `/virtual-audio-windows/`.

**`/for/gamers/` поднята до «делать».** Головной запрос `twitch streaming software` 600/мес,
`best streaming software for twitch` 200. Честная опора конкретна и проверяется по продукту:
отдельный источник Game Capture для DirectX и OpenGL, аппаратное кодирование NVENC / QuickSync /
AMF, источник Replay на горячую клавишу, встроенный Tip Notifier. Хаб `/for/` уже держит для неё
карточку «Soon». 🔴 Перед постройкой перемерить спрос по локалям через Search Console на уже
существующих страницах — скептик справедливо указал, что консоль отвечает на вопрос
«по каким запросам домен уже показывается в этой стране», и этот источник не был использован.

### Итоговый список к постройке (заменяет прежний из одиннадцати)

1. **Snap Camera** — собрана 2026-09-06, лежит закрытой.
2. **NVIDIA Broadcast** — сначала подтвердить требование RTX.
3. **DroidCam** — после развода запросов с `/phone-as-webcam/`.
4. **For Gamers** — после перемера по локалям в Search Console.

## 🎯 НОВЫЕ ОТКРЫТИЯ ИЗ ПОСЛЕДНЕГО АНАЛИЗА

> ⚠️ Раздел от 2026-05-20, оставлен как история. Волновая схема запуска (Wave 1/2/3 ниже)
> больше не действует — страницы выбираются по реальному спросу, см. разбор 2026-09-05 выше
> и правило в `CLAUDE.md` («BINDING — every localized page is targeted from real query data»).

Мы пересчитали данные по `/for/` (персон-секции). Найдены **2 огромные возможности которых не было в первом отчёте**:

### 🥇 YouTubers — НОВАЯ ТОП-1 ВОЗМОЖНОСТЬ

| Keyword | Volume | KD |
|---|---|---|
| **how to live stream on youtube** | **2,700** | **6** ⭐ |
| free live streaming software | 350 | 72 |
| youtube live streaming software | 300 | 82 |
| go live on youtube | 250 | 63 |
| **Cluster total** | **3,600** | mixed |

**«How to live stream on youtube» — 2700 vol, KD 6** — это БОЛЬШЕ чем весь «OBS alternative» кластер. Простой how-to-гайд может ранжироваться в топ-3.

### 🥈 VTubers — недооценённая ниша

| Keyword | Volume | KD |
|---|---|---|
| vtuber software | 1,000 | 67 |
| **how to be a vtuber** | **500** | **0** ⭐ |
| free vtuber software | 200 | 47 |
| **Cluster total** | **1,730** | mixed |

«How to be a vtuber» — 500 vol, **KD 0** — открытое поле, идеально для landing.

### Полный апдейт priorities

| Кластер | Volume | KD | Решение |
|---|---|---|---|
| **YouTubers (how to live stream)** | 2,700 | 6 | ⭐⭐⭐ TOP — Wave 1 |
| **OBS alternative** | 1,130 | 0 | ⭐⭐⭐ TOP — Wave 1 |
| **Churches** | 580 | <12 | ⭐⭐ HIGH — Wave 1 |
| **VTubers (how to be)** | 500 | 0 | ⭐⭐ HIGH — Wave 2 |
| Restream/StreamYard/SL/MC alternatives | 680 | 0 | ⭐ MED — Wave 2 |
| Snap Camera alternative | 150 | 0 | ⭐ MED — Wave 2 |
| Streamers (Twitch focus) | 200 | 12 | ⭐ MED — Wave 2 |
| Educators / Podcasters / Musicians | 100-300 | mixed | ⏸ SKIP или low priority |
| Business (virtual cam) | 20 | 0 | ⏸ Уже в VC page |

---

## 📅 ВРЕМЕННАЯ ЛИНИЯ

### 🚀 Wave 1 — Запуск 3 страниц (May 20-22)

Целевая аудитория: **самые большие volume + самые низкие KD**

1. **`/alternatives/obs/`** — 1,130 vol, KD 0
   - Сравнение SplitCam vs OBS Studio
   - Конкретные причины смены: easier setup, built-in virtual cam, OBS Project Import
   - CTA: Download free

2. **`/for/youtubers/`** — Page-level target: «How to live stream on YouTube» (2700 vol, KD 6)
   - Step-by-step guide
   - Screenshots / video demo
   - Schema.org HowTo для rich snippet
   - Bonus: «free YouTube live streaming software» mention

3. **`/for/churches/`** — Cluster target: ~580 vol, KD 2-12
   - Sunday service workflow
   - Multi-camera setup
   - Multistream FB + YouTube one click
   - Lower-thirds, song lyrics overlay
   - Cross-link `/alternatives/vmix/` (vMix paid alternative)

**Время на работу:** 2-3 дня (1 страница в день, глубоко)

### ⏰ Week 1 (May 27) — Проверка индексации

- Сходить в Google Search Console
- Подтвердить что 3 страницы проиндексированы
- Если нет — submit URL вручную
- Проверить нет ли технических ошибок

### ⏰ Week 2 (June 3) — Первые позиции

- Проверить позиции по target keywords
- Если на page 1 — отлично
- Если page 2-3 — нужны мелкие правки
- Если позиций нет — анализ почему

### ⏰ Week 3 (June 10) — Готовим Wave 2

Если Wave 1 ранжируется (хотя бы page 2-3):

**Wave 2 — 6 страниц (June 10-17):**

4. **`/alternatives/` hub** — обзорная + сравнительная таблица всех
5. **`/for/` hub** — галерея персон + переходы
6. **`/alternatives/restream/`** — 300 vol, KD 0
7. **`/alternatives/streamyard/`** — 200 vol, KD 0
8. **`/alternatives/streamlabs/`** — 90 vol, KD 0
9. **`/for/vtubers/`** — 500 vol, KD 0

### ⏰ Week 4 (June 19) — Анализ результатов

- Полный отчёт по Wave 1+2
- Decision: Wave 3 или итеративная доработка существующих?
- Decision: запускать link-building?

### 🚀 Wave 3 (July) — добиваем остатки

10-13:
- `/alternatives/manycam/`
- `/alternatives/snap-camera/`
- `/alternatives/vmix/`
- `/alternatives/meld-studio/`

14-16:
- `/for/streamers/` (если KD доступен)
- `/for/educators/` (если KD доступен)
- Skip: podcasters, musicians, business (низкий volume)

---

## 🛠 ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ К КАЖДОЙ СТРАНИЦЕ

Чтобы НЕ выглядело как content farm и Google не наказал:

✅ Минимум 1500 слов уникального текста
✅ Уникальные H1, title, meta description
✅ Schema.org: SoftwareApplication + (для alternatives) Product Comparison
✅ Schema.org HowTo для гайдов (YouTubers)
✅ Schema.org FAQPage для каждой страницы (5+ Q&A)
✅ Хлебные крошки (BreadcrumbList schema)
✅ Open Graph + Twitter Cards (свои для каждой страницы)
✅ Internal links: минимум 3 ссылки на другие страницы сайта
✅ External links: 1-2 на authoritative источники (Wikipedia, official OBS/Twitch docs)
✅ Реальный visual (screenshot, скриншот, diagram)
✅ Mobile responsive
✅ Page speed: загрузка <2s
✅ Sitemap.xml включает каждую новую страницу

---

## 📊 ПРОГНОЗ ТРАФИКА

Если Wave 1 ранжируется в top-5:

| Страница | Target Vol | Реалистичная позиция | Прогноз трафика/мес |
|---|---|---|---|
| /alternatives/obs/ | 1,130 | 3-5 | 100-200 |
| /for/youtubers/ | 2,700 | 5-10 | 80-150 |
| /for/churches/ | 580 | 2-4 | 100-180 |
| **Итого Wave 1** | – | – | **280-530/мес** |

Это **+13-25% к текущему трафику** только от 3 страниц.

После Wave 2 (через 1.5 месяца): **+30-50%**.
После Wave 3 (через 2.5 месяца): **+50-80%** = **3,300-4,000/мес vs текущие 2,200**.

Через 6 месяцев + backlinks: реалистично **6,000-10,000/мес**.

---

## ⚠️ ЧТО НЕ ДЕЛАТЬ

1. ❌ Не запускать все 16 страниц за неделю — Google это видит как spam
2. ❌ Не делать тонкий контент <1000 слов — низкий quality score
3. ❌ Не таргетить «multistream» (4400, KD 70) пока DR не вырастет
4. ❌ Не использовать AI-generated текст as-is — нужна редактура
5. ❌ Не забыть про adult-content cleanup на splitcam.com (отдельная задача)
