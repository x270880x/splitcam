# SplitCam — Japanese (`ja`) localization review

First-pass AI verdict: **good** · 5 item(s) to confirm (1 high · 1 medium · 3 low)

You are a native **Japanese** speaker. This is marketing copy for SplitCam (free live-streaming / virtual-camera software). For each item: write **KEEP** (original is fine), **APPLY** (use the suggestion), or your own wording.

Ignore anything about brand/tech terms in English (SplitCam, OBS, NVENC, QuickSync, AMF, RTMP(S), NDI, VST, Zoom, Teams, Meet, Discord, Twitch, YouTube, etc.) — those are intentional.


---


### 1. [high] page `/home/`
**Issue:** The H1 is grammatically broken. "無料の配信ソフトクリエイターのために" jams "無料の配信ソフト" (free streaming software) straight into "クリエイターのために" (for creators) with no particle or break, so a reader parses it as the nonsensical compound noun "free-streaming-software creator" (無料の配信ソフトクリエイター). This is the most prominent line on the site and reads unmistakably as a botched MT/copy-paste merge of two phrases. A native would never write this.

**Original:** «どこでもライブ配信。無料の配信ソフトクリエイターのために。»

**Suggested:** «クリエイターのための、どこでも使える無料ライブ配信ソフト。 (or, keeping two clauses: どこでもライブ配信を。クリエイターのための無料配信ソフト。)»

**Decision:** ____________________


### 2. [medium] page `/home/`
**Issue:** Awkward word order / dangling object-marker. "複数のプラットフォームへ配信を、1回のエンコードから" places を after 配信 but then breaks off, leaving the object hanging before the verb 送信します arrives much later. The を…、…から split reads like literal English ("send your stream to multiple platforms, from one encode"). A native would restructure.

**Original:** «複数のプラットフォームへ配信を、1回のエンコードから»

**Suggested:** «1回のエンコードで、複数のプラットフォームへ同時に配信。 (drop the stranded を; lead with the "one encode" point)»

**Decision:** ____________________


### 3. [low] page `/home/`
**Issue:** Truncated/units-dropped numbers. The list reads "Twitch に6Mbps、YouTube に4.5、TikTok に2.5" — 4.5 and 2.5 lose the Mbps unit that 6Mbps establishes, so they read as bare decimals. Native technical copy keeps the unit (or at least writes 4.5Mbps / 2.5Mbps) rather than leaving "4.5" and "2.5" floating.

**Original:** «例：Twitch に6Mbps、YouTube に4.5、TikTok に2.5»

**Suggested:** «例：Twitch に6Mbps、YouTube に4.5Mbps、TikTok に2.5Mbps»

**Decision:** ____________________


### 4. [low] page `/home/`
**Issue:** Internal number-format inconsistency. The home page uses "84以上" in the hero/feature copy (lines for マルチ配信), while every other page — and even the home FAQ region elsewhere — uses the form "84+" (e.g. 84+プラットフォーム). Within a single site the platform count should be written consistently; mixing 84以上 and 84+ looks unedited.

**Original:** «Kick ほか84以上へピアツーピアで»

**Suggested:** «Use one form site-wide. Either standardize on 84+（例：Kick ほか84+のプラットフォームへ）or on 84以上 everywhere — but not both.»

**Decision:** ____________________


### 5. [low] page `/alternatives/obs/`
**Issue:** Over-literal idiom calque. "助けてくれるというより、戦う相手のように感じられます" is a word-for-word rendering of English "feels like something you fight rather than something that helps you." 戦う相手 (an opponent you fight) for a software UI is unidiomatic in Japanese marketing copy; natives express this as the tool getting in your way / feeling like an obstacle.

**Original:** «助けてくれるというより、戦う相手のように感じられます»

**Suggested:** «作業を助けるどころか、むしろ使いこなすのに苦労する／立ちはだかるように感じられます»

**Decision:** ____________________
