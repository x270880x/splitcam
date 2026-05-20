# SplitCam Landing Page — Project Onboarding

## What this is
Marketing site for SplitCam — free streaming/virtual-camera software. Static HTML/CSS/JS deployed to GitHub Pages.

- **Repo**: `x270880x/splitcam` (GitHub)
- **Local path**: `/Users/splitcam/Desktop/splitcam/`
- **Live**: https://x270880x.github.io/splitcam/

## Pages currently deployed (5 total)
| Path | URL | Status |
|---|---|---|
| `/index.html` | https://x270880x.github.io/splitcam/ | Main landing (Variant A) — done |
| `/v2/index.html` | https://x270880x.github.io/splitcam/v2/ | Variant B — done |
| `/virtual-camera/index.html` | /virtual-camera/ | Sub-page — done |
| `/multistreaming/index.html` | /multistreaming/ | Sub-page — done |
| `/for/youtubers/index.html` | /for/youtubers/ | **SEO Wave 1, page 1/3 — DONE** ✅ |

## 🚨 IMMEDIATE NEXT TASK — Finish SEO Wave 1 (2 pages left)

**Background:** We ran full SEO analysis via Ahrefs API. Found massive keyword opportunities competitors take (Meld Studio, vMix). Started Wave 1 of two-section strategy: `/alternatives/` (X alternative) + `/for/` (persona pages).

### Wave 1 Page 1 — ✅ DONE
`/for/youtubers/` — targets "how to live stream on youtube" (2,700 vol, KD 6 — biggest find). Live now.

### Wave 1 Page 2 — TODO: `/for/churches/`
**Target keywords (~580 vol total, KD 2-12):**
- "church streaming software" (150 vol, KD 2)
- "church live streaming software" (150 vol, KD 3)
- "streaming services for churches" (150 vol, KD 12)
- "best church streaming software" (100 vol, KD 2)
- "church live stream software" (100 vol, KD 1)

**Why we can win:** vMix dominates this cluster (paid $60-1200) but we're free. Main page already features "For Churches" use case + multistream page has church use case.

**Content to build (model after /for/youtubers/):**
- Hero: "Live stream Sunday service to Facebook + YouTube — free"
- Sunday service workflow (multi-camera setup)
- Lower-thirds for speakers
- Song lyrics overlay (Browser Source)
- Multistream FB + YouTube + church website RTMP simultaneously
- Comparison: SplitCam (free) vs vMix ($60-1200) vs ProPresenter
- FAQ + Schema.org HowTo + FAQPage
- Cross-link `/multistreaming/`, `/alternatives/vmix/` (future), `/for/youtubers/`

### Wave 1 Page 3 — TODO: `/alternatives/obs/`
**Target keywords (~1,130 vol total, KD 0):**
- "obs alternative" (500 vol, KD 0)
- "obs studio alternative" (200 vol, KD 0)
- "obs alternatives" (200 vol, KD 0)
- "obs alternative mac" (80 vol, KD 0)
- "alternatives to obs" (150 vol, KD 0)

**Why we can win:** Meld Studio currently captures this (pos 2-3) with KD 0 — open field. We have legit answers: built-in virtual camera (vs needs plugin in OBS), AI background (vs needs plugin), one-click multistream (vs Multiple RTMP Outputs plugin), OBS Project Import feature.

**Content to build (comparison-focused):**
- Hero: "The free SplitCam alternative to OBS Studio"
- Why people search for OBS alternative (CPU load, learning curve, plugin maintenance, no mobile)
- SplitCam advantages: simpler UI, built-in features, mobile apps, OBS Project Import
- Honest where OBS is better: open source, bigger plugin ecosystem
- Comparison table (already drafted on /for/youtubers/ — reuse)
- Schema.org: ItemList comparison + FAQPage
- Cross-link `/for/youtubers/`, `/for/churches/`, `/multistreaming/`

## Critical design rules (from extensive iteration with user)

1. **All brand logos stored LOCALLY** in `/virtual-camera/assets/logos/` — Simple Icons CDN versions downloaded + 3 manually crafted (microsoftteams, slack, bluejeansnetwork — removed from Simple Icons per brand owner requests). No external CDN refs in HTML.
2. **SplitCam logo PNG at `/assets/splitcam.png`** — used via `<img src="..">` not base64 (extracted from inline earlier).
3. **No "Restream server" / "cloud middleman"** wording on multistream page — SplitCam is **peer-to-peer direct**. Triple-checked, all references fixed.
4. **iOS belongs in platforms list** (Win · macOS · iOS · Android).
5. **Skype is DEAD** (Microsoft retired May 2025) — never mention as live product.
6. **CNET 4.5/357 rating UNVERIFIED** — couldn't find on web search. Still referenced in Schema.org/Hero — user hasn't decided to remove. Real ratings exist on Softonic 4.7, UpdateStar 4.0, G2.
7. **LIVE badges should blink** wherever they appear (badge opacity + red dot pulse).
8. **What's New section** verified — all 6 features REAL (v10.8.50 changelog, May 2025).

## Key UI conventions
- Dark theme: `--app-base: #141420`, accent `--blue: #2878fc`, purple `--purple: #9c5bff`
- Font: Geist (Google Fonts), Geist Mono for code/labels
- Each page has favicon set linked (favicon.ico + various .png + apple-touch-icon + site.webmanifest)
- Hero pattern: eyebrow chip + h1 + sub + CTA + trust badges + visual on right
- Schema.org always included: at minimum BreadcrumbList + SoftwareApplication; bigger pages add HowTo + FAQPage

## /for/youtubers/ structural template (use for next pages)
```
NAV (fixed top, same on all pages)
BREADCRUMBS
HERO (eyebrow / h1 / sub / 2 CTA / 4 trust badges)
QUICK ANSWER box (rich snippet bait)
STEP-BY-STEP guide (5 numbered steps with time + pro tips)
BONUS callout box (with cross-link)
PRO TIPS grid (6 cards)
COMPARISON TABLE
FAQ (8 Q&A in Schema.org FAQPage)
RELATED cards (3 cross-links)
CTA block
FOOTER
```

## /seo/ folder

- `seo/ahrefs.py` — Ahrefs API collector (uses env var AHREFS_TOKEN)
- `seo/targets.txt` — 8 competitor domains analyzed
- `seo/keywords.txt` — 88 keywords researched
- `seo/data/*.json` — raw API results (gitignored — they contain live data)
- `seo/reports/` — 3 markdown analysis reports
- `seo/PLAN.md` — **MASTER PLAN with timeline + Wave 1/2/3**

**Ahrefs token** — user provided earlier this session. Token is `mpjnDpu-L5mjYW04-nzbQUCsaaF3N6q8P_Y4JCXs` (Lite plan, 100k units/mo, used ~6k). To run:
```bash
cd seo && AHREFS_TOKEN='mpjnDpu-L5mjYW04-nzbQUCsaaF3N6q8P_Y4JCXs' python3 ahrefs.py
```
**Security note:** Token shared in chat. User should regenerate after sessions end.

## SEO Roadmap (from /seo/PLAN.md)

**WAVE 1** (this session, in progress): 3 pages
- ✅ `/for/youtubers/` — 2,700 vol, KD 6
- ⏳ `/for/churches/` — 580 vol, KD <12 ← NEXT
- ⏳ `/alternatives/obs/` — 1,130 vol, KD 0 ← AFTER CHURCHES

**WAVE 2** (week 3+): 6 pages
- `/alternatives/` hub + `/for/` hub
- `/alternatives/restream/`, `/alternatives/streamyard/`, `/alternatives/streamlabs/`
- `/for/vtubers/` (target: "how to be a vtuber" — 500 vol, KD 0)

**WAVE 3** (month 2+): remaining alternatives + 2 more personas (streamers, educators)

**SKIP:** podcasters/musicians/business (volume too low per Ahrefs)

## 🔔 SEO follow-up reminders → `seo/REMINDERS.md`

Durable schedule lives in [`seo/REMINDERS.md`](seo/REMINDERS.md) (in this repo, travels with the project to any Mac/account). Open that file at the start of any SEO chat — it has the full task list with absolute dates, what to do for each, and a status column to mark things done.

**Do NOT** use `CronCreate` for these — it claims `durable: true` but writes nothing to disk; reminders set that way die with the chat session (confirmed 2026-05-20). iCloud Calendar (paired with the file above) is the right place for pings.

## Recent commit history (most recent first)
```
a8b9097 SEO Wave 1: launch /for/youtubers/ (2700 vol, KD 6)
33da10f SEO: extended keyword research + final PLAN.md
6d951e9 SEO: vMix analysis — Church cluster found
7056b1f SEO: Meld Studio analysis — OBS alternative cluster
031682b SEO infrastructure (ahrefs.py + first analysis)
7814498 Performance: extract base64 logo to /assets/splitcam.png
7aaa2b7 Multi-section honesty pass (Platforms+Tabs+Footer+Testimonials)
87372c1 What's New verified v10.8 + accuracy fixes
9eb5280 Main FAQ #4 fix (peer-to-peer instead of restream server)
```

## How to deploy
- **Local preview:** `file:///Users/splitcam/Desktop/splitcam/index.html`
- **Push:** `cd /Users/splitcam/Desktop/splitcam && git add . && git commit -m "..." && git push origin main`
- GitHub Pages auto-deploys in 30-90 sec
- **Revert:** `git revert HEAD --no-edit && git push`

## Communication style with user
- Russian (mostly) + English code/labels
- Concise answers with concrete next steps
- Show before/after for visual changes
- Commit individually so revert is easy
- Live URL + local file URL both shared after pushes
- User likes to make decisions on direction — present 2-3 options when in doubt
- User prefers building real things over planning forever — execute mode preferred

## What's been done in this session (May 2026)

1. ✅ Main page hero polish (CNET rating chip, 3 trust badges)
2. ✅ Spotlights synced with sub-pages (LIVE badges, peer-to-peer wording)
3. ✅ FAQ peer-to-peer fix
4. ✅ "What's New" verified — all real v10.8 features
5. ✅ Platforms strip + Tab + Footer fixes
6. ✅ Testimonials honest (real review platforms instead of fake CNET names)
7. ✅ Cross-page nav consistency (added "What's New" to sub-page navs)
8. ✅ Performance: base64 logo → /assets/splitcam.png (saved 30KB)
9. ✅ Ahrefs API integration + 3 analysis reports + master plan
10. ✅ SEO Wave 1 page 1: /for/youtubers/

## What user wants NEXT (start with this in new chat)

> **Continue SEO Wave 1.** Build remaining 2 pages:
> 1. `/for/churches/` — target "church streaming software" cluster (580 vol, KD 2-12)
> 2. `/alternatives/obs/` — target "obs alternative" cluster (1130 vol, KD 0)
>
> Model after `/for/youtubers/` (already deployed). Schema.org HowTo + FAQPage, comparison tables, cross-links. ~1500+ words each. Real content, not thin SEO bait.
>
> After both pages: commit + push. Schedule lives in [`seo/REMINDERS.md`](seo/REMINDERS.md) — no need to set cron reminders (they don't persist).
