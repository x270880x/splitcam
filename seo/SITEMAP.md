# SplitCam.com — Recommended Sitemap & Interlinking Map
*Created 2026-05-21 — based on IA analysis of OBS, Streamlabs, vMix, Meld Studio, PRISM Live, Ecamm Live, Wirecast.*

Status legend: ✅ built · 🔜 planned in PLAN.md · ➕ new recommendation (from competitor IA)

---

## PART A — Hierarchical sitemap (sections → pages)

```
splitcam.com/
│
├─ /  ............................... HOME ✅  (Variant A — final; /v2/ Variant B archived, noindex)
│
├─ PRODUCTS — /products/ ............ hub ✅
│   ├─ /products/windows/ .......... ➕  per-OS page (SEO: "splitcam windows")
│   ├─ /products/mac/ .............. ➕  per-OS page (SEO: "splitcam mac")
│   ├─ /products/ios/ .............. ➕  per-OS page
│   ├─ /products/android/ .......... ➕  per-OS page
│   └─ /products/remote/ ........... ➕  SplitCam Remote (phone-control app)
│
├─ FEATURES — /features/ ............ ➕  hub (optional but recommended)
│   ├─ /virtual-camera/ ............ ✅  feature page
│   ├─ /multistreaming/ ............ ✅  feature page
│   ├─ /features/ai-background/ .... ➕  (SEO: "ai background removal")
│   ├─ /features/scenes-layers/ .... ➕  (scenes, sources, layers)
│   ├─ /features/effects-filters/ .. ➕  (beauty + AR filters)
│   ├─ /features/screen-capture/ ... ➕  (SEO: "screen capture / game capture")
│   ├─ /features/recording/ ........ ➕  (local recording)
│   └─ /features/audio-mixer/ ...... ➕  (audio mixing, noise suppression)
│
├─ ALTERNATIVES — /alternatives/ .... hub 🔜 (Wave 2)
│   ├─ /alternatives/obs/ .......... ✅
│   ├─ /alternatives/streamlabs/ ... 🔜 Wave 2
│   ├─ /alternatives/restream/ ..... 🔜 Wave 2
│   ├─ /alternatives/streamyard/ ... 🔜 Wave 2
│   ├─ /alternatives/vmix/ ......... 🔜 Wave 3
│   ├─ /alternatives/manycam/ ...... 🔜 Wave 3
│   ├─ /alternatives/meld-studio/ .. 🔜 Wave 3
│   ├─ /alternatives/snap-camera/ .. 🔜 Wave 3
│   ├─ /alternatives/prism-live/ ... ➕  (PRISM Live is a direct competitor)
│   └─ /alternatives/ecamm/ ........ ➕  (optional — Mac streaming niche)
│
├─ FOR / USE-CASES — /for/ .......... hub 🔜 (Wave 2)
│   ├─ /for/youtubers/ ............. ✅
│   ├─ /for/churches/ ............. ✅
│   ├─ /for/vtubers/ ............. 🔜 Wave 2
│   ├─ /for/streamers/ .......... 🔜 Wave 3 (Twitch focus)
│   ├─ /for/educators/ ......... 🔜 Wave 3
│   ├─ /for/gamers/ ........... ➕  (game capture + multistream)
│   └─ /for/business/ ........ ➕  (video calls / virtual camera at work)
│
├─ RESOURCES
│   ├─ /blog/ ...................... ➕  (every competitor has one)
│   ├─ /help/ ...................... ✅  knowledge base (already on splitcam.com)
│   ├─ /tutorials/ ................. ➕  video guides hub
│   ├─ /whats-new/ ................. ✅ section on home  ➕ standalone changelog page
│   └─ /faq/ ....................... ✅  section/anchor on home
│
├─ /download ........................ ✅  (or /products/ doubles as the download hub)
│
└─ COMPANY / LEGAL
    ├─ /about/ ..................... ➕
    ├─ /contact/ ................... ➕
    ├─ /press/ ..................... ➕  (brand assets, logos, screenshots)
    ├─ /privacy/ ................... ✅  (privacy policy exists for Mac apps)
    └─ /terms/ ..................... ➕
```

### Why this shape (competitor evidence)
- **Per-OS product pages** — Streamlabs/vMix/Meld/PRISM/Ecamm all use per-product (not per-OS) pages; SplitCam's split is per-OS, so per-OS pages fit and capture "splitcam mac/windows" searches.
- **/features/ hub + feature pages** — split market: OBS/vMix/Ecamm/Wirecast use one big features page; Streamlabs/Meld use individual feature pages. Individual pages win for SEO (one keyword each).
- **/alternatives/ section** — only Meld Studio has explicit "vs" pages. This is an under-contested area — a real SplitCam advantage. Keep investing here.
- **/for/ use-case section** — only vMix does personas well (Churches, Education, Gaming, Sports). SplitCam already started this — strong differentiator vs OBS/Streamlabs.
- **Resources baseline** — every competitor has Blog + Help/Support; most have Docs/Tutorials. SplitCam currently lacks a blog — gap to fill.
- **4-column footer** — universal pattern: Product · Resources · Company · Legal.

---

## PART B — Interlinking map (perelinkovka)

### Global NAV (on every page) — recommended
```
[splitcam logo→/]  Products  Virtual Camera  Multistreaming  Alternatives  Help  [⬇ Download]
```
Currently: Products · Virtual Camera · Multistreaming · What's New · Help.
Recommendation: swap "What's New" → "Alternatives" in nav (What's New stays reachable from footer + home section).

### Global FOOTER (on every page) — 4 columns
```
PRODUCT            FEATURES           COMPARE             RESOURCES / COMPANY
Windows            Virtual Camera     vs OBS              Blog
Mac                Multistreaming     vs Streamlabs       Help
iOS                AI Background      vs vMix             Tutorials
Android            All features →     All alternatives →  What's New
SplitCam Remote                                           About · Contact
Download                                                  Privacy · Terms
```

### Link flow — who links to whom

```
                          ┌─────────────┐
                          │    HOME /   │  hub of hubs
                          └──────┬──────┘
        ┌────────────┬───────────┼────────────┬─────────────┐
        ▼            ▼           ▼            ▼             ▼
   /products/   /features/  /alternatives/  /for/      /blog/ /help/
    (hub)        (hub)        (hub)         (hub)      /download
        │            │           │            │
   ┌────┴────┐   ┌────┴────┐  ┌───┴────┐   ┌───┴────┐
   ▼         ▼   ▼         ▼  ▼        ▼   ▼        ▼
 windows   mac  virtual-  ai-  obs   vmix  youtubers churches
 ios android   camera   background streamlabs ...  vtubers ...
 remote        multistream ...
```

**Rule: every leaf page links UP to its hub and ACROSS to 2-4 siblings/related pages.**

### Cross-cluster links (the high-value perelinkovka)

| From | Links to | Why |
|---|---|---|
| HOME | all 4 hubs + Download + Blog + What's New | entry point |
| /products/remote/ | /products/ · /multistreaming/ · /features/scenes-layers/ | Remote controls these |
| /products/windows/ , /mac/ | /features/* · /download · /products/ | OS page → what it does |
| /multistreaming/ | /for/churches/ · /for/youtubers/ · /alternatives/restream/ | multistream is core to these personas/comparisons |
| /virtual-camera/ | /for/business/ · /for/vtubers/ · /features/ai-background/ | virtual cam use cases |
| /alternatives/obs/ | /for/youtubers/ · /for/churches/ · /multistreaming/ · /features/* | "switching from OBS" leads to use cases |
| /alternatives/vmix/ | /for/churches/ · /multistreaming/ | vMix dominates church streaming |
| /alternatives/streamlabs/ | /for/streamers/ · /features/effects-filters/ | Streamlabs = creator/Twitch tools |
| /alternatives/prism-live/ | /products/ios/ · /products/android/ · /virtual-camera/ | PRISM is mobile-strong |
| /for/youtubers/ | /alternatives/obs/ · /multistreaming/ · /for/vtubers/ | done ✅ |
| /for/churches/ | /alternatives/vmix/ · /multistreaming/ · /for/youtubers/ | done ✅ (vmix link pending its page) |
| /for/vtubers/ | /virtual-camera/ · /features/effects-filters/ · /alternatives/prism-live/ | VTubing = avatar/filters |
| /for/gamers/ | /features/screen-capture/ · /multistreaming/ · /alternatives/obs/ | game capture + multistream |
| every /alternatives/X/ | /alternatives/ hub + 2 sibling alternative pages | hub-and-spoke |
| every /for/X/ | /for/ hub + 2 sibling persona pages | hub-and-spoke |

### Depth rule
Keep every page **≤ 3 clicks from home**. Home → hub → leaf = 2 clicks. Don't nest deeper (no `/for/churches/multi-camera/` sub-sub-pages — make them sections within the page instead).

---

## PART C — Build priority (suggested)

1. **Now / built** — Home, /products/, /virtual-camera/, /multistreaming/, /for/youtubers/, /for/churches/, /alternatives/obs/  (/v2/ = archived Variant B, not public)
2. **Wave 2 (per PLAN.md, ~June 10)** — /alternatives/ hub, /for/ hub, /alternatives/{streamlabs,restream,streamyard}/, /for/vtubers/
3. **Wave 3 (per PLAN.md, ~July)** — /alternatives/{vmix,manycam,meld-studio,snap-camera}/, /for/{streamers,educators}/
4. **New, not yet in PLAN.md** — /features/ hub + 6 feature pages, per-OS /products/* pages, /alternatives/prism-live/, /for/{gamers,business}/, /blog/, /tutorials/, company/legal pages

Items in (4) are recommendations from this competitor analysis — not yet scheduled. Decide whether to fold them into Wave 2/3 or a later wave.
