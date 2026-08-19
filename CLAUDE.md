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

Pages (9 public + 1 archived):

| Path | Note |
|---|---|
| `/` | Main landing — **Variant A is final** |
| `/v2/` | Variant B — archived, `noindex`, unlinked. Reference only. |
| `/features/` | Features hub (all 35 locales) — replaces live splitcam.com/features. Not in global nav yet. |
| `/virtual-camera/` | Feature page |
| `/multistreaming/` | Feature page |
| `/virtual-audio-mac/` | **EN-only.** macOS virtual audio driver + its standalone installer (`mac-download/SplitCamVirtualAudio.pkg`). Entry points: the macOS cards on `/download/` and `/products/`, plus the combined hub card. |
| `/virtual-audio-windows/` | **EN-only.** The Windows virtual audio device, which ships inside SplitCam's own setup — no driver download exists for Windows. Entry point: the combined hub card. |
| `/products/` | Products hub — Win / macOS / iOS / Android + SplitCam Remote |
| `/donate-us/` | Donate page (all 35 locales) — donations go to **paypal.me/Katzovich**, amount chips are clickable links ($25-$1000). Keep-URL, matches live. |
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

**Release rule (user, 2026-07-14):** a build the user calls **beta** is **changelog-only** —
never touch the homepage version, never overwrite the latest pointers
(`win-download/SplitCamSetup_x64.msi`, `mac-download/SplitCam.dmg`), never bump `ver.txt` /
`macver.plist` / `versions.json`. **Applies even if the beta's number is higher than the
current stable.** Full rule + the stable-release flow: the **`splitcam-release` skill**
(it loads when you publish a build; `seo/REMINDERS.md` keeps only the summary).
Commit individually so any single change is easy to revert. After a push, share
the live URL and remind about `Cmd+Shift+R` (browser cache).

## Current state

- 🔴 **THE SERVER MOVED. Verified on the box 2026-08-12: web AND mail are both on
  `77.83.100.153`, panel `https://pl-rocket-da3.hostsila.org:2222/`, SSH
  `lwanngbs@77.83.100.153:22`, creds `~/.hostsila_da_ssh`, docroot
  `/home/lwanngbs/domains/splitcam.com/public_html`.** Confirmed live, not a staging copy:
  the access logs show current Cloudflare edge IPs (`172.69.x`, `172.70.x`, `104.23.x`)
  proxying `www.splitcam.com:443` to this box, ~20 MB of gzipped log per day. Mailboxes
  here: `admin`, `support`, `pola`. Every `185.67.3.44` / `rocket-da4` reference below and
  in `ONBOARDING.md` predates this move and is stale. **Do not trust "the server answers"
  as evidence** — `185.67.3.44`, `77.83.100.124` and `91.223.223.113` all still serve the
  site over HTTP and answer Dovecot on 993; only DNS and the logs are decisive.
  Dating the move: the `support@` maildir has mail delivered by `rocket-da4` up to 20 Jul
  and by `pl-rocket-da3` from 22 Jul on, so it happened in that gap and no doc recorded it.
- **Mail on the current box:** Exim 4.99.4 answering on 25 / 465 / 587, Dovecot on 993,
  mailboxes `admin`, `support`, `pola`; external mail demonstrably arriving.
  **`_dmarc.splitcam.com` is `p=reject`** — anything sending as `@splitcam.com` must go out
  through `mail.splitcam.com` SMTP, never through Gmail/Google IPs, or it is rejected
  outright (SPF unauthorized + DKIM signed by the wrong domain). Details: `seo/REMINDERS.md`.
  ⚠️ **SMTP cannot be tested from the work Mac** — 25/587/465 accept TCP there and close
  without a banner, which looks like a server-side block but is not: `smtp.gmail.com` and
  `smtp.yandex.ru` behave identically from that machine. Test SMTP over SSH, from inside.
  The ~8 days of mail (07-06 → 07-14) that stayed on cPanel were **written off by the
  user 2026-07-19** — not recovered, don't reopen. cPanel can be cancelled freely.
  Earlier cutovers (07-02 → cPanel `91.223.223.113`, 07-06 → DA `185.67.3.44`) and the
  rollback recipes for them: `seo/REMINDERS-LOG.md`.
- Homepage A/B resolved (2026-05-22): Variant A is final, `/v2/` archived.
- Site-wide version is **v10.9.2**. No installer size shown.
- **Deploy is site-wide via GitHub tarball → host overlay-copy** (not GitHub Pages, though
  that still auto-builds as staging). After any redirect change, keep the host docroot
  `.htaccess` = `seo/redirects.htaccess` and **purge Cloudflare cache**.
- Installers: host keeps 10.8.x–10.9.2 only; ≤10.7 + 4.x–8.x museum live on GitHub
  `x270880x/splitcam-release` (old URLs 301 to the same version's GitHub asset).

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
he sr hr da fi no sk fa** (ar/he/fa are RTL). That's all 15 pages (12 content +
`privacy-policy/` + `license-agreement/` full, + `changelog/` shell-only — its
~1817 technical release bullets stay EN) × 35 = **527 indexable pages** (incl. EN-only /download landing; verified against `sitemap.xml` 2026-07-19 — the older 526 figure predates `/plugins/`).
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
> **QA addendum (2026-06-28 audit — full detail in `ONBOARDING.md`):** after any
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

## RTL trap — never add CSS right after `<!--/RTLCSS-->`

The RTL locales (`ar`, `he`, `fa`) carry a `<!--RTLCSS-->` … `<!--/RTLCSS-->` marker region
**inside the page's `<style>` block**. Those markers are HTML comments, and HTML comments are
NOT valid CSS. The parser reads `<!--` as an ignorable CDO token, then treats `/RTLCSS` as the
start of a selector and swallows everything up to the next `{` — **silently eating the first
CSS rule that follows the closing marker**.

Hit for real 2026-07-18: a new `.rt-strip{max-width:1100px;…}` inserted right after
`<!--/RTLCSS-->` was destroyed on all three RTL pages (the strip stretched full-width), while
every later rule in the same block applied normally — which makes it look like a layout bug,
not a parsing bug.

**Rule: append new CSS BEFORE `<!--RTLCSS-->`, or before `</style>` on non-RTL pages.**
Inserting before the marker is also safe against `i18n_wire.py`, which regenerates only the
marker region. After any CSS insertion, verify on an RTL page that the first new rule actually
computes (`getComputedStyle(el).maxWidth` etc.), not just that the file contains the text.

## Important notes

0. **ALL internal URLs must be FULL absolute canonical** (`https://splitcam.com/...`,
   slashless for sub-pages, slash only for `/` and locale roots `/ru/`) — this covers
   `src`/`poster`/icons AND every `<a href>`. Pages are served at slashless canonical
   URLs, so page-relative paths resolve against the wrong base: images 404'd (orbit
   logos, 2026-07-02) and nav links DROPPED THE LOCALE (he/features -> EN products,
   2026-07-03). Enforced across all 527 pages (5369 subresources + 15807 anchors);
   `i18n.dropdown()` emits absolute; `linkcheck.py` validates absolute-internal against
   disk. Any NEW page/link/image must follow this.


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
10. Do NOT use `CronCreate` for SEO scheduling — it is session-only (in-memory,
    dies with the session, auto-expires after 7 days). **But `scheduled-tasks`
    IS durable** — it writes to `~/.claude/scheduled-tasks/<id>/SKILL.md` and
    survives restarts. Since 2026-07-19 three weekly tasks run from there:
    `splitcam-seo-weekly` (Mon), `reminders-overdue-check` (Mon),
    `repo-hygiene-weekly` (Fri) — all set to stay silent unless they find
    something. `seo/REMINDERS.md` remains the record of *what* is scheduled and
    why; the tasks are what actually fires. Note that a scheduled task only runs
    while the app is open (a missed run fires on next launch).

## /virtual-audio/ — the macOS audio driver (added 2026-08-19)

The page describes **SplitCamVirtualAudio**, a CoreAudio HAL plug-in that adds a virtual
audio device macOS apps see as an ordinary microphone, so a mix of mic + system sound +
music + video audio can be sent to Teams, Telegram, Discord, Zoom or anything with a mic
input. Facts on the page were read out of the package, not assumed — re-verify before
changing any of them:

- installer `mac-download/SplitCamVirtualAudio.pkg`, **37 726 bytes**, md5
  `bf87d328d79f8707c8ab9e56d01bbdf8`; driver bundle **1.1**, id `com.splitcam.caio.VirtualAudio`
- installs into `/Library/Audio/Plug-Ins/HAL` — **user-space plug-in, NOT a kernel extension**
- signed `Developer ID Installer: OMT-LIDER, TOV (QRBUBRN5RF)` and **notarised by Apple**
- 🔴 the binary is **arm64 only** — Apple Silicon. The page must never promise Intel support.
- the same driver also ships *inside* SplitCam.app for macOS; this package is the standalone
  install/repair path

⚠️ **Linking rules (user, 2026-08-19 — SUPERSEDED TWICE, this is the current state).**
History matters here because two earlier rules are still quoted in review tooling:
1. First the owner said the macOS page must be reachable **only** from the macOS card on `/download/`,
   explicitly not from the homepage and not from `/features/`.
2. Then they added `/products/` — its macOS card carries the same `.product-addon` block.
3. Then they **reversed the `/features/` ban**: the hub must carry a Virtual Audio feature card that
   covers **both platforms in one card** and links to **both** pages.
**Current, binding:** entry points are the macOS cards on `/download/` and `/products/` (Mac page only),
plus one combined card in `/features/` linking to both. Still **not** on the homepage and **not** in the nav.

⚠️ **The two pages stay independent in content, not in navigation.** `/virtual-audio-mac/` and
`/virtual-audio-windows/` must not cross-link body copy, must not share sections, and must not be
near-duplicates of each other — an adversarial review caught the first Windows draft being a
find-and-replace clone of the Mac page (identical H2s, identical 11-app list, verbatim sentences),
which would defeat the whole point of splitting the URLs. The hub card is the ONE place both are
mentioned together.

⚠️ **URL split (user-approved, 2026-08-19):** the page formerly at `/virtual-audio` is now
`/virtual-audio-mac`, with a 301 in `seo/redirects.htaccess` (rule 0.8, placed before the
trailing-slash rule so both `/virtual-audio` and `/virtual-audio/` resolve in one hop). The Windows
sibling is `/virtual-audio-windows`. Neither squats the platform-less query.

⚠️ **Windows virtual audio is BUILT IN — do not offer a download for it.** Evidence, all in the
Windows panel of `changelog/index.html`: v10.3.51 "Added SplitCam Virtual Audio device.";
v10.3.66 "New virtual microphone device driver." plus an installed-driver check that warns and lets
the program keep running; v10.3.77 "Audio driver updated.". 🔴 The v6.1 entry "Added virtual
microphone plug-in" sits in the **macOS** panel (`id="panel-mac"`) — it is NOT Windows evidence.

⚠️ **Mixer ≠ virtual microphone (owner's distinction, must stay unmistakable).** The **Audio Mixer**
combines sources *inside* SplitCam and that mix goes to the stream and the recording. The **virtual
microphone** is a *separate, additional* output that makes the mix available to Windows as an input
*device*, so other programs can select it. Do not write "outside SplitCam" for the device — it reads
as "not part of SplitCam", the exact misconception the page exists to kill; write "at the Windows
level". Also avoid asserting the device carries bit-identically "that same mix": the repo cannot
prove it, and the page itself notes horizontal and vertical canvases have independent audio.

## /virtual-audio-windows/ — the Windows device page (added 2026-08-19)

Sells "it is already installed, here is the difference between the mixer and the device, and where the
device turns up", NOT an install flow — Windows has no driver package. Deliberately shares no structure
with the Mac page: different headings, no 11-app grid, no 3-step install ladder, no requirements card row.
Two adversarial review rounds killed earlier drafts for cloning it; diff against `virtual-audio-mac/` before
adding any section.

- own CSS family `.vw-*` (two-lane hero diagram, device-list mock, mixer shot) — never reuse `.va-*` here
- the mixer visual is the **real** screenshot `assets/audio-mixer.png` plus the homepage's animated level
  technique, re-implemented as `.vw-shot` / `.vw-lvl` with keyframes `vwA…vwD`
- the Windows input list is a **CSS mock** (`.vw-dd`), clearly a diagram — no screenshot of one exists
- verified copy anchors: `Add new source layer` → `Audio Source` submenu (v10.5.38, so word it cautiously);
  Accentuate Microphone reacts to any sound, headset recommended; a failed driver load warns and SplitCam
  keeps running

🔴 **Correction to an earlier assumption:** the driver is bundled inside the app on **both** platforms.
`virtual-audio-mac/index.html` says so itself ("SplitCam for macOS already contains this audio driver").
The real difference is that macOS *additionally* ships a standalone `.pkg` for installing or repairing the
device on its own; Windows has no such package. Never write "built into Windows, downloaded on Mac".

## Localized surfaces for virtual audio (2026-08-19)

Both localized blocks exist in **all 35 locales**, inserted mechanically from one JSON of per-locale
translations (34 locale agents, each grepping its own pages first):
- `/products/` macOS card → `.product-addon` row linking to `/virtual-audio-mac`
- `/features/` hub → 9th card "Virtual Audio Device", **7th in order, right after Audio Mixer**, with two
  CTAs (Windows + Mac)

⚠️ The hub grid is a fixed `repeat(2,1fr)`. A 9th card orphans the last row, so
`.product-grid>.product:last-child:nth-child(odd){grid-column:1/-1}` was added to every hub file. If a card
is ever added or removed there, re-check that rule still produces a full-looking grid.

⚠️ `.product-cta` is a **two-item** flex row. A third chip broke the macOS card once — that is why the
driver link is a separate `.product-addon` block below the CTA, not another chip inside it.

⚠️ **Imagery available (audited 2026-08-19).** `assets/audio-mixer.png` (531×997) is a **genuine
Windows Audio Mixer screenshot** — four strips: Microphone (High Definition Audio Device), Audio
Playlist, www.youtube.com, System Audio. `index.html` already animates level bars over it
(`.mixer-img-wrap` + `.mixer-level`, keyframes `lvlMic/lvlMusic/lvlYT/lvlSys`) — reuse that, don't
reinvent it. 🔴 There is **no** screenshot anywhere of the virtual-audio device selector — no Windows
Sound panel, no app mic dropdown showing "SplitCam Virtual Audio". Build that as a CSS/SVG diagram
and never relabel an existing file as one. `v2/assets/store-*.png` are **macOS** shots — never use
them on a Windows page.

⚠️ **Brand icons must be real logos, never emoji.** The hero "any app with a mic input" row
uses the site's own SVG logos, copied into `virtual-audio/assets/logos/`
(`microsoftteams · telegram · discord · obsstudio`, same files as
`virtual-camera/assets/logos/`) via `<img class="va-logo" …>`. Generic *sources* (mic,
system sound, music, video audio) use inline stroke SVGs in a `.va-ico` tile. Emoji stayed
acceptable only in `.uc-ico` feature cards, which is the established site-wide pattern.
Shipped with emoji standing in for brands once; the owner rejected it on sight.

⚠️ **How the driver is linked from `/download/`:** the macOS card uses a dedicated
`.product-addon` row placed **after** `.product-cta`, not a third chip inside it.
`.product-cta` is a two-item flex row (store button + changelog); adding a third
`.product-changelog` chip there made the driver look like a second changelog link and broke
the card's rhythm — the owner flagged it. The add-on block carries a mic icon, an "Add-on"
tag and one line of copy, and keeps both product cards the same height at desktop width.

⚠️ `mac-download/` is host-managed and outside the git deploy, so the `.pkg` was uploaded
straight to the server over SSH — a site deploy will not remove it, and will not restore it
either if it is ever deleted.

⚠️ **Hero ordering trap:** on mobile `.vc-hero-content` becomes `display:contents` and the
hero children are ordered explicitly (eyebrow 1, h1 2, visual 3, CTA 4). Any new hero visual
needs its own `order:3` inside `@media(max-width:900px)`, otherwise it defaults to 0 and
renders *above the headline*. Hit for real while building this page.

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
