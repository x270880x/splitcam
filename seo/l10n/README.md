# `seo/l10n/` — localize one page into all 34 locales

Reusable replacement for the throwaway `scratchpad/va_*.py` scripts (virtual-audio
rollout, 2026-08-20) that were **not kept** and had to be rewritten for `/for/educators`.
Keep these — do not hand-translate a page or re-invent the extractor again.

## The four tools (all take file paths as args — no hardcoded scratch paths)

| Script | Job |
|---|---|
| `extract.py` | Pull translatable strings out of a page into a keyed dict, and inject them back. Guarantee: `inject(html, extract(html)) == html` byte-for-byte — run `--selftest` after any pattern change. `summary` is a leaf block (FAQ questions travel), and attribute/meta values are matched RAW so `&amp;` never breaks the match. |
| `keys.py` | Split the extracted strings into what a translator sees (head SEO block + everything between `<!-- BREADCRUMBS -->` and `<!-- FOOTER -->`) vs. the chrome, which is transplanted, never translated. |
| `build_locale.py` | Assemble a locale page: content+SEO from EN with translations injected; `<html>` tag, nav, mobile menu, footer, scripts transplanted from that locale's own donor page; breadcrumb trail from the donor with the last crumb swapped; JSON-LD **rebuilt from the finished localized DOM** so structured data can't drift from the visible text. |
| `hub_activate.py` | Turn the inert `<div class="hub-card soon">` for an audience into a live `<a>` link, reusing that locale's own "Open the guide →" wording. Card boundaries found by `<div>` nesting depth, not a lazy regex. |

Verifiers (independent of the translators' self-reports): `verify_tr.py` (JSON: keys, tag
multiset, hrefs, kept brand tokens, lengths) and `verify_page.py` (built page: JSON-LD
parses, FAQ=8, HowTo=5, chrome localized, redirect guard intact, self-referencing URLs).

## Pipeline

1. Get the EN page exactly right (it is the reference every locale agent reads).
2. `keys.py EN.html > src.json` → hand `src.json` + the brief to one agent per locale;
   each greps its own donor for established terminology and writes `<locale>.json`.
3. Per locale: `verify_tr.py` → `build_locale.py` → `verify_page.py` → `hub_activate.py`.
4. `python3 seo/i18n_wire.py` (hreflang / dropdown / sitemap) then
   `python3 seo/linkcheck.py --no-network` (must be 0 broken).

`build_locale.py`'s page path (`for/educators`) and the EN canonical URL are the only
page-specific constants — change those two for a different page.
