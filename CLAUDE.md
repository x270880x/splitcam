# CLAUDE.md — SplitCam main site

Shared context for terminal sessions and Dispatch sessions. Read this first.
Companion doc with fuller history: `ONBOARDING.md`.

## What this is

Marketing site for **SplitCam** — free streaming / virtual-camera software.
Static HTML/CSS/JS, no build step. This is the redesign destined to replace the
real **splitcam.com** (migration plan in `seo/MIGRATION.md`).

Sibling repo `../cam-streaming-guides/` holds the adult-cam how-to guides (separate
project, separate domain) — not covered here.

## Stack & structure

- Plain HTML/CSS/JS. No `package.json`, no bundler, no framework.
- Inline `<style>`/`<script>` per page. Dark theme: `--app-base:#141420`,
  `--blue:#2878fc`, `--purple:#9c5bff`. Font: Geist.
- `/seo/` — Python tooling: Ahrefs analytics (`ahrefs.py`, `pages.py`,
  `domains.py`) + `linkcheck.py` (site-wide link & interlinking audit — run
  after adding pages and before migration) + planning docs (`PLAN.md`,
  `SITEMAP.md`, `MIGRATION.md`, `REDIRECTS.md`, `REMINDERS.md`). Raw data
  in `seo/data/*.json` (gitignored).

Pages (7 public + 1 archived):

| Path | Note |
|---|---|
| `/` | Main landing — **Variant A is final** |
| `/v2/` | Variant B — archived, `noindex`, unlinked. Reference only. |
| `/virtual-camera/` | Feature page |
| `/multistreaming/` | Feature page |
| `/products/` | Products hub — Win / macOS / iOS / Android + SplitCam Remote |
| `/for/youtubers/` | SEO Wave 1 — structural template for SEO pages |
| `/for/churches/` | SEO Wave 1 |
| `/alternatives/obs/` | SEO Wave 1 |

SEO page template (from `/for/youtubers/`): NAV / BREADCRUMBS / HERO / QUICK
ANSWER / STEP-BY-STEP / BONUS / PRO TIPS / COMPARISON / FAQ / RELATED / CTA / FOOTER.

**SEO pages get unique body text.** The template (section order, CSS, nav,
footer) is shared, but the *prose* is not — never copy-paste step-by-step blocks
or feature blurbs between `/for/` and `/alternatives/` pages. Each page gets its
own examples, step ordering and audience framing (creator workflow vs church AV
team vs OBS migration, etc.). Near-duplicate body text triggers keyword
cannibalization. Audit with `seo/PAGE-SIMILARITY.md` after adding pages.

## Deploy

GitHub Pages, repo `x270880x/splitcam`, staging at
https://x270880x.github.io/splitcam/ (auto-deploys 30–90 s after push).

```bash
git add . && git commit -m "..." && git push origin main
```

Revert: `git revert HEAD --no-edit && git push`.
**Workflow rule:** after meaningful edits, commit + push immediately — don't ask.
Commit individually so any single change is easy to revert. After a push, share
the live URL and remind about `Cmd+Shift+R` (browser cache).

## Current state

- Homepage A/B resolved (2026-05-22): Variant A is final, `/v2/` archived.
- Site-wide version is **v10.9.2**. No installer size shown.
- Working tree clean as of last check; branch `main`.

## Infrastructure access (set up 2026-05-22 / 23)

- **GitHub: `x270880x/splitcam-release`** (public) — 36 releases, all Windows
  `.msi` installers from `splitcam.com/win-download/update/` (9.0.9 → 10.9.2)
  + the `10.8.62-restream-test` prerelease. Each release has the matching
  changelog from `splitcam-changes-win` / `history.txt` in its notes (24 with
  full changelog, 11 interim builds with a generic note + link).
- **GitHub: `x270880x/old_splitcam_site`** (PRIVATE 🔒) — full backup of the
  old splitcam.com `public_html` (excl. installers), in release
  `backup-2026-05-23` as `old_splitcam_site.tar.gz` (1.4 GB). Private because
  it contains `wp-config.php` with DB creds. Never make public.
- **SSH to splitcam.com server:** key at `~/.ssh/splitcam_deploy` (Ed25519,
  Mac-local). Server: `dfadnfvi@77.83.100.124` (cPanel host
  `pl-rocket-cms1.hostsila.org`), port 22. Note: `splitcam.com` itself is
  fronted by Cloudflare, SSH-only via the direct IP.
- **Cloudflare API token:** `~/.cloudflare_token` (chmod 600), scoped to zones
  `splitcamera.com` + `splitcam.com`, Analytics: Read only. Used for
  GraphQL Analytics queries — never echo or log the token; reference via
  `$(cat ~/.cloudflare_token)` inside curl headers only. **Was pasted in
  chat — rotate after the next use** (Cloudflare → API Tokens → Roll).
- **Ahrefs API token:** `~/.ahrefs_token` (chmod 600). Use with
  `seo/ahrefs.py` via `AHREFS_TOKEN=$(cat ~/.ahrefs_token) python3 ahrefs.py`.
  Same warning — was exposed in chat earlier, rotate when convenient
  (Ahrefs → Account → API → regenerate). Note "Important notes" #1
  below predates this file — the token IS still in this file until rotated.
- **Iso card honesty:** `/products/` iOS card has two features dimmed and
  tagged `in development` (AR filters, Picture-in-picture) — don't reword
  them as if they ship.

## Done — SEO Wave 1 ✅

`/for/youtubers/`, `/for/churches/`, `/alternatives/obs/` — all built & live.

## In progress / queued

- **SEO Wave 2** (~2026-06-10): `/alternatives/` hub, `/for/` hub,
  `/alternatives/{restream,streamyard,streamlabs}/`, `/for/vtubers/`.
- **Wave 3** (later): remaining alternatives + `/for/{streamers,educators}/`.
- **Migration to live splitcam.com**: only `/` is a true same-URL replacement;
  everything else is new URLs. See `seo/MIGRATION.md` + `seo/REDIRECTS.md`.
  Multi-locale — **all 35 languages DONE 2026-06-15** (see below).

## Localization — all 35 languages (built 2026-06-13 → 06-15)

Every page exists in **35 locales**: EN (root) + 34 under `/<lang>/...`:
**ru es de fr pt tr fil uk it vi id nl ro hi ja ms bg ar ko th pl hu sv zh el cs
he sr hr da fi no sk fa** (ar/he/fa are RTL). That's all 13 pages (10 content +
`privacy-policy/` + `license-agreement/` full, + `changelog/` shell-only — its
~1817 technical release bullets stay EN) × 35 = **455 indexable pages**.
Untranslated: `/v2/` (archived), `for/vtubers/` (noindex draft).

Built by Ahrefs "splitcam" demand: top 18 first (2026-06-13), then the remaining
17 (Waves 4–7 — ≤10/mo demand, mostly 0) completed 2026-06-15 for brand
completeness. `seo/i18n.py` `waves()` confirms 0 left. **RTL** (ar/he/fa) is
handled by `i18n.RTL_CSS` (forward-arrow flip via `svg:has(use[href="#i-arr"])`,
download split-button radii, vc-arrow connector) injected per RTL page by
`i18n_wire.py` into a regenerated `<!--RTLCSS-->` marker region.

> **Wave 4–7 build note (2026-06-15):** an earlier unattended run mass-translated
> these locales from a Bulgarian (`bg/`) scaffold and left systematic bugs —
> canonical/og/JSON-LD URLs pointing at `/bg/`, smart-quoted HTML attributes
> (broke links), and a few untranslated/Bulgarian pages. All were cleaned + the
> affected locales retranslated fresh from EN. If re-running a wave, **translate
> from `index.html` (EN), never from another locale's scaffold, and use only
> straight ASCII quotes in attributes/JSON-LD.**
>
> **QA addendum (2026-06-15 audit — full detail in `ONBOARDING.md`):** after any
> locale batch, run a mechanical full-site scan — lang tag · Cyrillic outside
> `<!--LD/HL/AD-->` · `„`/`”` quote glyphs · `<style>`/`<script>`/`<details>`
> balance · `json.loads` on every `ld+json`. Notes: the `„…"` low-quote is
> **correct** for de/bg/ro/pl/cs/hu/hr/sr/sk but a **bug** in th/he/ja/ko/zh/vi/
> hi/ar/fa (bg-scaffold residue) — scope `„` scans to those. Replacing `„X"`→`"X"`
> *inside* a JSON-LD value breaks the JSON (escape inner quotes `\"`). The Twitch
> simulcast date on `multistreaming` is **October 2023** everywhere (an EN-source
> "June 2024" once contradicted it across 13 locales). `fa` demand is unmeasurable
> (Ahrefs excludes Iran). Don't sample 3 pages/locale — bugs hide on all 13.

### The i18n engine (no build step — these two files ARE the system)
- **`seo/i18n.py`** — single source of truth: `LANG_ORDER` (demand-sorted),
  `LANG_DONE`, native names/flags/labels/paths, RTL set, `DEMAND`, and render
  helpers (`dropdown()`, `hreflang_block()`, `AUTO_DETECT_JS`, `DROPDOWN_CSS`).
- **`seo/i18n_wire.py`** — run it after adding/translating pages. It rebuilds,
  per page, listing **only the locales where that page exists on disk**: the
  `<details>` language dropdown (flags + native names, nav + burger), the
  hreflang block, the browser-language auto-redirect JS, the dropdown CSS, and
  `sitemap.xml`. Idempotent (marker-based). Also rewrites a locale page's
  sibling links to the EN fallback when the localized sibling doesn't exist yet
  (so partial waves never 404). **`python3 seo/i18n_wire.py` then
  `python3 seo/linkcheck.py --no-network` (must be 0 broken).**

### How to add languages (the proven pipeline)
1. Ahrefs per market → append a Wave table to `seo/I18N-KEYWORDS.md`.
2. Spawn ~5 parallel translation agents (one per language) per batch:
   homepage → SEO-core (vc/multistreaming/obs/youtubers) → rest → utility.
   Each reads the EN source for content + `ru/<page>/` for the exact
   path-shifts at that depth; switcher/hreflang are placeholders (the wiring
   rewrites them). Account session limits hit ~mid-large-batch — retry the
   failed locale's remaining pages.
3. Run `i18n_wire.py`, linkcheck, mark the langs in `LANG_DONE`, commit.

### Per-locale rules (binding: `seo/I18N-PLAN.md` — read before editing a localized page)
- **SEO:** Ahrefs per locale → the language's real keyword in title + meta
  description + H1 (NOT a literal EN translation). `seo/I18N-KEYWORDS.md` has
  the per-page map for all 18. Notable: **fil + hi search tech in ENGLISH**
  (English titles/keywords, local-language body); ja/de/etc. use their own.
- **Layout (mandatory, user 2026-06-13):** translated text is longer →
  `white-space:nowrap` on any translatable text is a bug; headings/hero use
  `white-space:normal` + `overflow-wrap:break-word`; nav collapses to burger
  ≤1100px. Check no overflow/clip/overlap at 1440/1280/390. Verify balanced
  `<style>…</style>` per file (an agent once shipped an unclosed one that broke
  the whole page render).
- **hreflang reciprocity** across all 34 + EN; **no `aggregateRating`** in any
  JSON-LD (crit rule #7); GA gtag byte-identical; canonicals → future
  `splitcam.com/<locale>/...`.
- **New EN page ⇒ build all 34 locales + rerun `i18n_wire.py`** (which adds it
  to every dropdown/hreflang/sitemap). Edit EN copy ⇒ mirror to 17. See
  [[feedback_multilang_sync]].
- Full SEO plan: `seo/PLAN.md`. Recommended IA: `seo/SITEMAP.md`.
  Schedule & follow-ups: `seo/REMINDERS.md` (open it in any SEO chat).

## Important notes

1. **`AHREFS_TOKEN` must be regenerated** — it was exposed in chat. Set the new
   token as an env var; never commit it. Ahrefs Lite plan, 100k units/mo.
2. Brand logos stored LOCALLY in `/virtual-camera/assets/logos/` — no external CDN.
3. SplitCam logo at `/assets/splitcam.png` — used via `<img>`, not base64.
4. No "Restream server" / "cloud middleman" wording — SplitCam is **peer-to-peer
   direct**.
5. iOS belongs in the platforms list (Win · macOS · iOS · Android).
6. **Skype is dead** (Microsoft retired it May 2025) — never mention it as live.
7. Rating = **4.7 / 357 reviews**, shown ONLY as a visible trust signal
   (homepage hero chip + stats box). **Never put it back into Schema.org**
   (`aggregateRating` was deliberately stripped from every page's JSON-LD
   so Google gets no review-snippet markup — avoids a structured-data
   manual action on a self-asserted rating). Real source ratings:
   Softonic 4.7, UpdateStar 4.0, G2. Don't add `aggregateRating` /
   `ratingValue` / `Review` markup to any indexed page.
8. LIVE badges blink (badge opacity + red dot pulse).
9. Each page needs the full favicon set + Schema.org (≥ BreadcrumbList +
   SoftwareApplication; bigger pages add HowTo + FAQPage).
10. Do NOT use `CronCreate` for SEO scheduling — it doesn't persist. Use
    `seo/REMINDERS.md`.

## Content check-list — run before committing any copy change

Whenever you add or rewrite user-facing text (steps, blurbs, headings, FAQ,
meta), verify all four before committing:

- **(a) Clarity & readability** — would the target reader understand it on the
  first pass? No truncated or garbled sentences, no jarring topic jumps.
- **(b) Plain, accessible wording** — no calques, no unexplained jargon, no
  awkward literal translations. Write like a native human, not an editor patching
  a string.
- **(c) On-topic for the page & audience** — language matches who the page is
  for (YouTube creator vs church AV volunteer vs OBS migrator). Don't leak
  generic copy that narrows or widens the audience by accident.
- **(d) Factual correctness & cross-page consistency** — versions (v10.9.2),
  feature names, platform lists (Win · macOS · iOS · Android), and numbers (e.g.
  "84+ platforms") must be correct AND identical across every page. One feature =
  one name everywhere. Check neighbouring untouched text still agrees with the
  edit.

## Mobile check — run after ANY layout or content change

The site is mobile-first traffic. After any edit to markup, CSS, or copy,
verify the mobile rendering before committing — never assume it's fine:

- Render every affected page in a headless browser at a **~390px viewport**
  (`puppeteer-core` + the system Chrome works; no Chromium download needed).
- Confirm **no horizontal body scroll** — `document.documentElement.scrollWidth`
  must equal `window.innerWidth`. Any excess means something overflows.
- Confirm nothing runs off-screen, blocks are aligned, padding is even, text is
  readable, and the page looks tidy — not just "no errors".
- Wide elements (tables, code blocks, media) must scroll inside their own
  container, never push the page wider.
- Re-check **desktop (~1440px)** too, so the mobile fix didn't regress it.
- Save proof screenshots to `seo/screenshots/` and actually open them to look.

## Working with the user

Russian (mostly) + English code/labels. Concise, concrete next steps. Show
before/after for visual changes. Present 2–3 options when in doubt — the user
makes the calls. Execute over endless planning.
