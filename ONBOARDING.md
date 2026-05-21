# SplitCam — Project Onboarding

*Last updated: 2026-05-21. Open this at the start of any new chat to get up to speed.*

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

## Pages deployed (8)
| Path | Note |
|---|---|
| `/` | Main landing (Variant A) |
| `/v2/` | Main landing Variant B — A/B variant, **pick A or B before going to splitcam.com** |
| `/virtual-camera/` | Feature page |
| `/multistreaming/` | Feature page |
| `/products/` | Products hub — Windows/Mac/iOS/Android + SplitCam Remote |
| `/for/youtubers/` | SEO Wave 1 — "how to live stream on youtube" |
| `/for/churches/` | SEO Wave 1 — "church streaming software" |
| `/alternatives/obs/` | SEO Wave 1 — "obs alternative" |

## SEO status
- **Wave 1 — DONE** ✅ (youtubers, churches, obs — all built & live).
- **Wave 2 — pending (~2026-06-10):** `/alternatives/` hub, `/for/` hub, `/alternatives/{restream,streamyard,streamlabs}/`, `/for/vtubers/`.
- **Wave 3 — later:** remaining alternatives + `/for/{streamers,educators}/`.
- Full plan: `seo/PLAN.md`. Recommended IA: `seo/SITEMAP.md`.
- **Schedule & follow-ups: `seo/REMINDERS.md`** — open it in any SEO chat (indexing checks, ranking checks, wave launches with dates). Do NOT use `CronCreate` — it doesn't persist.

## Migration to live splitcam.com
`seo/MIGRATION.md` — only the homepage `/` is a true same-URL replacement; everything else is new URLs. `seo/REDIRECTS.md` — 301 strategy + per-page weights from Ahrefs. Open decisions: homepage A vs B, RU/ES locales.

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
- Nav (7 pages): Products · Virtual Camera · Multistreaming · What's New · Help. `/v2/` has its own nav.
- Each page: favicon set + Schema.org (≥ BreadcrumbList + SoftwareApplication; bigger pages add HowTo + FAQPage).
- `/for/youtubers/` is the structural template for SEO pages: NAV / BREADCRUMBS / HERO / QUICK ANSWER / STEP-BY-STEP / BONUS / PRO TIPS / COMPARISON / FAQ / RELATED / CTA / FOOTER.

## /seo/ folder
- `ahrefs.py` — domain + keyword collector · `pages.py` — per-URL weight · `domains.py` — domain weight checker
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
| multi-stream.io | 14 | live, ranks for "free multistreaming" — possible cannibalization with `/multistreaming/` |
| splitstream.com | 4 | live, weak — candidate to 301 → splitcam.com |
| split.cam | 0 | dormant, clean brand domain — reserve / short links |
| (adult) | — | new neutral domain still to register |

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

## Recent commits — main splitcam repo (most recent first)
```
7a14118 SEO: add domain weight checker (seo/domains.py)
a0f1a9d SEO: per-page weight collector + redirect strategy
ba62fbe SEO: add live-site migration plan (seo/MIGRATION.md)
8de62db SEO: add recommended sitemap + interlinking map (seo/SITEMAP.md)
7ed026b Update version to v10.9.2 site-wide; remove ~85 MB; add Products to nav
5c6f138 Add /products/ hub page
91c575a SEO Wave 1 page 3: /alternatives/obs/
20d2c7c SEO Wave 1 page 2: /for/churches/
```
(cam-streaming-guides repo has its own history — full adult-guides build.)
