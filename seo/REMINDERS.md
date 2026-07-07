# SEO Reminders — Wave 1 follow-up

> **For future Claude (or me):** This file is the durable replacement for in-chat cron reminders, which die when a chat session ends. Check the table below at the start of any new SEO-related chat. If today's date is on or past a "do by" date below, run the linked task.

**Wave 1 launched:** 2026-05-20 (3 pages live on GitHub Pages).

## Schedule

| Do by | Status | Task | What to do |
|---|---|---|---|
| **2026-05-25** | ✅ 2026-07-02 CONFIRMED LIVE — play.google.com com.splitcam = 200, links active site-wide | SplitCam Android — Play Store approval check | See section below |
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

## Standing rule — Hebrew locale: SplitCam is FEMININE (2026-07-02)

In `he/`, the brand **SplitCam takes feminine agreement** (as תוכנה): verbs, adjectives,
pronouns — `SplitCam עובדת / תומכת / חינמית / זמינה`, `היא / אותה`. The whole locale was
unified 2026-07-02 (all 15 pages, JSON-LD included). **Any new or edited `he/` copy must
keep feminine agreement** — don't reintroduce `SplitCam עובד / חינמי / הוא`. Same applies
to SplitCam Remote (אפליקציה). Words agreeing with other subjects (צוות, דרייבר, שידור,
OBS…) keep their own gender.

## Pre-migration — legacy page decisions (2026-06-28, both RESOLVED)

- `/contact-us` (+ `/ru/kontakty`, `/es/contactenos`) — **RESOLVED 2026-06-28: 301 →
  `/help`** (the support hub: Telegram · Forum · FAQ). No static page rebuilt, no form
  backend needed. In `redirects.htaccess` + cloudflare CSV. (Old `aboutus.html` retargeted
  to `/help` too, to avoid a 2-hop chain.)
- `/donate-us` (+ `/ru/pozhertvovat`, `/es/donarnos`) — **RESOLVED 2026-06-28: BUILT** in
  all 35 locales (slashless `/donate-us`). **Updated 2026-06-30:** donations now go to
  **`paypal.me/Katzovich`** — amount chips ($25/$50/$100/$200/$500/$1000) are clickable
  `paypal.me/Katzovich/<amt>USD` links; the old hosted button (`32FNT59FAVDPN`) was
  removed everywhere. Old localized ru/es donate URLs 301 → `/ru/donate-us`,
  `/es/donate-us` (in `redirects.htaccess` + CSV). If the PayPal target ever changes,
  update it in all 35 `*/donate-us/index.html`.

---

## NEW host migration — status + cutover checklist (2026-06-29/30)

New prod target: **cPanel `~jntckkaf` on rocket-cp2.hostsila.org** (cutover IP
`91.223.223.113`), preview http://rocket-cp2.hostsila.org/~jntckkaf/. SSH creds:
`~/.hostsila_ssh` (new, full shell), `~/.splitcam_old_ssh` (old, SFTP-only). See the
2026-06-29/30 session log in `ONBOARDING.md` and memory `project-splitcam-hosting`.

**Already on the new host:** full redesign (slashless/features/donate/footers/Skype-0),
`win-download/` (installers updated to 10.9.2 build; 32-bit untouched), `ver.php`,
`ofcf-turnstile.php`, all three `ver.txt` = **10.9.2**, `.well-known/assetlinks.json`.
**Verified 2026-07-02:** full sweep — all 578 deployable repo files byte-identical (md5)
on the host, 0 drift; win-download fully AV-audited 0 infected (manifest
`~/clamav/fullscan-2026-07-02.log` on the host: path|md5|verdict for every file).

## ✅ CUTOVER EXECUTED — 2026-07-02 ~19:00
splitcam.com + www -> **91.223.223.113** (proxied), cache purged, live battery green
(pages 200, slashless 301, all redirect classes incl. adult->camstreamguide, ver.php/.cfg/
installer OK). Mail PINNED to old server first: mail/webmail = A 77.83.100.124 (DNS only),
MX -> mail.splitcam.com — old server must stay alive for mail. www->apex 301 via CF dynamic
redirect rule. Origin cert = CF Origin CA (to 2041). Rollback: A records back to
77.83.100.124. Post-cutover follow-ups below.

**MAIL MIGRATED — 2026-07-02 ~20:40.** All 7 mailboxes (admin, pola, wpscmail + 4 stubs,
~35 MB) moved old->new cPanel with passwords (etc/shadow copy); local delivery verified;
delta-check = 0 lost messages. DNS: mail/webmail A -> 91.223.223.113, MX -> mail.splitcam.com,
SPF += new IP, DKIM TXT -> new host key. Client settings unchanged (mail.splitcam.com).
Old server: no active role left; keep ~2 weeks as fallback, then decommission decision.

**Post-cutover follow-ups:**
- Mail: watch AutoSSL issues cert for mail./webmail. (until then clients may see a
  name-mismatch warning); after ~2 weeks remove old IPs (77.83.100.124, 185.67.0.5,
  194.28.87.164) from SPF; user should test-login each mailbox.
- ~~Submit sitemap in GSC~~ ✅ done 2026-07-02; watch indexing of 34 locales
  (old robots blocked /de/ /tr/ /hi/ /ar/ — now open) — first coverage check +7d.
- Build /for/streamers + /for/educators, retarget the 6 blog rules from /for.
- Re-issue the CF Origin cert pair (private key transited chat 2026-07-02) — low risk, free.
- Re-run indexing/ranking checks (+7d, +14d) and Month-1-style Ahrefs vs baseline (+30d).
- Old server: keep alive (mail + adult-source pages); decide mail migration separately.
- Watch new-host bandwidth usage (16 GB installers now on live traffic) — hoster quota unknown.

**Original checklist (executed):**
- **SHIP `/for/streamers` + `/for/educators` BEFORE cutover** (user 2026-07-02: blog 301s
  already point at these planned Wave-3 URLs — 5 rules → /for/streamers, 1 → /for/educators.
  If they can't ship in time, flip those 6 rules in `seo/redirects.htaccess` to `/for`).
- Point splitcam.com DNS → `91.223.223.113`.
- **REPLACE** the docroot `.htaccess` with current `seo/redirects.htaccess` — the file
  already sitting on the host is the STALE 2026-05-21 generation (no slashless
  RewriteRule, no ru/es 301s, no contact-us→help, no donate). Replace, don't append.
  (Inert on the preview — anchored `^/` patterns never match `/~jntckkaf/` URIs.)
- ~~Fix `.cfg` serving BEFORE cutover~~ — **RESOLVED 2026-07-02 via Cloudflare.** The new
  host 403s `*.cfg` at the SERVER level (extension-based, pre-file-check, applies to real
  vhosts too — `.htaccess` Require/rewrite/Options all tested, cannot override; hoster
  ticket would be the only host-side fix). Solution in place: **3 Cloudflare Transform
  rules** on the splitcam.com zone (ids `999f7264…`/`ec0c8b86…`/`5d64c6c8…`) rewrite
  `/win-download/update/{proxy,ingests,ingests2}.cfg` → `…/{…}_cfg.bin`; the `.bin`
  hardlink copies exist on BOTH origins (old host via SFTP, new host via `ln`), so the
  rule is live-neutral now and cutover-proof later. Verified through live CF: all three
  .cfg URLs 200, md5 byte-identical. **Sync rule:** if a `.cfg` ever changes, refresh its
  `_cfg.bin` twin (hardlink on the new host survives in-place edits, NOT replace-by-rename).
  Rollback: delete the zone's `http_request_transform` ruleset.
- Re-deploy the redesign if the repo changed since (host pulls the GitHub main tarball and
  overlay-copies, excluding `.git/seo/v2/.claude/*.md/.nojekyll`; never `--delete` or you
  wipe win-download).
- Purge Cloudflare cache for `win-download/SplitCamSetup_x64.msi` (cache rule, 1-day TTL).

## ver.txt policy — RESOLVED (user, 2026-06-30)

The weekly-ramp idea was dropped. **All ver.txt track the current release.** Set
2026-06-30 to **10.9.2** (the live version): root `/ver.txt` (was 8.4.0.0),
`win-download/update/ver.txt` (already 10.9.2), `win-download/update/light/ver.txt`
(was 10.5.0). `ver.php` just echoes the root `/ver.txt` + its mtime.

**STANDING RULE:** when a new SplitCam version ships on the site, **10 days after the
release** set **all three ver.txt** to the new version string (plain text, no trailing
newline, e.g. `10.9.2`). The matching new installer must already be deployed first.

All three ver.txt are **host-managed** (NOT in the git repo — removed root `/ver.txt`
from the repo so a re-deploy overlay can't reset it). Edit them directly on the host via
SSH (`~/.hostsila_ssh`).

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
## ✅ DirectAdmin TRIAL server provisioned + fully staged (2026-07-06)
Turbo NVMe Trial ordered. **SSH creds: `~/.hostsila_da_ssh`** (chmod 600). Server
`rocket-da4.hostsila.org`, IP **185.67.3.44**, user **lwanngbs**, docroot
`/home/lwanngbs/domains/splitcam.com/public_html`. PHP 7.4, wget/curl present.
Already deployed there (parallel to live cPanel, NOT cut over): all 527 pages + infra
(`ver.php`, `ofcf-turnstile.php`, `.htaccess`=redirects, `ver.txt`x3, `site.webmanifest`,
IndexNow key, real `.cfg` files) + 21 installers (10.8.x–10.9.2 + light, 9.3G).
**KEY WIN: DA serves `.cfg` natively (200, no 403!)** → at cutover the 3 Cloudflare
`.cfg`→`_cfg.bin` transform rules become UNNEEDED (can delete them). Battery on the DA
origin (curl --resolve …:185.67.3.44) = all green: pages 200, slashless 301, redirect
classes incl. blog/adult/installer-to-GitHub, `.cfg` 200, custom 404. `ver.php` outputs
empty — but SAME as live cPanel (it reads ver.txt, never echoes; app reads ver.txt
directly), so parity confirmed. Trial has NO mail yet — mail migration is a separate
step. Remaining before real cutover: ~~install CF Origin cert on DA~~ ✅ DONE 2026-07-06,
verify mail plan, flip DNS to 185.67.3.44 + purge, keep cPanel ~2wk fallback.

**✅ SSL on DA — DONE 2026-07-06.** DA now serves the **CloudFlare Origin Certificate**
(CN=CloudFlare Origin Certificate, SAN `splitcam.com`+`*.splitcam.com`, valid to 2041) on
:443 for both apex+www SNI → works in CF Full **and** Full-strict, so the DNS flip won't
need any CF SSL-mode change. Method (fully API, no dashboard, private key never in chat):
pulled the SAME CF Origin cert+key already installed on live cPanel — cert via UAPI
`SSL/installed_hosts` (`certificate_text`), key via UAPI `Fileman/get_file_content` on
`~/ssl/keys/b2c9b_….key` (matched to cert by modulus md5 `26fd59…`) — then installed on DA
via panel API `CMD_API_SSL action=save type=paste` (DA API reachable at
`https://185.67.3.44:2222` with the SSH creds). Disabled DA's LE auto-renew for splitcam.com
so it can't overwrite the Origin cert. Key files shredded from scratchpad after install.
**Still pending (hygiene, NOT blocking):** re-issue a FRESH CF Origin pair (the reused key
transited chat 2026-07-02) — needs the CF dashboard or the Origin CA Key (our zone API token
returns 1016 on the Origin CA endpoint, can't automate).

**⚠️ MAIL CANNOT be pre-staged on DA (found 2026-07-06).** Tried; hit an access wall:
DA's mail-auth store is root/mail-owned and invisible to the user (`/etc/virtual/` absent,
`~/etc/` absent, per-box `$6$` hash not readable/writable over SSH), and DA API `CMD_API_POP`
only accepts **plaintext** passwords — we hold only the cPanel `$6$` hashes (irreversible,
readable via cPanel UAPI `Fileman` on `~/etc/splitcam.com/shadow`). So passwords can't be
ported "unchanged" by us, and messages would go **stale** anyway (MX stays on cPanel until
the flip). → **Do mail AT cutover**, pick one:
  - **(A) hostsila support server-side migration** [recommended — both plans are the SAME
    provider (cPanel + DA on hostsila); they have root, preserve passwords + messages, zero
    client reconfig]. Open a ticket on cutover day.
  - **(B) imapsync** cPanel-IMAP→DA-IMAP with **user-supplied plaintext** box passwords:
    create the 7 DA boxes via `CMD_API_POP` with the SAME plaintext passwords (→ clients
    unchanged) then imapsync copies all folders/messages. Needs the plaintext from the user.
  - **(C) fresh passwords** on DA + user updates the ~3 real clients once (simplest).
The 7 boxes = **~29 MB total**: `admin@` ~28 MB is the only substantial one; `pola@` ~0.6 MB,
`wpscmail@` ~0.25 MB; 4 persona stubs (`damonwilson/michaelfroman/frederickkempe/martinkimani`)
~77 KB each. SSL scaffold already done, so cutover = mail (one of A/B/C) + DNS flip + purge.

**✅ FULL PARITY AUDIT — DA vs live cPanel, 2026-07-06.** Everything except mail is byte-clean:
- **Site:** 579 deployable repo files → **0 missing, 0 md5 drift** on DA (byte-identical). DA
  has only the expected host-managed extras (`.htaccess`=repo md5, IndexNow key, `ver.php`,
  `ver.txt`, `ofcf-turnstile.php`, default `cgi-bin/.htaccess`).
- **win-download:** was missing **2** update-mechanism files (`update/2024-05-26.txt` = v10.7.44
  release-notes, `update/ingests.tar.gz` = ingest bundle) — both were live-200/DA-404; **copied
  cPanel→DA + verified** (200, md5 match). Now 32/32 at parity. Installer sizes all match.
- **Redirects (curl --resolve on DA):** every class fires — slashless 301, contact/ru/es→help,
  donate localized, blog→camstreamguide, forum→help, adult→camstreamguide, installer+archive→
  github, branded 404 (SIGNAL LOST), `.msi`=`application/x-msi`+`attachment`.
- **PHP:** `ver.php` & `ofcf-turnstile.php` DA≡live (byte-identical responses).
- **SEO files on DA:** robots (→splitcam.com/sitemap.xml), sitemap.xml (526 URLs), favicon,
  apple-touch, assetlinks — all 200. **Domains:** only `splitcam.com`, no sub/addon/parked
  on either side — nothing extra to move.
- **Couldn't verify:** cPanel cron list (its Cron API module is server-side broken) — low risk
  (ver-ramp was dropped, nothing time-based), glance at cPanel→Cron Jobs UI if paranoid.
So the ONLY thing left to move at cutover is **mail**; content+infra+redirects+SSL are done.

## ✅✅ DA CUTOVER EXECUTED — 2026-07-06 (WEB now on DirectAdmin)
Flipped **web only**: Cloudflare A `splitcam.com` + `www` → **185.67.3.44** (proxied), cache
purged. **Mail LEFT on cPanel** on purpose — `mail`/`webmail` A (91.223.223.113) + `MX →
mail.splitcam.com` untouched, so mail keeps flowing to cPanel (no mail-migration risk today).
Confirmed DA is the live origin via a unique probe file served through live CF (exact match,
then removed). Live battery all green through CF: pages incl. /ru/, slashless 301, contact→help,
blog→camstreamguide, installer→github, `.cfg` 200, `.msi`=x-msi+attachment, branded 404, ver.php.
- **Live origin now: DA `lwanngbs@185.67.3.44`** (SSH `~/.hostsila_da_ssh`, panel API :2222).
- **cPanel `jntckkaf@91.223.223.113` = FALLBACK** (still serves mail; keep ~2 wks, then decide).
- **ROLLBACK (fast):** CF A `splitcam.com`+`www` back to `91.223.223.113` + purge. cPanel web
  is untouched and still fully deployed, so rollback is instant.
- **Record IDs** (for future flips): apex `d824889430ec8c50ca7ce74ea0a52636`, www
  `29269e69d16ba4434327c3439067cf66`.
**Post-cutover follow-ups:**
1. Watch 48 h (traffic, errors, new-host bandwidth — 9.3 GB installers now on DA egress).
2. **Delete the 3 CF `.cfg` transform rules** (`http_request_transform` ruleset) — DA serves
   `.cfg` natively; left them today to change one thing at a time. Verified `.cfg`=200 via CF WITH
   rules still on, so removal is safe anytime after stability confirmed.
3. **Mail migration** (method A/B/C above) — do BEFORE cancelling cPanel; until then cPanel must
   stay alive for mail. User: send a test mail to confirm delivery still works (should — untouched).
4. Then flip `mail`/`webmail` A + re-point once mail is on DA, and decommission cPanel.

## Installers split: pre-10.8 → GitHub-only (2026-07-06, user request)
Host keeps ONLY 10.8.x–10.9.2 (+ boevye + light) = 9.3G (was 16G). Everything older lives
on **GitHub `x270880x/splitcam-release`**: releases v9.0.9–v10.7.44 (per-version msi/x64
assets) + new **`legacy-archive`** release (7 museum .exe 4.2–8.1 + `splitcam.exe` stub).
Changelog download-arrows already point straight at the GitHub assets. Old host URLs
`/win-download/update/*` + `/archive/*` + `/splitcam.exe` → **301 to the SAME version's
GitHub asset** (38 rules in `seo/redirects.htaccess`, NOT to the new version — user wants
the requested old version to actually download). Verified live end-to-end (206 through
2 hops).

## Panel migration cPanel -> DirectAdmin (planned ~2026-08-01, user 2026-07-06: DA plan is 2x cheaper)
Wait until Google digests the 526 pages (check GSC coverage first). New DA plan = new server/IP.
Checklist (mirror of the 2026-07-02 cutover, proven twice):
1. User: order the DA plan KEEPING the cPanel plan active in parallel; save creds to a
   chmod-600 file (like ~/.hostsila_ssh) — never in chat.
2. Transfer: site tarball via GitHub (deploy2.sh pattern) + win-download 16GB host-to-host
   (wget/rsync) + docroot .htaccess from seo/redirects.htaccess + ver.php/ofcf-turnstile.php
   + ver.txt x3 (host-managed!) + win-download/update/.htaccess + *_cfg.bin hardlinks
   + IndexNow key file (485c...txt) + 7 mailboxes (mail dirs + passwords).
3. SSL: ✅ DONE 2026-07-06 — CF Origin cert (reused from cPanel) installed on DA, serves apex+www. (Re-issue a fresh pair later via dashboard — hygiene only.)
4. Domain: add splitcam.com alias on DA BEFORE DNS flip.
5. Test EVERYTHING via curl --resolve on the new IP (redirect battery 35+, cfg via CF,
   installer range, ver.php, mail ports) BEFORE touching DNS.
6. Flip A records (apex+www) via CF API, purge everything, live battery, watch 48h.
7. Keep cPanel plan ~2 weeks as fallback, then cancel. Update memory/ONBOARDING/REMINDERS creds+IP.
Known trap to re-verify on the new server: global Apache quirks (the .cfg 403 story) — CF
transform rules cover .cfg regardless; adapt deploy tooling from cPanel UAPI to DA API.

## Search-engine registration (2026-07-02, post-cutover)
- **IndexNow — DONE:** all 526 sitemap URLs submitted (api.indexnow.org 200, bing 200,
  yandex 202). Key file: https://splitcam.com/485c229ee85ee55f1967363aabec7e9a.txt (host-managed,
  in public_html; NOT in the repo — re-upload if docroot is ever rebuilt from scratch).
  **Practice:** after adding/renaming pages, re-submit changed URLs:
  POST https://api.indexnow.org/indexnow {host, key, keyLocation, urlList}.
- **Google — DONE:** sitemap.xml submitted in GSC by user 2026-07-02 (property
  sc-domain:splitcam.com, DNS-verified). Check coverage report in ~2-3 days.
- Optional later: Bing Webmaster Tools (import from GSC), Yandex Webmaster UI for RU market.


## Developer docs resurrected at /plugins/ (2026-07-07)
The old site's Developers section is BACK: full Doxygen mirror (94 files — SplitCam Plugin
API: IPlugin/IImageSource/IWebSource, `splitcam_plugin.h`, `SamplePlugin.zip`) rescued from
the old origin (77.83.100.124, still serving) into repo `/plugins/`, GA injected. Footer
"Developers" link (translated) on ALL 527 pages → `https://splitcam.com/plugins/`.
Rules: **/plugins/ is the ONE trailing-slash dir** (relative hrefs; `/plugins` 301s back to
`/plugins/` — exception carved into the slashless RewriteRule block); `/help/developers-docs`
+ `/es/ayuda/guia-para-desarrolladores` 301 → `/plugins/` (above the /help catch-all).
`linkcheck.py` SKIP_DIRS includes `plugins`; **deliberately NOT in sitemap.xml** (legacy
tech docs; discovery via 527 footer links) — do not "fix" that. If the plugin API ever gets
a real product page, build it as a normal locale page and keep /plugins/ as the docs.

## macOS direct download + auto-update feed (2026-07-07, host-managed, NOT in git)
Rescued from the dying old host `77.83.100.124` onto DA — all under docroot `/mac-download/`:
- **`SplitCam.dmg`** — current Mac build **v1.22 (build 259)**, 282 MB, macOS 12+, signed
  (Team QRBUBRN5RF). Linked from the changelog Mac panel (version label = download link).
- **`update/macver.plist`** (old feed format) + **`update/versions.json`** (new format) — the
  Mac app polls `https://splitcam.com/mac-download/update/` for these. Both now advertise
  **actualVersion 1.22 / actualBuildNumber 259**, `downloadURL = /mac-download/SplitCam.dmg`.
- **`update/restream.json`** + **`update/services.json`** — restream-server + channel/service
  config the app also fetches (services.json is JSON5: has trailing commas — mirror byte-for-byte,
  do NOT reserialize). Left unchanged.
These files are **host-managed** (like ver.txt / win-download / IndexNow key — NOT in the git
repo, so a docroot rebuild won't touch them; re-upload from scratch if the docroot is ever wiped).
**STANDING RULE — when a new macOS build ships:** replace `SplitCam.dmg`, then bump BOTH
`update/macver.plist` (actualVersion + actualBuildNumber + downloadURL) AND the `macOS` block of
`update/versions.json`, and add the release to the Mac changelog panel (localized New/Updated/Fixed
labels, English notes, version label → DMG, bump the macOS tab-count incl. fa Persian numerals).
(Note: versions.json's `windows` block is stale at 10.7.18 — the Windows app uses `win-download/
update/ver.txt` = 10.9.2 instead, so it's harmless; fix only if something starts reading it.)
