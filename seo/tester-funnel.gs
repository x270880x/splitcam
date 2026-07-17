/**
 * SplitCam Remote — Android closed-testing tester funnel (semi-auto).
 * Bound to the Form-responses Google Sheet (Extensions -> Apps Script from that Sheet).
 *
 * WHY SEMI and not full auto: the Play Developer API (edits.testers) only manages Google
 * GROUPS, never individual emails / "email lists" ("email lists are not supported by this
 * resource"). Consumer Gmail groups have no member-add API. So adding a signup to the
 * Console tester list is inherently manual on this setup. Everything else is automated.
 *
 * FLOW
 *   1. Someone submits the form  -> a row auto-appends here (Form link) and you get the
 *      built-in "new response" email (Responses tab -> 3-dot -> Get email notifications).
 *   2. You add their Google account to the Play Console closed-test list (manual, batch).
 *   3. You TICK the "Added to Console" checkbox on their row(s).
 *   4. Menu: SplitCam -> "Send opt-in link to ticked rows"  -> emails them the opt-in link
 *      and stamps "Link sent".
 *
 * The opt-in link only works AFTER the address is on a tester list, which is exactly why
 * the link goes out on YOUR tick, not on form submit (sending earlier = "app not available").
 *
 * SETUP (once): open this Sheet -> Extensions -> Apps Script -> paste this file -> Save.
 * Back in the Sheet, reload; run SplitCam -> "Set up sheet (add columns)" and approve the
 * one-time Google authorization (Gmail send + Sheets). Consumer-Gmail mail quota is
 * ~100 recipients/day (plenty for a 12-tester test).
 */

var OPT_IN_URL   = 'https://play.google.com/apps/testing/com.splitcam.remote';
var PLAY_LISTING = 'https://play.google.com/store/apps/details?id=com.splitcam.remote';
var REPLY_TO     = 'splitcameramail@gmail.com';
var FROM_NAME    = 'SplitCam';
var ADDED_HEADER = 'Added to Console';
var SENT_HEADER  = 'Link sent';

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('SplitCam')
    .addItem('Send opt-in link to ticked rows', 'sendOptInToTicked')
    .addSeparator()
    .addItem('Set up sheet (add columns)', 'setupSheet')
    .addToUi();
}

/** Adds the "Added to Console" checkbox column and the "Link sent" column if missing. */
function setupSheet() {
  var sh = SpreadsheetApp.getActiveSheet();
  var lastCol = Math.max(sh.getLastColumn(), 1);
  var headers = sh.getRange(1, 1, 1, lastCol).getValues()[0];
  function ensure(name) {
    var i = headers.indexOf(name);
    if (i === -1) {
      lastCol += 1;
      sh.getRange(1, lastCol).setValue(name);
      headers.push(name);
      i = headers.length - 1;
    }
    return i + 1; // 1-based column
  }
  var addedCol = ensure(ADDED_HEADER);
  ensure(SENT_HEADER);
  var lastRow = Math.max(sh.getLastRow(), 2);
  sh.getRange(2, addedCol, lastRow - 1, 1).insertCheckboxes();
  SpreadsheetApp.getUi().alert(
    'Ready. When you have added someone to the Play Console list, tick "' + ADDED_HEADER +
    '" on their row, then run SplitCam -> "Send opt-in link to ticked rows".');
}

/** First column whose header names the Google-account question. */
function findEmailColumn_(headers) {
  for (var i = 0; i < headers.length; i++) {
    if (/Google account|Аккаунт Google/i.test(String(headers[i]))) return i;
  }
  return 1; // fallback: column B (right after Timestamp)
}

function sendOptInToTicked() {
  var ui = SpreadsheetApp.getUi();
  var sh = SpreadsheetApp.getActiveSheet();
  var data = sh.getDataRange().getValues();
  var headers = data[0];
  var emailC = findEmailColumn_(headers);
  var addedC = headers.indexOf(ADDED_HEADER);
  var sentC = headers.indexOf(SENT_HEADER);
  if (addedC === -1 || sentC === -1) { ui.alert('Run "Set up sheet (add columns)" first.'); return; }

  var quota = MailApp.getRemainingDailyQuota();
  var sent = 0, skipped = 0, hitQuota = false;
  for (var r = 1; r < data.length; r++) {
    var row = data[r];
    var ticked = row[addedC] === true;
    var already = String(row[sentC] || '').length > 0;
    var email = String(row[emailC] || '').trim();
    if (!ticked || already) continue;
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { skipped++; continue; }
    if (sent >= quota) { hitQuota = true; break; }
    MailApp.sendEmail({
      to: email, replyTo: REPLY_TO, name: FROM_NAME,
      subject: 'SplitCam Remote: два нажатия с телефона — и приложение у вас',
      body: buildBody_(email)
    });
    sh.getRange(r + 1, sentC + 1).setValue(new Date());
    sent++;
  }
  var msg = 'Отправлено ссылок: ' + sent + '. Пропущено (плохой email): ' + skipped +
            '. Остаток квоты на сегодня: ' + (quota - sent) + '.';
  if (hitQuota) msg += '\n\nДневная квота исчерпана — остальные уйдут завтра.';
  ui.alert(msg);
}

/** Bilingual opt-in email (RU first, EN below). */
function buildBody_(email) {
  return [
    'Здравствуйте!',
    '',
    'Ваш адрес (' + email + ') в списке тестировщиков SplitCam Remote для Android.',
    'Два нажатия, оба — на телефоне. Займёт минуты три.',
    '',
    'ШАГ 1 — откройте страницу теста (на телефоне, где вошли именно в этот аккаунт):',
    OPT_IN_URL,
    'Нажмите «Стать тестировщиком». Страница ответит «Вы стали тестировщиком» — это ЕЩЁ НЕ установка.',
    '',
    'ШАГ 2 — установите (тот самый шаг, который все пропускают):',
    'На той же странице нажмите ссылку на Google Play, затем «Установить». Прямая ссылка:',
    PLAY_LISTING,
    'Если Play пишет «приложение недоступно» — подождите 10–15 минут (доступ ещё расходится)',
    'и проверьте, что в Play Маркете выбран ИМЕННО этот аккаунт.',
    '',
    'ШАГ 3 — попробуйте один раз по-настоящему: запустите SplitCam на компьютере, откройте',
    'Remote, спаритесь по той же Wi-Fi, переключите сцену из другого конца комнаты. Ответьте',
    'на это письмо — напишите, что сломалось. Это нам ценнее всего.',
    '',
    'Пожалуйста, не удаляйте приложение до релиза — Play засчитывает участие, только пока оно установлено.',
    '',
    '— — —',
    '',
    'Hi,',
    '',
    'Your address (' + email + ') is on the tester list for SplitCam Remote for Android.',
    'Two taps, both on the phone. About three minutes.',
    '',
    'STEP 1 — open the test page (on the phone signed in to THIS account):',
    OPT_IN_URL,
    'Tap "Become a tester". The page says "You\'re a tester" — that is NOT the install.',
    '',
    'STEP 2 — install (the step everyone skips):',
    'On that same page tap the Google Play link, then "Install". Direct link:',
    PLAY_LISTING,
    'If Play says "app not available", wait 10-15 min (access is still propagating) and make',
    'sure the Play Store is on THIS account.',
    '',
    'STEP 3 — use it once for real: run SplitCam on your PC, open Remote, pair over the same',
    'Wi-Fi, switch a scene from across the room. Reply with anything that broke.',
    '',
    'Please keep it installed until launch — Play only counts you while it is installed.',
    '',
    '— SplitCam',
    ''
  ].join('\n');
}
