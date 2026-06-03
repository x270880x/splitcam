# `/for/vtubers/` — page plan

Build plan for the highest-value missing SEO page. Follows the SEO
template (NAV / BREADCRUMBS / HERO / QUICK ANSWER / STEP-BY-STEP /
BONUS / PRO TIPS / COMPARISON / FAQ / RELATED / CTA / FOOTER) used by
`/for/youtubers/` and `/for/churches/`. **Body copy must be unique** —
do not paste from youtubers/churches (CLAUDE.md rule).

## Why this page first

| Keyword | Vol (US) | KD | Note |
|---|---|---|---|
| **how to be a vtuber** | 500 | **0** | 🔥 jackpot — KD 0, informational, page can own it |
| **vtuber software** | 1000 | 67 | hard head term; long-game |
| **free vtuber software** | 200 | 47 | mid — "free" angle is our edge |
| **vtuber streaming** | 30 | 1 | easy long-tail |

Total ~1730 vol sitting on an "In development" stub. The KD-0
"how to be a vtuber" (500) alone is free traffic if we publish a
genuine how-to.

## Meta

- **Title** (≤60): `How to Be a VTuber — Free VTuber Software Setup | SplitCam`
  - Leads with the KD-0 winner "how to be a vtuber" + "free vtuber software".
- **Description** (~150): `How to be a VTuber on a budget — free VTuber software to add your avatar, AI background, face tracking and chromakey, then go live or hit any meeting app. Win, Mac, iOS, Android.`
- **Canonical**: `https://splitcam.com/for/vtubers/`
- **Keywords meta**: how to be a vtuber, vtuber software, free vtuber software, vtuber streaming software, vtube studio splitcam, vtuber virtual camera
- **OG/Twitter**: type=article, title/desc mirrored, image = hero poster (or a vtuber-specific cover if produced later)
- **H1**: `How to be a VTuber — free software, real avatar, zero green screen.`
  (contains exact "how to be a vtuber" + "free software")

## Schema.org (@graph)

Mirror the youtubers/churches stack:
1. **BreadcrumbList** — SplitCam › Use Cases › For VTubers
2. **HowTo** — "How to Be a VTuber and Go Live" (5 steps, totalTime PT10M)
3. **SoftwareApplication** — SplitCam + AggregateRating 4.7/357
4. **FAQPage** — 6–8 Qs (see below)

## Section-by-section content

### HERO
- Eyebrow: `For VTubers`
- H1 (above)
- Sub: lead with the promise — "Become a VTuber with free software: pipe
  your Live2D / 3D avatar through SplitCam, add AI background, face
  tracking and chromakey, then stream to Twitch/YouTube or drop the
  avatar into any meeting app as a virtual camera."
- CTA: Free Download + "Jump to setup"
- Badges: Free forever · No green screen · Win·macOS·iOS·Android

### QUICK ANSWER (featured-snippet bait — targets "how to be a vtuber")
A 40–55 word direct answer block:
> "To become a VTuber you need three things: an avatar (Live2D via
> VTube Studio, or a 3D model), face/motion tracking, and software to
> composite and broadcast it. SplitCam is the free layer that takes
> your avatar, removes the background with AI, and outputs it to
> Twitch, YouTube or any meeting app — no green screen, no subscription."

This paragraph is the play for the KD-0 "how to be a vtuber" snippet.

### STEP-BY-STEP — "How to be a VTuber in 5 steps" (HowTo schema source)
1. **Pick and rig your avatar** — Live2D model in VTube Studio (2D) or a
   3D model in Warudo/VSeeFace. Free starter avatars exist; webcam face
   tracking drives the mouth/eyes.
2. **Bring the avatar into SplitCam** — add VTube Studio (or your avatar
   app) as a window/game/Spout source. Apply chromakey or AI background
   removal so only the avatar shows — no green screen needed.
3. **Add your scene** — overlays, alerts, lower-thirds, game capture
   behind the avatar. Build wide / chat / BRB scenes, switch with
   hotkeys.
4. **Beauty + 3D masks (optional)** — face masking, 3D masks, Streamfog
   lenses on top of the avatar for extra flair.
5. **Go live or join a call** — multistream to Twitch + YouTube at once,
   or pick "SplitCam Camera" in Zoom/Discord to appear as your avatar in
   any video app.

Each step ~50–80 words, unique copy, with the timing chips (~2 min etc).

### BONUS — "Be a VTuber in video calls too"
Short block: the virtual-camera angle (avatar in Discord/Zoom/Meet).
Cross-links to `/virtual-camera/`. Unique to this page (youtubers/churches
don't have it).

### PRO TIPS (3–4, with emoji + glow per the site language)
- 🎭 Layer the avatar over game capture for reaction streams
- ✨ AI background beats chromakey if your room has uneven light
- 🎙 Route mic through the VST chain for a cleaner voice
- ⚡ Replay Source for instant clip moments mid-stream

### COMPARISON — "SplitCam vs other VTuber setups"
Table vs the alternatives VTubers actually consider:
| | SplitCam (free) | VTube Studio alone | OBS + plugins | Streamlabs |
|---|---|---|---|---|
| Avatar compositing | ✓ | partial | ✓ (plugins) | ✓ |
| AI background (no green screen) | ✓ | ✗ | plugin | ✗ |
| Multistream built-in | ✓ | ✗ | plugin | paid |
| Virtual camera to meeting apps | ✓ | ✗ | ✓ | ✓ |
| Price | Free | Free | Free | Freemium |
Honest: VTube Studio still does the actual rigging — SplitCam is the
broadcast/compositing layer on top.

### FAQ (FAQPage schema) — draft Qs
1. How do I become a VTuber for free? (→ avatar app + SplitCam, KD-0 intent)
2. What software do VTubers use? (vtuber software term)
3. Do I need a green screen to be a VTuber? (no — AI background)
4. Can I use my VTube Studio avatar in SplitCam? (yes — window/Spout source)
5. Can I be a VTuber in Zoom or Discord? (yes — virtual camera)
6. Do I need an expensive PC to VTube? (hardware reality)
7. Can I multistream as a VTuber to Twitch and YouTube? (yes)
8. Is SplitCam really free for VTubing? (yes, no watermark)

### RELATED
Link to: `/for/youtubers/`, `/virtual-camera/`, `/multistreaming/`,
`/for/` hub.

### CTA + FOOTER
Standard free-download CTA + shared footer.

## Internal-linking actions when shipped
- `/for/` hub: flip the "For VTubers" card from stub → live link `vtubers/`
- Homepage use-cases: the "For VTubers" 🎭 card could link here (currently
  the homepage VTubers card is a `.usecase soon` div — make it an `<a>`)
- `/virtual-camera/` uc-card "VTubers in video calls" → link here
- Add to `sitemap.xml` (priority 0.7, changefreq monthly)
- Schema BreadcrumbList parent = /for/

## Keyword placement checklist (post-build)
- [ ] "how to be a vtuber" in H1 + QUICK ANSWER + 1 FAQ Q
- [ ] "vtuber software" in title + a H2 + body ×2
- [ ] "free vtuber software" in description + body ×1
- [ ] "vtuber streaming" / "virtual camera" naturally in body
- [ ] body ≥ 1400 words (match youtubers/churches depth)
- [ ] run seo/PAGE-SIMILARITY.md vs youtubers/churches — must be unique
