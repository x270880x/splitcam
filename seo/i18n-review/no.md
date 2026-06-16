# SplitCam — Norwegian (`no`) localization review

First-pass AI verdict: **good** · 22 item(s) to confirm (0 high · 15 medium · 7 low)

You are a native **Norwegian** speaker. This is marketing copy for SplitCam (free live-streaming / virtual-camera software). For each item: write **KEEP** (original is fine), **APPLY** (use the suggestion), or your own wording.

Ignore anything about brand/tech terms in English (SplitCam, OBS, NVENC, QuickSync, AMF, RTMP(S), NDI, VST, Zoom, Teams, Meet, Discord, Twitch, YouTube, etc.) — those are intentional.


---


### 1. [medium] page `/home/`
**Issue:** English plural 'reprises' left untranslated. Norwegian plural of 'reprise' is 'repriser'. As written it is an English word in a Norwegian sentence.

**Original:** «Umiddelbare slow-mo-reprises under spilling»

**Suggested:** «Umiddelbare slow-mo-repriser under spilling»

**Decision:** ____________________


### 2. [medium] page `/home/`
**Issue:** 'lag lag' collides two homonyms (imperative 'lag' = make + noun 'lag' = layer), which reads as an accidental word-doubling and is confusing. Natives would rephrase.

**Original:** «Dra, endre størrelse og lag lag i scenen din.»

**Suggested:** «Dra, endre størrelse og stable lagene i scenen din.»

**Decision:** ____________________


### 3. [medium] page `/home/`
**Issue:** 'inni SplitCam' is colloquial/spoken register; for 'works inside SplitCam' a native marketing text uses 'i SplitCam' or 'inne i SplitCam'.

**Original:** «kompresjon fungerer inni SplitCam»

**Suggested:** «kompresjon fungerer i SplitCam»

**Decision:** ____________________


### 4. [medium] page `/home/`
**Issue:** 'Ubegrenset med X' (and 'Bygg ubegrenset med scener') is a colloquial construction unsuited to marketing copy. Standard written Norwegian is 'ubegrenset antall X' / 'ubegrensede X'. Occurs several times (home li 'Ubegrenset med scener', 'Ubegrenset med lydkilder', p 'Bygg ubegrenset med scener').

**Original:** «Bygg ubegrenset med scener og bytt mellom dem»

**Suggested:** «Bygg et ubegrenset antall scener og bytt mellom dem»

**Decision:** ____________________


### 5. [medium] page `/multistreaming/`
**Issue:** Broken syntax: 'de 17 Mbps opplastingen din' mixes a quantity and a definite noun ungrammatically. Should be 'om opplastingen din på 17 Mbps klarer det'.

**Original:** «Den forteller deg om de 17 Mbps opplastingen din klarer det»

**Suggested:** «Den forteller deg om opplastingen din på 17 Mbps klarer det»

**Decision:** ____________________


### 6. [medium] page `/multistreaming/`
**Issue:** 'frafall' / 'den frafalne plattformen' is the wrong domain word — in Norwegian 'frafall/frafalne' means students dropping out or rural depopulation, not a dropped stream/connection. The page itself uses the correct idiom 'faller ut' elsewhere (li 'Hvis én destinasjon faller ut'), so this is also internally inconsistent. Use 'brudd' / 'plattformen som falt ut'.

**Original:** «og varsler før det blir frafall»

**Suggested:** «og varsler før det oppstår brudd»

**Decision:** ____________________


### 7. [medium] page `/multistreaming/`
**Issue:** Continuation of the 'frafall' problem: 'den frafalne plattformen' (also appears in the FAQ on this page). Native phrasing is 'plattformen som falt ut'.

**Original:** «SplitCam kobler seg automatisk til den frafalne plattformen igjen»

**Suggested:** «SplitCam kobler seg automatisk til plattformen som falt ut igjen»

**Decision:** ____________________


### 8. [medium] page `/alternatives/obs/`
**Issue:** The action button is called 'Go Live' (English) here and on the switch-steps section, but everywhere else on the site it is the Norwegian 'Gå live' (home, for/youtubers, etc.). This is an inconsistent UI-label translation that will confuse users about what the in-app button actually says.

**Original:** «Huk av boksene, lim inn nøklene, klikk Go Live.»

**Suggested:** «Huk av boksene, lim inn nøklene, klikk Gå live.»

**Decision:** ____________________


### 9. [medium] page `/alternatives/obs/`
**Issue:** 'Stream Settings' is left in English here (and glossed only on the churches page), while the youtubers page localizes the same menu as 'Strømmeinnstillinger'. Inconsistent UI naming.

**Original:** «I SplitCam åpner du Stream Settings.»

**Suggested:** «I SplitCam åpner du Strømmeinnstillingene.»

**Decision:** ____________________


### 10. [medium] page `/virtual-camera/`
**Issue:** 'nedre tredjedeler' is a literal calque of 'lower thirds'. Norwegian video production calls these 'navneplater' / 'bunntekster' (the for/youtubers and for/churches pages even use 'navneskilt'/'tekstplakat'). Calque + inconsistent terminology. Appears twice on this page.

**Original:** «Legg til nedre tredjedeler med navn og tittel.»

**Suggested:** «Legg til navneplater med navn og tittel.»

**Decision:** ____________________


### 11. [medium] page `/virtual-camera/`
**Issue:** 'leppe-touch-up' mixes Norwegian and English inside a single compound and reads as half-translated. Use a Norwegian term.

**Original:** «hårfarge, leppe-touch-up, øyeforstørring»

**Suggested:** «hårfarge, lepperetusj, øyeforstørring»

**Decision:** ____________________


### 12. [medium] page `/virtual-camera/`
**Issue:** Inconsistent rendering of 'green screen' across the site: 'grønn skjerm' (home), 'grønnskjerm' (this page, several times) and 'green screen' (alternatives/obs). Pick one form site-wide; 'grønnskjerm' (one word) or the loanword 'green screen' are both natural, but the mix is jarring.

**Original:** «Bytt ut den rotete bakgrunnen din med AI-registrert uskarphet eller et eget bilde — uten grønnskjerm.»

**Suggested:** «Standardize on one form, e.g. '…uten grønn skjerm.' to match the home page (or change the home page to 'grønnskjerm').»

**Decision:** ____________________


### 13. [medium] page `/products/`
**Issue:** 'node-til-node' is used for peer-to-peer here, but every other page uses 'peer-to-peer' (which the brief lists as the accepted term). Inconsistent and unusual; a Norwegian reader will not immediately equate the two.

**Original:** «Multistream til 84+ plattformer node-til-node»

**Suggested:** «Multistream til 84+ plattformer peer-to-peer»

**Decision:** ____________________


### 14. [medium] page `/for/youtubers/`
**Issue:** YouTube's 'Unlisted' privacy setting is translated two different ways: 'Ulistet' here and 'Uoppført' on the churches page. YouTube's official Norwegian UI uses 'Uoppført'; 'Ulistet' is a non-standard calque. Use 'Uoppført' for consistency and to match the real product.

**Original:** «setter du personvernet på den første strømmen til Ulistet»

**Suggested:** «setter du personvernet på den første strømmen til Uoppført»

**Decision:** ____________________


### 15. [medium] page `/for/youtubers/`
**Issue:** The encoder concept is rendered three different ways across the site: English 'encoder' (this page, 5x), Norwegianized 'enkoder' (churches page: 'enkoderens', 'strøm-enkoder', 'Enkoderen'), and 'koder'/'koding' (obs page). Pick one. Native usage favors 'koder' or 'enkoder'; mixing the raw English 'encoder' with 'enkoder' on a Norwegian site is inconsistent.

**Original:** «SplitCam finner maskinvare-encoderen din automatisk ved oppstart»

**Suggested:** «SplitCam finner maskinvarekoderen din automatisk ved oppstart (and align the churches page to the same word)»

**Decision:** ____________________


### 16. [low] page `/multistreaming/`
**Issue:** 'fra én enkelt koding' reads awkwardly — 'koding' as a count noun for a single encode pass is unidiomatic. Natives would say 'fra én enkoding' or rephrase to 'koder videoen din én gang'.

**Original:** «Stream til flere plattformer fra én enkelt koding»

**Suggested:** «Stream til flere plattformer med én enkelt enkoding»

**Decision:** ____________________


### 17. [low] page `/home/`
**Issue:** Dangling past participle 'sendt' — 'fra én enkelt koding, sendt peer-to-peer' should be a finite verb agreeing with the stream being sent.

**Original:** «sendt peer-to-peer til Twitch, YouTube, Facebook, Kick og 84+ andre samtidig»

**Suggested:** «som sendes peer-to-peer til Twitch, YouTube, Facebook, Kick og 84+ andre samtidig»

**Decision:** ____________________


### 18. [low] page `/home/`
**Issue:** 'knirkefri ytelse' is an unusual collocation ('knirkefri' = squeak-free, used for hinges/floors, not performance). Native choice for smooth performance under load is 'sømløs ytelse' or 'jevn ytelse'.

**Original:** «knirkefri ytelse under tung belastning»

**Suggested:** «sømløs ytelse under tung belastning»

**Decision:** ____________________


### 19. [low] page `/alternatives/obs/`
**Issue:** 'gratis som i gratis øl, ikke gratis som i fri ytring' is a literal calque of the English 'free as in beer, not free as in speech'. The pun does not carry in Norwegian, and the FOSS distinction natives use is 'gratis' vs 'fri programvare' (not 'fri ytring'). Better to state it plainly.

**Original:** «SplitCam er gratis som i gratis øl, ikke gratis som i fri ytring.»

**Suggested:** «SplitCam er gratis programvare, men ikke fri/åpen programvare.»

**Decision:** ____________________


### 20. [low] page `/multistreaming/`
**Issue:** Compound spelled two ways across the site: 'strøminnstillinger' (multistreaming, obs, churches) vs 'strømmeinnstillinger' (for/youtubers). Choose one form site-wide.

**Original:** «Still inn hver enkelt i strøminnstillingene.»

**Suggested:** «Pick one spelling, e.g. 'strømmeinnstillingene', and use it everywhere.»

**Decision:** ____________________


### 21. [low] page `/products/`
**Issue:** Imperative verb 'stream' (English) is used as a heading here, while the multistreaming page uses the Norwegian imperative 'Strøm' for the same idea. Minor verb-form inconsistency.

**Original:** «Stream fra hvilken som helst enhet»

**Suggested:** «Strøm fra hvilken som helst enhet»

**Decision:** ____________________


### 22. [low] page `/products/`
**Issue:** 'Alt gratis, hele tiden' calques 'all free, all the time'; 'hele tiden' means 'constantly/the whole time' and reads oddly for 'forever/always'. Natural choice is 'alltid'.

**Original:** «Alt gratis, hele tiden.»

**Suggested:** «Alt gratis, alltid.»

**Decision:** ____________________
