# SplitCam.com — Migration Plan (live site → new site)
*Created 2026-05-21. Compares the live splitcam.com (≈260 indexed URLs) against the redesigned site currently on GitHub Pages.*

## Key finding up front

Only **one** page is a true same-URL 1:1 replacement: the **homepage `/`**.
Everything else we've built (`/virtual-camera/`, `/multistreaming/`, `/products/`, `/for/*`, `/alternatives/*`) sits at **new URLs that don't exist on the live site**. That's actually good news — new URLs carry **no redirect risk** and **no "replacement" spam risk**. They're purely additive.

The migration is therefore: **(1) swap the homepage, (2) add new pages in waves, (3) decide what to do with a handful of legacy pages (`/features`, `/download`, `/tour/*`, locales).**

---

## LIST 1 — Ready to replace NOW (finished replacement exists)

| Live URL | Our replacement | Action | Risk |
|---|---|---|---|
| `/` (homepage) | `index.html` (Variant A) | Direct swap, same URL | Low — temporary ranking wobble 1-4 wks, normal |

Open decision before swap: **Variant A vs Variant B (`/v2/`)** — pick one homepage. Only A or B goes live, not both. `/v2/` should not be a public URL.

---

## LIST 2 — Live pages that still need a replacement / decision

These pages exist on splitcam.com and are indexed. We have NOT built a replacement. Each needs a decision: rebuild, redirect, or leave.

| Live URL | What it is | Recommended action |
|---|---|---|
| `/features` | Features overview page | Build a `/features/` hub (see SITEMAP.md) OR 301 → `/products/`. Don't leave it pointing at an old design while homepage is new. |
| `/download` | Main download page | Build a new `/download` OR let `/products/` serve as the download hub and 301 `/download` → `/products/`. |
| `/downloadnew` | Duplicate/alternate download page | 301 → `/download` (or `/products/`). Kill the duplicate. |
| `/tour` + 6 sub-pages | Old product-tour walkthrough | Concept is dated. 301 the lot → `/features/` or `/products/`. Don't rebuild as-is. |
| `/more-plugins` | Plugins / add-ons page | Decide if still relevant. If yes — light refresh; if no — 301 → `/features/`. |
| `/splitcam-changes-win`, `/splitcam-changes-mac` | OS-split changelogs | Build one `/whats-new/` (or `/changelog/`) page; 301 both old URLs to it. |
| `/donate-us` | Donation page | Leave, or light restyle to match new design. Low priority. |
| `/contact-us` | Contact page | Light restyle to match new design, same URL. |
| `/license-agreement`, `/privacy-policy`, `/privacy-policy-for-mac-apps` | Legal | Leave URLs; restyle later. No SEO impact. |
| `/help/*` (~115 EN pages) | Help / docs / tutorials | OUT OF SCOPE of the redesign. Leave entirely. Re-skin later if desired. |
| `/blog/` (+ categories) | Blog | Leave. Keep — SITEMAP.md flags blog as a strength to grow. |
| `/forum/` | Community forum | Leave — separate app. |
| `/download-splitcam-for-macos-mojave-and-catalina` | Legacy-macOS download | Leave (serves old-OS users) or fold into `/products/mac/`. |
| `/download-archive-for-windows` | Windows download archive | Leave or fold into `/products/windows/`. |

### Locale variants — needs its own decision
- `/ru/` ≈95 pages, `/es/` ≈45 pages — fully built and indexed.
- `/tr/`, `/hi/`, `/de/`, `/ar/` — exist but robots-blocked.
- We built **English only**. If we swap the EN homepage, the RU/ES sites still show the old design → split-brand inconsistency.
- **Decision needed:** (a) localize the new homepage to RU/ES before/with launch, (b) launch EN first and localize RU/ES in a follow-up, or (c) leave locales on the old design indefinitely. Given the user is Russian-speaking, RU likely matters.

---

## LIST 3 — New pages (no live equivalent — release in waves)

These are net-new URLs. No redirect needed. Release in waves to avoid the content-farm spam signal (per PLAN.md).

### 3a — Already built ✅ (ready to publish)
| New URL | Type |
|---|---|
| `/virtual-camera/` | Feature page |
| `/multistreaming/` | Feature page |
| `/products/` | Products hub |
| `/for/youtubers/` | SEO persona page |
| `/for/churches/` | SEO persona page |
| `/alternatives/obs/` | SEO comparison page |

> Note: `/virtual-camera/` and `/multistreaming/` topically overlap the live `/help/multi-streaming` docs, but they are **separate new marketing URLs** — additive, not replacements. The help docs stay where they are.

### 3b — Planned, not built yet (from PLAN.md + SITEMAP.md)
| New URL | Wave |
|---|---|
| `/alternatives/` hub | Wave 2 |
| `/for/` hub | Wave 2 |
| `/alternatives/streamlabs/`, `/restream/`, `/streamyard/` | Wave 2 |
| `/for/vtubers/` | Wave 2 |
| `/alternatives/vmix/`, `/manycam/`, `/meld-studio/`, `/snap-camera/` | Wave 3 |
| `/for/streamers/`, `/for/educators/` | Wave 3 |
| `/features/` hub + 6 feature pages | unscheduled (SITEMAP.md rec) |
| `/products/windows/`, `/mac/`, `/ios/`, `/android/`, `/remote/` | unscheduled (SITEMAP.md rec) |
| `/alternatives/prism-live/`, `/alternatives/ecamm/` | unscheduled (SITEMAP.md rec) |
| `/for/gamers/`, `/for/business/` | unscheduled (SITEMAP.md rec) |
| `/whats-new/`, `/tutorials/`, `/about/` | unscheduled (SITEMAP.md rec) |

---

## Recommended launch sequence

1. **Pick homepage variant** (A or B) — blocking decision.
2. **Launch step 1 — homepage + already-built new pages.** Swap `/`, publish the 6 List-3a pages. They're new URLs, safe to ship together (they're a coherent site section, not a thin-content dump).
3. **Redirect cleanup.** 301 `/downloadnew` → `/download`, `/tour/*` → `/features/` or `/products/`, changelog pages → `/whats-new/`. Build `/whats-new/` and `/features/` (or decide redirects) before/with this step.
4. **Decide locales** (RU/ES) — see List 2.
5. **Waves 2 & 3** — per PLAN.md calendar, the remaining new pages.

## What is NOT touched
`/help/*` (~115 pages), `/blog/`, `/forum/`, legal pages — left on the existing site. The redesign covers marketing pages only.
