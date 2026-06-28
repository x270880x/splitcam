# SEO Reminders — Wave 1 follow-up

> **For future Claude (or me):** This file is the durable replacement for in-chat cron reminders, which die when a chat session ends. Check the table below at the start of any new SEO-related chat. If today's date is on or past a "do by" date below, run the linked task.

**Wave 1 launched:** 2026-05-20 (3 pages live on GitHub Pages).

## Schedule

| Do by | Status | Task | What to do |
|---|---|---|---|
| **2026-05-25** | ✅ 2026-06-11 done | SplitCam Android — Play Store approval check | See section below |
| **2026-05-27** | ✅ 2026-06-11 done — NOT indexed | Week 1 indexing check | See section below |
| **2026-06-03** | ✅ 2026-06-11 done — 0 keywords | Week 2 ranking check | See section below |
| **2026-06-10** | ⏸ postponed by user 2026-06-11 — revisit at Month-1 review (2026-06-19) | Wave 2 — 4 SEO pages + dropdown nav rebuild | See section below |
| **2026-06-19** | ⏳ pending | Month 1 full review | See section below |

When a task is done, change `⏳ pending` → `✅ YYYY-MM-DD done` so future-you/Claude can skip it.

## Standing rule — link every feature/product page FROM the `/features/` hub (user, 2026-06-28)

`/features/` is the central hub. **Whenever a new feature or product page is built**
(a dedicated AI-background, scenes/layers, effects, audio-mixer, screen-capture, or any
future `/multistreaming/`-type page), add an outbound link from its matching `/features/`
card — the existing pattern is `<a … class="product-changelog">Learn more <svg…></a>`
inside that card's `.product-cta`. **Then mirror the link into all 35 locale `/features/`
pages** (the link text is translated), and rerun `python3 seo/i18n_wire.py` +
`python3 seo/linkcheck.py --no-network` (must be 0).

Currently linked from `/features/`: Virtual Camera → `/virtual-camera/`, Multistreaming →
`/multistreaming/`, OBS Import → `/alternatives/obs/`, Remote → `/products/`. Still
UNLINKED (no dedicated page yet — link them the moment one ships): **AI Background
Removal · Scenes/Sources/Layers · Effects/Filters/Beauty · Audio Mixer · Screen & Window
Capture.** Don't forget.

## Pre-migration — keep-URL pages still to build (2026-06-28)

These live splitcam.com pages are **kept (same URL), NOT redirected** — build them in the
redesign before go-live so the URL survives migration (each has modest backlinks). Do NOT
301 them to the homepage (soft-404 risk + loses the function).
- `/contact-us` (+ `/ru/kontakty`, `/es/contactenos`) — contact page. **Open question:**
  the old page used a WordPress form; a static rebuild needs a form backend (Formspree /
  mailto / etc.) — decide before building. Content can be pulled from the old-site backup
  (private repo `x270880x/old_splitcam_site`, release `backup-2026-05-23`).
- `/donate-us` (+ `/ru/pozhertvovat`, `/es/donarnos`) — donation page. Low priority; keep
  URL, light restyle, pull donation links from the backup.
URL form: build them slashless like everything else (`/contact-us`, `/ru/kontakty` …) and
run `i18n_wire.py` + `linkcheck.py` after. Until built, leave them on the old host.

---

## 2026-05-25 — SplitCam Android: Play Store approval check

**Context:** As of 2026-05-22 the SplitCam Android app is still pending Google Play review. Because of that, the Android / Google Play store buttons in the SplitCam Remote section on `/products/` are shown as a disabled "Coming soon" state (the iOS Remote button too — no confirmed live store URL yet).

**What to do:**
- Check Google Play for the SplitCam Android build: search the store, or try `https://play.google.com/store/apps/details?id=com.splitcam`.
- If approved & live: in `products/index.html`, swap the "Coming soon" Android/Google Play button back to a real `<a href="...">` with the live Play Store URL.
- Also ask the user for the iOS SplitCam Remote App Store URL if that app is live, and restore that button too.
- If still pending: leave as "Coming soon" and re-check in a few days.

**If Android (and ideally iOS) Remote goes live, reopen this decision:**
On 2026-05-23 the user and Claude decided NOT to build a dedicated
`/products/remote/` page yet — Remote isn't shipped, content is thin,
SEO volume is low, and a "Coming soon" landing would just bounce users.
Once the store links are real, revisit: build `/products/remote/` (full
product page) + add a third spotlight on the homepage (Multistream /
Virtual Camera / **Remote**) and condense the Remote block on `/products/`
into a teaser linking to the new page. Schema.org SoftwareApplication
for the mobile app on the new page.

**✅ Result (2026-06-11):**
- **Main mobile apps are live on BOTH stores** and were already linked from
  the `/products/` platform cards: iOS `id1543666414`, Android `com.splitcam`
  ("SplitCam Live Multistreaming", SplitCam Labs., 10K+ installs).
- **SplitCam Remote (the separate companion app): iOS is LIVE** —
  `https://apps.apple.com/app/splitcam-remote/id6760961594`, v1.2,
  iOS 17+, current version released 2026-05-19, seller OMT-LIDER TOV.
  **Android Remote does NOT exist yet** (Play dev page lists only
  `com.splitcam`) → Google Play button stays "Coming soon".
- Site updated (commit `4ba08fd`): Remote App Store button is a real link
  (solid `btn-store` style), Pair Step 02 copy, JSON-LD `MobileApplication`
  → `operatingSystem: iOS` + `installUrl`, `/changelog/` Remote panel text.
- macOS compatibility of Remote confirmed via Mac App Store v1.13 release
  notes ("Added support for remote control via SplitCam Remote application
  for iOS") — the "Works with Windows 10/11 and macOS 13+" copy is correct.
- `/products/remote/` page decision stays parked — **re-open when Android
  Remote ships** (one-store app page is still thin).

---

## 2026-05-27 — Week 1 indexing check

**Goal:** Confirm Google indexed all 3 Wave 1 pages.

**Pages to check:**
1. https://x270880x.github.io/splitcam/for/youtubers/ — target "how to live stream on youtube" (2,700 vol, KD 6)
2. https://x270880x.github.io/splitcam/for/churches/ — target "church streaming software" (~580 vol total, KD 2-12)
3. https://x270880x.github.io/splitcam/alternatives/obs/ — target "obs alternative" (~1,130 vol, KD 0)

**Steps:**
- Open Google Search Console for the property
- For each URL: URL Inspection → confirm "URL is on Google"
- If any page is **not** indexed: click "Request Indexing" manually
- Note initial impressions / clicks (will mostly be zero this early — that's normal)

**Quick test without GSC:** Google `site:x270880x.github.io/splitcam/for/youtubers/` — if the page shows up, it's indexed.

**✅ Result (2026-06-11): NOT indexed.** `site:` search returns nothing from
`x270880x.github.io`; Ahrefs (prefix `x270880x.github.io/splitcam/`) shows
**0 organic keywords / 0 traffic**.

**Root cause found (same day): staging is unindexable BY DESIGN.** Every
page carries `<link rel="canonical" href="https://splitcam.com/...">`,
`sitemap.xml` lists only `splitcam.com` URLs, and `robots.txt` points to
`https://splitcam.com/sitemap.xml`. Google treats every staging URL as a
duplicate of its future splitcam.com home → it will never index the
github.io host. This is the correct pre-launch pattern (no duplicate
content, staging never competes with the real domain) — **do not "fix" it
and do not create a GSC property for x270880x.github.io (pointless: the
canonicals veto indexing, and the sitemap can't even be submitted there —
foreign-host URLs).** The week-1/week-2 indexing expectations in this file
were written before this setup; real indexing/ranking checks only make
sense **after migration to splitcam.com**.

**What IS useful now: a GSC property for `splitcam.com` itself** —
baseline queries/impressions before migration + instant readiness on
migration day. Do NOT submit the new-structure sitemap there until the
new URLs actually exist on splitcam.com (they'd be 404s today).

---

## 2026-06-03 — Week 2 ranking check

**Goal:** See actual ranking positions, identify "almost on page 1" keywords to push.

**For each page, check Google rankings for target keywords:**

`/for/youtubers/`:
- "how to live stream on youtube"
- "youtube live streaming software"
- "free youtube live streaming"

`/for/churches/`:
- "church streaming software"
- "best church streaming software"
- "church live stream software"

`/alternatives/obs/`:
- "obs alternative"
- "obs studio alternative"
- "obs alternative mac"

**Tools:** GSC "Performance" tab → filter by query, or Ahrefs `organic-keywords` endpoint.

**Re-run Ahrefs** to see total keyword count change vs baseline:
```bash
cd "/Users/splitcam/Documents/Дизайны/SplitCam/SPLITCAM DEV./splitcam/seo"
AHREFS_TOKEN='<token from ONBOARDING.md — REGENERATE FIRST>' python3 ahrefs.py
```
Compare result to baseline reports in `seo/reports/`.

**Output:** identify keywords ranking position 11-30 (close to page 1). These are the ones to push with extra internal links or minor content tweaks **before** Wave 2 launches.

**✅ Result (2026-06-11): nothing ranks** — direct consequence of the
non-indexing above (Ahrefs metrics + organic-keywords for the prefix both
return zero). Nothing to push yet; re-run this check after the staging
host gets indexed or after migration to splitcam.com.

---

## 2026-06-10 — Wave 2 launch (6 pages)

**Goal:** Build the next 6 SEO pages per `seo/PLAN.md` Wave 2 spec.

**Before starting:**
- Review week-2 ranking data (above) — if anything from Wave 1 is exploding or dying, adjust Wave 2 priorities
- Re-read `seo/PLAN.md` (might have been updated)
- Re-read `ONBOARDING.md` for current project state
- Check `for/youtubers/index.html`, `for/churches/index.html`, `alternatives/obs/index.html` as templates

**Pages to build (per PLAN.md):**
- ~~`/alternatives/` hub~~ — ✅ built 2026-05-22
- ~~`/for/` hub~~ — ✅ built 2026-05-22
1. `/alternatives/restream/` — target "restream alternative"
2. `/alternatives/streamyard/` — target "streamyard alternative"
3. `/alternatives/streamlabs/` — target "streamlabs alternative"
4. `/for/vtubers/` — target "how to be a vtuber" (500 vol, KD 0)

**Also in Wave 2 — dropdown navigation rebuild:**
Once the pages above exist, the `/alternatives/` and `/for/` sections each have
4+ live leaf pages — that's the point a dropdown nav earns its keep. Do it
properly:
- Extract the nav into a single `nav.js` snippet so it's defined once, not
  copy-pasted across every page (today: ~11 pages each with its own `<nav>`).
- Add hover/click **dropdown menus** on the "Alternatives" and a new "Use Cases"
  nav item, listing their leaf pages. The nav item itself still links to the
  hub page (hub pages keep their standalone SEO value — do NOT replace them).
- Add a **mobile burger menu** — mobile currently has NO menu at all
  (`.nav-links` are just `display:none` below 900px). The burger must expose
  every nav item incl. the dropdowns.
- Deferred from 2026-05-22 on purpose: with only 1–2 live leaf pages per
  section a dropdown looked empty and wasn't worth the per-page maintenance.

**Ask the user before starting** — priorities might have shifted in 3 weeks.

**Status note (2026-06-11):** asked the user — **postponed** (also declined
GSC-for-staging setup for now; SEO payoff is expected at the splitcam.com
migration). Revisit both at the Month-1 review on 2026-06-19. Scope check done:
- `/for/vtubers/` already exists as a **noindex draft** — review + enable,
  don't build from scratch.
- **Mobile burger menu already exists site-wide** (shipped in the
  2026-06-07 session, `nav-burger` on all 14 pages) — remaining nav scope
  is only the **desktop dropdowns** for Alternatives / Use Cases (+ the
  optional `nav.js` extraction; nav is still copy-pasted per page).

---

## 2026-06-19 — Month 1 full review

**Goal:** Write a real report on what worked, what didn't, and what Wave 3 should be.

**Data to collect:**

**Google Search Console (all SEO pages):**
- Total impressions / clicks / avg position per page
- Top 20 queries actually driving traffic
- Pages with high impressions but low CTR → title/meta tuning candidates
- Pages with **zero** impressions → need internal link push or content thinning

**Ahrefs (re-run):**
```bash
cd "/Users/splitcam/Documents/Дизайны/SplitCam/SPLITCAM DEV./splitcam/seo"
AHREFS_TOKEN='<token — REGENERATE FIRST>' python3 ahrefs.py
```
Compare DR / ranked keyword count / traffic estimate vs baseline in `seo/reports/`.

**Output:** write `seo/reports/month1.md` covering:
- What worked (winning pages/keywords)
- What didn't (dead pages — kill or rebuild?)
- Wave 3 recommendation (which clusters to target next)

**Reminder:** the Ahrefs token shared in ONBOARDING.md should have been regenerated by now. If not, regenerate it first.

---

## How to use this file

- **Bookmark it** in your editor / browser
- **Open at start of any SEO chat** — Claude can `Read` this file and pick up exactly where things left off
- **Update status** in the table as tasks complete (don't delete sections — useful for context later)
- **Don't trust the cron tool for durable reminders** — it lied about `durable: true` in May 2026; reminders set that way died with the chat session. Use this file + iCloud Calendar instead.
