# SplitCam — Project Onboarding

*Last updated: 2026-06-12. Open this at the start of any new chat to get up to speed.*

## Two projects

Both repos live under `/Users/splitcam/Documents/Дизайны/SplitCam/SPLITCAM DEV./`.

| Project | Local folder | GitHub repo | Live (staging) |
|---|---|---|---|
| **Main SplitCam site** | `SPLITCAM DEV./splitcam/` | `x270880x/splitcam` | https://x270880x.github.io/splitcam/ |
| **cam-streaming-guides** (adult-cam guides) | `SPLITCAM DEV./cam-streaming-guides/` | `x270880x/cam-streaming-guides` | https://x270880x.github.io/cam-streaming-guides/ |

Both are static HTML deployed via GitHub Pages (auto-deploy 30–90 sec after push).
**Workflow rule:** after meaningful edits, commit + push immediately — don't ask.

---

# PROJECT 1 — Main SplitCam site (`/splitcam/`)

Marketing site for SplitCam — free streaming / virtual-camera software. Static HTML/CSS/JS.
Destined to replace the redesign of the real **splitcam.com** (see `seo/MIGRATION.md`).

## Pages deployed (9 public + 1 archived)
| Path | Note |
|---|---|
| `/` | Main landing — **Variant A is the final homepage** |
| `/v2/` | Variant B — **archived** (A won the A/B). `noindex`, unlinked. Kept for reference only, never goes to splitcam.com. |
| `/products/` | Products hub — Windows/Mac/iOS/Android + SplitCam Remote. iOS card has 2 features tagged "in development" (AR filters, Picture-in-picture) — don't reword as shipped. Remote: **iOS app LIVE** (App Store id6760961594, button live since 2026-06-11); Android Remote not released — Google Play stays "Coming soon". |
| `/virtual-camera/` | Feature page |
| `/multistreaming/` | Feature page |
| `/alternatives/` | Hub for "vs X" comparisons. Live cards: OBS. "Soon" cards: Streamlabs, Restream, StreamYard, vMix, ManyCam. |
| `/alternatives/obs/` | SEO Wave 1 — "obs alternative" |
| `/for/` | Use-cases hub (labelled "Use Cases" in nav). Live cards: YouTubers, Churches. "Soon" cards: VTubers, Gamers, Educators, Streamers. |
| `/for/youtubers/` | SEO Wave 1 — "how to live stream on youtube" |
| `/for/churches/` | SEO Wave 1 — "church streaming software" |

Nav order site-wide: **Products · Virtual Camera · Multistreaming · Alternatives · Use Cases · Help**. (Dropdown nav rebuild is queued — see `seo/REMINDERS.md`.)

## SEO status
- **Wave 1 — DONE** ✅ (youtubers, churches, obs — all built & live).
- **Wave 2 — pending (~2026-06-10):** `/alternatives/` hub, `/for/` hub, `/alternatives/{restream,streamyard,streamlabs}/`, `/for/vtubers/`.
- **Wave 3 — later:** remaining alternatives + `/for/{streamers,educators}/`.
- Full plan: `seo/PLAN.md`. Recommended IA: `seo/SITEMAP.md`.
- **Schedule & follow-ups: `seo/REMINDERS.md`** — open it in any SEO chat (indexing checks, ranking checks, wave launches with dates). Do NOT use `CronCreate` — it doesn't persist.

## Migration to live splitcam.com
`seo/MIGRATION.md` — only the homepage `/` is a true same-URL replacement; everything else is new URLs. `seo/REDIRECTS.md` — 301 strategy + per-page weights from Ahrefs. Open decision: RU/ES locales. (Homepage A vs B — resolved 2026-05-22: A is final, `/v2/` archived.)

## Critical design rules
1. Brand logos stored LOCALLY in `/virtual-camera/assets/logos/` — no external CDN refs.
2. SplitCam logo PNG at `/assets/splitcam.png` — used via `<img>`, not base64.
3. No "Restream server" / "cloud middleman" wording — SplitCam is **peer-to-peer direct**.
4. iOS belongs in the platforms list (Win · macOS · iOS · Android).
5. Skype is DEAD (Microsoft retired it May 2025) — never mention as a live product.
6. CNET 4.5/357 rating is UNVERIFIED — still in Schema.org/Hero; user hasn't decided to remove. Real ratings: Softonic 4.7, UpdateStar 4.0, G2.
7. LIVE badges blink (badge opacity + red dot pulse).
8. Current version is **v10.9.2** — used site-wide. No installer size shown ("~85 MB" was removed as unverified).

## UI conventions
- Dark theme: `--app-base:#141420`, `--blue:#2878fc`, `--purple:#9c5bff`. Font: Geist.
- Nav (7 pages): Products · Virtual Camera · Multistreaming · What's New · Help. (`/v2/` is archived and has its own separate nav.)
- Each page: favicon set + Schema.org (≥ BreadcrumbList + SoftwareApplication; bigger pages add HowTo + FAQPage).
- `/for/youtubers/` is the structural template for SEO pages: NAV / BREADCRUMBS / HERO / QUICK ANSWER / STEP-BY-STEP / BONUS / PRO TIPS / COMPARISON / FAQ / RELATED / CTA / FOOTER.

## /seo/ folder
- `ahrefs.py` — domain + keyword collector · `pages.py` — per-URL weight · `domains.py` — domain weight checker
- `linkcheck.py` — site-wide link & interlinking audit (broken links/anchors/resources, external HTTP, nav-vs-contextual graph, sitemap sync). Run before migration and after adding pages.
- `PLAN.md` (master plan) · `SITEMAP.md` · `MIGRATION.md` · `REDIRECTS.md` · `REMINDERS.md`
- `reports/` — 3 analysis reports · `data/*.json` — raw Ahrefs output (gitignored)
- Ahrefs: set `AHREFS_TOKEN` env var. **The token shared in chat must be regenerated — it was exposed.** Lite plan, 100k units/mo.

---

# PROJECT 2 — cam-streaming-guides (`/cam-streaming-guides/`)

Adult-cam how-to guides ("how to stream on <platform> with SplitCam"). Built to move the
adult-cam content OFF splitcam.com onto a separate neutral domain (brand-cleanup decision —
adult = revenue, so it gets its own domain + 301s, not deletion).

## State
- **60 pages**: 19 platforms × EN/RU/ES + 3 language hubs.
- Built by a **static generator**: `build.py` + `platforms_en.py` / `platforms_ru.py` / `platforms_es.py`. Edit data → rerun `python3 build.py`.
- Each page: hero with platform×SplitCam collab logo (variant C, animated), quick answer, YouTube video guide, 5 steps, tips, FAQ, full Schema.org, EN/RU/ES switcher.
- All pages `noindex` — it's staging.
- `INVENTORY.md` (73 source adult pages on splitcam.com), `REDIRECTS.md` (301 map, `NEWDOMAIN.com` placeholder).
- Asset slots: `logos/<slug>.svg` (platform logos) and `shots/<slug>-<n>.png` (screenshots) — drop files, rerun build.

## Pending for launch
- Register a neutral adult domain → replace `NEWDOMAIN.com` everywhere, connect domain, remove `noindex`.
- Apply the `.htaccess` 301 block on splitcam.com **after** the new site is live.
- Optional: official platform logos into `logos/`, screenshots into `shots/`, Android SplitCam Remote link.

## Multi-language rule
Any content added/changed in one language must be replicated to all locales (EN/RU/ES) — keep `platforms_*.py` in sync.

---

## Domain portfolio (all owned by the user)
| Domain | DR | Note |
|---|---|---|
| splitcam.com | 55 | main site — the authority anchor |
| splitcamera.com | 45 | legacy SplitCam domain — fully 301 → splitcam.com via one Cloudflare rule `http.host contains "splitcamera.com"` (apex + www + blog + forum, completed 2026-05-22). DR 45 from ~950 live refdomains, 0 organic keywords. `blog`/`forum` were empty placeholder WordPress installs (no posts) — redirected, nothing to preserve. |
| multi-stream.io | 14 | live, ranks for "free multistreaming" — possible cannibalization with `/multistreaming/` |
| splitstream.com | 4 | live, weak — candidate to 301 → splitcam.com |
| split.cam | 0 | dormant, clean brand domain — reserve / short links |
| camstreamguide.com | — | neutral adult domain for cam-streaming-guides (registered; DNS/Pages connect pending) |

## Infrastructure access (set up 2026-05-22 / 23)

Files kept locally on the Mac (chmod 600), referenced via `$(cat …)` in
commands so the secret never appears in command output or chat.

### GitHub repositories
- **`x270880x/splitcam-release`** (public) — 36 releases, all Windows `.msi`
  installers mirrored from `splitcam.com/win-download/update/` (versions
  `v9.0.9` → `v10.9.2`, plus the `v10.8.62-restream-test` prerelease). Each
  release carries the matching changelog from `splitcam-changes-win` /
  `history.txt` (24 with full notes; 11 interim builds with a generic note
  + link to the full history). `v10.9.2` is marked Latest. Filenames are
  versioned (`10.9.2_x64.msi`), so the canonical "latest" download URL is
  `releases/download/v10.9.2/10.9.2_x64.msi`. Open follow-up: also drop a
  fixed-name copy in the latest release if/when site Download buttons need
  a stable `releases/latest/download/SplitCamSetup_x64.msi` URL.
- **`x270880x/old_splitcam_site`** (**PRIVATE 🔒**) — full backup of the old
  splitcam.com `public_html` (excluding the installer archive — that's in
  `splitcam-release`). Stored as `old_splitcam_site.tar.gz` (~1.4 GB) on
  the release `backup-2026-05-23`. **Keep private** — contains
  `wp-config.php` with DB credentials and other secrets.

### SSH to splitcam.com origin server
- Key: `~/.ssh/splitcam_deploy` (Ed25519, only on Mac — never copy to other
  machines). Public part lives in the server's `~/.ssh/authorized_keys`.
- Server: `dfadnfvi@77.83.100.124` (Hetzner box, cPanel host
  `pl-rocket-cms1.hostsila.org`), port 22.
- Quick connect: `ssh -i ~/.ssh/splitcam_deploy dfadnfvi@77.83.100.124`.
- Note: `splitcam.com` itself is fronted by Cloudflare, so SSH only via the
  direct IP — `ssh dfadnfvi@splitcam.com` fails (CF doesn't proxy SSH).
- Site root on server: `~/public_html` (19 GB; 17 GB is the
  `win-download/update/` installer archive, the rest is the live PHP site
  + WP blog/forum).

### API tokens (saved locally; rotate when convenient)
- **Cloudflare** — `~/.cloudflare_token`, scoped to zones `splitcamera.com`
  + `splitcam.com`, **Analytics: Read only**. Use:
  `curl -H "Authorization: Bearer $(cat ~/.cloudflare_token)" …`.
- **Ahrefs** — `~/.ahrefs_token`, used by `seo/ahrefs.py` as:
  `AHREFS_TOKEN=$(cat ~/.ahrefs_token) python3 ahrefs.py`. Lite plan, 100k
  units/mo.
- ⚠️ Both tokens were pasted in chat earlier — rotate when you can
  (Cloudflare → API Tokens → Roll; Ahrefs → Account → API → regenerate),
  then overwrite the file with the new value. The file paths don't change.
- The server password the user pasted in chat — **never saved on disk**.
  SSH-key login replaces it; change the password in the cPanel panel when
  you can.

### What the redirect-rule fix bought us (2026-05-22)
Side-effect worth knowing: after the `http.host contains "splitcamera.com"`
rule went live, Cloudflare's auto-protection started 403-blocking a
botnet (~3.5 M req/14 h, 49% PH, 17% CI) hitting `www.splitcamera.com`. As
a result, splitcam.com Cloudflare traffic dropped **−86.6%** in the same
10-hour window vs the previous day, origin-server traffic dropped −20%
(~70k fewer requests/day). The blocking is correct — bots, not users.
Documented in Cloudflare Analytics (free plan).

## Communication style with user
- Russian (mostly) + English code/labels. Concise, concrete next steps.
- Show before/after for visual changes. Commit individually so revert is easy.
- Share live URL after pushes; remind about `Cmd+Shift+R` (browser cache).
- User makes the calls — present 2-3 options when in doubt. Execute mode preferred over endless planning.

## How to deploy (either repo)
```bash
cd "/Users/splitcam/Documents/Дизайны/SplitCam/SPLITCAM DEV./<repo>"
git add . && git commit -m "..." && git push origin main
```
Revert: `git revert HEAD --no-edit && git push`.

## Session log — 2026-06-07 (UI polish + perf + SEO pass)

Big sweep across the public site. Themes:

**Video / perf — flicker fix (important pattern).** The `ms-flow-vis`
fan diagrams on **/multistreaming/** and **/virtual-camera/** each ran
**6 simultaneous `<video>` of `stream-preview.mp4`** (unsynced loops,
no poster) → visible flicker + decode load. Fix: replaced every preview
`<video>` with a static poster frame
(`multistreaming/assets/stream-preview-poster.jpg`, extracted via
ffmpeg). Both blocks are now fully static imagery; "live" feel comes
from CSS only (blinking LIVE badge, flow-pulse dots, colored
active-stream bars). CSS scoped to **direct children**
(`.ms-platform-card>img`) so the small app/platform logo `<img>`s in the
labels keep their icon size. `stream-preview.mp4` is now unused but
**kept on disk on purpose** (reserve). Homepage's 4 videos
(hero-spotlight, audience-scene, audience-game/Apex PiP, vc-presenter)
are different single-instance clips with posters + an off-screen pause
observer — left as real video (genuine motion), not flickering.

**Mobile centering / hero reorder.** Homepage hero fully centered on
≤900px (title, desc, Download split-button, badges, rating chip).
Section CTA buttons ("See how multistreaming works", "See compatible
apps") centered on mobile. SEO/`for`/`alternatives` pages got a mobile
hero reorder (H1 → visual/orb → Download → copy) + centered CTA.
Homepage multistream `bc-rows` viz was cramped on mobile (animated bar
squished to ~38px) — shrank `.bc-nm`/`.bc-kbps`, trimmed padding, added
`white-space:nowrap` so the bar is ~112px and rows are a uniform 38px.
Verified `scrollWidth == innerWidth` at 390px on every change.

**/products/ cleanup.** Removed the hero download split-button +
platform dropdown + "Compare all platforms" (redundant above the card
grid). Bottom-aligned the 4 platform cards' download buttons
(flex column + `margin-top:auto`) so they line up across each row.
Hero sub now leads with "Every SplitCam download is free" (SEO).
Both Remote store buttons are grey "Coming soon".

**Rating.** Now **4.7 / 357 reviews**, visible-only (hero chip + stats).
**`aggregateRating` stripped from every page's JSON-LD** so Google gets
no review-snippet markup — see Critical rule #7 in CLAUDE.md. Never
re-add it.

**SEO keyword pass (Ahrefs-backed, per-page, no cannibalization).**
Audited meta-vs-body; wove each page's own missing title keyword into
body copy — homepage: "free streaming software" (450), "free live
streaming software" (350), "stream/broadcast to multiple platforms",
"virtual camera for zoom", "virtual webcam"; /virtual-camera/: "virtual
camera for Zoom"; /products/: "SplitCam download"; /multistreaming/:
"broadcast to multiple platforms". Alternative-keywords
(restream/streamyard/streamlabs/manycam) deliberately left for the
planned `/alternatives/*` Wave-2 pages.

**Icons / content.** Feature grid + "What's new" switched to a unified
Lucide line-art set; "What's new" now lists 6 real recent features
(Restream Server Picker, Vertical Canvas, Replay, 3D Transform, Luma
Wipe/Slide/Swipe, Virtual Camera Routing) from the changelog. Use-case
cards got themed icons (YouTube red play SVG, trophy, theatre mask).
"How creators use it" expanded 3→6 stories. SplitCam Remote phone
mockup on /products/ = real iPhone screenshot + CSS overlays (LIVE
square, green platform badges, SplitCam·REMOTE pill); Remote pairing
copy fixed to mention QR + auto-discovery (never "no QR").

(GA4 `G-S1THLDP1XV` is on all public pages. `/for/vtubers/` exists as a
noindex DRAFT, not yet enabled.)

## Session log — 2026-06-09 (mini iteration)

Small visual tweaks on **/virtual-camera/** orbit-center SplitCam logo:
- Desktop: 66 → 57 → 55 → **60** px (net ≈ −9% from original; bumped
  back up after we shrunk too far).
- Mobile (≤900px): added a separate rule, **49** px (≈ −17% from
  desktop original 66, so mobile reads as a touch smaller in the
  cramped vertical hero stack).

(No other site-wide changes this iteration.)

## Session log — 2026-06-11 (overdue SEO reminders sweep + Remote iOS live)

Worked through the overdue items in `seo/REMINDERS.md` (full results live there):

- **Play Store check:** main mobile apps are live on both stores and were
  already linked from the `/products/` cards. **SplitCam Remote for iOS is
  LIVE** — App Store `id6760961594`, v1.2, iOS 17+, released 2026-05-19.
  Android Remote not released (dev page lists only `com.splitcam`).
  → `/products/` Remote section: App Store button is now a real link
  (promoted to solid `btn-store`), Google Play stays "Coming soon";
  Pair Step-02 copy, JSON-LD (`operatingSystem: iOS` + `installUrl`) and
  the `/changelog/` Remote panel updated. Commit `4ba08fd`. macOS support
  of Remote confirmed via the Mac app v1.13 release notes.
- **Indexing/ranking checks (weeks 1-2):** staging is **NOT indexed** —
  `site:` empty, Ahrefs 0 keywords for the `x270880x.github.io/splitcam/`
  prefix, no GSC property. Open decision: set up GSC for staging (HTML-file
  verification + sitemap submit) vs. wait for the splitcam.com migration.
- **Wave 2:** user asked for go/no-go. Scope refined: `/for/vtubers/` exists
  as a noindex draft (enable, don't rebuild); mobile burger already shipped
  site-wide on 2026-06-07, so remaining nav work = desktop dropdowns for
  Alternatives/Use Cases (+ optional `nav.js` extraction).
- `/products/remote/` page decision stays parked until Android Remote ships.

## Session log — 2026-06-12 (later same day)

- **Homepage pill-dot fix (`91e6c3c`):** the green "Live Multi-Streaming
  Studio" hero dot looked static — two `@keyframes` were both named
  `live-pulse` and the stats-dot one overrode the hero rings. Renamed the
  hero animation `pill-sonar`. Lesson: keyframes names are global per page.
- **Multistreaming scene-preview video restored (`80075e0`), desktop-only,**
  per user — partial revision of the 2026-06-07 "fully static" decision.
  The BIG `.ms-scene-preview` is a looping video again; the six platform
  thumbs stay static posters (six parallel loops were the flicker source).
  Implementation: poster `<img>` in HTML; JS swaps in ONE `<video>` only
  at >900px (mobile downloads nothing), `preload=metadata`, plays only
  in-view + visible tab (IO + visibilitychange), reduced-motion respected.
  Assets: `stream-preview-av1.mp4` 87KB (svt-av1 crf52, codecs string
  `av01.0.04M.08`) + `stream-preview-h264.mp4` 147KB (x264 crf33) — master
  `stream-preview.mp4` (375KB) kept untouched as the re-encode source.

## Session log — 2026-06-12 (full link & interlinking audit)

Built `seo/linkcheck.py` and ran a site-wide audit (user request):

- **Links: clean.** 0 broken internal links / anchors / resources / slash
  redirects across all 15 pages. External 29/31 OK; facebook.com 400 is
  bot-blocking only (200 with a mobile UA). Sitemap ↔ disk in full sync;
  noindex pages excluded; nothing links to the vtubers draft.
- **One real dead external:** `installmonetizer.com` (domain gone) in
  `/privacy-policy/` — a whole legacy "InstallMonetizer products" section
  from the old site references a dead service. **OPEN: user to decide —
  delete the section vs unlink.** Likely the policy text predates reality.
- **Interlinking verdict:** structurally sufficient (flat ≤1-click
  architecture, hubs↔leaves, RELATED blocks, breadcrumbs; feature pages
  correctly get the most contextual weight). Two gaps: (1) SEO leaves have
  zero nav presence — fixed by Wave 2 dropdowns when they come; (2) feature
  pages didn't link down to leaves with keyword anchors — **fixed** (commit
  `2fcad1c`): 4 links added (ms→churches, ms→youtubers, vc→youtubers,
  vc→obs; JSON-LD FAQ mirrored). Leaves now: youtubers 7 / churches 5 /
  obs 6 contextual inlinks.

## Recent commits — main splitcam repo (most recent first)
```
65e5745 seo/linkcheck.py: site-wide link & interlinking audit tool
2fcad1c Interlinking: keyword-anchor links from feature pages down to SEO leaves
5311488 REMINDERS: Wave 2 + GSC-staging postponed by user; revisit at Month-1 review
684e45c REMINDERS: staging is unindexable by design (canonicals -> splitcam.com)
a496694 ONBOARDING + REMINDERS: log 2026-06-11 sweep
4ba08fd SplitCam Remote for iOS is live: activate App Store button on /products/
28be593 Virtual-camera hero: shrink mobile orbit-center logo (54 → 49px); desktop 60
c243ef9 Virtual-camera hero: bump orbit-center logo 10% on desktop (55 → 60px)
717e327 Virtual-camera hero: orbit-center logo 2% smaller on mobile (54px)
d1dc7b7 Virtual-camera hero: orbit-center logo 57 → 55px
cd3429d Virtual-camera hero: shrink the orbit-center SplitCam logo 13% (66 → 57px)
3dab94f ONBOARDING: log the 2026-06-07 UI/perf/SEO session + refresh commit list
e8d0b05 Center hero CTA on mobile (/alternatives/obs/)
79f4794 Mobile hero reorder + centered CTA on /virtual-camera/
9cfaf9a Mobile hero reorder + centered CTA on /multistreaming/
8f049f9 Mobile hero reorder on /for/churches/: H1 → visual → Download → copy
b1f2504 Virtual-camera viz: 6 videos → static (flicker fix)
3d5ce08 Multistreaming viz: go fully static — kill the last looping video
5acd204 Multistreaming viz: stop the flicker — 6 videos → 1 + posters
c02721f Homepage mobile: center section CTA buttons + fix cramped multistream viz
f4229bd Homepage hero: center everything on mobile
18bbc00 Products hero: drop the download split-button, dropdown and Compare
fe536c1 Products: bottom-align the download buttons across each card row
```
(cam-streaming-guides repo has its own history — full adult-guides build.)
