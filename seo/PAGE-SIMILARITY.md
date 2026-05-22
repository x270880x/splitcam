# Page Similarity Report — duplicate / similar content audit

*Generated 2026-05-22. Method below. Re-run anytime the pages change.*

## Method

- Visible text only — HTML stripped, `<script>/<style>/<svg>` dropped.
- Shared **`<nav>` / `<header>` / `<footer>`** excluded (boilerplate); 4-word
  shingles repeated across ≥ half the pages also flagged as template and removed
  from the literal-overlap count.
- Two metrics per pair:
  - **Cosine** — TF-IDF cosine over unigrams + bigrams = *thematic* similarity
    (do the pages talk about the same things / target the same keywords).
  - **Phrase** — 4-word shingle Jaccard = *literal* text duplication (verbatim
    sentences copied between pages).
- "Closest neighbour" is ranked by cosine.

## Summary table — closest neighbour per page (sorted by % similarity desc)

| Page | Closest neighbour | Cosine | Phrase | Comment |
|---|---|---:|---:|---|
| `/v2/` | `/` | 23.2% | 3.9% | `/v2/` is the archived Variant B of the homepage — shares hero + feature copy ("0.3 fps impact", "across Zoom and YouTube", "no cloud middleman", "commercial use, no watermark"). **No SEO risk:** `/v2/` is `noindex` and unlinked. |
| `/` | `/v2/` | 23.2% | 3.9% | Same pair. Against indexable pages the homepage's real closest is `/for/youtubers/` (21.6%). |
| `/for/youtubers/` | `/` | 21.6% | 2.2% | SEO page reuses homepage feature copy — platform list ("Windows 10/11 · macOS 11 · iOS"), "background removal, no green screen", "commercial use, no watermark". Different search intent (brand landing vs how-to query) → low cannibalization risk. |
| `/for/churches/` | `/for/youtubers/` | 20.6% | 2.6% | **Highest same-type overlap.** Both Wave-1 SEO pages on the same template; share near-identical step-by-step text ("add a browser source", "wireless second camera", "AI background removal built in", "bitrate in real time"). Target queries differ ("church streaming software" vs "live stream on youtube") → moderate risk; keep the how-to steps phrased uniquely per page. |
| `/alternatives/obs/` | `/for/youtubers/` | 20.6% | 2.5% | Same as above — shared SEO-template step-by-step + feature blurbs. OBS page adds its own comparison/encoder content, so net unique content is high. Moderate-low risk. |
| `/multistreaming/` | `/` | 19.3% | 2.2% | Homepage's multistreaming section summarizes this feature page — shared bitrate math ("2.5 Mbps", "84 other platforms", "no cloud middleman"). By design; keep `/multistreaming/` canonical for multistreaming keywords. |
| `/virtual-camera/` | `/` | 18.4% | 1.4% | Homepage's virtual-camera section summarizes this feature page — shared copy ("virtual webcam in Zoom/Teams", "beauty effects / skin smoother", "16:9 and landscape"). By design; low risk. |
| `/products/` | `/` | 13.0% | 0.2% | Only one shared phrase ("no green screen needed"). Products hub is short (703 words) and almost entirely unique download-hub content. Negligible risk. |

## Content size (visible words, content area only)

| Page | Words |
|---|---:|
| `/alternatives/obs/` | 2049 |
| `/for/churches/` | 2032 |
| `/` | 1940 |
| `/multistreaming/` | 1701 |
| `/for/youtubers/` | 1545 |
| `/virtual-camera/` | 1379 |
| `/v2/` | 835 |
| `/products/` | 703 |

## Verdict — cannibalization risk

**Overall: healthy.** No two indexable pages are near-duplicates — peak thematic
similarity is 23% and peak literal-phrase overlap 3.9%. For static marketing
pages this is well within safe range.

Pairs worth watching:

1. **The three SEO pages with each other** — `/for/youtubers/`, `/for/churches/`,
   `/alternatives/obs/` cluster at ~20% cosine and ~2.5% phrase because they
   share the SEO template's step-by-step block almost verbatim. They target
   distinct queries, so this is the *only* genuine (moderate-low) cannibalization
   group. Recommendation: as new `/for/` and `/alternatives/` pages ship in
   Wave 2, rewrite the how-to steps per page rather than copy-pasting — otherwise
   the cluster's literal overlap grows. (Commit `7b0705d` already started this.)

2. **Homepage vs feature pages** (`/multistreaming/`, `/virtual-camera/`) — the
   homepage intentionally summarizes the feature pages. Not a risk as long as the
   feature page stays the canonical target for its keyword; the homepage should
   rank for brand/generic terms only.

3. **`/` ↔ `/v2/`** — the largest raw number (23.2% / 3.9%) but *not* a risk:
   `/v2/` is `noindex` and unlinked. It never reaches splitcam.com. If it ever
   were exposed, it would be a true near-duplicate of the homepage.

No action required before Wave 2; just keep SEO-page step text unique per page.
