# SplitCam — Project Onboarding

*Last updated: 2026-07-06. Open this at the start of any new chat to get up to speed.*

> **⚡ SINCE 2026-07-02 (read this first — the rest of "Current state" predates cutover):**
> - **splitcam.com WEB is LIVE on DirectAdmin** — 2nd cutover **2026-07-06** (CF A apex+www →
>   `185.67.3.44`, DA `lwanngbs@…`, CF Origin cert to 2041). **MAIL still on cPanel**
>   `jntckkaf@91.223.223.113` (`mail`/`webmail`/MX left there) → cPanel = fallback, keep ~2 wks,
>   migrate mail before cancelling. Rollback = CF apex+www A back to `91.223.223.113` + purge.
>   (1st cutover 2026-07-02 was old host `dfadnfvi@77.83.100.124` → that cPanel; mail moved then.)
> - **All internal URLs are now FULL absolute canonical** (`https://splitcam.com/...`) —
>   subresources AND `<a href>` (see CLAUDE.md rule 0). Fixed slashless-URL breakage
>   (orbit-logo 404s, locale-dropping nav, JS platform-menu double-domain).
> - **526-locale SEO audit + all 287 fixes applied** (titles/desc/keywords/native grammar),
>   report `seo/reports/seo-audit-2026-07-02.md`.
> - **Forum shut down** — scrubbed from `/help` (35 locales); support = Telegram + FAQ.
> - **Blog: 109 posts → thematic 301s**; `.cfg` served via 3 Cloudflare transform rules
>   (`_cfg.bin` twins); custom branded **404** live; `no-ads` firewall rule re-enabled.
> - **Installers split (2026-07-06):** host keeps only 10.8.x–10.9.2 (9.3G, was 16G);
>   everything ≤10.7 + museum 4.x–8.x → GitHub `x270880x/splitcam-release` (incl. new
>   `legacy-archive` release). Old URLs 301 to the **same version's** GitHub asset.
> - **Search engines registered:** GSC sitemap submitted + IndexNow (526 URLs → Bing/Yandex).
> - **DirectAdmin cutover DONE 2026-07-06** (`185.67.3.44`, creds `~/.hostsila_da_ssh`, panel
>   API :2222) — 2×-cheaper than cPanel. Full byte-parity audit passed pre-flip (579 files 0
>   drift; 2 win-download update files copied; all redirects/404/PHP/SEO verified), CF Origin
>   cert installed, DA confirmed live origin via probe. `.cfg` native → **still-TODO: delete the
>   3 CF `.cfg` transform rules** after 48h. Details: `seo/REMINDERS.md` "DA CUTOVER EXECUTED".

## ⭐ Current state (read first)
- Site is live in **all 35 languages**. Disk math (self-checking): **528** total
  `index.html` = 34 locales × 15 pages (510) + 18 EN-root pages, **minus 2 `noindex`**
  (`v2/` archived, `for/vtubers/` draft) = **526 indexable** = **526 `<loc>` in
  `sitemap.xml`** (exact match). EN root + 34 under `/<lang>/`: ru es de fr pt tr fil
  uk it vi id nl ro hi ja ms bg ar ko th pl hu sv zh el cs he sr hr da fi no sk fa.
  **RTL locales: ar, he, fa** (sr = Latin-script Serbian → LTR).
- **EN-only (non-localized) pages** — this is why EN root has 18 index.html but each
  locale has 15: `/download/` (real indexed landing page, canonical
  `https://splitcam.com/download`; referenced by 3 sitemap `<loc>` for platform URLs),
  `/for/vtubers/` (`noindex` draft — review + enable, don't rebuild), `/v2/` (`noindex`
  archived Variant B, unlinked, own assets/nav — never ships).
- **URL form = slashless (2026-06-28).** canonical / og:url / hreflang / sitemap /
  JSON-LD URLs have **no trailing slash** on sub-pages (`/download`, `/features`,
  `/ru/products`) — only the site root `/` and locale roots `/ru/` keep a slash. Exact
  rule (single source `i18n.page_url()`): keep the slash iff `page_path == ''`, else
  `rstrip('/')`. This matches live splitcam.com byte-for-byte (it serves `/download`,
  301s `/download/` away) so Google maps the redesign onto the indexed URLs instantly on
  migration. Production Apache enforces it via the RewriteRule block at the **end** of
  `seo/redirects.htaccess`; GitHub Pages staging keeps serving the directory form
  (`/download/`) and that's fine (canonical points to production). Internal nav links
  keep their slash so staging never 301-hops and `linkcheck` stays green.
- **`/features/` hub** (all 35 locales) — replaces live splitcam.com/features (ranks
  for "splitcam"). Overview: virtual camera, multistreaming, AI background,
  scenes/layers, effects, audio mixer, capture, OBS import + Remote panel + FAQ. Sitemap
  weight: priority **0.9**, changefreq monthly. **Not yet in the global nav** (reachable
  via sitemap, language dropdown, breadcrumb, footer) — adding it as a nav item is an
  open option.
- **`/donate-us/`** (all 35 locales) — keep-URL donate page. Donations go to
  **`paypal.me/Katzovich`**; amount chips ($25/$50/$100/$200/$500/$1000) are clickable
  `paypal.me/Katzovich/<amt>USD` links (the old PayPal hosted-button was replaced — **0
  `hosted_button_id` remain** in any HTML). Sitemap weight: priority **0.3**, changefreq
  yearly. **Features + Donate are footer links on every page.**
- **Host migration DONE — cutover executed 2026-07-02** (see the ⚡ box at top). Live host
  = cPanel `jntckkaf@91.223.223.113`, docroot `~/public_html`, Cloudflare in front. Deploy
  = host pulls the GitHub `main` tarball and overlay-copies (excludes
  `.git/seo/v2/.claude/*.md/.nojekyll`, **never `--delete`** or `win-download/` is wiped);
  the boevoy `.htaccess` in the docroot = `seo/redirects.htaccess` (kept in sync on every
  redirect change). After each deploy: **purge Cloudflare cache**. SSH creds
  `~/.hostsila_ssh`. A DirectAdmin trial (`185.67.3.44`) is staged as a cheaper replacement
  (not cut over) — details in `seo/REMINDERS.md`.
- **`ver.txt` policy — RESOLVED (host-managed).** The earlier weekly-ramp idea was
  dropped. All three `ver.txt` track the **current** release and are set to **10.9.2**:
  root `/ver.txt`, `win-download/update/ver.txt`, `win-download/update/light/ver.txt`.
  They live **only on the host** (root `/ver.txt` was removed from the git repo so an
  overlay re-deploy can't reset it); edit them on the host via SSH. `ver.php` echoes root
  `/ver.txt` + its mtime. **Standing rule:** ~10 days after a new SplitCam release ships,
  set all three to the new version string — plain text, **no trailing newline** — with
  the matching installer deployed first.
- **Antivirus scan COMPLETE — 0 infected site-wide, 100% coverage.** Host: 529 HTML+PHP
  pages clean. `win-download/` audited in three passes: 24 big installers that OOM-killed
  `clamscan` on the host (CloudLinux LVE PMEM cap, not hardware) → Mac ClamAV 1.5.2, 24/24
  clean (2026-07-01); then 2026-07-02 the remaining **42 files with no persisted verdict**
  (the first host pass logged only SKIP paths, not the clean ones, and installers were
  updated after it) — incl. all 3 current installers + the whole 10.5→10.9 x64 series —
  downloaded to the Mac with md5 integrity check vs the host and scanned: **42/42 clean**.
  Full audit manifest (`path|md5|verdict` for every win-download file):
  `~/clamav/fullscan-2026-07-02.log` on the host. Lesson: always persist CLEAN paths, not
  just counters.
- **Full host↔repo sweep (2026-07-02): 0 drift.** All **578** deployable repo files
  (pages, assets, sitemap, robots, favicons…) are byte-identical (md5) on the new host.
  The only drift found — a stale `hero-spotlight.mp4`+poster (pre-watermark-fix, deployed
  Jun 30) — was re-deployed from GitHub raw and re-verified. Host-managed extras
  (`ver.php`, `ver.txt`, `ofcf-turnstile.php`, `.htaccess`) intact; all `ver.txt` 10.9.2.
  Found (and same-day RESOLVED) a cutover blocker: the new host 403s
  `win-download/update/*.cfg` (app config: ingest lists / proxy) at the server level —
  unfixable from the account. **Fixed via 3 Cloudflare Transform rules** rewriting the
  `.cfg` URLs to `_cfg.bin` twins that exist on both origins; verified 200 + md5-identical
  through live CF. Details + sync/rollback notes in `seo/REMINDERS.md` cutover checklist.
- **Skype is fully removed site-wide (0 mentions)** — Microsoft retired it May 2025.
- The whole language system is two files: **`seo/i18n.py`** (config + render helpers +
  `RTL_CSS`) and **`seo/i18n_wire.py`** (rebuilds dropdown/hreflang/auto-detect/sitemap +
  per-RTL-page CSS across every page). See the "Localization — all 35 languages" section
  in **CLAUDE.md** for the full how-to. Run `i18n_wire.py` then `linkcheck.py --no-network`
  (must be 0) after any add/translate.
- Per-locale keyword maps: `seo/I18N-KEYWORDS.md` (waves 1-3; waves 4-7 were brand-led,
  ~0 demand). Binding spec: `seo/I18N-PLAN.md`.
- The 17 lowest-demand locales (waves 4–7, ≤10/mo, mostly 0) were completed 2026-06-15
  for brand completeness — **see the 2026-06-15 session log below** (it involved cleaning
  up an unattended mass-translation run; lessons recorded there).
- **Working tree has 3 untracked files** (not clean): `AGENTS.md` (a STALE duplicate of
  `CLAUDE.md` — do NOT commit as-is; it would regress page counts and drop the
  `/features/` + `/donate-us/` rows; delete it or regenerate from `CLAUDE.md`), plus
  `seo/screenshots/download_desktop_1440.png` + `download_mobile_390.png` (mobile/desktop
  proof shots for the `/download` page — safe to commit). `CLAUDE.md` is the fuller
  reference but is itself slightly stale on the headline count (still says 525 indexable,
  predates `/features/` + `/donate-us/`) — the real source of truth for page counts is the
  sitemap/disk (**526**). `linkcheck` 0 broken across 526 pages.

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
The redesign destined to replace the real **splitcam.com** (see `seo/MIGRATION.md`).
Platforms: **Win · macOS · iOS · Android**. Version **v10.9.2** site-wide.

## Pages deployed (15 localized page-types + `/download` (EN-only) = 16 public URL-types; + 2 `noindex`)

Every locale ships 15 page-types; EN root additionally has `/download/` (public) plus the
2 `noindex` pages. Nav-facing subset below.

| Path | Note |
|---|---|
| `/` | Main landing — **Variant A is the final homepage** |
| `/download/` | **Download landing (EN-only, indexed).** Preserves splitcam.com/download equity (crown-jewel URL, 556 referring domains). Canonical `https://splitcam.com/download`. Win/Mac/iOS/Android. Referenced by 3 sitemap `<loc>` (platform download URLs resolve here). Not localized. |
| `/v2/` | Variant B — **archived** (A won the A/B). `noindex`, unlinked, own assets/nav. Never goes to splitcam.com. |
| `/products/` | Products hub — Win/macOS/iOS/Android + SplitCam Remote. iOS card has 2 features tagged "in development" (AR filters, Picture-in-picture) — don't reword as shipped. Remote: **iOS app LIVE** (App Store id6760961594, button live since 2026-06-11); Android Remote not released — Google Play stays "Coming soon". |
| `/features/` | **Features hub** (all 35 locales) — virtual camera, multistreaming, AI background, scenes/layers, effects, audio mixer, capture, OBS import + Remote panel + FAQ. Replaces live splitcam.com/features. Not in global nav yet. |
| `/donate-us/` | **Donate page** (all 35 locales) — keep-URL, matches live splitcam.com/donate-us. Donations to **`paypal.me/Katzovich`**; amount chips are clickable `paypal.me/Katzovich/<amt>USD` links ($25–$1000). ru/es `pozhertvovat`/`donarnos` 301 here. |
| `/virtual-camera/` | Feature page |
| `/multistreaming/` | Feature page (Twitch simulcast date = **October 2023** everywhere) |
| `/alternatives/` | Hub for "vs X" comparisons. Live cards: OBS. "Soon" cards: Streamlabs, Restream, StreamYard, vMix, ManyCam. |
| `/alternatives/obs/` | SEO Wave 1 — "obs alternative" |
| `/for/` | Use-cases hub (labelled "Use Cases" in nav). Live cards: YouTubers, Churches. "Soon" cards: VTubers, Gamers, Educators, Streamers. |
| `/for/youtubers/` | SEO Wave 1 — "how to live stream on youtube" (structural template for SEO pages) |
| `/for/churches/` | SEO Wave 1 — "church streaming software" |
| `/for/vtubers/` | **`noindex` draft, EN-only, unlinked** — review + enable, don't rebuild. |
| `/help/` · `/changelog/` · `/privacy-policy/` · `/license-agreement/` | Utility pages (all 35 locales; `changelog/` shell localized, its ~1860 release bullets stay EN). |

Nav order site-wide (6 items): **Products · Virtual Camera · Multistreaming · Alternatives · Use Cases · Help**. Features is a footer link (not in the global nav yet). (Dropdown nav rebuild is queued — see `seo/REMINDERS.md`.)

## SEO status
- **Wave 1 — DONE** ✅ (youtubers, churches, obs — all built & live).
- **Wave 2 — POSTPONED** by the user (2026-06-11), revisit at the Month-1 review:
  `/alternatives/{restream,streamyard,streamlabs}/`, `/for/vtubers/` (exists as a
  `noindex` draft — enable, don't rebuild), + desktop dropdown-nav rebuild. (`/alternatives/`
  and `/for/` hubs are already built.)
- **Wave 3 — later:** `/alternatives/{vmix,manycam,meld-studio,snap-camera}/`, `/for/{streamers,educators}/`.
- **Standing rule:** every new feature/product page must be linked FROM its matching
  `/features/` hub card (`<a class="product-changelog">Learn more</a>` in `.product-cta`),
  mirrored into all 35 locale `/features/` pages, then rerun `i18n_wire.py` + `linkcheck.py
  --no-network` (0). Still unlinked (no dedicated page yet): AI Background Removal,
  Scenes/Sources/Layers, Effects/Filters/Beauty, Audio Mixer, Screen & Window Capture.
- `/products/remote/` is **parked** until the Android SplitCam Remote app ships.
- Indexing/ranking checks only become meaningful **after** the splitcam.com cutover —
  staging is unindexable by design (canonicals all point at splitcam.com). Month-1 review
  (write `seo/reports/month1.md` from GSC + Ahrefs) is still pending.
- Full plan: `seo/PLAN.md`. Recommended IA: `seo/SITEMAP.md`.
- **Schedule & follow-ups: `seo/REMINDERS.md`** — open it in any SEO chat. Do NOT use `CronCreate` — it doesn't persist.

## Migration to live splitcam.com
`seo/MIGRATION.md` (strategy) + `seo/redirects.htaccess` (301 map). Only the homepage `/`
is a true same-URL replacement; every other page is a net-new additive URL or a slashless
match to an existing live URL. `seo/redirects.htaccess` structure: (a) dead-URL 301s (apply
now), (b) removed/changed-page 301s incl. `/contact-us → /help` (apply at migration), (c)
ru/es old-slug 301s → uniform English locale slugs (incl. donate), (d) the slashless
RewriteRule block **kept LAST**. Placement: paste the block **above** `# BEGIN WordPress` in
the site-root `.htaccess`; requires `AllowOverride FileInfo`; remove any pre-existing WP
trailing-slash rule first to avoid redirect loops. `/download` is KEPT (not redirected).
`/contact-us` (+ `/ru/kontakty`, `/es/contactenos`) 301 → `/help` (no static page rebuilt).

## Critical design rules
1. Brand logos stored LOCALLY in `/virtual-camera/assets/logos/` — no external CDN refs.
2. SplitCam logo PNG at `/assets/splitcam.png` — used via `<img>`, not base64.
3. No "Restream server" / "cloud middleman" wording — SplitCam is **peer-to-peer direct**.
4. iOS belongs in the platforms list (**Win · macOS · iOS · Android**).
5. Skype is DEAD (Microsoft retired it May 2025) — never mention as a live product.
6. Rating = **4.7 / 357 reviews**, shown ONLY as a visible trust signal (homepage hero chip
   + stats box). **Never put it back into Schema.org** — `aggregateRating` was deliberately
   stripped from every page's JSON-LD (0 present) to avoid a self-asserted-rating structured-
   data manual action. Real source ratings: Softonic 4.7, UpdateStar 4.0, G2.
7. LIVE badges blink (badge opacity + red dot pulse).
8. Current version is **v10.9.2** — used site-wide, the only app version present. No
   installer size shown ("~85 MB" was removed as unverified). ("FFMPEG 7.1" / "version 6.1"
   are dependency mentions, not SplitCam's version.)

## UI conventions
- Dark theme: `--app-base:#141420`, `--blue:#2878fc`, `--purple:#9c5bff`. Font: Geist.
- Nav (6 items): **Products · Virtual Camera · Multistreaming · Alternatives · Use Cases · Help** (`/v2/` is archived and has its own separate nav).
- Each page: favicon set + Schema.org (≥ BreadcrumbList + SoftwareApplication; bigger pages add HowTo + FAQPage) — **never** `aggregateRating`.
- `/for/youtubers/` is the structural template for SEO pages: NAV / BREADCRUMBS / HERO / QUICK ANSWER / STEP-BY-STEP / BONUS / PRO TIPS / COMPARISON / FAQ / RELATED / CTA / FOOTER. SEO pages get **unique body prose** — never copy-paste blocks between `/for/` and `/alternatives/` (cannibalization).
- Homepage hero uses **one `<video>` + canvas mirrors** and a single-decoder pattern (video-flicker/keyframes-are-global lessons in the 2026-06-12 session logs). Hero clips live at `assets/`: `audience-game.mp4`, `audience-scene.mp4`, `hero-spotlight.mp4`, `vc-presenter.mp4`.

## /seo/ folder
- `ahrefs.py` — domain + keyword collector · `pages.py` — per-URL weight · `domains.py` — domain weight checker
- `i18n.py` + `i18n_wire.py` — the no-build-step localization engine (see CLAUDE.md).
- `linkcheck.py` — site-wide link & interlinking audit (broken links/anchors/resources, external HTTP, nav-vs-contextual graph, sitemap-vs-disk sync). Run before migration and after adding pages.
- `deploy_preview.py` — local-only, gitignored preview uploader (cPanel-API HTTPS:2083, not FTP) → the `~jntckkaf` preview only, never the live site.
- `PLAN.md` · `SITEMAP.md` · `MIGRATION.md` · `redirects.htaccess` · `redirects-cloudflare.csv` · `REMINDERS.md` (the operational cutover + ver.txt truth) · `I18N-PLAN.md` · `I18N-KEYWORDS.md`
- `reports/` — analysis reports · `screenshots/` — proof shots (tracked) · `data/*.json` — raw Ahrefs output (gitignored)
- Ahrefs: set `AHREFS_TOKEN` env var from `~/.ahrefs_token`. Lite plan, 100k units/mo.

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
- Register / connect the neutral adult domain (`camstreamguide.com`, registered) → replace `NEWDOMAIN.com` everywhere, connect domain, remove `noindex`.
- Apply the `.htaccess` 301 block on splitcam.com **after** the new site is live.
- Optional: official platform logos into `logos/`, screenshots into `shots/`, Android SplitCam Remote link.

## Multi-language rule
Any content added/changed in one language must be replicated to all locales (EN/RU/ES) — keep `platforms_*.py` in sync.

---

## Domain portfolio (all owned by the user)
| Domain | DR | Note |
|---|---|---|
| splitcam.com | 55 | main site — the authority anchor. Cloudflare zone `d78682c510a9fa3285c47bb52a11e0f4`; anti-bot custom WAF rule active. |
| splitcamera.com | 45 | legacy SplitCam domain — fully 301 → splitcam.com. DR 45 from ~950 refdomains, 0 organic keywords. Cloudflare zone `ab15c739562f274acdb762ab8f96fa49`; anti-bot custom WAF rule active (bot magnet). |
| splitstream.com | 4 | live, weak — candidate to 301 → splitcam.com. Cloudflare zone `b1263e196d8f2c3edc0822bf66d79dd8`; **no** custom WAF rule yet. |
| multi-stream.io | 14 | live, ranks for "free multistreaming" — possible cannibalization with `/multistreaming/`. |
| split.cam | 0 | dormant, clean brand domain — reserve / short links. |
| camstreamguide.com | — | neutral adult domain for cam-streaming-guides (registered; DNS/Pages connect pending). |

## Infrastructure access
All secrets live in **chmod-600 dotfiles in the user's home dir**. Reference them ONLY by
file path inside curl/ssh (e.g. `$(cat ~/.hostsila_ssh)`) — **never echo, paste, log, or
commit the secret value.**

### GitHub repositories
- **`x270880x/splitcam`** (public) — this repo; GitHub Pages staging https://x270880x.github.io/splitcam/ (auto-deploy 30–90 s after push to main).
- **`x270880x/splitcam-release`** (public) — 36 Windows `.msi` releases (`v9.0.9` → `v10.9.2`, + `v10.8.62-restream-test` prerelease). `v10.9.2` is Latest. Canonical latest URL: `releases/download/v10.9.2/10.9.2_x64.msi`.
- **`x270880x/old_splitcam_site`** (**PRIVATE 🔒**) — full backup of the old splitcam.com `public_html` as `old_splitcam_site.tar.gz` (~1.4 GB) on release `backup-2026-05-23`. Contains `wp-config.php` DB creds — **never make public**.

### NEW production / cutover host (redesign target)
- cPanel/Apache on **rocket-cp2.hostsila.org**, account user **jntckkaf**, cutover server IP **91.223.223.113**. cPanel UI https://rocket-cp2.hostsila.org:2083/.
- Full SSH shell: `ssh jntckkaf@91.223.223.113 -p 22` (wget/curl available, ~336 GB free). **scp/sftp subsystem is DISABLED** — push files via base64-over-ssh-exec or cPanel-API HTTPS:2083 upload.
- Docroot `/home/jntckkaf/public_html`. Work is deployed to **preview only**, live at http://rocket-cp2.hostsila.org/~jntckkaf/, via `seo/deploy_preview.py`. **splitcam.com live is NOT touched until the user says go.**
- Creds (chmod 600): cPanel password `~/.hostsila_cpanel`; SSH password `~/.hostsila_ssh` (same cPanel account, full shell). The three host-managed `ver.txt` are edited here over SSH.

### OLD host (current live splitcam.com origin, behind Cloudflare) — legacy
- IP **77.83.100.124**, port 22, user **dfadnfvi**, cPanel host `pl-rocket-cms1.hostsila.org`, docroot `/home/dfadnfvi/public_html` (the bulk is the `win-download/` installer archive — **~16 GB**, measured 1:1 on the new host — plus the live PHP/WP site + blog/forum).
- SSH command-exec works: `ssh -oPubkeyAuthentication=no dfadnfvi@77.83.100.124 "<cmd>"` (SFTP works too but recursive get truncates large dirs — prefer SSH-grep). Origin can be hit directly, bypassing Cloudflare: `curl --resolve splitcam.com:443:77.83.100.124 -k`.
- Creds (chmod 600): password `~/.splitcam_old_ssh`; Ed25519 key `~/.ssh/splitcam_deploy` (Mac-local, never copy off).

### Cloudflare
- Fronts the domains (DNS/CDN, Free plan). API token `~/.cloudflare_token` (chmod 600); scope includes Analytics Read + Firewall/Rulesets Edit + Cache Rules Edit (Cache Purge **not** granted). Three zones (see Domain portfolio). Anti-bot custom firewall rule (block) on splitcam.com + splitcamera.com; splitstream.com has none yet.
- Cache rule caches `win-download/SplitCamSetup_x64.msi` (1-day TTL) → **purge on every new installer release**.

### Ahrefs
- Token `~/.ahrefs_token` (chmod 600). Use with `seo/ahrefs.py`: `AHREFS_TOKEN=$(cat ~/.ahrefs_token) python3 ahrefs.py`. Lite plan, 100k units/mo.

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
**Auto-push:** after meaningful complete edits, commit + push `origin main` without asking; still ask before destructive git ops (force push, `reset --hard`, revert of published commits, branch deletion).

## Session log — 2026-07-02 → 07-06 (CUTOVER + mail + SEO fixes + UI hardening + installer split + DA trial)

- **CUTOVER (07-02):** DNS apex+www → `91.223.223.113` via Cloudflare API; installed a
  **Cloudflare Origin CA cert** on the host (origin was serving an expired mm.hostpro.ua
  self-signed → would break Full-strict); www→apex 301 as a CF dynamic-redirect rule;
  purge-everything. Live battery green. Mail pinned to old server first, then **fully
  migrated** (7 mailboxes, passwords, DKIM/SPF) to the new host.
- **Cloudflare `.cfg` fix:** the new cPanel 403s `*.cfg` server-wide (extension-based,
  unfixable from the account) → 3 **Transform rules** rewrite
  `/win-download/update/{proxy,ingests,ingests2}.cfg` → `_cfg.bin` twins (hardlinks on
  both origins). DirectAdmin serves `.cfg` natively, so these rules become removable after
  a DA cutover.
- **SEO audit (35 locales, ~70 agents) + 287 fixes applied** — keyword placement, native
  grammar, EN products/download de-cannibalization, EN-template calques, meta lengths.
  Report: `seo/reports/seo-audit-2026-07-02.md`.
- **Redirects grew to a full 301 map:** legacy WP `/help/*`, `/blog/*` (109 posts routed
  by topic to vc/multistreaming/changelog/features/for), `/forum/*`→/help, adult cluster
  (75 rules) → camstreamguide.com, mac-privacy/mojave pages, contact-us→help. Forum
  removed from `/help` (35 locales, native).
- **Absolute-URL sweep** (CLAUDE.md rule 0): 5369 subresources + 15807 `<a href>` made full
  canonical across 527 pages; `i18n.dropdown()` + `linkcheck.py` updated to match. Fixed:
  orbit-logo/help/multistreaming-video 404s, locale-dropping nav, the JS platform-menu
  double-domain bug, stale `/splitcam/` manifest paths.
- **UI hardening (all mobile-verified via headless Chrome):** branded multilingual **404**;
  changelog per-version **download buttons** (merged chip+arrow, hover-highlight, dimmed
  when no file) + removed "Older builds" block; **compact sticky header** ≤520px (logo
  shrinks, download+burger pinned); hero `overflow-x: clip` (an 800px glow was inflating
  the mobile viewport and pushing the header off-screen); bitrate pulse → GPU transform;
  header Download buttons on help/changelog/privacy/license (211) fixed to `/download`;
  `.msi` MIME/attachment header (was renaming to .exe).
- **Installer split (07-06):** pre-10.8 → GitHub-only; host 16G → 9.3G; 38 same-version
  301s; new `legacy-archive` GitHub release for the 4.x–8.x .exe + stub.
- **Search-engine registration:** GSC sitemap submitted; IndexNow 526 URLs (key file on
  host). `no-ads` firewall rule re-enabled. Cloudflare stats healthy (~30k uniques/day,
  blocks = bot scanners only).
- **DirectAdmin trial** provisioned + fully staged in parallel (see `seo/REMINDERS.md`).

## Session log — 2026-06-30 -> 07-02 (features + donate, Skype scrub, footers, slashless URLs, host migration finalized, AV scan, hero-video redesign)

Covers the block after the 2026-06-29/30 log (commit `958c429`). Newest-first.

**Hero-video redesign (2026-07-01 → 07-02, 12 commits, HEAD `dd92b72`):**
- Swapped the presenter to a new creator clip (`6875068`) and removed the trial watermark (`14169ae`, `f9afc79`). Hero clips live at `assets/`: `audience-game.mp4`, `audience-scene.mp4`, `hero-spotlight.mp4`, `vc-presenter.mp4`.
- Fully covered the right transition panel to hide old-video edge remnants (`6dd870f`).
- Playback-speed tuning: 1.15x → ~1.32x → settled on **1.2x** for clean 30fps / no judder; livelier source window (src t=12..30.7s) (`1e383ec`, `8be62bf`, `d988017`).
- Restored then thickened (4px) the vivid red top-border on the right vertical transition panel (`0a87173`, `71f4f25`).
- Panel relayout: bigger panels (+10% compound), gap tuned 21px → 10px, then panels −5% for edge breathing room (`2367384`, `c91563b`, `dd92b72`).

**Antivirus scan finished (2026-07-01, `75a3667`):** the 24 big installers that OOM-killed `clamscan` on the host (CloudLinux LVE PMEM cap, not hardware) were pulled to the Mac (1.8 GB via the `~jntckkaf` preview URL) and scanned with Homebrew ClamAV 1.5.2 (fresh DB, deep unpack, no cap) → **24/24 clean**. Combined with the earlier host scan (529 HTML+PHP + 45 `win-download/` installers clean), the site is now **0 infected everywhere**.

**`ver.txt` finalized + policy recorded (2026-06-30, `e2861c0`, `6469baf`):** the weekly-ramp idea was dropped. All three `ver.txt` (root `/ver.txt`, `win-download/update/ver.txt`, `win-download/update/light/ver.txt`) set to **10.9.2** on the host. Root `/ver.txt` was **dropped from the repo** (host-managed, so an overlay re-deploy can't reset it); it had briefly been added as legacy 8.4.0.0 in `156a37e`, then removed. `ver.php` echoes root `/ver.txt` + mtime. Standing rule: ~10 days after each new release, set all three to the new version string (plain text, no trailing newline), installer deployed first.

**Already in the 06-29/30 log (`958c429`), recapped for continuity:** `/features/` hub + `/donate-us/` built EN then natively localized to all 34 locales; donate switched to `paypal.me/Katzovich` with clickable amount chips ($25/$50/$100/$200/$500/$1000 → `/<amt>USD`), old hosted-button dropped (`0ec26af`, `51a7987`); Features + Donate footer links on every page (`45d4c7a`); slashless canonical/og/hreflang/sitemap URLs; Skype removed site-wide (0 mentions); the old→new cPanel host migration finalized; `.well-known/assetlinks.json` + `.nojekyll` added (`bfda3a8`).

**Counts reconciled to disk (2026-07-02):** 528 total `index.html` − 2 `noindex` (`v2/`, `for/vtubers/`) = **526 indexable = 526 sitemap `<loc>`**. 0 `hosted_button_id` remain in HTML; 35 files use `paypal.me/Katzovich`; 603 `10.9.2` occurrences, no other version.

**Working-tree note:** 3 untracked files — `AGENTS.md` (a STALE duplicate of `CLAUDE.md`: "455 indexable pages", "7 public", "2026-06-15 audit", missing the `/features/` + `/donate-us/` rows — do NOT commit as-is; delete or regenerate from `CLAUDE.md`), and `seo/screenshots/download_desktop_1440.png` + `download_mobile_390.png` (proof shots for the `/download` page — safe to commit).

**Cutover still pending** (user hasn't said go): point splitcam.com DNS → 91.223.223.113; drop `seo/redirects.htaccess` into the live docroot `.htaccess` (never on the preview); re-deploy overlay without `--delete`; purge Cloudflare cache for `win-download/SplitCamSetup_x64.msi`.

## Session log — 2026-06-29/30 (new pages, URL form, + full old→new host migration)

Huge session. Two halves: (A) repo/SEO work, (B) migrating the live-site infra to the
new cPanel host and deploying the redesign there.

**(A) Repo / SEO — all committed & pushed (`x270880x/splitcam`):**
- **Slashless URL form (Option A).** canonical / og:url / hreflang / sitemap / JSON-LD
  are slashless on every sub-page (`/download`, `/features`, `/ru/products`) to match
  live splitcam.com byte-for-byte; only `/` and locale roots (`/ru/`) keep a slash.
  Single source: `i18n.page_url()`. Production `.htaccess` enforces it (RewriteRule in
  `seo/redirects.htaccess`). Internal nav links keep their slash (staging stays green).
- **`/features/` + `/donate-us/`** built EN, then natively localized to all 34 locales
  (two `features-localize` / `donate-localize` workflows: native writer + adversarial
  native reviewer per locale, 68 agents each). Donate uses **paypal.me/Katzovich** with
  clickable amount chips (`/25USD`…`/1000USD`); the old PayPal hosted-button was dropped.
- **Footer: Features + Donate links added to every page** (525) — both footer styles
  (standard `.footer-links` + the homepage multi-column `.foot-col`), native labels.
- **Skype removed site-wide** (changelog ×35, v2, features FAQ) → 0 mentions.
- **Redirects** (`redirects.htaccess` + cloudflare CSV): slashless serving; ru/es old
  localized slugs → new (`/ru/osobennosti`→`/ru/features` …); `/contact-us`→`/help`;
  donate. **URL set verified one-to-one vs live splitcam.com** (EN pages match exactly;
  new pages are additive 404s; ru/es decided = uniform slugs + 301).
- Added to repo: `/.well-known/assetlinks.json`, `.nojekyll`. (`/ver.txt` is
  **host-managed**, not in the repo — see the ver.txt policy in `seo/REMINDERS.md`.)

**(B) OLD → NEW cPanel host migration (the new prod target, `~jntckkaf/public_html`):**
- **SSH access (saved, see Infrastructure section + memory `project-splitcam-hosting`):**
  NEW host `jntckkaf@91.223.223.113` = full shell (creds `~/.hostsila_ssh`); OLD host
  `dfadnfvi@77.83.100.124` = nologin shell but **SFTP works** (creds `~/.splitcam_old_ssh`).
  Both hosts block `scp`/legacy-scp (sftp-subsystem only) → push small files via
  **base64 over ssh-exec**, automate the password with `expect` (no sshpass on this Mac).
- **win-download/** (≈16 GB, the Windows installer tree) pulled server-side onto the new
  host via **origin-direct** (`curl --resolve splitcam.com:443:77.83.100.124 -k` — the new
  host's datacenter IP gets 503 from Cloudflare, origin-direct bypasses it). Contents:
  root installers (`SplitCamSetup.msi` 32-bit, `SplitCamSetup_x64.msi`, `_SplitCamSetup_x64.msi`,
  `splitcam.exe` v9.0.7.16-legacy), `update/` (46 historical MSIs + `ingests.cfg/2`,
  `proxy.cfg`, `ver.txt`, `history.txt`), `update/light/` (a slow "light" channel:
  `10.4.75_x64.msi` + its `ver.txt`), `archive/` (7 legacy 4.x–8.x exes). vcredist deleted
  per user. **Both x64 MSIs + light's installer updated to the current build** (`f69f844f`,
  10.9.2); 32-bit left as-is; `light/ver.txt` set to 10.5.0 (filenames kept).
- **PHP source** (`ver.php`, `ofcf-turnstile.php`) pulled off the OLD host via SFTP (NOT
  retrievable over HTTP — server executes them). Both portable (no DB/secret/host
  hardcode; `ofcf-turnstile.php` is a Cloudflare-Turnstile login captcha, public sitekey).
  Uploaded + verified executing on the new host.
- **Antivirus — DONE, 0 infected everywhere.** No AV anywhere + clamav.net is
  Cloudflare-blocked. Installed **ClamAV 0.105.2 on the host** (extracted from the
  GitHub-release `.deb` via `ar`+python `tarfile`; 1.5.2 needed glibc 2.29, host has 2.28 →
  version-hunt found 0.105.2 works). DB pulled via `curl` with the ClamAV User-Agent (default
  UA 403s). Host scan: **529 HTML+PHP pages = 0 infected**; `win-download` per-file =
  45 clean / 0 infected / **24 skipped** — the 24 big old installers OOM-kill clamscan
  (exit 137 at ~18s, independent of `--scan-archive=no` / all-parsers-off) due to the
  per-user **CloudLinux LVE memory cap** (host box has 131 GB RAM & `ulimit -v unlimited`, so
  it's the LVE PMEM quota, not hardware). Those **24 were then scanned locally on the Mac**
  (ClamAV **1.5.2**, fresh DB 2026-07-01, deep unpack, no memory cap — pulled via the
  `~jntckkaf` preview URL, 1.8 GB): **24/24 clean, 0 infected.** Net: everything downloaded &
  deployed to the new host is clean; the 24 are official vendor installers (md5-identical to
  live splitcam.com). Repeatable: `brew`'s clamav on the Mac has no LVE cap and a newer engine
  — use it for anything the host can't deep-unpack.
- **Full redesign deployed to the host** by having the host download the repo main tarball
  from GitHub (codeload — reachable; clamav.net/Cloudflare-fronted sites 403 the host) and
  **overlay-copying** the public files into `~jntckkaf/public_html` (excluded
  `.git/seo/v2/.claude/*.md/.nojekyll`; `cp` without `--delete` so win-download/ver.php
  survive). Host went 457 → 527 pages, now has features/donate/slashless/footers/Skype-0.
  **`.htaccess` NOT redeployed to the preview** (the slashless RewriteRule would break the
  `/~jntckkaf/` userdir serving — it's a cutover-time, live-docroot thing).

**OPEN / pending:**
- **Staged `ver.txt` rollout** — user wants weekly +1-minor bumps toward 10.9.2, then
  "10 days after a new site version". 3 ver.txt on host (root 8.4.0.0, update/ 10.9.2,
  light/ 10.5.0) + ver.php (reads root). Which files to ramp = awaiting decision. In
  `seo/REMINDERS.md`.
- DNS cutover to `91.223.223.113` + drop `seo/redirects.htaccess` into the live docroot.
- Re-deploy redesign at cutover if the repo changed since.

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

## Session log — 2026-06-15 (i18n: 18 → all 35 languages + runaway cleanup)

Took the site from 18 to **all 35 languages** (455 pages). The hard part wasn't the
translation — it was recovering from an **unattended background run** that mass-
translated ~all locales from a Bulgarian (`bg/`) scaffold and committed+pushed it with
systematic bugs, then kept clobbering files for hours (Cyrillic project-path NFC/NFD
instability; a full Claude restart was needed to kill it).

- **Bugs cleaned across 34 locales:** canonical/og:url/og:locale/JSON-LD URLs → `/bg/`
  (~98 pages); smart/curly quotes in HTML attributes + JSON-LD (broke ~150 links +
  JSON-LD); untranslated Bulgarian pages; an absolute `/multistreaming/` FAQ link on
  all 30 homepages. Fixed surgically (per-locale `/bg/`→`/<L>/`, curly→straight,
  JSON-LD repair + remove-fallback, restored vi/ro/bg/de `for/youtubers` JSON-LD from
  the pre-runaway commit).
- **Rebuilt 7 scaffold-only locales fresh from EN** — da, fa (RTL), fi, hr, no, sk,
  sr (Latin) — 13 pages each, one opus agent per page, linkcheck-gated commit per locale.
- **RTL** (ar/he/fa): `i18n.RTL_CSS` (forward-arrow flip `svg:has(use[href="#i-arr"])`,
  download split-button radii via `[data-dl-primary]`, vc-arrow connector) injected per
  RTL page by `i18n_wire.py` into a `<!--RTLCSS-->` marker region.
- **Final:** 35 × 13 = 455 pages; linkcheck 0, JSON-LD 0 broken, 0 `/bg/` canonical,
  0 curly attrs, no Bulgarian leaks, gtag byte-identical. Logs/report: `../wave4-7-logs/`.
- **Lessons (also in CLAUDE.md):** translate from `index.html` (EN), NEVER from another
  locale's scaffold; only straight ASCII quotes in attributes/JSON-LD; one opus agent
  per page (sonnet hits the 32K output cap on 1000+ line pages); never leave an
  unattended translation run unsupervised.

## Session log — 2026-06-28 (full QA audit: native + Ahrefs + SEO, all 35)

After the 06-15 build, a deep QA pass (user: "проверь как нативный пользователь каждого
языка + ahrefs + seo"). The earlier 3-pages-per-locale review **under-sampled** —
real bugs hid on the other 10 page types. Audited the under-reviewed content pages
(vc / multistreaming / obs / for-churches) per locale with native-speaker agents +
**mechanical full-site scans** (35×13 = 442 pages). Found & fixed a long tail of
bg-scaffold residue the first cleanup missed:

- **Critical visible-render bugs:** raw JSON-string literals shown as page text
  where real content belonged (`sr/virtual-camera` hero + a FAQ; `sr/multistreaming`
  a heading); `da/for/churches` had **every å/æ/ø stripped to ASCII** (0→346,
  SERP-visible); `hr/for/churches` Step 2 spliced with Step 5 + an **unclosed
  `<details>`** (broke FAQ render) + a duplicate related-card; `hr/virtual-camera`
  truncated hero. All reconstructed from the EN source.
- **Quote glyphs:** the German low-quote `„…"` survived in non-European-convention
  locales — **he** (54, 6 pages; the first reviewers mis-called `„` "proper Hebrew
  quotes"), **th** (21). **zh** used wrong-facing `”…”` (24) instead of `「…」` house
  style. → he/th straight `"`, zh `「」`. **`„` is CORRECT for de/bg/ro/pl/cs/hu/hr/
  sr/sk; it's a BUG only in th/he/ja/ko/zh/vi/hi/ar/fa — scope any `„` scan to those.**
- **Twitch date self-contradiction:** EN-source `multistreaming` FAQ said both "since
  June 2024" and "since October 2023"; it had propagated to 13 locales. Unified to
  October 2023 (matches the JSON-LD). Fix the EN master, then mirror.
- **Missing JSON-LD:** 13 pages had only a `<!-- Schema.org -->` comment, no markup
  (sr×4, zh×3, da/el/hr/sv/cs/he). Added per-page schema copied from `ru`/EN siblings
  + translated to match each page's visible FAQ/HowTo. **A quote-fix agent then broke
  5 he JSON-LD blocks** — replacing `„X"` with straight `"X"` *inside* a JSON string
  value yields invalid JSON; escape inner quotes as `\"` (or single quotes). Caught
  by the scanner, fixed same session.
- **Grammar/term:** `it` virtual-camera split (camera/telecamera → **webcam virtuale**,
  89×) + generic "restream" misuse (clashes with the Restream competitor it argues
  against); `hr` "simultcast"×12; cs/sk/pl/el/bg minor one-offs.
- **SEO (Ahrefs, ~954 units of 100k):** `th` homepage targeted ซอฟต์แวร์สตรีม (**0/mo**)
  → switched to **โปรแกรมสตรีม (200/KD0)**; `id` wove in **aplikasi live streaming
  (4886/mo — the project's biggest keyword)**; `ja` standalone 配信ソフト (648);
  trimmed over-length pt/uk/ro/ru/fi homepage title/meta. New-market Ahrefs confirmed
  Waves 4–7 ≤10/mo (mostly 0). **`fa` is unmeasurable — Iran (`ir`) is excluded from
  Ahrefs' country list (sanctions).**
- **Cross-page term drift** (fi/no/hu/da/nl/vi): a feature named differently across a
  locale's pages (e.g. "Multistream" vs "Monilähetys") → unified to each locale's
  majority / feature-page term.

Final scan (442 pages): 0 unbalanced tags · 0 stray quotes · 0 Twitch-2024 · 0
Cyrillic-outside-markers · 0 invalid JSON-LD · 0 unclosed details. ~17 thematic
commits, all pushed.

**Lessons:** (1) review more than a 3-page sample — the bg scaffold left bugs on
every page type; (2) scope `„`-quote scans by language convention (it's right in
half of Europe); (3) re-validate JSON-LD after any quote/text edit; (4) keep a
mechanical full-site scanner (lang tag · Cyrillic-outside-`<!--LD/HL/AD-->` · `„`/`”`
glyphs · `<style>`/`<script>`/`<details>` balance · `json.loads` every ld+json) and
run it after every locale batch — agents miss what a grep catches, and a grep misses
what a native reads.

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

## Session log — 2026-06-13 (i18n: 3 → 18 languages + dropdown/auto-detect + fixes)

Big session. After the RU/ES work (logged below), the user asked to take the
site to all the languages cam-streaming-guides has (35), natively, in waves of
5, Ahrefs-checked, layout-safe. Built the system and shipped **18 languages**
(top-18 by Ahrefs demand; Waves 1–3). Remaining 17 are ≤10/mo demand, mostly 0.

**Built the i18n engine (no build step):**
- `seo/i18n.py` — 35-locale config (demand-ordered `LANG_ORDER`, `LANG_DONE`,
  native names/flags/labels/paths, RTL set, `DEMAND`) + render helpers
  (dropdown, hreflang, auto-detect JS, dropdown CSS). Ported from camstreamguide.
- `seo/i18n_wire.py` — run after translating; rebuilds dropdown + hreflang +
  auto-redirect + dropdown CSS + `sitemap.xml` across every page, listing only
  locales where each page exists, with EN-fallback for missing siblings (partial
  waves never 404). Idempotent (markers). Always pair with `linkcheck`.
- Replaced the old inline EN·RU·ES 3-button switcher with a `<details>` flag
  dropdown (now 18 langs) + browser-language auto-redirect (localStorage +
  navigator.languages, like camstreamguide).

**Waves (5 langs each, ~5 parallel agents/batch: homepage → SEO-core → rest →
utility):** W1 de/fr/pt/tr/fil · W2 uk/it/vi/id/nl · W3 ro/hi/ja/ms/bg. Per-locale
Ahrefs keywords in `seo/I18N-KEYWORDS.md`. Big wins: ID «aplikasi live streaming»
4886, DE «streaming software» 598 + «obs alternative» 274 (both KD0), PT «como
fazer live no youtube» 1995, JA 配信ソフト 648 / YouTube配信やり方 436, hi EN-SEO
(streaming software 920). **fil + hi: English titles/keywords** (those markets
search tech in English), local-language body. changelog kept 1817 EN bullets per
locale (shell only). Account session limits hit on big batches — retried.

**Layout/content fixes this session:**
- Hero H1 `.blue` keyword had `white-space:nowrap` → overflowed under the app-
  window in long locales → `white-space:normal` + `overflow-wrap:break-word`.
- Nav: long labels + switcher clipped the header button → collapse to burger
  ≤1100px + tighter gaps (all pages).
- uk homepage had a duplicate `<style>` + missing `</style>` (agent bug) that
  broke the whole render → fixed; now verify balanced `<style>` per file.
- Fixed Cyrillic «масOS»→«macOS» typo in the changelog bullet (was in EN source,
  propagated to all locales).
- Removed the dead **InstallMonetizer** section from privacy-policy on all 18
  locales (defunct PPI-bundling disclosure from the old site; dead domain;
  contradicted the "free, no bundle" positioning).
- RU `/ru/virtual-camera/` compatibility grid/orbit: swapped in Яндекс Телемост
  + MAX (RU video-call platforms) for the RU audience.

**To continue to 35:** `python3 seo/i18n.py` prints the remaining waves
(ar/ko/th/pl/hu → …). Same pipeline. But flag the ~0 demand first.

## Session log — 2026-06-13 (RU + ES localization — whole site)

Translated the entire content site into Russian and Spanish (like
cam-streaming-guides), native streaming-scene copy with Ahrefs-picked
keywords per locale. Now **30 content pages**: EN root + `/ru/` + `/es/`,
10 pages each (`/`, products, virtual-camera, multistreaming, alternatives,
alternatives/obs, for, for/youtubers, for/churches, help). Not translated:
changelog, privacy-policy, license-agreement, /v2/, for/vtubers draft.

- **Keywords (Ahrefs ru/es/mx) → `seo/I18N-KEYWORDS.md`.** Notable: RU
  «рестрим» 996, «программа для стрима» 150/KD2, «мультистрим» 100/KD0,
  «как стримить на ютубе» 90/KD0, «трансляция богослужения» 40/KD1;
  ES «multistream» ~700 (kept as the anglicism), «software de streaming» 140,
  «alternativas a OBS» 90 (plural), «cómo hacer un directo en YouTube» 75.
  Each primary key sits in its page's title/H1.
- **Spec → `seo/I18N-PLAN.md`** (binding): URL scheme `/ru/…` `/es/…`,
  per-depth path-shift rules, hreflang/canonical templates, switcher
  markup+CSS, RU/ES glossary + tone, invariants, QA. Assets are NOT copied —
  localized pages reference the EN tree's assets via `../` (e.g. VC partner
  logos at `../virtual-camera/assets/logos/`).
- **hreflang reciprocity:** all 30 pages (incl. the 10 EN originals, patched
  this session) declare en/ru/es/x-default. `sitemap.xml` rebuilt with
  `xhtml:link` alternates (33 url entries, 120 alternates).
- **Language switcher** EN·RU·ES in nav + burger on every page.
- Built mostly by parallel subagents (one page-pair each); a couple hit
  session limits mid-run and were redone. linkcheck: **0 broken across 35
  pages**; mobile (390px) + desktop (1440px) spot-checked on RU home and
  ES multistreaming. Canonicals point at the future `splitcam.com/<locale>/`.
- This closes the migration plan's "Open decision: RU/ES locales".
- **Upkeep rule:** new EN page ⇒ also build `/ru/` + `/es/` + 3 sitemap
  entries; edit copy in one language ⇒ mirror to the other two.

**Utility pages added same day (user: "translate everything", overriding the
leave-changelog/legal-in-EN convention):** `privacy-policy/` + `license-
agreement/` fully translated RU/ES; `changelog/` shell localized (nav, hero,
intros, all 243 New/Improved/Fixed labels, coming-soon panels, footer, title)
while the **1817 technical release bullets stay EN** — Ahrefs shows 0 search
volume for changelog/privacy/license in every locale, and the bullets change
every release. So now **13 pages × 3 locales**. EN utility originals also got
reciprocal hreflang + switcher. sitemap = 39 entries / 156 alternates.
If the user ever wants the 1817 changelog bullets translated too, that's the
one remaining (low-value, high-token) piece left as EN on purpose.

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
  Assets (after the `c973729` squeeze): `stream-preview-av1.mp4` **48KB**
  (svt-av1 crf58, 15fps, codecs string `av01.0.04M.08`) +
  `stream-preview-h264.mp4` **98KB** (x264 crf36, 15fps) — master
  `stream-preview.mp4` (375KB, 20fps) kept untouched as the re-encode
  source. Tried & rejected: av1 crf63 (21KB — visibly soft) and GIF
  (480px/10fps/128colors = **1.98MB**, ~40× heavier — never GIF this).
- **Follow-up (`0d0765f`): video on ALL diagram tiles** — user wanted the
  five platform thumbs animated too. Done WITHOUT re-introducing parallel
  videos: each thumb is a 320×180 `<canvas>` painted from the one video
  via `requestVideoFrameCallback` (rAF fallback) — single decoder,
  frame-perfect sync. Transparent canvas shows the poster (CSS background)
  until the first frame. The "+79" card stays a styled div. Mobile still
  fully static, zero video bytes. Pattern to remember: **one `<video>` +
  canvas mirrors** is the only sanctioned way to multiply this clip.

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
dd92b72 hero video: panels -5% for edge breathing room
c91563b hero video: panels +10% (compound), gap halved to 10px
2367384 hero video: relayout — bigger panels (+10%), wider gap (21px), vivid red top-border
71f4f25 hero video: thicker red top-border (4px) at very top edge of vertical panel
d988017 hero video: 1.2x speed = clean 30fps (fix judder)
0a87173 hero video: restore red top-border on right (vertical) transition panel
8be62bf hero video: extra 1.15x speed (total ~1.32x)
1e383ec hero video: speed 1.15x + livelier source window (src t=12..30.7s)
6dd870f hero video: fully cover right transition panel (fix old-video edge remnants)
f9afc79 hero video: swap presenter to new creator clip (6875068)
14169ae hero video: swap presenter to new clip, remove trial watermark
75a3667 docs: AV scan complete — 24 host-unscannable installers verified clean on Mac (ClamAV 1.5.2), 0 infected site-wide
6469baf docs: ver.txt policy (host-managed, 10.9.2, bump 10d after release) in ONBOARDING + REMINDERS
e2861c0 ops: all ver.txt -> 10.9.2 (host); record ver policy (host-managed, bump 10d after release); drop /ver.txt from repo
958c429 docs: session log 2026-06-29/30 (new pages + URL form + old→new host migration) + cutover/ver-rollout reminders
156a37e chore: add /ver.txt (legacy app update-check file, 8.4.0.0) from live splitcam.com
fdc30a1 chore: nudge GitHub Pages rebuild for .well-known/assetlinks.json
bfda3a8 chore: add /.well-known/assetlinks.json (Android Digital Asset Links) + .nojekyll
51a7987 donate: switch to paypal.me/Katzovich; amount chips are now clickable links (all 35 locales)
0ec26af donate: change suggested amount chips to $25/$50/$100/$200/$500/$1000 (all 35 locales)
```

(cam-streaming-guides repo has its own history — full adult-guides build.)
