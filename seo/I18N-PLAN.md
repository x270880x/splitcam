# I18N plan — RU / ES localization of the main site

*Binding spec for every translated page. Written 2026-06-12. Keyword map: `I18N-KEYWORDS.md`.*

## Scope

- Locales: `ru`, `es`. URL scheme: `/ru/<same path>/`, `/es/<same path>/` mirroring the EN tree.
- **10 content pages:** `/` `products/` `virtual-camera/` `multistreaming/` `alternatives/`
  `alternatives/obs/` `for/` `for/youtubers/` `for/churches/` `help/`.
- **Utility pages (added 2026-06-13, user rule "translate everything"):**
  `privacy-policy/`, `license-agreement/` — translate FULLY.
  `changelog/` — localize the page shell only (nav, hero, platform intros,
  tab labels, `New/Improved/Fixed` section headers, footer, meta/title,
  hreflang, switcher). The ~1817 technical release `<li>` bullets stay EN:
  0 search volume (Ahrefs, all locales) + they change every release.
- **NOT translated:** `/v2/` (archived), `for/vtubers/` (noindex draft), `seo/`.
- **SEO rule (every new/edited page):** Ahrefs per locale → the language's
  real keyword goes in title + meta description + H1 (not a literal EN
  translation). Utility pages have ~0 volume → translate cleanly, no forcing.

## Per-file rules

1. `<html lang="ru">` / `<html lang="es">`.
2. **head:** translate `<title>`, `meta description/keywords`, OG + Twitter (title/description).
   Lead with the page's PRIMARY keyword from `I18N-KEYWORDS.md`.
   - `canonical` → `https://splitcam.com/ru/<path>/` (resp. `/es/`).
   - `og:url` → same localized URL. `og:locale` → `ru_RU` / `es_ES`. `og:image` — unchanged.
   - **hreflang block** (every translated page AND its EN original):
     ```html
     <link rel="alternate" hreflang="en" href="https://splitcam.com/<path>/">
     <link rel="alternate" hreflang="ru" href="https://splitcam.com/ru/<path>/">
     <link rel="alternate" hreflang="es" href="https://splitcam.com/es/<path>/">
     <link rel="alternate" hreflang="x-default" href="https://splitcam.com/<path>/">
     ```
     (for the homepage `<path>/` is just ``.)
3. **JSON-LD:** translate `name`, `description`, `alternateName`, FAQ `name`/`text`,
   HowTo steps, Breadcrumb item names. Breadcrumb/`url` fields → localized splitcam.com URLs.
   Keep `@type`s, `softwareVersion` etc. **NEVER add `aggregateRating`** (critical rule #7).
4. **GA gtag block** — keep byte-identical.
5. **Body:** translate every user-visible string: headings, copy, button labels, `alt`,
   `aria-label`, `title` attrs, badge texts, and **UI strings inside inline JS configs**
   (e.g. the download-menu `label`/`sub` fields). Never touch logic, selectors, URLs,
   class names, CSS (except nothing), or the structure.
6. Write the COMPLETE file — same structure end-to-end, closing `</html>` present.

## Path shifting (the #1 source of bugs — be exact)

Translated pages sit ONE level deeper than their EN originals.

- From `/ru/index.html` (EN original at `/index.html`):
  - `assets/x` → `../assets/x` · `favicon-32x32.png` → `../favicon-32x32.png`
  - internal page links `products/`, `virtual-camera/` etc. — KEEP AS IS
    (they resolve to `/ru/products/` — the localized sibling, which is what we want)
  - links to UNTRANSLATED pages: `changelog/` → `../changelog/`,
    `privacy-policy/` → `../privacy-policy/`, `license-agreement/` → `../license-agreement/`
- From `/ru/<section>/index.html` (EN original at `/<section>/index.html`):
  - same-dir assets `assets/x` → `../../<section>/assets/x` (assets are NOT copied — reuse EN ones)
  - `../assets/x` → `../../assets/x` · favicons `../favicon…` → `../../favicon…`
  - sibling page links `../products/`, `../for/youtubers/` etc. — KEEP AS IS (→ localized siblings)
  - untranslated: `../changelog/` → `../../changelog/` (same for the two legal pages)
  - `href="../"` (logo/home) — KEEP (→ `/ru/`)
- External `http(s)://`, `#anchors`, `mailto:` — unchanged.

## Language switcher (every translated page; EN pages get it in a separate pass)

Markup — insert in `<div class="nav-right">` BEFORE the download split-button,
AND at the bottom of `#nav-mobile` (burger):

```html
<div class="lang-sw" aria-label="Language">
  <a href="<abs-or-rel EN url>" hreflang="en" lang="en">EN</a>
  <span class="on" lang="ru">RU</span>
  <a href="<rel ES url>" hreflang="es" lang="es">ES</a>
</div>
```
(on the ES page `ES` is the `<span class="on">`, links point to EN + RU equivalents;
use relative URLs: e.g. from `/ru/products/` → EN `../../products/`, ES `../../es/products/`.)

CSS — add once to the page `<style>` (same on every page):
```css
.lang-sw{display:inline-flex;align-items:center;gap:2px;padding:3px;border:1px solid var(--app-border);border-radius:8px;background:rgba(255,255,255,.02)}
.lang-sw a,.lang-sw .on{font-size:10.5px;font-weight:700;letter-spacing:.4px;padding:3px 7px;border-radius:6px;color:var(--text-sub);text-decoration:none}
.lang-sw a:hover{color:var(--text);background:rgba(255,255,255,.05)}
.lang-sw .on{color:#fff;background:var(--blue)}
@media (max-width:900px){.nav-right .lang-sw{display:none}}
#nav-mobile .lang-sw{margin:10px 16px 4px}
```

## Tone & glossary

**RU** — обращение на «вы» (строчная), живой язык стрим-сцены, без канцелярита и калек.
- стрим, стримить, мультистрим, рестрим, прямой эфир / трансляция (для церквей — «трансляция богослужения», «трансляция службы»)
- сцена, источник, оверлей, нижняя треть («lower thirds» → «титры/нижняя треть»), битрейт, чат, донаты, зрители
- virtual camera → «виртуальная камера»; webcam → «веб-камера»; Go Live → «В эфир»
- free → «бесплатно/бесплатная» (не «свободная»); seamlessly → «без пауз и склеек»
- Coming soon → «Скоро»; Download → «Скачать»; in development → «в разработке»

**ES** — tú, нейтральный международный испанский (понятен и в Испании, и в LatAm).
- hacer un directo (ES) / transmitir en vivo (LatAm) — use BOTH naturally
- multistream (как есть!), streaming, overlay, escena, fuente, bitrate, chat en vivo, espectadores
- video (без тильды — нейтрально), PC / equipo (не «ordenador»), gratis / gratuito
- NO vosotros forms; Go Live → «Salir en vivo»; Download → «Descargar»; Coming soon → «Próximamente»

## Invariants (identical across ALL languages — check before writing)

- Version **v10.9.2** everywhere it appears; Mac app v1.19 where it appears.
- Rating chip: RU «4,7 · 357 отзывов», ES «4,7 · 357 reseñas» (digits unchanged).
- **84+ platforms** → «84+ платформ» / «84+ plataformas».
- Platforms list: Windows · macOS · iOS · Android (untranslated names).
- SplitCam Remote: **iOS — live in the App Store; Android — Coming soon/Скоро/Próximamente.**
  Pairing = QR-код **или** авто-обнаружение в Wi-Fi (NEVER say "no QR").
- Peer-to-peer: «напрямую с вашего компьютера, без облачного посредника» /
  «directo desde tu equipo, sin intermediarios en la nube». No "Restream server" wording.
- Skype is dead — must not appear as a live product (it doesn't in EN; don't introduce it).
- Brand names, app names, feature names from the changelog (Vertical Canvas, Luma Wipe…) stay EN.

## QA after writing

- `python3 seo/linkcheck.py --no-network` MUST report 0 broken internal links/resources.
- Mobile ≤900px and desktop 1440px spot-check on at least `/ru/` and `/es/multistreaming/`.
- grep the new tree for `v10.9.2`, `84+`, `aggregateRating` (must be absent), `lang="`.
- `sitemap.xml` gets all 20 new URLs in the same commit.
