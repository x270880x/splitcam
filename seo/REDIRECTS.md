# SplitCam.com — Page Weight & Redirect Strategy
*Created 2026-05-21. Data: Ahrefs API, US market, `seo/data/splitcam.com-pages.json` (108 URLs with weight). Raw export is gitignored — rerun `python3 seo/pages.py` to refresh.*

## How to read "weight"
- **traffic** — monthly organic visits (US). Tells you what to *improve*.
- **refdomains (rd)** — unique sites linking to the page. Tells you what you must *not lose* — this is the irreplaceable asset.
- **keywords / top_keyword_position** — what the page ranks for. Must be preserved through any rewrite.

A page can have huge weight with near-zero traffic (e.g. `/help` = 753 rd, 0 traffic). Backlinks are the thing redirects protect.

---

## What to do with removed / dead pages — the short answer

**Use a `301 redirect`.** A removed page that 301s to a live page:
- **stops "hanging on the site"** — visitors and Googlebot land on the live page, the old page is gone from view;
- **keeps its value** — ~90%+ of link equity passes to the redirect target.

That is exactly "не терять и не висеть" — you get both.

### The 5 rules
1. **Redirect to the most *relevant* live page — never blindly to the homepage.** Google treats a redirect to an irrelevant page as a "soft 404" and passes almost no equity. `/tour/use-effects/` → `/features/` (good); → `/` (bad).
2. **One hop.** Point the old URL directly at the final target. No A→B→C chains.
3. **Keep redirects for years**, not a month. Link equity transfers slowly.
4. **Zero-weight pages don't need effort.** No traffic + no backlinks + no rankings → a plain `404`/`410` is fine; Google drops them. Don't redirect junk just to redirect it.
5. **Hotlinked images** (`/blog/img/*`, `/wp-content/*`) can't be 301'd to a page usefully. Either keep the image file at its path, or accept the small loss.

Where redirects live: splitcam.com is WordPress/Apache (`/wp-content/` present) → `.htaccess` rules or a redirect plugin. (Note: GitHub Pages can't do real 301s — this is for the production host.)

---

## TIER 1 — Crown jewels — NEVER change these URLs
| URL | traffic | refdomains | note |
|---|---:|---:|---|
| `/` | 1856 | 3300 | the whole domain's authority anchor |
| `/download` | 94 | 556 | #1 conversion page |
| `/help` | 0 | 753 | backlink hub — keep URL alive even though no traffic |
| `/features` | 39 | 37 | ranks for "splitcam" |

Redesign = swap content on these, **keep the exact URL**.

---

## TIER 2 — Strong backlinks, must be preserved (keep URL or 301 with care)
| URL | traffic | refdomains | recommended action |
|---|---:|---:|---|
| `/help/start/how-to-stream-on-streamray` | 4 | **1008** | keep URL — huge backlink mass (likely adult/spammy; see note below) |
| `/help/start/how-to-stream-on-onlyfans` | 22 | 138 | keep — also high traffic value |
| `/win-download/SplitCamSetup.msi` / `_x64.msi` | — | 67 / 49 | installer files — keep paths or 301 to current installer |
| `/forum/` | 0 | 61 | keep — separate app |
| `/splitcam-changes-win` | 0 | 41 | 301 → new `/whats-new/` |
| `/ru/` + `/ru/help-ru/...bongacams`, `...stripchat` | — | 144 / 109 / 100 | keep RU URLs (locale decision pending) |
| `/blog/` + `/blog/category/*` | — | 27 (+600-700 ext links) | keep blog |
| `/more-plugins` | 0 | 23 | 301 → `/features/` if removed |
| `/contact-us` | — | 12 | keep URL, restyle |
| `/help/multi-streaming` | 0 | 10 | keep — or 301 → new `/multistreaming/` |
| legal: `/privacy-policy`, `/license-agreement` | — | 7-8 | keep URLs |

---

## TIER 3 — Modest help pages (per-platform guides, 5-30 rd each)
Conferencing + how-to-add-X + per-platform streaming guides. Each has 5-30 refdomains and small traffic. When the help section is reworked: **keep each URL**, improve content in place. Only 301 if a URL genuinely must change.

---

## TIER 4 — Legacy / dead URLs — these are the "удаленные страницы" to fix NOW
These old-structure URLs still have backlinks but mostly show `http_code: null` (Ahrefs can't fetch them → likely already dead/404). Their link equity is **leaking into a void right now** — set 301s and recapture it.

| Dead/old URL | refdomains | → 301 target |
|---|---:|---|
| `/download.html` | 32 | `/download` |
| `/SplitCamSetup.exe` | 20 | `/download` (or current installer) |
| `/russian/` | 19 | `/ru/` |
| `/cgi-sys/suspendedpage.cgi` | 19 | `/` (hosting-suspension junk page — recapture stray links) |
| `/aboutus.html` | 9 | `/about/` (new) or `/contact-us` |
| `/russian/download.html` | 8 | `/ru/downloads` |
| `/russian/index.html` | 7 | `/ru/` |
| `/german/` | 5 | `/de/` or `/` |
| `http://splitcam.com/`, `www.` variants | 529 / 15 | already 301 ✅ — verify they stay |

Pages removed in the redesign — redirect map:
| Removed page | → 301 target |
|---|---|
| `/downloadnew` (dup) | `/download` |
| `/tour` + 6 `/tour/*` sub-pages | `/features/` |
| `/splitcam-changes-win`, `/splitcam-changes-mac` | `/whats-new/` |
| `/more-plugins` (if cut) | `/features/` |

---

## ⚠️ Adult-content collision
`/help/start/how-to-stream-on-streamray` (1008 rd), the OnlyFans/Flirt4Free/CamSoda/Stripchat/XLoveCam guides, and the RU bongacams/stripchat pages carry significant weight — but they're adult-cam content, and PLAN.md flags an "adult-content cleanup" task.

Decision point: if these are removed for brand reasons, **do NOT 301 them into clean marketing pages** — spammy adult backlinks would drag bad signals into the new page. For adult pages being cut: either `410 Gone`, or 301 only within the adult cluster. Their weight is sacrificed by design — that's the cost of the brand cleanup, accept it consciously.

---

## Next step
Cross-reference this with `seo/MIGRATION.md` List 2. Every page there that changes URL or gets removed needs a row in an `.htaccess` redirect block. I can generate that `.htaccess` block once the homepage variant + locale decisions are made.
