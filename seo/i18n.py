#!/usr/bin/env python3
"""Central i18n config + render helpers for the splitcam site (no build step).

This is the single source of truth for the language system that the wave rollout
and the wiring script (`i18n_wire.py`, added with Wave 1) consume. It mirrors the
proven camstreamguide.com setup (dropdown + browser-language auto-redirect) but is
ordered by the Ahrefs "splitcam" demand we measured 2026-06-13 so the most-searched
languages ship first and sit at the top of the dropdown.

Nothing here touches pages on its own — import and call the render_* helpers.
"""

# Order = Ahrefs "splitcam" search demand (2026-06-13), highest first.
# EN is the root/default. RU+ES already shipped. The rest roll out 5 per wave.
LANG_ORDER = [
    "en",                                  # root / x-default
    "fil", "fr", "pt", "de", "tr",         # Wave 1  (488/434/341/329/315)
    "uk", "ru", "it", "vi", "id",          # Wave 2  (272/196*/151/150/103)   *ru done
    "nl", "es", "ro", "hi", "ja",          # Wave 3  (99/89*/82/60/60)         *es done
    "ms", "bg", "ar", "ko", "th",          # Wave 4  (37/22/10/10/10)
    "pl", "hu", "sv", "zh", "el",          # Wave 5  (10/10/10/0/0)
    "cs", "he", "sr", "hr", "da",          # Wave 6  (0…)
    "fi", "no", "sk", "fa",                # Wave 7  (0…)  fa = no Ahrefs data
]

# Already live (skip in waves). Update as waves land.
LANG_DONE = {"en","ru","es","fil","fr","pt","de","tr","uk","it","vi","id","nl","ro","hi","ja","ms","bg",
             "ar","ko","th","pl","hu","sv","zh","el","cs","he",
             "sr"}  # Wave 6 in progress 2026-06-14

RTL_LANGS = {"ar", "he", "fa"}


def is_rtl(locale):
    """True for right-to-left locales (Arabic, Hebrew, Persian)."""
    return locale in RTL_LANGS


# URL path prefix per locale. EN at root ("").
LANG_PATH = {L: ("" if L == "en" else f"{L}/") for L in LANG_ORDER}

# Native language name (shown in the dropdown menu rows).
LANG_NATIVE = {
    "en": "English", "ru": "Русский", "es": "Español", "de": "Deutsch",
    "fr": "Français", "it": "Italiano", "pt": "Português", "nl": "Nederlands",
    "ro": "Română", "bg": "Български", "hu": "Magyar", "el": "Ελληνικά",
    "fi": "Suomi", "da": "Dansk", "no": "Norsk", "sr": "Српски", "hr": "Hrvatski",
    "zh": "中文", "ja": "日本語", "ar": "العربية", "th": "ไทย", "fil": "Filipino",
    "tr": "Türkçe", "id": "Bahasa Indonesia", "vi": "Tiếng Việt", "pl": "Polski",
    "ko": "한국어", "uk": "Українська", "cs": "Čeština", "sk": "Slovenčina",
    "sv": "Svenska", "ms": "Bahasa Melayu", "he": "עברית", "fa": "فارسی", "hi": "हिन्दी",
}

# Short code shown on the closed dropdown button.
LANG_LABEL = {
    "en": "EN", "ru": "RU", "es": "ES", "de": "DE", "fr": "FR", "it": "IT",
    "pt": "PT", "nl": "NL", "ro": "RO", "bg": "BG", "hu": "HU", "el": "EL",
    "fi": "FI", "da": "DA", "no": "NO", "sr": "SR", "hr": "HR", "zh": "中",
    "ja": "日", "ar": "ع", "th": "ไทย", "fil": "FIL", "tr": "TR", "id": "ID",
    "vi": "VI", "pl": "PL", "ko": "KO", "uk": "UK", "cs": "CS", "sk": "SK",
    "sv": "SV", "ms": "MS", "he": "עב", "fa": "فا", "hi": "हि",
}

LANG_FLAG = {
    "en": "🇬🇧", "ru": "🇷🇺", "es": "🇪🇸", "de": "🇩🇪", "fr": "🇫🇷", "it": "🇮🇹",
    "pt": "🇧🇷", "nl": "🇳🇱", "ro": "🇷🇴", "bg": "🇧🇬", "hu": "🇭🇺", "el": "🇬🇷",
    "fi": "🇫🇮", "da": "🇩🇰", "no": "🇳🇴", "sr": "🇷🇸", "hr": "🇭🇷", "zh": "🇨🇳",
    "ja": "🇯🇵", "ar": "🇸🇦", "th": "🇹🇭", "fil": "🇵🇭", "tr": "🇹🇷", "id": "🇮🇩",
    "vi": "🇻🇳", "pl": "🇵🇱", "ko": "🇰🇷", "uk": "🇺🇦", "cs": "🇨🇿", "sk": "🇸🇰",
    "sv": "🇸🇪", "ms": "🇲🇾", "he": "🇮🇱", "fa": "🇮🇷", "hi": "🇮🇳",
}

# Ahrefs "splitcam" brand volume / month by market (2026-06-13). For prioritising.
DEMAND = {
    "fil": 488, "fr": 434, "pt": 341, "de": 329, "tr": 315, "uk": 272, "ru": 196,
    "it": 151, "vi": 150, "id": 103, "nl": 99, "es": 89, "ro": 82, "hi": 60,
    "ja": 60, "ms": 37, "bg": 22, "ar": 10, "ko": 10, "th": 10, "pl": 10,
    "hu": 10, "sv": 10, "zh": 0, "el": 0, "cs": 0, "he": 0, "sr": 0, "hr": 0,
    "da": 0, "fi": 0, "no": 0, "sk": 0, "fa": None,
}

SITE = "https://splitcam.com"


def waves():
    """Yield (n, [langs]) waves of 5 new (not-yet-done) languages, demand-ordered."""
    todo = [L for L in LANG_ORDER if L not in LANG_DONE]
    for i in range(0, len(todo), 5):
        yield i // 5 + 1, todo[i:i + 5]


def hreflang_block(page_path, available):
    """page_path: '' for home, 'products/' etc. available: set of live locales."""
    rows = []
    for L in LANG_ORDER:
        if L not in available:
            continue
        href = f"{SITE}/{LANG_PATH[L]}{page_path}"
        rows.append(f'<link rel="alternate" hreflang="{L}" href="{href}">')
    rows.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/{page_path}">')
    return "\n".join(rows)


def dropdown(cur, available, page_path, depth):
    """Render the <details> language dropdown.
    depth: relative prefix back to site root from the page, e.g. '' (home),
    '../' (depth-2), '../../' (depth-3). Links target the localized sibling.
    """
    items = []
    for L in LANG_ORDER:
        if L not in available:
            continue
        href = f"{depth}{LANG_PATH[L]}{page_path}" or "./"
        cls = ' class="cur"' if L == cur else ""
        items.append(
            f'<a href="{href}" data-lang="{L}" hreflang="{L}" lang="{L}"{cls}>'
            f'<span class="lf">{LANG_FLAG[L]}</span>'
            f'<span class="ln">{LANG_NATIVE[L]}</span></a>'
        )
    return (
        '<details class="lang-dl"><summary aria-label="Language">'
        f'<span class="lf">{LANG_FLAG[cur]}</span>'
        f'<span class="lc">{LANG_LABEL[cur]}</span>'
        '<span class="dl-caret">▾</span></summary>'
        f'<div class="lang-dl-menu">{"".join(items)}</div></details>'
    )


# Browser-language auto-redirect (honours a saved click, else navigator.languages).
# __LANG_LIST__ is replaced with the JSON array of live locales by the wiring step.
AUTO_DETECT_JS = """<script>
(function(){try{
var L=__LANG_LIST__;
var cur=document.documentElement.lang;
var path=location.pathname;if(path.charAt(0)==="/")path=path.substring(1);
var parts=path.split("/");if(L.indexOf(parts[0])>=0)parts.shift();
var slug=parts.join("/");
function go(lang){var p=lang==="en"?"/"+slug:"/"+lang+"/"+slug;if(p!==location.pathname){document.documentElement.style.visibility="hidden";location.replace(p+location.search+location.hash);}}
var stored;try{stored=localStorage.getItem("preferred_lang");}catch(e){}
if(stored&&L.indexOf(stored)>=0){if(stored!==cur)go(stored);}
else{var bl=navigator.languages||(navigator.language?[navigator.language]:[]);for(var i=0;i<bl.length;i++){var c=bl[i].toLowerCase().split("-")[0];if(c==="nb"||c==="nn")c="no";if(c==="tl")c="fil";if(L.indexOf(c)>=0){if(c!==cur)go(c);break;}}}
if(document.addEventListener){document.addEventListener("click",function(e){var t=e.target;while(t&&t!==document){if(t.tagName==="A"&&t.getAttribute&&t.getAttribute("data-lang")){try{localStorage.setItem("preferred_lang",t.getAttribute("data-lang"));}catch(e){}break;}t=t.parentNode;}},true);}
}catch(e){}})();
</script>"""

# Dropdown CSS (one copy per page <style>). Dark theme, matches the site tokens.
DROPDOWN_CSS = """.lang-dl{position:relative;display:inline-block}
.lang-dl>summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:6px;padding:6px 9px;border:1px solid var(--app-border);border-radius:8px;background:rgba(255,255,255,.02);font-size:11.5px;font-weight:700;color:var(--text-sub);user-select:none}
.lang-dl>summary::-webkit-details-marker{display:none}
.lang-dl>summary:hover{color:var(--text);background:rgba(255,255,255,.05)}
.lang-dl .lf{font-size:13px;line-height:1}.lang-dl .lc{letter-spacing:.4px}
.lang-dl .dl-caret{font-size:9px;opacity:.7}
.lang-dl-menu{position:absolute;top:calc(100% + 6px);right:0;z-index:60;min-width:180px;max-height:60vh;overflow-y:auto;padding:6px;background:var(--app-panel);border:1px solid var(--app-border2);border-radius:10px;box-shadow:0 12px 32px -8px rgba(0,0,0,.6);display:grid;gap:1px}
.lang-dl-menu a{display:flex;align-items:center;gap:9px;padding:7px 10px;border-radius:7px;font-size:13px;font-weight:500;color:var(--text-sub);text-decoration:none;white-space:nowrap}
.lang-dl-menu a:hover{background:rgba(255,255,255,.05);color:var(--text)}
.lang-dl-menu a.cur{color:#fff;background:var(--blue)}
.lang-dl-menu .lf{font-size:15px}
@media(max-width:1100px){.nav-right .lang-dl{display:none}}
#nav-mobile .lang-dl{display:block;margin:10px 16px 4px}
#nav-mobile .lang-dl-menu{position:static;max-height:none;box-shadow:none;margin-top:6px}"""


# RTL layout fixes — injected into RTL-locale pages by i18n_wire.py (rules only bite
# under dir="rtl", so they're inert for LTR). Two real bugs the dir flip alone leaves:
#  1. horizontal "forward" arrows (the #i-arr glyph in CTAs / "video -> platforms")
#     still point right; mirror them.
#  2. the download split-button's corner rounding doesn't swap, so the main button +
#     dropdown toggle stop reading as one joined control. Re-mirror the radii.
RTL_CSS = """[dir="rtl"] svg:has(use[href="#i-arr"]){transform:scaleX(-1)}
[dir="rtl"] .dl>[data-dl-primary]{border-radius:0 8px 8px 0}
[dir="rtl"] .dl>.dl-toggle{border-radius:8px 0 0 8px}
[dir="rtl"] .vc-arrow{transform:scaleX(-1)}"""


if __name__ == "__main__":
    print(f"{len(LANG_ORDER)} locales; done={sorted(LANG_DONE)}")
    for n, w in waves():
        print(f"  Wave {n}: {w}  (demand {[DEMAND.get(l) for l in w]})")
