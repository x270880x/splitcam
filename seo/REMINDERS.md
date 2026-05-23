# SEO Reminders — Wave 1 follow-up

> **For future Claude (or me):** This file is the durable replacement for in-chat cron reminders, which die when a chat session ends. Check the table below at the start of any new SEO-related chat. If today's date is on or past a "do by" date below, run the linked task.

**Wave 1 launched:** 2026-05-20 (3 pages live on GitHub Pages).

## Schedule

| Do by | Status | Task | What to do |
|---|---|---|---|
| **2026-05-25** | ⏳ pending | SplitCam Android — Play Store approval check | See section below |
| **2026-05-27** | ⏳ pending | Week 1 indexing check | See section below |
| **2026-06-03** | ⏳ pending | Week 2 ranking check | See section below |
| **2026-06-10** | ⏳ pending | Wave 2 — 4 SEO pages + dropdown nav rebuild | See section below |
| **2026-06-19** | ⏳ pending | Month 1 full review | See section below |

When a task is done, change `⏳ pending` → `✅ YYYY-MM-DD done` so future-you/Claude can skip it.

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
