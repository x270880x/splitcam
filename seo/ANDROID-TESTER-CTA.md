# Android tester recruitment CTA — /products/ (34 locales + EN)

**Status: SHIPPED 2026-07-17.** The disabled "Coming soon" Google Play chip in the SplitCam
Remote panel on `/products/` is now a live outlined "Become a tester" button in all 35
locales, linking to the signup form (NOT the opt-in URL directly — a stranger clicking the
opt-in link gets "app not available"; the form → manual add → email flow is what works).
The Step-02 prose was updated from "coming soon" to "in closed testing — join the tester
program". Button uses `btn-store btn-store-2` (outlined/secondary) so it reads as "join
testing", distinct from the solid App Store button ("download now").

Form: https://docs.google.com/forms/d/e/1FAIpQLSeJmQt04MVYcil0nzVRg9s3_QdvEV41tm3bh9WR5CObAeIbdA/viewform
Verified: linkcheck 0 broken, tags balanced + JSON-LD valid across all 35, and 390px render
clean on EN / ru (longest label "Стать тестировщиком" fits) / ar (RTL); 1440px no regress.

The Google-Group approach was dropped — the Testers radio is Email-list-OR-Group, so a Group
would have detached the existing lists. Website signups instead go to a NEW `web-testers`
email list (see `seo/TESTER-FUNNEL-COPY.md`), added alongside the existing lists.

## What this is

SplitCam Remote for **Android** is in Google Play **closed testing** under a personal
developer account, so it is subject to the "12 testers opted-in continuously for 14 days"
production-access gate. (This is a DIFFERENT app from `com.splitcam`, which is long live
in production with 10K+ installs — that one is not affected.)

Plan: convert the existing dead "Coming soon" Google Play chip in the SplitCam Remote
panel on `/products/` into a live "Become a tester" link, recruiting real desktop-SplitCam
users into the closed test. Rationale: the counter is only gate one — gate two is an
undocumented **engagement** review, and site-recruited users actually open the app,
where friends recruited for the count do not.

## Blocked on (account owner, Play Console)

1. **The closed-test opt-in URL** (Testing -> Closed testing -> Testers -> Copy link).
2. **A Google Group** — required, because you cannot add anonymous website visitors to an
   email list. Group membership is the only mechanism that accepts open sign-ups.

### DO NOT do this blindly — the migration risk

Google's doc: *"Only users who are members of the Google Groups you enter will be able to
join your test."* Switching the live track from an email list to a Group **narrows**
eligibility to group members. The current 12 testers are on an email list and are NOT
group members. **Google does not document any grandfathering for this transition.** That
silence is the finding. Verify in Console whether an email list and a Google Group can be
attached to the SAME track simultaneously:

- **If yes** -> zero risk. The current 12 stay on the list untouched; the website funnel
  runs through the Group.
- **If it is an either/or radio** -> postpone the public funnel until the current cycle
  completes. 5 accumulated days are worth more than extra testers.

## Verified facts (researched 2026-07-17, adversarially checked)

- **More testers do NOT shorten the 14 days.** The window is per-tester, not per-track. A
  tester who opts in on day 10 starts their own 14 days on day 10. 20-30 testers buys
  dropout insurance and engagement, never speed.
- **No cap to worry about.** Email lists hold 2,000; Groups are unlimited. The "1,000
  tester limit on closed tracks" circulating on blogs is a misreading — that number is the
  *minimum* for **open** testing, a floor, not a ceiling. Open testing is anyway blocked
  until production access, so you cannot be pushed into it.
- **Public recruitment is explicitly RECOMMENDED by Google**, not risky: *"reach out to
  communities where users are likely to exist and actively recruit them... post about your
  app on social media and ask your followers to sign up for testing."* Docs also require
  testers "representative of your app's future users" — desktop SplitCam users are the
  textbook case. The scare terms ("irregular testing activity", battery-curve detection,
  new-account trust weight) appear on **no official Google page**; they trace to sites
  selling $29-45 tester packages.
- **Tester count does not appear in the production-access application at all.** It asks
  about engagement, feedback gathered, and **what you changed in response**. "No changes
  were needed" is a known rejection trigger — collect real feedback and ship real fixes.
- **Do NOT freeze the build.** Shipping releases during closed testing does not reset the
  counter (two Google Diamond Product Experts state this plainly), and Google's rejection
  email cites *failure to ship updates* as a rejection reason. "Don't touch the app" is
  backwards.
- **Joining the Group != opting in.** Two separate steps; the 14-day counter starts at
  opt-in. Expect heavy funnel drop-off — recruit 16-30 to land 12 reliable.
- **Only confirmed counter-killer: a tester pressing "Leave the program."** Irreversible
  for that tester's streak.
- **Do not upload a CSV mid-cycle** — it overwrites rather than appends.
- **"14 more days starting from the review date" is undocumented.** Whether the 5
  accumulated days survive a review cannot be answered from any authoritative source;
  `review date`/`14 more days`/`restart`/`reset` return zero hits in Google's Help Center.
  Safe play: apply only when BOTH the streak counter reads >=14 AND >=14 days have passed
  since the review date. Waiting for the later of the two costs nothing.

## The copy (all reviewed by a second native speaker per locale)

EN source: small `Closed testing`, bold `Become a tester`.

Deliberately NOT "Android beta": (a) the same page already tags the shipping
`SplitCam for Android` card "Beta", so it would put two different Android betas on one
page; (b) this is a closed test requiring a group join, so "beta" promises exactly what
the user will not get.

Each label matches **Google Play's own vocabulary in that locale**, so the button and its
destination page use the same word.

| loc | small | bold |
|---|---|---|
| **EN** | `Closed testing` | `Become a tester` |
| **ru** | `Закрытый тест` | `Стать тестировщиком` |
| **es** | `Prueba cerrada` | `Hazte tester` |
| **de** | `Geschlossener Test` | `Tester werden` |
| **fr** | `Test fermé` | `Devenir testeur` |
| **pt** | `Teste fechado` | `Seja testador` |
| **tr** | `Kapalı test` | `Teste katılın` |
| **fil** | `Closed na pag-test` | `Maging tester` |
| **uk** | `Закрите тестування` | `Стати тестувальником` |
| **it** | `Test chiuso` | `Diventa un tester` |
| **vi** | `Thử nghiệm khép kín` | `Đăng ký thử nghiệm` |
| **id** | `Pengujian tertutup` | `Jadi penguji` |
| **nl** | `Gesloten test` | `Word tester` |
| **ro** | `Testare închisă` | `Devino tester` |
| **hi** | `Closed testing` | `Tester बनिए` |
| **ja** | `クローズドテスト` | `テスターになる` |
| **ms** | `Ujian tertutup` | `Jadi penguji` |
| **bg** | `Затворено тестване` | `Станете изпитател` |
| **ar** | `اختبار مغلق` | `انضم كمُختبِر` |
| **ko** | `비공개 테스트` | `테스터 신청` |
| **th** | `การทดสอบแบบปิด` | `สมัครเป็นผู้ทดสอบ` |
| **pl** | `Testy zamknięte` | `Zostań testerem` |
| **hu** | `Zárt tesztelés` | `Legyél tesztelő` |
| **sv** | `Sluten testning` | `Bli testare` |
| **zh** | `封闭测试` | `申请成为测试员` |
| **el** | `Κλειστή δοκιμή` | `Γίνετε δοκιμαστές` |
| **cs** | `Uzavřený test` | `Stát se testerem` |
| **he** | `בדיקה סגורה` | `הצטרפו כבודקים` |
| **sr** | `Zatvoreno testiranje` | `Postani tester` |
| **hr** | `Ograničen pristup` | `Postanite tester` |
| **da** | `Lukket test` | `Bliv tester` |
| **fi** | `Suljettu testaus` | `Ryhdy testaajaksi` |
| **no** | `Lukket testing` | `Bli tester` |
| **sk** | `Uzavreté testovanie` | `Stať sa testerom` |
| **fa** | `آزمایش بسته` | `تست‌کننده شوید` |

### Corrections the native review caught

These are recorded because they are a recurring trap, not one-offs — the loanword
"tester" means a **measuring device** or a **cosmetics sample** in several languages:

- **uk** — noun audit: тестер = multimeter/perfume sample; Play uk says "Стати тестувальником"
- **id** — noun audit: tester = lipstick sample on a shelf; Play id uses "penguji"
- **fa** — noun audit: تستر = perfume sample / probe device; Play fa uses an agent noun
- **bg** — noun audit: Play bg says "Станете изпитател" verbatim; "тестер" absent from Google bg strings
- **fil** — REVERTED an earlier bad "fix" — "na" is the ligature, not the adverb "already". Google fil Play help itself uses "Closed na pag-test"

Cleared as genuinely fine (the loanword IS what Google Play itself uses there): `pl`
Zostań testerem, `cs` Stát se testerem, `sk` Stať sa testerom, `sr` Postani tester, `hr`
Postanite tester, `es` Hazte tester, `it` Diventa un tester, `ro` Devino tester, `el`
Γίνετε δοκιμαστές, `fi` Ryhdy testaajaksi, `hi` Tester बनिए.

Other catches: `fr` **Test fermé** — without the acute, "Test ferme" parses as "the test
closes". `bg` small **Затворено тестване** — "Затворен тест" means "a closed exam"
(Bulgarian тест = quiz). `hr` small **Ograničen pristup** — "Zatvoreni program" reads as
closed-SOURCE software. `de` **Android-Beta** needed the hyphen (Deppenleerzeichen).

## Step-02 prose replacement

Replaces the "the Android version is coming soon" sentence. EN:

> Free on the App Store for iPhone and iPad (iOS 17+); the Android version is in closed
> testing — join the tester program to try it early. Make sure your phone is on the same
> Wi-Fi as the streaming PC.

Note: `iOS 17+` here is CORRECT and is not a typo for the `iOS 16+` elsewhere on the page.
They are two different apps — SplitCam Remote (`id6760961594`) is iOS 17+; SplitCam Live
Multistreaming (`id1543666414`) is iOS 16+. A review agent flagged this as a
contradiction; it was verified as a false alarm. Do not "fix" it.

**ru** — Бесплатно в App Store для iPhone и iPad (iOS 17+); версия для Android пока доступна только участникам закрытого тестирования — станьте тестировщиком, чтобы попробовать её раньше всех. Убедитесь, что телефон в той же сети Wi-Fi, что и стриминговый компьютер.

**es** — Gratis en el App Store para iPhone y iPad (iOS 17+); la versión para Android está en fase de pruebas cerradas: apúntate al programa de testers para probarla antes que nadie. Asegúrate de que tu teléfono esté en la misma red Wi-Fi que el equipo desde el que transmites.

**de** — Kostenlos im App Store für iPhone und iPad (iOS 17+); die Android-Version befindet sich noch im geschlossenen Test — tritt dem Testprogramm bei, um sie vorab auszuprobieren. Achte darauf, dass dein Handy im selben WLAN ist wie der Streaming-PC.

**fr** — Gratuit sur l'App Store pour iPhone et iPad (iOS 17+) ; la version Android est encore en test fermé — inscrivez-vous au programme pour l'essayer en avant-première. Vérifiez que votre téléphone est sur le même Wi-Fi que le PC de streaming.

**pt** — Grátis na App Store para iPhone e iPad (iOS 17+); a versão para Android está em teste fechado — entre no programa de testadores para experimentar antes do lançamento. Confira se o celular está na mesma rede Wi-Fi do computador da transmissão.

**tr** — iPhone ve iPad için App Store'da ücretsiz (iOS 17+); Android sürümü ise kapalı testte — ilk deneyenlerden olmak için test programına kaydolun. Telefonunuzun yayın bilgisayarınızla aynı Wi-Fi ağında olduğundan emin olun.

**fil** — Libre sa App Store para sa iPhone at iPad (iOS 17+); nasa closed testing pa ang Android version — sumali sa tester program para masubukan ito nang maaga. Siguraduhing nasa parehong Wi-Fi ang phone mo at ang streaming PC.

**uk** — Безкоштовно в App Store для iPhone та iPad (iOS 17+); версія для Android поки що проходить закрите тестування — приєднуйтеся до програми тестування, щоб отримати ранній доступ. Переконайтеся, що телефон у тій самій мережі Wi-Fi, що й стрімінговий комп'ютер.

**it** — Gratis sull'App Store per iPhone e iPad (iOS 17+); la versione Android è ancora in beta chiusa: iscriviti come tester per provarla in anteprima. Assicurati che il telefono sia sulla stessa rete Wi-Fi del PC di streaming.

**vi** — Miễn phí trên App Store cho iPhone và iPad (iOS 17+); bản Android hiện đang thử nghiệm kín — đăng ký tham gia để dùng thử sớm. Hãy đảm bảo điện thoại và máy tính dùng để stream ở cùng một mạng Wi-Fi.

**id** — Gratis di App Store untuk iPhone dan iPad (iOS 17+); versi Android masih dalam pengujian tertutup — gabung ke program tester untuk mencobanya lebih awal. Pastikan HP berada di Wi-Fi yang sama dengan komputer streaming.

**nl** — Gratis in de App Store voor iPhone en iPad (iOS 17+); de Android-versie is nog in een gesloten testfase — word tester om de app alvast te proberen. Zorg dat je telefoon op hetzelfde wifi-netwerk zit als de stream-pc.

**ro** — Gratuit în App Store pentru iPhone și iPad (iOS 17+); versiunea pentru Android e în testare închisă — înscrie-te în program ca s-o încerci înainte de lansare. Asigură-te că telefonul e în aceeași rețea Wi-Fi ca și computerul de streaming.

**hi** — iPhone और iPad (iOS 17+) के लिए App Store पर free; Android version अभी closed testing में है — इसे सबसे पहले try करने के लिए tester program join कीजिए. ध्यान रखिए कि आपका phone और streaming PC एक ही Wi-Fi पर हों.

**ja** — iPhone・iPad（iOS 17+）版は App Store で無料。Android 版は現在クローズドテスト中。テストに参加すれば、ひと足先に試せます。スマホが配信用PCと同じ Wi-Fi に接続されていることを確認してください。

**ms** — Percuma di App Store untuk iPhone dan iPad (iOS 17+); versi Android masih dalam ujian tertutup — sertai program pengujian untuk mencubanya lebih awal. Pastikan telefon anda berada dalam rangkaian Wi-Fi yang sama dengan PC streaming.

**bg** — Безплатно в App Store за iPhone и iPad (iOS 17+); версията за Android е в затворено тестване — включете се в програмата за тестери, за да я изпробвате първи. Уверете се, че телефонът е в същата Wi-Fi мрежа като стрийминг компютъра.

**ar** — مجاني على App Store لـ iPhone وiPad (iOS 17+). أما نسخة Android فما زالت في مرحلة الاختبار المغلق — سجّل في برنامج المُختبِرين لتجربتها مبكرًا. تأكّد من أن هاتفك على شبكة Wi-Fi نفسها التي عليها حاسوب البث.

**ko** — iPhone·iPad용 앱은 App Store에서 무료로 받을 수 있습니다(iOS 17 이상). Android 버전은 아직 비공개 테스트 중이며, 테스터로 등록하면 미리 사용해 볼 수 있습니다. 휴대폰과 방송용 PC가 같은 Wi-Fi에 연결되어 있는지 확인하세요.

**th** — ฟรีบน App Store สำหรับ iPhone และ iPad (iOS 17+) ส่วนเวอร์ชัน Android อยู่ระหว่างการทดสอบแบบปิด — สมัครเป็นผู้ทดสอบเพื่อลองใช้ก่อนใคร ตรวจสอบให้แน่ใจว่าโทรศัพท์อยู่บน Wi-Fi เดียวกับพีซีสตรีม

**pl** — Za darmo w App Store na iPhone'a i iPada (iOS 17+); wersja na Androida jest w fazie testów zamkniętych — dołącz do programu testerów, aby wypróbować ją jeszcze przed premierą. Upewnij się, że telefon jest w tej samej sieci Wi-Fi co komputer streamingowy.

**hu** — Ingyenes az App Store-ban iPhone-ra és iPadre (iOS 17+); az Android-verzió zárt tesztelés alatt áll — jelentkezz a tesztelői programba, és próbáld ki az elsők között. Győződj meg róla, hogy a telefonod ugyanazon a Wi-Fin van, mint a streamelő gép.

**sv** — Gratis i App Store för iPhone och iPad (iOS 17+); Android-versionen är i sluten testning — gå med i testprogrammet så blir du en av de första som får prova den. Se till att telefonen och streamingdatorn är på samma Wi-Fi-nätverk.

**zh** — 在 App Store 免费下载，适用于 iPhone 和 iPad（iOS 17+）；Android 版正在封闭测试，申请成为测试员即可抢先体验。请确保手机与直播电脑连入同一 Wi-Fi 网络。

**el** — Δωρεάν στο App Store για iPhone και iPad (iOS 17+)· η έκδοση Android βρίσκεται ακόμη σε κλειστή δοκιμή — δηλώστε συμμετοχή στο πρόγραμμα beta για να τη δοκιμάσετε πρώτοι. Βεβαιωθείτε ότι το κινητό είναι στο ίδιο Wi-Fi με τον υπολογιστή streaming.

**cs** — Zdarma v App Store pro iPhone a iPad (iOS 17+); verze pro Android je zatím v uzavřeném testování — zapojte se jako tester a vyzkoušejte ji mezi prvními. Ujistěte se, že telefon je ve stejné Wi-Fi síti jako streamovací počítač.

**he** — חינם ב-App Store ל-iPhone ול-iPad ‏(iOS 17+); גרסת ה-Android עדיין בבדיקה סגורה — הצטרפו לתוכנית הבודקים כדי לקבל גישה עוד לפני ההשקה. ודאו שהטלפון נמצא באותה רשת Wi-Fi כמו מחשב השידור.

**sr** — Besplatno u App Storeu za iPhone i iPad (iOS 17+); verzija za Android je u zatvorenom testiranju — prijavite se za beta program i isprobajte je među prvima. Uverite se da su telefon i streaming računar na istoj Wi-Fi mreži.

**hr** — Besplatno u App Storeu za iPhone i iPad (iOS 17+); verzija za Android je u zatvorenom testiranju — prijavite se kao tester i isprobajte je među prvima. Pobrinite se da je telefon u istoj Wi-Fi mreži kao streaming računalo.

**da** — Gratis i App Store til iPhone og iPad (iOS 17+); Android-versionen er i lukket test — tilmeld dig testprogrammet for at prøve den før alle andre. Sørg for, at telefonen er på det samme Wi-Fi-netværk som stream-computeren.

**fi** — Ilmainen App Storessa iPhonelle ja iPadille (iOS 17+); Android-versio on suljetussa testauksessa – liity testiryhmään, niin pääset kokeilemaan sitä ennakkoon. Varmista, että puhelimesi on samassa Wi-Fi-verkossa kuin striimauskone.

**no** — Gratis i App Store for iPhone og iPad (iOS 17+). Android-versjonen er i lukket testing — bli med i testprogrammet for å prøve den tidlig. Sørg for at telefonen er koblet til samme Wi-Fi som streaming-PC-en.

**sk** — Zadarmo v App Store pre iPhone a iPad (iOS 17+); verzia pre Android je v uzavretom testovaní — prihláste sa ako tester a vyskúšajte ju medzi prvými. Uistite sa, že je telefón v rovnakej Wi-Fi ako streamovacie PC.

**fa** — رایگان در App Store برای iPhone و iPad (iOS 17+)؛ نسخه‌ی اندروید فعلاً در مرحله‌ی تست محدود است — به جمع تسترها بپیوندید تا زودتر آن را امتحان کنید. مطمئن شوید گوشی شما روی همان Wi-Fi کامپیوتر استریم است.

## Apply checklist (once the opt-in URL exists)

1. In all 35 `*/products/index.html`: replace the disabled
   `<span class="btn-store btn-store-2" style="opacity:.55;cursor:not-allowed" aria-disabled="true">`
   with `<a href="OPT_IN_URL" class="btn-store btn-store-2" target="_blank" rel="noopener">`,
   and swap the `<small>`/`<b>` text per the table above. Keep the closing tag in sync
   (`</span>` -> `</a>`).
2. Replace the Step-02 prose per locale.
3. `python3 seo/i18n_wire.py`
4. `python3 seo/linkcheck.py --no-network` — must be 0 broken.
5. Mobile check at ~390px AND desktop ~1440px. **Specific risk:** `ru` bold
   "Стать тестировщиком" is 19 chars vs 13 for the longest existing bold label
   ("Mac App Store"); `de` "Geschlossener Test" and `fil` "Closed na pag-test" are 18.
   Confirm `.btn-store` does not overflow or clip. Screenshots to `seo/screenshots/`.
6. Commit individually so it is trivially revertible.

## Revert trigger

**When SplitCam Remote for Android reaches production**, revert this: the chip becomes a
normal Play Store link (like the iOS one), and the Step-02 prose drops the closed-testing
sentence. Also re-open the parked `/products/remote/` decision — per `seo/REMINDERS.md`
that page was deferred *because* Remote was one-store-only, and Android shipping is the
stated condition for revisiting it.
