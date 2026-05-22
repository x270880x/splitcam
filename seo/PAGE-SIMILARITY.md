# Page Similarity Report — duplicate / similar content audit

*Updated 2026-05-22 after the SEO-page uniqueness rewrite and the post-review
correctness fixes. Method below.*

## Method

- Visible text only — HTML stripped, `<script>/<style>/<svg>` dropped.
- Shared **`<nav>` / `<header>` / `<footer>`** excluded as boilerplate.
- Two metrics per pair:
  - **Cosine** — TF-IDF cosine over unigrams + bigrams = *thematic* similarity
    (do the pages target the same keywords / talk about the same things).
  - **Phrase** — 4-word shingle Jaccard = *literal* text duplication (verbatim
    sentences copied between pages).
- "Closest neighbour" is ranked by cosine.

## Summary table — closest neighbour per page (sorted by % similarity desc)

| Page | Closest neighbour | Cosine | Phrase | Comment |
|---|---|---:|---:|---|
| `/v2/` | `/` | 23.2% | 3.9% | `/v2/` is the archived Variant B of the homepage — shares hero + feature copy. **No SEO risk:** `/v2/` is `noindex` and unlinked. |
| `/` | `/v2/` | 23.2% | 3.9% | Same pair. Against indexable pages the homepage's real closest is `/for/youtubers/` (20.0%). |
| `/for/youtubers/` | `/` | 20.0% | 2.0% | SEO page shares feature vocabulary with the homepage. Different search intent (brand landing vs how-to query) → low cannibalization risk. |
| `/alternatives/obs/` | `/for/youtubers/` | 19.5% | 2.1% | Both discuss SplitCam-vs-OBS. Residual overlap is the OBS feature-comparison table + OBS FAQ that the YouTubers page also carries. Distinct target queries → low risk. See follow-up note below. |
| `/multistreaming/` | `/` | 19.3% | 2.2% | Homepage's multistreaming section summarizes this feature page. By design; keep `/multistreaming/` canonical for multistreaming keywords. |
| `/for/churches/` | `/for/youtubers/` | 18.7% | 1.8% | The two how-to guides. After the rewrite they share only generic product vocabulary — step text, examples and audience framing now differ (creator workflow vs volunteer AV team). Low risk. |
| `/virtual-camera/` | `/` | 18.4% | 1.4% | Homepage's virtual-camera section summarizes this feature page. By design; low risk. |
| `/products/` | `/` | 13.1% | 0.2% | Products hub is short and almost entirely unique download-hub content. Negligible risk. |

## SEO-page trio — before vs after the uniqueness rewrite

| Pair | Cosine before | Cosine after | Phrase before | Phrase after |
|---|---:|---:|---:|---:|
| `/for/youtubers/` ↔ `/for/churches/` | 20.6% | **18.7%** | 2.6% | **1.8%** |
| `/for/youtubers/` ↔ `/alternatives/obs/` | 20.6% | **19.5%** | 2.5% | **2.1%** |
| `/for/churches/` ↔ `/alternatives/obs/` | 14.0% | **13.9%** | 0.6% | **0.6%** |

What changed: the step-by-step blocks and repeated feature blurbs were rewritten
per audience — YouTuber creator workflow, church volunteer AV team, OBS-migration
comparison. Verbatim phrases that recurred across pages ("phone as a wireless
second camera", "add a Browser Source pointing at…", "status bar shows dropped
frames… bitrate in real time", "after that, going live is one click") were
reworded uniquely on each page.

A follow-up editorial review then corrected several factual / readability issues
(platform count, dropped "no time limit" detail, encoder overclaim, an awkward
phrase). Those fixes restored a little shared product vocabulary, nudging the
trio cosine up ~0.2–0.3 pp — negligible, and correctness takes priority over the
metric.

## Content size (visible words, content area only)

| Page | Words |
|---|---:|
| `/for/churches/` | 2058 |
| `/alternatives/obs/` | 2049 |
| `/` | 1940 |
| `/multistreaming/` | 1701 |
| `/for/youtubers/` | 1650 |
| `/virtual-camera/` | 1379 |
| `/v2/` | 835 |
| `/products/` | 703 |

## Verdict — cannibalization risk

**Healthy.** No two indexable pages are near-duplicates. Peak indexable cosine is
20.0% and peak literal-phrase overlap 2.2% — well within safe range.

The SEO-page trio is no longer the standout cluster: its thematic similarity sits
in the 14–20% band, the same band as the homepage-vs-feature-page pairs, and
literal-phrase overlap is at or near 2%.

### Follow-up (not blocking)

`/for/youtubers/` ↔ `/alternatives/obs/` stays at 19.5% because the YouTubers
page carries its own full "SplitCam vs OBS" feature-comparison table plus several
OBS-specific FAQ entries — content that structurally mirrors the dedicated
`/alternatives/obs/` page. If this pair needs to drop further, trim the YouTubers
comparison table to a short callout that links to `/alternatives/obs/` for the
full breakdown. Optional; current risk is low.

### Rule going forward

New `/for/` and `/alternatives/` pages must be written with unique body text —
no copy-pasting step blocks or feature blurbs between pages. Each page gets its
own examples, ordering and audience framing. Run the pre-commit content
check-list in `CLAUDE.md` before committing any copy changes.
