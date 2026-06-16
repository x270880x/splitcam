# SplitCam — Finnish (`fi`) localization review

First-pass AI verdict: **good** · 33 item(s) to confirm (2 high · 20 medium · 11 low)

You are a native **Finnish** speaker. This is marketing copy for SplitCam (free live-streaming / virtual-camera software). For each item: write **KEEP** (original is fine), **APPLY** (use the suggestion), or your own wording.

Ignore anything about brand/tech terms in English (SplitCam, OBS, NVENC, QuickSync, AMF, RTMP(S), NDI, VST, Zoom, Teams, Meet, Discord, Twitch, YouTube, etc.) — those are intentional.


---


### 1. [high] page `/alternatives/obs/`
**Issue:** Vowel-harmony grammar errors on the OBS page: 'SplitCam' contains a back vowel (a), so all case endings must be back-vowel (-ssa, -lla, -a), never front (-ssä, -llä, -ä). The whole rest of the site correctly writes SplitCamissa / SplitCamilla / SplitCamia; only this page slips into the incorrect front forms. A native would immediately read these as wrong.

**Original:** «SplitCamissä on OBS Project Import»

**Suggested:** «SplitCamissa on OBS Project Import. Same fix for every front-vowel instance on this page: 'SplitCamillä pääset lähetykseen' → 'SplitCamilla pääset lähetykseen' (L289), 'Avaa SplitCamissä Stream Settings' → 'Avaa SplitCamissa Stream Settings' (L295), 'SplitCamillä on pienempi lisäosaekosysteemi' → 'SplitCamilla on pienempi…' (L313), '…lainkaan SplitCamissä' → '…lainkaan SplitCamissa' (L313), 'Kokeile SplitCamiä' → 'Kokeile SplitCamia' (L318).»

**Decision:** ____________________


### 2. [high] page `/alternatives/obs/`
**Issue:** Core feature term is translated two different ways across the site. The home, multistreaming, virtual-camera, for/youtubers and for/churches pages call an OBS scene 'näkymä', but the alternatives/obs and products pages call it 'kohtaus'. Both are valid Finnish, but mixing them for the product's central concept reads as two translators who never compared notes. Pick ONE and apply it everywhere (for OBS scenes 'kohtaus' is the more literal match, but 'näkymä' dominates the site, so standardising on 'näkymä' is the smaller edit).

**Original:** «Tuo OBS-kohtauskokoelmasi yhdellä klikkauksella»

**Suggested:** «If standardising on 'näkymä': 'Tuo OBS-näkymäkokoelmasi yhdellä klikkauksella'. Apply consistently to 'kohtaus/kohtaukset/kohtauskokoelma/kohtaus- ja lähdemalli' on the OBS and products pages (e.g. L249, L254, L282, L443, L455, L476).»

**Decision:** ____________________


### 3. [medium] page `/for/youtubers/`
**Issue:** Redundant phrasing: 'lähetät suoraa lähetystä' repeats the same stem (broadcast a broadcast) and reads clumsy.

**Original:** «Näin lähetät suoraa lähetystä YouTubessa»

**Suggested:** «Näin teet suoran lähetyksen YouTubeen (or: Näin striimaat YouTubessa).»

**Decision:** ____________________


### 4. [medium] page `/for/youtubers/`
**Issue:** Grammatically broken sentence: 'Tarvitset [accusative] … eikä [no…]' does not agree. As written it reads 'You need a verified account and no streaming restrictions', but the two halves are stitched together ungrammatically.

**Original:** «Tarvitset vahvistetun YouTube-tilin (puhelinvahvistus) eikä suoratoistorajoituksia viimeisen 90 päivän aikana.»

**Suggested:** «Tarvitset vahvistetun YouTube-tilin (puhelinvahvistus), eikä tililläsi saa olla suoratoistorajoituksia viimeisen 90 päivän ajalta.»

**Decision:** ____________________


### 5. [medium] page `/home/`
**Issue:** Calque of 'every source you'll ever need'. In affirmative Finnish 'joita ikinä tarvitset' is a loose anglicism; native marketing copy tightens it.

**Original:** «Kaikki lähteet, joita ikinä tarvitset lähetykseen»

**Suggested:** «Kaikki lähetykseen tarvitsemasi lähteet (also at L48: 'Kaikki lähteet, joita ikinä tarvitset' → 'Kaikki tarvitsemasi lähteet').»

**Decision:** ____________________


### 6. [medium] page `/home/`
**Issue:** Calque of 'built right in'. The adjective 'sisäänrakennettu' is used correctly elsewhere, but as a verb phrase 'rakennettu valmiiksi sisään' is unidiomatic.

**Original:** «Ja loputkin on rakennettu valmiiksi sisään.»

**Suggested:** «Ja kaikki muukin on valmiina / Ja loputkin ovat valmiina sisäänrakennettuina.»

**Decision:** ____________________


### 7. [medium] page `/for/youtubers/`
**Issue:** 'web-kamera' (loan) appears on the YouTubers page (L327, L334, L366) while the entire rest of the site uses the native 'verkkokamera'. Inconsistent within one product.

**Original:** «web-kamera puhuvan pään kuvaa varten»

**Suggested:** «verkkokamera puhuvan pään kuvaa varten (replace all 'web-kamera' with 'verkkokamera').»

**Decision:** ____________________


### 8. [medium] page `/for/youtubers/`
**Issue:** Source/feature names are translated on the home page (Pelinkaappaus, Selainlähde, näytön kaappaus) but left in English here (Game Capture, Screen Capture, Browser Source). Either keep all English (if they match the app UI) or translate consistently; mixing within the marketing copy is jarring.

**Original:** «Game Capture DirectX/OpenGL-peleihin, Screen Capture opastusvideoihin ja reaktioihin, Browser Source»

**Suggested:** «Pick one convention site-wide, e.g. 'Game Capture (pelinkaappaus) DirectX/OpenGL-peleihin, Screen Capture (näytönkaappaus) …, Browser Source (selainlähde)…' or fully translate to match L18–L19.»

**Decision:** ____________________


### 9. [medium] page `/alternatives/obs/`
**Issue:** Inconsistent term for 'overlay'. This page uses the English 'overlay/overlayt/overlayllä' (L260, L276, L300, L301), while the home and virtual-camera pages use the Finnish 'päällyste' (L188, L213, L241). Standardise.

**Original:** «Toistopuskurin overlay»

**Suggested:** «Toistopuskurin päällyste (or keep English everywhere). Note L334 adds yet a third variant 'päällyksiin' — unify to 'päällyste'.»

**Decision:** ____________________


### 10. [medium] page `/for/youtubers/`
**Issue:** Three different terms for 'stream key' across the site: 'lähetysavain' (home/multistreaming/obs), 'suoratoiston avain' and 'suoratoistoavain' (youtubers/churches). A native editor would pick one.

**Original:** «suoratoiston avain»

**Suggested:** «Standardise on one term, e.g. 'suoratoistoavain', everywhere (cf. 'lähetysavain' at L14, L132, L295; 'suoratoistoavaimet' at L380).»

**Decision:** ____________________


### 11. [medium] page `/home/`
**Issue:** Three coinages for the 'cloud middleman/relay': 'pilvivälikäsi' (home/multistreaming, awkward), 'pilvivälittäjä' (churches, natural) and 'pilvivälitys' (products). Unify; 'pilvivälittäjä' reads most naturally.

**Original:** «Ei pilvivälikättä»

**Suggested:** «Ei pilvivälittäjää (apply consistently; replace 'pilvivälikäsi/pilvivälikättä' at L9, L136, L153, L168, L172).»

**Decision:** ____________________


### 12. [medium] page `/for/youtubers/`
**Issue:** Technical inaccuracy a streaming-savvy reader would catch: sending the stream directly from your PC to each platform's ingest is NOT 'vertaisverkko' (peer-to-peer). P2P means traffic between end-user peers; this is direct client-to-server. The home/multistreaming pages correctly say just 'suoraan koneeltasi'.

**Original:** «menevät vertaisverkossa suoraan koneeltasi»

**Suggested:** «menevät suoraan koneeltasi (drop 'vertaisverkossa'; also L358, L365, and the related-guide blurb at L315 'miksi peer-to-peer voittaa…').»

**Decision:** ____________________


### 13. [medium] page `/home/`
**Issue:** 'äänitasoa kohti' is confusing: 'äänitaso' reads as audio LEVEL (volume), not audio track/layer. The sibling line L33 correctly uses 'tasokohtainen'. Here it should reference the layer/track.

**Original:** «A/V-synkronointiin äänitasoa kohti»

**Suggested:** «A/V-synkronointiin tasokohtaisesti (or: …ääniraitaa kohti).»

**Decision:** ____________________


### 14. [medium] page `/virtual-camera/`
**Issue:** 'vaihtelu' (variation/fluctuation) is used where 'vaihtaminen' (switching) is meant. You don't avoid screen-share 'variation', you avoid 'switching'.

**Original:** «kömpelön ruudunjaon vaihtelun sijaan»

**Suggested:** «kömpelön ruudunjaon vaihtamisen sijaan (same fix at L195: 'Ei kokoonpanon vaihtelua' → 'Ei kokoonpanon vaihtamista').»

**Decision:** ____________________


### 15. [medium] page `/virtual-camera/`
**Issue:** Semantically off: the AI recognises the person/silhouette, not the blur. 'tekoälyn tunnistamalla sumennuksella' literally means 'with blur that AI recognises'.

**Original:** «tekoälyn tunnistamalla sumennuksella»

**Suggested:** «tekoälypohjaisella sumennuksella.»

**Decision:** ____________________


### 16. [medium] page `/multistreaming/`
**Issue:** 'Tavoita … ansaintamalli' is a mismatch: you reach an audience ('tavoittaa'), you don't 'reach' a monetisation model. You tap into / leverage it.

**Original:** «Tavoita YouTuben algoritmi ja Kickin tekijäystävällinen ansaintamalli»

**Suggested:** «Hyödynnä YouTuben algoritmi ja Kickin tekijäystävällinen ansaintamalli.»

**Decision:** ____________________


### 17. [medium] page `/virtual-camera/`
**Issue:** Unclear phrasing. 'Verkkokameramallien tason parannuksia' ('enhancements at the level of webcam models') is confusing — every webcam is a 'webcam model'. The intent is 'enhancements of the grade flagship/expensive cameras give'.

**Original:** «Verkkokameramallien tason parannuksia suorana.»

**Suggested:** «Huippukameroiden tasoiset parannukset suorana. (or: Kalliiden kameroiden veroista kuvanparannusta suorana.)»

**Decision:** ____________________


### 18. [medium] page `/alternatives/obs/`
**Issue:** 'Vahingoittamatonta.' as a standalone lead reads oddly in Finnish (neuter partitive of 'undamaging'). English 'Non-destructive' needs a noun or a fuller clause.

**Original:** «Vahingoittamatonta.»

**Suggested:** «Vahingoittamaton siirto. (or: Mikään ei katoa.)»

**Decision:** ____________________


### 19. [medium] page `/alternatives/obs/`
**Issue:** Anglicism 'kontribuoida takaisin' (contribute back). Native Finnish for contributing to open-source is 'osallistua kehitykseen'.

**Original:** «kontribuoidaksesi takaisin»

**Suggested:** «osallistuaksesi kehitykseen (also L312 'kontribuointimalli' → 'osallistumismalli').»

**Decision:** ____________________


### 20. [medium] page `/alternatives/obs/`
**Issue:** The 'free as in beer / free as in speech' idiom is rendered word-for-word and won't land for a Finnish reader; 'ilmainen kuin ilmaiskaljat' is also tautological (ilmainen + ilmaiskaljat).

**Original:** «ilmainen kuin ilmaiskaljat, ei ilmainen kuin sananvapaus»

**Suggested:** «ilmaista käyttää, mutta ei avointa lähdekoodiltaan (drop the idiom or explain it).»

**Decision:** ____________________


### 21. [medium] page `/alternatives/obs/`
**Issue:** Vowel-harmony inconsistency for 'Teams' in the inessive: this page (and a couple of others, e.g. L276, L366) write 'Teamsissä', while home/multistreaming/virtual-camera write 'Teamsissa' (L41, L99, L210, L233). Pick one form; 'Teamsissa' dominates the site.

**Original:** «Teamsissä, Meetissä ja Discordissa»

**Suggested:** «Teamsissa, Meetissä ja Discordissa (standardise to 'Teamsissa' everywhere).»

**Decision:** ____________________


### 22. [medium] page `/home/`
**Issue:** Logical slip: '…vähäisempien pudonneiden kuvien saamiseksi' literally means 'in order to GET fewer dropped frames' — you don't want to obtain dropped frames at all. Recast as a benefit.

**Original:** «vähäisempien pudonneiden kuvien saamiseksi»

**Suggested:** «jotta viive ja pudonneiden kuvien määrä jäävät pienemmiksi (or: …pienemmän viiveen ja harvempien pudonneiden kuvien vuoksi).»

**Decision:** ____________________


### 23. [low] page `/home/`
**Issue:** Unit notation inconsistency: 'Mbps' here vs 'Mbit/s' everywhere else (e.g. L125, L134, L158).

**Original:** «6 Mbps Twitchiin, 4,5 YouTubeen»

**Suggested:** «6 Mbit/s Twitchiin, 4,5 Mbit/s YouTubeen.»

**Decision:** ____________________


### 24. [low] page `/alternatives/obs/`
**Issue:** Inconsistent term for the encoding process: 'enkoodaus'/'laitteistoenkoodaus' here vs the native 'koodaus' / 'laitteistokoodaus' on other pages (L9 'yhdestä koodauksesta', L450 'Laitteistokoodaus').

**Original:** «kaikki yhdestä enkoodauksesta»

**Suggested:** «kaikki yhdestä koodauksesta (pick one: encoder = enkooderi/koodain, encoding = koodaus, consistently).»

**Decision:** ____________________


### 25. [low] page `/home/`
**Issue:** 'verkon yli' / 'Wi-Fin yli' is a calque of 'over the network'. Acceptable in casual FI tech writing, but 'kautta'/'välityksellä' is cleaner native register and appears site-wide (L20, L50, L264, L278, L334, L385).

**Original:** «Puhelin langattomana kamerana verkon yli»

**Suggested:** «Puhelin langattomana kamerana verkon kautta (or: lähiverkossa).»

**Decision:** ____________________


### 26. [low] page `/virtual-camera/`
**Issue:** Term for 'canvas' varies: 'piirtoalue' here vs the loan 'kanvas' on other pages (L46, L86, L123, L159, L160, L461). Standardise.

**Original:** «Vaihda piirtoalue pystytilaan»

**Suggested:** «Vaihda kanvas pystytilaan (or use 'piirtoalue' everywhere).»

**Decision:** ____________________


### 27. [low] page `/multistreaming/`
**Issue:** 'ei seurauksia yksityisyydelle' ('no consequences for privacy') is a slight calque; the site elsewhere uses the more natural 'ei huolta yksityisyydestä' (L168) / 'ei tietosuojahuolia' (L11).

**Original:** «ei seurauksia yksityisyydelle»

**Suggested:** «ei huolta yksityisyydestä (or: ei vaikutuksia yksityisyyteen).»

**Decision:** ____________________


### 28. [low] page `/home/`
**Issue:** Colloquial 'merkkaa/merkata' (to mark/annotate) is used in marketing copy (L59, L79), while L197 correctly uses the standard 'merkitse'. Use the standard form in copy.

**Original:** «Merkkaa diojesi päälle»

**Suggested:** «Merkitse diojesi päälle (and L79 'voin merkata dioja' → 'voin merkitä dioja').»

**Decision:** ____________________


### 29. [low] page `/multistreaming/`
**Issue:** The primary CTA button is referred to by four different names across the site: 'Go Live' (L135, L174, L181, L272), 'Mene liveen' (L68), 'Aloita lähetys' (L330+), 'Lähetä suorana' (L380, L393). If the app's button literally says 'Go Live', keep that consistently; otherwise pick one Finnish label.

**Original:** «Paina Go Live»

**Suggested:** «Standardise the button label site-wide (e.g. always 'Go Live' if that is the UI string, with a Finnish gloss on first use).»

**Decision:** ____________________


### 30. [low] page `/multistreaming/`
**Issue:** Mixed handling of 'ingest': English 'ingest-osoite'/'ingestiin'/'ingest-palvelin' (L136, L152, L156, L166) vs the Finnish 'vastaanotto'/'vastaanottopalvelin' (L343, L393). Choose one.

**Original:** «jokaisen kohteen ingest-osoitteeseen»

**Suggested:** «jokaisen kohteen vastaanotto-osoitteeseen (or keep 'ingest' everywhere).»

**Decision:** ____________________


### 31. [low] page `/for/churches/`
**Issue:** 'alateksti' in Finnish means subtitle/caption; for an on-screen name+title banner (lower third) it's slightly off. The site also uses 'alapalkki' (L199, L389) and 'alagrafiikka' (L29, L61, L88) for the same thing — three terms. 'alapalkki' or 'nimiplanssi' fits a name banner best.

**Original:** «alatekstit saarnaajalle»

**Suggested:** «alapalkit saarnaajalle (and unify alateksti/alapalkki/alagrafiikka across the site).»

**Decision:** ____________________


### 32. [low] page `/for/youtubers/`
**Issue:** 'SplitCamin näyttö seuraa…' reads as 'SplitCam's screen monitors…' ('näyttö' = physical display). The intended meaning is the in-app status monitor; L429 correctly uses 'tilanäyttö'.

**Original:** «SplitCamin näyttö seuraa enkooderin kuormaa»

**Suggested:** «SplitCamin tilanäyttö seuraa enkooderin kuormaa (or simply 'SplitCam seuraa enkooderin kuormaa').»

**Decision:** ____________________


### 33. [low] page `/home/`
**Issue:** Possible numeric inconsistency: 'Twitch, YouTube, Facebook, Kick ja yli 84 muuhun' implies 84 platforms BEYOND the four named (=88+), whereas the rest of the site frames the catalogue as '84+ platforms total' (L10, L107, L132, L168). Same pattern at L109.

**Original:** «ja yli 84 muuhun yhtä aikaa»

**Suggested:** «ja kymmeniin muihin yhtä aikaa (avoid implying 4 + 84; or align the count with the '84+ total' framing).»

**Decision:** ____________________
