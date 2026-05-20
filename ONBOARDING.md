# SplitCam Landing Page — Project Onboarding

## What this is
Marketing site for SplitCam — free streaming/virtual-camera software. Static HTML/CSS/JS deployed to GitHub Pages.

- **Repo**: `x270880x/splitcam` (GitHub)
- **Local path**: `/Users/splitcam/Desktop/splitcam/`
- **Live**: https://x270880x.github.io/splitcam/

## Pages (4 total)
| Path | URL | Status |
|---|---|---|
| `/index.html` | https://x270880x.github.io/splitcam/ | Main landing (Variant A) |
| `/v2/index.html` | https://x270880x.github.io/splitcam/v2/ | Alternative landing (Variant B) |
| `/virtual-camera/index.html` | https://x270880x.github.io/splitcam/virtual-camera/ | Virtual Camera SEO page |
| `/multistreaming/index.html` | https://x270880x.github.io/splitcam/multistreaming/ | Multistreaming SEO page |

## Tech / decisions
- **No framework** — vanilla HTML+CSS+JS, single-file per page (everything inlined). No build step.
- **Dark theme** with `--app-base: #141420`, accent `--blue: #2878fc`, purple `--purple: #9c5bff`.
- **Font**: Geist (Google Fonts) + Geist Mono for code/labels.
- **Brand logos**: all 12 brand SVGs hosted locally in `/virtual-camera/assets/logos/` (Zoom, MS Teams, Meet, Discord, Telegram, WhatsApp, OBS, Webex, Slack, Jitsi, BlueJeans, GoToMeeting). Originally fetched from Simple Icons CDN, now self-hosted. 3 were manually crafted (MS Teams, Slack, BlueJeans — removed from Simple Icons per brand owner requests).
- **Favicon**: full set generated from `splitcam.png` — `favicon.ico` (16/32/48), `favicon-16/32/48/192/512.png`, `apple-touch-icon.png` (180), `site.webmanifest`. Linked from all 4 HTML pages.
- **Hero video**: `/assets/hero-spotlight.mp4` (~184KB, 1080p CRF28 20fps). Pauses on blur/visibility for performance.
- **Diagram video**: `/multistreaming/assets/stream-preview.mp4` (~384KB) referenced cross-page from VC.

## Current main page hero structure
- NAV (with logo icon + CNET rating in some places)
- HERO with: `Live Multi-Streaming Studio` pill + CNET ★★★★★ 4.5 rating chip, H1 with cycling word (creators/streamers/gamers/VTubers/podcasters/educators), download button with OS detection (Win/Mac/iOS/Android), 3 trust badges (Free forever / No watermark / Platforms)
- PLATFORMS STRIP (Twitch, YouTube, Facebook, Kick, TikTok, Instagram, X, LinkedIn, Discord, RTMP + 74 more)
- STATS (5 boxes including live counter `25,001,285+ STREAMS DELIVERED` — random tick every 2-7s adding 0-4)
- STREAMING FEATURES TABS (4 tabs: Multi-streaming / Sources / Audience / Quality)
- MULTISTREAMING spotlight → links to `/multistreaming/`
- VIRTUAL CAMERA spotlight → links to `/virtual-camera/`
- ALL FEATURES GRID (9 cells)
- USE CASES
- QUICK START
- TESTIMONIALS
- WHAT'S NEW
- FAQ
- CTA
- FOOTER

## /multistreaming/ page structure
After section reorder (synthesis of ChatGPT analysis):
1. HERO with hub-and-spoke visualization: SplitCam Live Multistream pill (3 lines: name / Streaming Studio Software / One stream → to many platforms) + blinking LIVE + thick central pipe with big running dot → hub node with 2 rings → 7 fan-out lines with small running dots → 7 destination cards (YouTube/Twitch/Facebook/Kick/TikTok/Custom RTMP/+79 More). Each card has blinking red LIVE badge.
2. POPULAR MULTISTREAM COMBOS — 9 long-tail combo cards
3. HOW IT WORKS (3 steps)
4. USE CASES (6 audiences)
5. WHAT IS MULTISTREAMING (with big video diagram)
6. KEY FEATURES (6 cells)
7. CTA
8. FAQ (12 questions, FAQPage schema for rich snippets)

SEO: comprehensive meta + Schema.org (SoftwareApplication + HowTo + FAQPage + BreadcrumbList). Keywords cover multistream, simulcast, dual stream, Restream/Streamlabs/StreamYard alternative.

## /virtual-camera/ page structure
After section reorder:
1. HERO with orbital visualization: SplitCam logo (66px, pulsing) center + "SplitCam" text. 3 orbital rings with 12 brand logos arranged in 4+4+4 pattern matching multistream layout. Ring 1 = Zoom/Teams/Meet/Discord. Ring 2 = Telegram/WhatsApp/OBS/Slack. Ring 3 = Webex/GoToMeeting/Jitsi/BlueJeans.
2. UNIVERSAL COMPATIBILITY (apps grid) — 12 cards: Zoom (47px), Teams, Meet, Discord, Telegram, WhatsApp (row 1), OBS, Slack, Webex, GoToMeeting, Jitsi, +50 more (row 2)
3. USE CASES
4. HOW IT WORKS (3 steps)
5. WHAT IS A VIRTUAL CAMERA — with diagram inside SplitCam Studio window shell (macOS-style title bar). Video shows "SplitCam Virtual Camera" overlay + LIVE badge → middle pill → 6 app cards (Zoom/Teams/Meet/Discord/Telegram + 50 More)
6. FEATURES
7. CTA
8. FAQ (12 questions)

Note: Skype was REMOVED everywhere — Microsoft retired Skype May 2025. FaceTime was REPLACED with GoToMeeting (Apple restricts virtual cameras in modern FaceTime).

## Visualization design decisions
- **Multistream hero** = hub-and-spoke (one pipe → hub → 7 lines). Replaced earlier orbit visualization at user's request, matched sketch they provided.
- **Virtual Camera hero** = orbital (3 concentric rings). Kept distinct from multistream's hub-and-spoke for visual differentiation between the two products.
- Both use same brand-blue (#2878fc) for pipes/orbits, animated SVG dots for "data flowing" feel.

## Important style/copy rules (set by user)
- All brand logos stored LOCALLY (no external CDN URLs in HTML). Self-hosted in `/virtual-camera/assets/logos/`.
- No "Restream server" / "cloud middleman" wording on multistream page — SplitCam is **peer-to-peer direct**.
- iOS belongs in platforms list (Win · macOS · iOS · Android), removed and re-added once.
- Skype is dead (May 2025) — never mention as live product.
- CNET rating: 4.5 stars, 357 reviews — used consistently.
- LIVE badges should blink (badge opacity + red dot pulse) wherever they appear.

## Recent commits (most recent first)
```
4a6c0b3 Main page spotlights synced with sub-pages (Multistream + VC) + bug fix in Features grid
ddb9142 Main page hero polish — trust signals + visual hierarchy (CNET rating chip + 3 trust badges)
7dbd6be /multistreaming/ replace orbit visualization with hub-and-spoke design
b7afdb4 Preview v7 (eventually applied to live page)
... (many preview iterations v1-v7 leading to hub-and-spoke)
69f6d95 Orbit + def-block polish (15% smaller orbit center logos)
444df1e /virtual-camera/ adopt /multistreaming/'s proven 'What is multistreaming' section layout pattern
06fa28d Fix broken nav links in sub-pages (Multistreaming/Features anchor fixes)
c581d16 Add site favicon set generated from SplitCam logo
381b6d5 Main page hero badges simplified
0ff94b7 Main page: add live 'STREAMS DELIVERED' counter to stats
ce4b809 /virtual-camera/ self-host all brand logos locally (removed Simple Icons CDN dependency)
```

## Suggested next tasks
Per user-requested plan, after Hero polish + Spotlights sync (both DONE), suggested next:
1. **Testimonials** with real CNET quotes / Trustpilot — both main page and sub-pages need stronger social proof
2. **Comparison table** SplitCam vs OBS vs Restream vs Streamlabs — strong SEO ("X alternative" queries) + conversion aid
3. **SEO infrastructure** — `sitemap.xml` + `robots.txt` + custom OG preview images per page (currently all share `hero-spotlight-poster.jpg`)
4. **OS-detection for download** — verify Mac users see `.dmg` link, Win users `.exe`, etc.
5. **Performance** — base64 logo currently embedded in some places, could move to file
6. **Blog/Learn section** for SEO long-tail (articles like "How to multistream to X", "Best webcam settings")

## How to deploy / test
- **Local preview**: `file:///Users/splitcam/Desktop/splitcam/index.html` (open in browser, no server needed)
- **Push to live**: `cd /Users/splitcam/Desktop/splitcam && git add . && git commit -m "..." && git push origin main`. GitHub Pages auto-deploys in 30-90 sec.
- **Revert last commit**: `git revert HEAD --no-edit && git push`
- **Check deploy status**: https://github.com/x270880x/splitcam/actions

## Files of note
- `/index.html` — main page
- `/virtual-camera/index.html` — VC page
- `/multistreaming/index.html` — MS page
- `/v2/index.html` — alternative landing
- `/virtual-camera/assets/logos/*.svg` — all brand logos
- `/virtual-camera/assets/logos/splitcam.png` — SplitCam brand mark (66-80px in orbits)
- `/assets/hero-spotlight.mp4` — main hero video
- `/multistreaming/assets/stream-preview.mp4` — diagram video (cross-referenced from VC)
- `/favicon.ico`, `/favicon-*.png`, `/apple-touch-icon.png`, `/site.webmanifest` — favicon set

## Communication style with user
- Russian (mostly) + English code/labels
- User prefers concise answers with concrete next steps
- Show before/after for visual changes
- Always commit changes individually with descriptive messages so revert is easy
- Live URL + local file URL both shared after pushes
