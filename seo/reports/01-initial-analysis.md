# SEO Analysis — Initial Data Pull
*Generated from Ahrefs API, country: US, date: 2026-05-20*

---

## 🚨 Critical findings

### 1. Splitcam.com сильно отстаёт от конкурентов

| Domain | DR | Organic Traffic/mo (US) | vs SplitCam |
|---|---|---|---|
| **splitcam.com** | **55** | **2,206** | baseline |
| obsproject.com | 88 | 593,726 | **269× больше** |
| streamlabs.com | 84 | 142,436 | 65× |
| streamyard.com | 83 | 141,796 | 64× |
| restream.io | 79 | 130,379 | 59× |
| reincubate.com (Camo) | 72 | 25,990 | 12× |
| manycam.com | 70 | 5,142 | 2.3× |

**Вывод:** Domain Rating 55 — это OK, но органический трафик в 50-270 раз меньше чем у прямых конкурентов. Это не проблема авторитета — это проблема **контента и таргетинга**.

### 2. Splitcam.com ранжируется по неправильным keywords

Из топ-20 organic keywords splitcam.com:

| Keyword | Vol | Pos | Trafic |
|---|---|---|---|
| splitcam (brand) | 1700 | 1 | 1773 |
| split cam | 200 | 1 | 159 |
| splitcam download | 70 | 1 | 67 |
| **how to go live on onlyfans** | 200 | 7 | 11 |
| **camsoda live** | 250 | 7 | 8 |
| **stripchat live stream** | 100 | 5 | 8 |
| webcam splitter | 20 | 1 | 8 |
| **strip cam** | 3600 | 22 | 6 |
| **flirt for free cam** | 50 | 3 | 6 |
| **x love cam** | 100 | 7 | 5 |
| **flirt4** | 1700 | 3 | 5 |
| **xlove cam** | 100 | 8 | 5 |
| **stip cam** | 30 | 2 | 5 |
| **streamate login** | 150 | 7 | 4 |
| ... etc |  |  |  |

**~80% organic трафика** = brand-запросы ("splitcam" etc.). Остальное — **adult/cam queries** (camsoda, stripchat, flirt4, OnlyFans, etc.). 

**Это плохо потому что:**
- Google ассоциирует домен с adult-нишей → меньше доверия в business/streaming сегменте
- Посетители приходят НЕ за streaming studio
- Конверсия в скачивание = почти 0
- Ни один streaming/multistream/virtual camera query не приносит трафик в top-20

---

## 💎 Главные SEO-возможности

### 🟢 Низкая конкуренция, есть volume (Quick wins)

| Keyword | Volume | KD | CPC | Стратегия |
|---|---|---|---|---|
| **simulcast** | 3600 | **22** | $0.35 | Сделать landing «What is simulcasting» |
| **restream alternative** | 300 | **0** | $2.50 | Strong comparison page |
| **streamyard alternative** | 200 | **0** | $1.70 | Comparison page |
| **virtual webcam** | 150 | **0** | $0.30 | Альт-страница для virtual-camera |
| **snap camera alternative** | 150 | **0** | $1.00 | Comparison (Snap Camera мертв с 2023) |
| **manycam alternative** | 90 | **0** | $1.40 | Comparison page |
| **streamlabs alternative** | 90 | **0** | $1.00 | Comparison page |
| **broadcast to multiple platforms** | 70 | 36 | – | Landing page |
| **virtual camera for zoom** | 20 | **0** | – | Section on VC page |
| **how to stream to twitch and youtube** | 10 | **0** | $0.40 | How-to article |

### 🟡 Хороший volume, средняя конкуренция

| Keyword | Volume | KD | CPC | Стратегия |
|---|---|---|---|---|
| **obs virtual camera** | 3300 | 37 | $0.30 | Boost VC page для этого запроса |
| **multistreaming software** | 150 | 56 | $1.30 | Текущая multistream page, усилить |

### 🔴 Высокий volume, тяжёлая конкуренция

| Keyword | Volume | KD | CPC |
|---|---|---|---|
| **multistream** | 4400 | 70 | $1.80 |
| **virtual camera** | 800 | 47 | $0.15 |
| **free multistreaming** | 80 | 66 | $1.50 |
| **multi streaming software** | 60 | 63 | $3.00 |

Эти **возможны** но требуют времени, backlinks, контента. Не первый приоритет.

### ⚠️ Zero-volume keywords (мы оптимизируем напрасно)

В наших meta мы продвигаем:

| Keyword | Volume |
|---|---|
| splitcam multistream | **0** |
| splitcam virtual camera | **0** |
| virtual camera for teams | **0** |
| multistream to twitch and youtube | **0** |

Эти фразы **никто не ищет** (по Ahrefs). Их можно убрать из meta keywords и H1.

---

## 🎯 План действий (приоритезированный)

### Phase 1 — Quick wins (этот месяц)

1. **Создать comparison таблицу** «SplitCam vs OBS / Restream / StreamYard / Streamlabs / ManyCam» на главной или отдельной странице. Targets: `restream alternative` / `streamyard alternative` / `streamlabs alternative` / `manycam alternative` — все **KD 0**. Reach ~580 vol/mo total.

2. **Усилить «simulcast»** как ключевое слово на multistream-странице. Volume 3600, KD 22 — best opportunity / effort ratio. Добавить в H1 один из вариантов или sub-section.

3. **Boost «OBS virtual camera»** на VC-странице. Volume 3300, KD 37. Уже упоминается как «OBS Virtual Camera alternative» — усилить в title/H1/H2.

4. **Snap Camera alternative page** — отдельная мини-страница или секция. Snap Camera умер в 2023, эти 150 запросов уже ищут замену.

### Phase 2 — Content gap (2-3 месяца)

5. **Adult-content cleanup** — убрать или переписать страницы которые ранжируются по camsoda/stripchat/flirt4. Это тянет нерелевантный трафик и портит SEO-репутацию. Альтернатива: вынести их в отдельный subdomain.

6. **Article: "How to stream to Twitch and YouTube"** — короткий how-to с конкретными шагами. Volume 10 но KD 0 — лёгкий ranking.

7. **Article: "What is simulcasting"** — образовательный контент. Volume 3600, KD 22 — главный долгосрочный win.

### Phase 3 — Long-term (3-6 месяцев)

8. Закрыть keyword gap с конкурентами:
   - obsproject.com ранжируется по сотням keywords — изучить какие applicable для нас
   - streamlabs.com / streamyard.com — то же самое
9. Backlink-building (DR 55 → 65+)

---

## 📊 Текущее использование Ahrefs API

- План: Lite, billed monthly
- Лимит: 100,000 units/мес
- Использовано: 4,050 units (4%)
- Осталось: ~96,000 units (можно ещё ~25-30 полных прогонов)
