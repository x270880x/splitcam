# SplitCam Remote — tester funnel copy (form + opt-in email)

**Status: form is LIVE. Site button NOT deployed yet.**

## Semi-automation (built 2026-07-18)

**Full zero-touch is NOT possible on this setup** and was not built. Verified against official
docs: the Play Developer API `edits.testers` manages only Google GROUPS ("email lists are not
supported by this resource"), and consumer-Gmail groups have no member-add API — so adding a
signup to the Console tester list is inherently manual here. Automating it would require a paid
Workspace/Cloud Identity domain AND switching the live track from email-list to group, which
risks zeroing the 12 testers' 14-day streak. Not worth it before the gate clears.

What WAS built (safe, no risk to the streak):
- **Form email notifications: ON** — you get an email per new signup.
- **Responses linked to a Google Sheet:**
  https://docs.google.com/spreadsheets/d/1qEGIHXiwP0od9o8RXmZ_VGQ6ObeFszZBOMDOJttfm5o/edit
  (col A timestamp, B = Google account, C = use-case)
- **Apps Script written:** `seo/tester-funnel.gs` — a "SplitCam" menu in that Sheet that
  emails the opt-in link (RU+EN) to rows you tick as "Added to Console", and stamps "Link sent".
  The link is sent on YOUR tick (after you add them to Console), never on submit — sending
  before they're on a list would give them "app not available".

The ONE manual step that can't be automated: adding the email to the Console tester list.

### Finish the setup (owner, ~3 min — the OAuth grant is yours to make)
1. Open the responses Sheet (link above) → **Extensions → Apps Script**.
2. Delete the stub `Code.gs`, paste all of `seo/tester-funnel.gs`, **Save**.
3. Reload the Sheet → new **SplitCam** menu → **Set up sheet (add columns)**.
4. Approve the one-time Google authorization (it grants the script Gmail-send + Sheets; the
   "app isn't verified → Advanced → Go to project → Allow" screen is expected for a personal
   script). This grant is deliberately left to you — it lets the script send email as you.

### Daily use
Notification arrives → add the Google account(s) to the Console list → in the Sheet tick
**Added to Console** on those rows → **SplitCam → Send opt-in link to ticked rows**. Done.

## Contact address — read this before "improving" it

**The address is `splitcameramail@gmail.com`.** Chosen by the user 2026-07-17.

`support@splitcam.com` DOES NOT EXIST. An earlier draft of this document invented it as a
plausible-looking address; it was never real. Verified 2026-07-17:
- Zero email addresses appear anywhere on splitcam.com (527 pages, no mailto:, no contact page).
- The only occurrences of `support@splitcam.com` in the whole repo were in this file.
- splitcam.com does accept mail (MX -> mail.splitcam.com -> 91.223.223.113, the old cPanel),
  but whether a `support@` mailbox exists could not be confirmed: the stored
  `~/.hostsila_cpanel` password returns 401 against rocket-cp2.hostsila.org:2083.
- The real, publicly listed addresses on the live `com.splitcam` Play listing are
  `splitcam2010@gmail.com` and `splitcameramail@gmail.com`.

`splitcameramail@gmail.com` is also the Play Console account and the destination for the
testing-feedback email notifications turned on 2026-07-17 — so tester replies, Play feedback
notifications, and Console mail all land in one inbox.

## The live form (created 2026-07-17)

**https://docs.google.com/forms/d/e/1FAIpQLSeJmQt04MVYcil0nzVRg9s3_QdvEV41tm3bh9WR5CObAeIbdA/viewform**

Editor: https://docs.google.com/forms/d/1ppkogblkrtiebFL_Sgm4vtvAlUcjTgqoTC7yXc44Y6I/edit
(owned by splitcameramail@gmail.com, the Play Console account — authuser=5)

Built to the spec below. Verified settings:
- Access **Anyone with the link**; nobody notified on publish.
- **Collect email addresses = Do not collect** — deliberate. An auto-stamped browser account
  (whatever Google the desktop is signed into) would fight the hand-typed PHONE account and
  we would not know which to trust. The viewform notice "your email will not be visible to
  the recipient" is Google reassuring the respondent, not a leak.
- **Limit to 1 response = off** — deliberate, the confirmation message tells people to
  resubmit if they typo'd their address.
- Field 1 is required and is NOT called "email"; field 2 is optional so it can never block submit.

## Play Console state after the 2026-07-17 working session

Done live, via the Console UI (all on the RADIO = Email lists; the Google Groups radio was
never touched):

1. **Manual tester added.** `Forveo134@gmail.com` -> the `test` email list (34 -> 35).
   Applies immediately (adding to an already-attached list needs no review). That person
   still has to opt in + install + use it themselves via
   https://play.google.com/apps/testing/com.splitcam.remote.
2. **Feedback channel set + submitted.** Testers tab "Feedback URL or email address" =
   `splitcameramail@gmail.com`. Submitted for review; **in review since 2026-07-17**
   (Google review typically <=7 days). This is independent of the 14-day tester streak.
3. **`web-testers` email list created**, seeded with `splitcameramail@gmail.com` (the seed
   only satisfies Google's "at least one address" requirement on a list). Creating it
   auto-attached it to the RC-1 track, so there is now a **staged, NOT-yet-submitted**
   change: "Add 1 email list: web-testers". It was deliberately NOT submitted, because
   submitting it would cancel + restart the in-progress feedback-URL review and add wait
   time. It will ride along with the next submission (e.g. the 1.2 build / when the site
   button ships).

   **Caveat for whoever adds website signups next:** the list EXISTS but its ATTACHMENT to
   the RC-1 track is still staged. Emails added to `web-testers` are not live testers until
   that attach is published. Either submit the staged change once the feedback-URL review
   finishes, or bundle it with the next release. (Meanwhile, to make a signup live
   immediately, add them to the already-attached `test` list instead.)

## The opt-in URL (read from Play Console 2026-07-17)

**https://play.google.com/apps/testing/com.splitcam.remote = `https://play.google.com/apps/testing/com.splitcam.remote`**

This is the "Join on the web" link from Testing -> Closed testing -> RC-1 -> Testers.
It only works for addresses that are already on an attached email list — a stranger who
opens it gets "app not available", which is exactly why the funnel needs the manual add
step in between.

https://play.google.com/store/apps/details?id=com.splitcam.remote = `https://play.google.com/store/apps/details?id=com.splitcam.remote`
(same destination as the "Download it on Google Play" link on the opt-in page; also only
resolves for opted-in testers while the app is in closed testing).

Still needed: a `web-testers` email list in Play Console, and the site button wired to the
form URL.

Companion doc: `seo/ANDROID-TESTER-CTA.md` (the 35-locale button copy for /products/).

## Why this exists — the numbers that define the problem

Play Console, checked 2026-07-17 (app `com.splitcam.remote`, track RC-1):

| | |
|---|---|
| Emails already on tester lists | **77** (of-live 25, spli_cam_remote 18, test 34) |
| Opted in | **12** |
| **Actually installed** | **1** |
| Testing feedback, all time | **1 entry** ("super", v1.0, 2026-05-06, unanswered) |
| Feedback URL field | empty |
| Feedback email notifications | was OFF -> **turned ON 2026-07-17** |
| Last release | 2026-05-28 (v1.1) |
| Production application | **REJECTED 2026-07-11 11:06** |
| Counter | "12 testers opted in for 6 days" = exactly the days since the review -> the streak restarts at the review date |
| Earliest re-apply | **2026-07-25** (review date + 14) |

The 77 -> 1 collapse is the whole problem. Google's rejection reason list names
"your testers not being engaged with your app" verbatim. Recruiting MORE people into a
funnel that converts 77 to 1 fixes nothing — this copy exists to fix the conversion.

## Strategy note — do not rush 2026-07-25

Every rejection restarts the 14 days from the NEW review date. Applying unprepared on
Jul 25 -> rejected ~Aug 1 -> next window Aug 15. Applying PREPARED on ~Aug 1 is FASTER
than applying unprepared on Jul 25. The counter is not the binding constraint; the
engagement story is.

The production application (verified from Play Console's own "Preview questions") asks:
- Part 1: how easy was recruiting; **what engagement did you get — did testers use all
  features, was usage like a real user's**; **summarize the feedback and how you collected it**
- Part 2: intended audience; how the app provides value; expected first-year installs
- Part 3: **what did you change based on the closed test**; how did you decide it was ready

With 1 install, 1 word of feedback, and no release since May 28, Parts 1 and 3 have no
honest answer. That is why Jul 11 failed.

## Mechanism — why a form and not a Google Group

The Testers tab is a RADIO: `Email lists` OR `Google Groups`. Switching to Groups would
detach all 77 addresses and very likely burn the 12 opted-in testers' streak — Google
documents no grandfathering. **Do not touch that radio.**

But the email lists themselves are CHECKBOXES *inside* the Email option. So: create a
NEW list (e.g. `web-testers`), tick it alongside the existing three, and add website
signups there. Purely additive, touches nothing that currently works.

Funnel: site button -> Google Form -> we add the address to `web-testers` -> we email the
opt-in link -> they opt in -> **they install** -> they use it once for real.

---

# SplitCam Remote — Android closed testing: final copy

Everything below is paste-ready. Only `https://play.google.com/apps/testing/com.splitcam.remote`, `https://play.google.com/store/apps/details?id=com.splitcam.remote` and `[QR]` need real values.

---

## 1. The Google Form

### 1.1 Placement (this is part of the copy — do not skip)

On `splitcam.com/products`, the Android card's CTA must be **two things, not one**:

- Button: **Открыть форму на телефоне** / **Open the form on your phone**
- Next to it: `[QR]` — a QR code pointing at the form URL, with the caption below.

**RU caption:** `Отсканируйте с того Android-телефона, куда поставите Remote. Так адрес аккаунта подставится сам.`
**EN caption:** `Scan it with the Android phone you'll install Remote on. That way the account address fills itself in.`

Also in Google Forms settings: **turn on "Collect email addresses → Verified"** *only if* you can guarantee the form is opened on the phone. If both desktop and phone traffic will exist, leave it **off** — a verified desktop-account stamp fighting a hand-typed phone address is worse than either alone.

---

### 1.2 Title

**RU:** `SplitCam Remote для Android — закрытое тестирование`
**EN:** `SplitCam Remote for Android — closed testing`

---

### 1.3 Intro

**RU:**
```
Одно поле. Ссылка придёт в течение суток.

Заполняйте с того самого Android-телефона, на который поставите Remote —
тогда нужный адрес можно скопировать, а не вспоминать.
```

**EN:**
```
One field. The link arrives within 24 hours.

Fill this in on the Android phone you'll install Remote on — then you can copy
the address you need instead of recalling it.
```

---

### 1.4 Fields

#### Field 1 — required

**Label RU:** `Аккаунт Google, в который вы вошли на Android-телефоне`
**Label EN:** `The Google account you're signed in to on your Android phone`

**Help RU:**
```
Возьмите телефон: Play Маркет -> аватарка справа сверху. Адрес под вашим именем —
его и вписывайте. Даже если обычно вы даёте другой. Google открывает доступ не
человеку, а конкретному аккаунту: любой другой адрес — и Play скажет
"приложение недоступно", а мы это со своей стороны починить не сможем.
Переписываете руками — буква в букву.
```

**Help EN:**
```
Pick up the phone: Play Store -> avatar, top right. The address under your name —
that's the one. Even if you'd normally give a different one. Google grants access
to an account, not to a person: any other address and Play says "app not
available", and there is nothing we can fix from our side. Typing it by hand? Copy
it character for character.
```

*Why no confirmation checkbox and no second "repeat the address" field:* a tickbox next to a label that already states the constraint just trains people to click past constraints, and it fires **after** the reflex has already filled the box. The label is 8px above the cursor and is the last thing read before typing — that's the only slot that works.

*Why the errand points at Play Маркет and not Настройки -> Google:* Settings shows the phone's **primary** account. Play gates on the account **selected in the Play Store**, which on a multi-account phone is frequently a different one. Sending a diligent tester to the wrong screen is worse than sending them nowhere.

#### Field 2 — optional

**Label RU:** `Для чего вы используете SplitCam? (необязательно, одна строка)`
**Label EN:** `What do you use SplitCam for? (optional, one line)`

**Help RU:** `Стримы на Twitch, созвоны, запись уроков, служба в церкви — как есть. По ответу мы поймём, какие кнопки должны быть у вас под большим пальцем, и о чём вас спросить дальше.`
**Help EN:** `Twitch streams, calls, recording lessons, a church service — as it is. It tells us which buttons belong under your thumb, and what to ask you about next.`

*Optional, so it can never block submit. It is the only field that pays the user back: it lets the follow-up name their actual scene instead of a generic one.*

**Everything else is cut.** Name, phone model, Android version: we'll be in a reply thread with these people anyway — diagnostics collected 24h before they're usable cost conversion at the exact top of a funnel that's already collapsing.

---

### 1.5 Confirmation message

**RU:**
```
Готово.

В течение суток живой человек впишет ваш адрес в список тестировщиков в Google
Play Console и пришлёт письмо со ссылкой. Автоматики тут нет — поэтому не мгновенно.

Дальше будет два нажатия: сначала "Стать тестировщиком", потом "Установить" в Play.
Само приложение не установится — это разные действия, и почти все останавливаются
на первом.

Три вещи, пока ждёте:

1. Добавьте splitcameramail@gmail.com в контакты. Письмо любит падать в "Промоакции".
2. Не ищите SplitCam Remote в Play прямо сейчас — вы его не найдёте, и это нормально:
   пока вас нет в списке, для вашего аккаунта приложения не существует.
3. Когда придёт ссылка, запустите SplitCam на компьютере, прежде чем открывать
   Remote. Это пульт — ему нужно чем управлять.

Ошиблись адресом? Отправьте форму ещё раз — возьмём последний.
Письма нет через сутки? Напишите на splitcameramail@gmail.com, тема "Remote — нет ссылки".
Скорее всего, в адресе опечатка, и без вас мы об этом не узнаем.
```

**EN:**
```
Done.

Within 24 hours a real person will type your address into the tester list in
Google Play Console and email you the link. There's no automation here — that's
why it isn't instant.

After that it's two taps: first "Become a tester", then "Install" in Play. The app
does not install itself — those are separate actions, and almost everyone stops
after the first one.

Three things while you wait:

1. Add splitcameramail@gmail.com to your contacts. The email likes to land in Promotions.
2. Don't go looking for SplitCam Remote in Play right now — you won't find it, and
   that's correct: until you're on the list, the app doesn't exist for your account.
3. When the link arrives, start SplitCam on your computer before you open Remote.
   It's a remote — it needs something to control.

Wrong address? Just submit the form again — we take the last one.
No email after 24 hours? Write to splitcameramail@gmail.com, subject "Remote — no link".
It's most likely a typo in the address, and we'll never know unless you tell us.
```

*The "submit again" line can't fire on its own — a typo'd address means the user never learns anything went wrong. That's what the support@ line is for: it triggers on **silence**, which is the moment the failure finally becomes observable to the user.*

---

## 2. The opt-in email

### Subject

**RU:** `SplitCam Remote: два нажатия с телефона — и приложение у вас`
**EN:** `SplitCam Remote: two taps on your phone and it's installed`

*Not "your link is ready". The link isn't the deliverable, the installed app is — and a subject selling a link is the first reinforcement of the exact confusion the body then spends four lines undoing.*

### Body — RU

```
Здравствуйте!

Ваш адрес в списке тестировщиков SplitCam Remote для Android. Доступ открыт именно
для этого адреса — того, на который пришло это письмо. Дальше пригодится.

Два нажатия, оба — на телефоне. Займёт минуты три.

Лучше всего сделать это, сидя за компьютером с запущенным SplitCam и с телефоном в
руке: тогда пять минут из шага 3 случатся сразу, а не "потом". Если вы сейчас не за
ним — поставьте письму звёздочку, оно понадобится ещё раз.

Читаете с компьютера? Ссылка отсюда не сработает — оба шага делаются на телефоне.
Откройте это письмо в почте на телефоне.

--------------------------------------------------
ШАГ 1. Откройте страницу теста
--------------------------------------------------

Ссылка: https://play.google.com/apps/testing/com.splitcam.remote

Нажмите "Стать тестировщиком".

Страница ответит: "Вы стали тестировщиком". Это ещё не установка. На первом шаге
ничего не устанавливается — вам выдали пропуск, но внутрь вы ещё не зашли.
Приложение появится на телефоне только после шага 2.

--------------------------------------------------
ШАГ 2. Установите приложение (тот самый шаг, который все пропускают)
--------------------------------------------------

На той же странице, сразу под подтверждением, появится ссылка "Скачайте приложение
в Google Play". Нажмите её, а на странице приложения — "Установить". Дождитесь,
пока кнопка не превратится в "Открыть". Вот теперь приложение у вас.

Потеряли ту страницу? Вот прямая ссылка на Remote в Play, ведёт туда же:
https://play.google.com/store/apps/details?id=com.splitcam.remote

Если ссылка открыла play.google.com в браузере, а не приложение Play — нажмите
"Открыть в приложении". Устанавливать надо из приложения Play.

Кнопка "Установить" неактивна или её нет? Закройте Play полностью и откройте
заново — пару минут он показывает старое состояние.

Play пишет "приложение недоступно" / "недоступно в вашей стране" / "разработчик не
выпустил приложение для вашего устройства"? Это не блокировка по стране и не
поломка, хотя выглядит один в один. Две причины, по порядку:

  1. Play ещё не догнал. Доступ появляется не мгновенно. Подождите 10-15 минут и
     обновите страницу.
  2. Не тот аккаунт. Play Маркет -> аватарка справа сверху -> адрес под вашим
     именем. Совпадает с адресом, на который пришло это письмо? Если нет — ответьте
     одной строкой: "не тот аккаунт, правильный: ___". Поправим за пару минут,
     заново ничего заполнять не надо.

--------------------------------------------------
ШАГ 3. Пять минут, ради которых всё затевалось
--------------------------------------------------

Сделайте это прямо сейчас, не откладывая до следующего эфира. Это правда минута.

  - SplitCam запущен на компьютере, телефон в той же сети Wi-Fi.
  - Откройте Remote — он сам найдёт компьютер. Нажмите на него.
  - Переключите сцену с телефона. Посмотрите на экран компьютера: картинка сменилась?
  - Теперь встаньте и отойдите в другой конец комнаты. С дивана, из кухни —
    откуда угодно. Переключите сцену обратно.
  - Уберите громкость любого слоя ползунком и верните.
  - Включите запись, подождите секунд десять, остановите. Проверьте, что файл на месте.

Если это работает из другого конца комнаты — приложение делает ровно то, ради чего
мы его написали: SplitCam больше не привязан к клавиатуре. На iPhone так уже год.
Теперь и у вас.

Remote не видит компьютер? Почти всегда дело в сети: телефон в гостевой сети, или
2.4 и 5 ГГц у роутера — это две разные сети, или Windows-брандмауэр не спросил
разрешения. Если за полминуты компьютер не появился — ответьте на письмо. Это само
по себе баг, и такой отчёт нам ценнее всего.

А в ближайшем настоящем эфире или созвоне возьмите пульт по-настоящему. Пять минут
на диване покажут, что кнопки нажимаются. Только реальный эфир покажет, куда тянется
большой палец, когда думать некогда.

И оставьте приложение на телефоне до релиза: Play засчитывает участие, только пока
оно установлено.

--------------------------------------------------
ОДНА СТРОЧКА ОТ ВАС
--------------------------------------------------

Ответьте на это письмо сегодня. Одной строки хватит, серьёзно: "работает, но
компьютер находится секунд десять" или "запись не включилась ни разу".

Самое ценное: что оказалось не там, где вы ждали, что искали и не нашли, и в какой
момент вы подумали "да ну, проще встать и нажать на компьютере". Последнее — лучшее,
что вы можете нам сказать. Ругать можно и нужно, мы за этим и позвали.

Денег за тестирование мы не платим — Google это прямо запрещает. Всё, что мы можем
предложить: вы получили Remote раньше всех и решаете, каким он выйдет. Пока
интерфейс не застыл, мы можем менять что угодно. После релиза так уже не получится.

Пожалуйста, не пропадайте молча. Если вы застряли и ничего не написали, для нас это
выглядит как "передумал человек" — и мы никогда не узнаем, что сломалось. Вас реально
мало, и каждый на счету.

Команда SplitCam
splitcameramail@gmail.com
```

### Body — EN

```
Hi,

Your address is on the tester list for SplitCam Remote for Android. Access is
granted to this exact address — the one this email arrived at. That matters later.

Two taps, both on the phone. About three minutes.

Best done sitting at your computer with SplitCam running and your phone in hand:
then the five minutes in step 3 happen now instead of "later". If you're not at it
right now, star this email — you'll need it again.

Reading this on a computer? The link won't work from here — both steps happen on
the phone. Open this email in your phone's mail app.

--------------------------------------------------
STEP 1. Open the test page
--------------------------------------------------

Link: https://play.google.com/apps/testing/com.splitcam.remote

Tap "Become a tester".

The page will answer: "You're a tester." That is not the install. Step 1 puts
nothing on your phone — you've been issued a pass, but you haven't walked in yet.
The app only lands on the phone after step 2.

--------------------------------------------------
STEP 2. Install the app (the step everyone skips)
--------------------------------------------------

On that same page, right under the confirmation, there's a link: "Download it on
Google Play". Tap it, then on the app page tap "Install". Wait until the button
turns into "Open". Now you actually have the app.

Lost that page? Here's the direct link to Remote in Play, same destination:
https://play.google.com/store/apps/details?id=com.splitcam.remote

If the link opened play.google.com in a browser rather than the Play app, tap
"Open in app". You need to install from the Play app.

Install greyed out or missing? Close Play completely and reopen it — it shows the
old state for a minute or two.

Play says "app not available" / "not available in your country" / "the developer
has not released this app for your device"? That is not a country block and not a
bug, even though it looks exactly like one. Two causes, in order:

  1. Play hasn't caught up. Access doesn't propagate instantly. Wait 10-15 minutes
     and refresh.
  2. Wrong account. Play Store -> avatar, top right -> the address under your name.
     Does it match the address this email arrived at? If not, reply with one line:
     "wrong account, the right one is ___". We'll fix it in a couple of minutes —
     you don't have to fill in anything again.

--------------------------------------------------
STEP 3. The five minutes this was all for
--------------------------------------------------

Do it now, not next stream. It genuinely takes a minute.

  - SplitCam running on the computer, phone on the same Wi-Fi.
  - Open Remote — it finds the computer on its own. Tap it.
  - Switch a scene from the phone. Look at the computer screen: did the picture change?
  - Now get up and walk to the other end of the room. Couch, kitchen, wherever.
    Switch it back.
  - Pull any layer's volume down with the slider, then back up.
  - Hit record, wait ten seconds, stop. Check the file is there.

If that works from across the room, the app is doing exactly what we built it for:
SplitCam isn't chained to the keyboard anymore. iPhone users have had this for a
year. Now it's yours.

Remote can't see the computer? It's nearly always the network: phone on a guest
network, or your router's 2.4 and 5 GHz are two separate networks, or the Windows
firewall never asked. If the computer hasn't appeared within thirty seconds, reply
to this email. That's a bug in itself, and it's the most valuable report we can get.

Then use it for real on your next actual stream or call. Five minutes on the couch
proves the buttons work. Only a real stream shows where your thumb reaches when
there's no time to think.

And leave it installed until release — Play only counts you while the app is on
the phone.

--------------------------------------------------
ONE LINE FROM YOU
--------------------------------------------------

Reply to this email today. One line is genuinely enough: "works, but finding my
computer takes ten seconds" or "recording never started".

Most valuable of all: what wasn't where you expected, what you looked for and
couldn't find, and the moment you thought "forget it, faster to walk over and click
it myself". That last one is the best thing you can tell us. Complaining is allowed
and encouraged — that's what we invited you for.

We don't pay for testing — Google flatly forbids it. All we can offer: you got
Remote before anyone else, and you decide what ships. While the interface hasn't
set, we can change anything. After release that stops being true.

Please don't drop out silently. If you get stuck and say nothing, it looks to us
like you changed your mind — and we never find out what broke. There really aren't
many of you, and every one counts.

The SplitCam team
splitcameramail@gmail.com
```

---

## 2b. Bonus (do not skip this one)

Play Console tells you who opted in and who never installed. That list is where 11 of your 12 people are sitting. One email is worth more than every word above.

**Send at +48h to opted-in-not-installed:**

**Subject RU:** `Вы в списке — но приложения на телефоне ещё нет (одно нажатие)`
**Subject EN:** `You're on the list — but the app isn't on your phone yet (one tap)`

**RU:**
```
Вы нажали "Стать тестировщиком" — спасибо. Но само приложение так и не
установилось: это отдельное нажатие, и его пропускают почти все.

С телефона: https://play.google.com/store/apps/details?id=com.splitcam.remote -> "Установить".

Не получается или Play пишет, что приложение недоступно? Ответьте одной строкой,
что видите на экране. Разберёмся.
```

**EN:**
```
You tapped "Become a tester" — thank you. But the app itself never installed: that's
a separate tap, and almost everyone skips it.

From your phone: https://play.google.com/store/apps/details?id=com.splitcam.remote -> "Install".

Not working, or Play says the app isn't available? Reply with one line about what's
on your screen. We'll sort it.
```

---

## 3. Notes on the decisions you might question

**The form is on the phone, and that's the actual anti-wrong-email mechanism.** Every prose defense — labels, warnings, checkboxes — is fighting Chrome's desktop autofill, which requires no reading at all: focus, tap, done. You cannot out-write a reflex that skips the text. Moving the form to the device that holds the ground truth means the wrong address stops being possible-but-discouraged and starts being awkward-to-produce. The QR is not decoration; it's the fix. Everything else is backup.

**One required field, and no confirmation checkbox.** A tickbox fires after the reflex has already filled the box, so honest people tick it without going back — it's rationalization, not verification. And a checkbox sitting next to a label that already states the constraint teaches people that constraints are things you click past. If you want a gate, the label *is* the gate: it's the last text read before typing.

**The label never says "email".** "Email" is a category people answer from muscle memory with their primary address. "The Google account you're signed in to on your Android phone" is a question about a device — there's no reflex answer, so they have to look. That's the whole trick.

**The errand says Play Маркет -> аватарка, not Настройки -> Google.** Settings shows the phone's primary account; Play gates on the account selected in the Play Store. On a phone with personal + work + one old account those differ often, and a tester who follows a wrong instruction perfectly then reads our email saying "you're on a different account" — which they'll correctly read as a lie.

**No "не уверены?" conditional.** The person who types their work address isn't uncertain. They're confidently wrong. A conditional hands exactly that person a free pass out of the one instruction that would've saved them. Hence the unconditional "Возьмите телефон" plus "Даже если обычно вы даёте другой" — the only sentence aimed at someone who already "knows" the answer.

**"App not available" gets two causes, propagation delay first.** Blaming the account single-cause is confidently wrong for anyone hitting Play's normal lag with a correct address — it tells them the only explanation is a mistake they know they didn't make, which converts a ten-minute wait into a permanent abandon plus blame. Wait-and-refresh costs one line and saves the users who did everything right.

**Step numbering is 1/2/3 and nothing else.** No "step 2 of 3" in the subject: an email labelled step 2 invites the reader to do it and wait for step 3 to arrive — which is the opt-in-mistaken-for-done failure, induced by the counter meant to prevent it.

**The completion signal is parked after install, never after opt-in.** "Вы стали тестировщиком" is Google's green success page, and it is the thing that kills this funnel. So we name the lie ("Страница ответит... Это ещё не установка"), and put our own "Вот теперь приложение у вас" on the far side of it, with a self-verifiable end state: the button says "Открыть".

**The session is "now", not "next time you go live".** A SplitCam user doesn't go live on demand — they go live Sunday. Install is today; a session booked for "whenever" is a session that never happens. So the email opens by asking them to read it at the desk with SplitCam running, and then cashes that immediately. The real stream is asked for *second*, as a return visit — that's two sessions from one email instead of one deferred maybe.

**Pairing is a step, not a footnote.** The most likely path to a dead install is: tap the icon, desktop is off or phone's on the guest SSID, nothing appears, app is "broken", app is closed — and per the brief, we never hear about it. Wrong-email at least throws a legible Play error. This one fails silently, so it gets the same treatment: preconditions stated, failure pre-diagnosed (guest network / 2.4 vs 5 GHz / firewall), reply path attached.

**"Поставьте эфир на паузу" is not in the checklist.** It's impossible unless they're actually live, and a five-minute list with an undoable item on it makes the whole list feel like it wasn't written by anyone who tried it.

**The 14-day line is there because Play counts continuous opt-in.** A tester who uses it once and uninstalls on day 3 zeroes their own streak and you find out never. One sentence now beats a second email in two weeks.

**No incentive language anywhere.** Stated once, plainly: we don't pay, Google forbids it, what you get is early access and influence. For someone who runs SplitCam daily, "tell us what annoys you and we fix it before release" is a real offer — and honesty about the absence of payment is itself the credibility.

**RU specifics:** "Аккаунт Google" (Google's own RU string on the screen we send them to), «буква в букву» not "символ в символ", «На первом шаге ничего не устанавливается» not the calqued «Первый шаг ничего не устанавливает», «приближает релиз» never «двигает релиз» (which means *postpone*), «Кнопки не там, где надо?» never «раскладка» (= keyboard layout), no gendered self-attestations, ё throughout. Straight ASCII quotes per constraint — note that a Russian reader would expect «ёлочки» here, so if these strings ever move somewhere the quoting rule doesn't apply, swap them.
