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
- `/seo/` — Python tooling for Ahrefs analytics (`ahrefs.py`, `pages.py`,
  `domains.py`) + planning docs (`PLAN.md`, `SITEMAP.md`, `MIGRATION.md`,
  `REDIRECTS.md`, `REMINDERS.md`). Raw data in `seo/data/*.json` (gitignored).

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

## Done — SEO Wave 1 ✅

`/for/youtubers/`, `/for/churches/`, `/alternatives/obs/` — all built & live.

## In progress / queued

- **SEO Wave 2** (~2026-06-10): `/alternatives/` hub, `/for/` hub,
  `/alternatives/{restream,streamyard,streamlabs}/`, `/for/vtubers/`.
- **Wave 3** (later): remaining alternatives + `/for/{streamers,educators}/`.
- **Migration to live splitcam.com**: only `/` is a true same-URL replacement;
  everything else is new URLs. See `seo/MIGRATION.md` + `seo/REDIRECTS.md`.
  Open decision: RU/ES locales.
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
7. CNET 4.5/357 rating is UNVERIFIED — still in Schema.org/Hero; user hasn't
   decided to remove. Real ratings: Softonic 4.7, UpdateStar 4.0, G2.
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
