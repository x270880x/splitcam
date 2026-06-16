# SplitCam — Czech (`cs`) localization review

First-pass AI verdict: **good** · 10 item(s) to confirm (1 high · 5 medium · 4 low)

You are a native **Czech** speaker. This is marketing copy for SplitCam (free live-streaming / virtual-camera software). For each item: write **KEEP** (original is fine), **APPLY** (use the suggestion), or your own wording.

Ignore anything about brand/tech terms in English (SplitCam, OBS, NVENC, QuickSync, AMF, RTMP(S), NDI, VST, Zoom, Teams, Meet, Discord, Twitch, YouTube, etc.) — those are intentional.


---


### 1. [high] page `/for/churches/`
**Issue:** Preposition vocalization error. Before a word beginning with 's' + consonant Czech requires 'se', not 's'. 's skromnými' is wrong; it must be 'se skromnými'.

**Original:** «macOS 11+ s skromnými hardwarovými požadavky»

**Suggested:** «macOS 11+ se skromnými hardwarovými požadavky»

**Decision:** ____________________


### 2. [medium] page `/for/youtubers/`
**Issue:** Grammatical gender error. 'šablona' is feminine, so the locative must agree as feminine: 'v připravené šabloně'. 'v připraveném šabloně' uses masculine/neuter agreement and is wrong.

**Original:** «RTMP adresa je zabudovaná v připraveném šabloně»

**Suggested:** «RTMP adresa je zabudovaná v připravené šabloně»

**Decision:** ____________________


### 3. [medium] page `/alternatives/obs/`
**Issue:** Mistranslation / broken sentence fragment. The source 'Owned by Logitech' (Streamlabs is owned by Logitech) became 'Vlastní Logitech', which reads as 'owns Logitech' or a dangling 'proprietary Logitech'. The meaning is reversed/unclear.

**Original:** «Vlastní Logitech.»

**Suggested:** «Patří společnosti Logitech.»

**Decision:** ____________________


### 4. [medium] page `/for/churches/`
**Issue:** Preposition vocalization error. Before 'studio' (s+t cluster) Czech requires 'ze', not 'z'. 'z studio.youtube.com' is unidiomatic; native phrasing also adds a noun.

**Original:** «vložte stream klíč z studio.youtube.com»

**Suggested:** «vložte stream klíč ze studio.youtube.com (resp. ze stránky studio.youtube.com)»

**Decision:** ____________________


### 5. [medium] page `/home / multistreaming / for/youtubers / for/churches / alternatives/obs/`
**Issue:** Inconsistent / wrong closing quotation mark. Czech uses the pair „ … " (low opening + high curly closing). Many places correctly do this (e.g. „Naživo"), but a large number of strings close with a straight ASCII quote instead — e.g. button labels „Živě", „Zahájit přenos", and the testimonials on the home page. This straight-quote closing recurs on lines such as 76–81, 272, 295, 330, 338, 340–342, 346, 348, 351, 358, 363, 380, 392, 393, 397, 412, 414, 416, 423. Standardize all closings to the Czech high curly quote.

**Original:** «bez žonglování mezi aplikacemi."»

**Suggested:** «bez žonglování mezi aplikacemi.“  (use the Czech closing quote „ … “ everywhere, e.g. „Živě“, „Zahájit přenos“)»

**Decision:** ____________________


### 6. [medium] page `/multistreaming/`
**Issue:** Awkward word order — calque of 'creator-generous monetization'. 'k tvůrcům štědrá monetizace Kicku' splits the adjective phrase unnaturally. Native order puts the modifier after the noun.

**Original:** «Algoritmy YouTube plus k tvůrcům štědrá monetizace Kicku — jedním vysíláním.»

**Suggested:** «Algoritmy YouTube plus monetizace Kicku štědrá k tvůrcům — jedním vysíláním.»

**Decision:** ____________________


### 7. [low] page `/for/youtubers / for/churches/`
**Issue:** Terminology inconsistency. Everywhere else the site uses the loanword 'stream', but in a few sentences the video stream is translated as 'Proud' (literally 'current/flow'), which sounds archaic/unidiomatic for live video — especially 'Proud cestuje' (the stream travels) and the sudden past tense 'Proud zamířil'. Recurs on lines 340, 343, 380, 393, 423.

**Original:** «Proud cestuje přímo z vašeho počítače, bez cloudového prostředníka»

**Suggested:** «Stream jde přímo z vašeho počítače, bez cloudového prostředníka»

**Decision:** ____________________


### 8. [low] page `/products/`
**Issue:** Anglicism inconsistent with the rest of the site. The phrase 'Jděte live' / 'jděte live' mixes English 'live' into otherwise fully Czech copy that elsewhere uses 'živě' / 'naživo' / 'jít živě'. Recurs on lines 459, 479, 486.

**Original:** «Jděte live vertikálně (Reels/Shorts) nebo horizontálně z telefonu»

**Suggested:** «Vysílejte živě na výšku (Reels/Shorts) nebo na šířku z telefonu»

**Decision:** ____________________


### 9. [low] page `/help/`
**Issue:** Wrong-direction closing quote. This line uses the English high-opening quote ” as the closing mark ('takto?”') instead of the Czech closing quote “. Mirrors the broader quote-consistency problem.

**Original:** «zeptejte se „má X fungovat takto?”»

**Suggested:** «zeptejte se „má X fungovat takto?“»

**Decision:** ____________________


### 10. [low] page `/products/`
**Issue:** Mild calque. 'sahání na klávesnici' (reaching onto the keyboard) is understandable but slightly awkward; a more natural collocation reads better.

**Original:** «Žádné nešikovné sahání na klávesnici.»

**Suggested:** «Žádné nešikovné tápání po klávesnici.»

**Decision:** ____________________
