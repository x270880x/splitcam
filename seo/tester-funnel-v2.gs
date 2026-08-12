/**
 * SplitCam Remote — Android closed-testing tester funnel (semi-auto, 35 locales).
 * Bound to the Form-responses Google Sheet (Extensions -> Apps Script from that Sheet).
 *
 * WHY SEMI and not full auto: the Play Developer API (edits.testers) only manages Google
 * GROUPS, never individual emails / "email lists" ("email lists are not supported by this
 * resource"). Consumer Gmail groups have no member-add API. So adding a signup to the
 * Console tester list is inherently manual on this setup. Everything else is automated.
 *
 * FLOW
 *   1. Someone submits one of the 35 localized forms -> a row appends to THAT form's tab.
 *   2. You add their Google account to the Play Console closed-test list (manual, batch).
 *   3. You TICK the "Added to Console" checkbox on their row(s), on any tab.
 *   4. Menu: SplitCam -> "Send opt-in link to ticked rows" -> emails each of them the
 *      opt-in link IN THE LANGUAGE OF THE FORM THEY SIGNED UP THROUGH, and stamps
 *      "Link sent".
 *   +  A daily 13:00 email digest reports how many people submitted, across all tabs.
 *
 * The opt-in link only works AFTER the address is on a tester list, which is exactly why
 * the link goes out on YOUR tick, not on form submit (sending earlier = "app not available").
 *
 * SETUP (once): open this Sheet -> Extensions -> Apps Script -> paste this file -> Save.
 * Reload the Sheet. Run SplitCam -> "Set up sheet (add columns)" and approve the one-time
 * Google authorization (Gmail send + Sheets). Then SplitCam -> "Enable daily 13:00 report".
 * Consumer-Gmail mail quota is ~100 recipients/day.
 * If the report fires at the wrong local time, set the timezone in File -> Project Settings.
 *
 * SENDING FROM support@splitcam.com
 *   Apps Script always sends as the Google account that owns the script, and support@ is a
 *   mailbox on our own DirectAdmin server, not a Google account. The only way to make Gmail
 *   put it in the From: header is to register it as a verified "Send mail as" alias:
 *     Gmail (owner account) -> Settings -> Accounts and Import -> "Send mail as" ->
 *     Add another email address:
 *         Name:     SplitCam
 *         Address:  support@splitcam.com
 *         [x] Treat as an alias
 *     Next -> SMTP of our own server:
 *         SMTP server: mail.splitcam.com     Port: 465     SSL
 *         Username:    support@splitcam.com  Password: the mailbox password (DirectAdmin)
 *     Google mails a confirmation code to support@splitcam.com — read it in webmail and
 *     confirm. After that GmailApp.getAliases() lists it and this script uses it.
 *   Run SplitCam -> "Check sender address" to verify. It refuses to guess: with no alias
 *   the send is blocked rather than quietly going out from someone's personal Gmail.
 */

var OPT_IN_URL   = 'https://play.google.com/apps/testing/com.splitcam.remote';
var PLAY_LISTING = 'https://play.google.com/store/apps/details?id=com.splitcam.remote';
var SENDER       = 'support@splitcam.com';       // must be the owner OR a verified alias
var REPLY_TO     = 'support@splitcam.com';       // where tester feedback lands
var REPORT_TO    = 'splitcameramail@gmail.com';  // daily digest to the owner
var FROM_NAME    = 'SplitCam';
var ADDED_HEADER = 'Added to Console';
var SENT_HEADER  = 'Link sent';
var LOCALE_HEADER = 'Locale';                     // filled in automatically, for your eyes
var FORM_URLS_SHEET = 'FORM URLS';                // written by seo/make-tester-forms.gs

//<!--COPY-->
// Generated block — DO NOT EDIT HERE. Edit seo/tester-email-i18n.json and rerun
// `python3 seo/build_tester_funnel.py`. Everything between the COPY markers is
// overwritten by that script.
var COPY = {};
var LABEL_TO_LOCALE = {};
//<!--/COPY-->

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('SplitCam')
    .addItem('Send opt-in link to ticked rows', 'sendOptInToTicked')
    .addSeparator()
    .addItem('Set up sheet (add columns)', 'setupSheet')
    .addItem('Check sender address', 'checkSender')
    .addItem('Preview one email', 'previewEmail')
    .addSeparator()
    .addItem('Enable daily 13:00 report', 'installDailyTrigger')
    .addItem('Send report now (test)', 'dailyDigest')
    .addToUi();
}

/* ------------------------------------------------------------------ sender */

/**
 * Which address will the mail come from, and can we force it?
 * Returns {mode:'owner'|'alias'|'blocked', from:string, effective:string}
 */
function senderState_() {
  var effective = Session.getEffectiveUser().getEmail();
  if (effective && effective.toLowerCase() === SENDER.toLowerCase()) {
    return { mode: 'owner', from: '', effective: effective };
  }
  var aliases = [];
  try { aliases = GmailApp.getAliases(); } catch (e) { aliases = []; }
  for (var i = 0; i < aliases.length; i++) {
    if (String(aliases[i]).toLowerCase() === SENDER.toLowerCase()) {
      return { mode: 'alias', from: aliases[i], effective: effective };
    }
  }
  return { mode: 'blocked', from: '', effective: effective };
}

function checkSender() {
  var s = senderState_();
  var ui = SpreadsheetApp.getUi();
  if (s.mode === 'owner') {
    ui.alert('OK. Mail goes out as ' + SENDER + ' (this script is owned by that account).');
  } else if (s.mode === 'alias') {
    ui.alert('OK. Mail goes out as ' + SENDER + ' via a verified Gmail alias on ' +
             s.effective + '.');
  } else {
    ui.alert('BLOCKED — mail would go out as ' + s.effective + ', not ' + SENDER + '.\n\n' +
             'Fix one of these, then re-check:\n' +
             '  a) move this script to the ' + SENDER + ' account, or\n' +
             '  b) in ' + s.effective + ' Gmail: Settings -> Accounts -> "Send mail as" ->\n' +
             '     add ' + SENDER + ' and confirm the verification mail.\n\n' +
             'Sending is disabled until then, so nothing goes out from the wrong address.');
  }
}

/* ------------------------------------------------------- locale of a tab */

/** Every tab that a Google Form writes into. */
function responseSheets_() {
  var out = [];
  var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
  for (var i = 0; i < sheets.length; i++) {
    var name = sheets[i].getName();
    if (name === FORM_URLS_SHEET) continue;
    var url = null;
    try { url = sheets[i].getFormUrl(); } catch (e) { url = null; }
    if (url) out.push(sheets[i]);
    else if (/^form responses/i.test(name)) out.push(sheets[i]);
  }
  return out;
}

/** Long id-ish tokens in a Forms URL. Published and edit URLs carry DIFFERENT ids. */
function formIds_(url) {
  var ids = String(url || '').match(/[A-Za-z0-9_-]{20,}/g);
  return ids || [];
}

/**
 * locale -> ids, from the FORM URLS sheet that make-tester-forms.gs wrote
 * (col A locale, col B published URL, col C edit URL).
 */
function localeIndex_() {
  var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(FORM_URLS_SHEET);
  var map = {};   // id -> locale
  if (!sh) return map;
  var rows = sh.getDataRange().getValues();
  for (var r = 1; r < rows.length; r++) {
    var loc = String(rows[r][0] || '').trim();
    if (!loc) continue;
    var ids = formIds_(rows[r][1]).concat(formIds_(rows[r][2]));
    for (var i = 0; i < ids.length; i++) map[ids[i]] = loc;
  }
  return map;
}

/** The locale of one response tab, or '' when it cannot be established. */
function sheetLocale_(sh, index) {
  var url = null;
  try { url = sh.getFormUrl(); } catch (e) { url = null; }
  var ids = formIds_(url);
  for (var i = 0; i < ids.length; i++) {
    if (index[ids[i]]) return index[ids[i]];
  }
  // Fallback: the question label is localized, so it fingerprints the form.
  var header = String(sh.getRange(1, 2).getValue() || '').trim();
  if (header && LABEL_TO_LOCALE[header]) return LABEL_TO_LOCALE[header];
  return '';
}

/** Copy for a locale, falling back to English. */
function copyFor_(locale) {
  return COPY[locale] || COPY.EN;
}

/* --------------------------------------------------------------- the sheet */

/** Appends `name` to the header row if missing. Returns its 1-based column. */
function ensureColumn_(sh, headers, name) {
  var i = headers.indexOf(name);
  if (i === -1) {
    headers.push(name);
    sh.getRange(1, headers.length).setValue(name);
    i = headers.length - 1;
  }
  return i + 1;
}

/** Adds "Added to Console" / "Link sent" / "Locale" to EVERY response tab. */
function setupSheet() {
  var sheets = responseSheets_();
  var index = localeIndex_();
  var touched = 0, unknown = [];
  for (var s = 0; s < sheets.length; s++) {
    var sh = sheets[s];
    var lastCol = Math.max(sh.getLastColumn(), 1);
    var headers = sh.getRange(1, 1, 1, lastCol).getValues()[0];
    var addedCol = ensureColumn_(sh, headers, ADDED_HEADER);
    ensureColumn_(sh, headers, SENT_HEADER);
    var locCol = ensureColumn_(sh, headers, LOCALE_HEADER);
    var lastRow = Math.max(sh.getLastRow(), 2);
    sh.getRange(2, addedCol, lastRow - 1, 1).insertCheckboxes();
    var loc = sheetLocale_(sh, index);
    sh.getRange(1, locCol).setNote(loc ? 'detected locale: ' + loc : 'LOCALE NOT DETECTED');
    if (!loc) unknown.push(sh.getName());
    touched++;
  }
  var msg = 'Ready. Prepared ' + touched + ' response tab(s).\n\n' +
            'When you have added someone to the Play Console list, tick "' + ADDED_HEADER +
            '" on their row (any tab), then run SplitCam -> "Send opt-in link to ticked rows".';
  if (unknown.length) {
    msg += '\n\nLocale NOT detected on: ' + unknown.join(', ') +
           '\nThose rows would get the English email. Check the "' + FORM_URLS_SHEET +
           '" sheet still lists every form.';
  }
  SpreadsheetApp.getUi().alert(msg);
}

/** Column holding the typed Google account. These forms are one-question: column B. */
function findEmailColumn_(headers) {
  for (var i = 0; i < headers.length; i++) {
    if (/Google account|Аккаунт Google/i.test(String(headers[i]))) return i;
  }
  return 1; // column B, the single question on every localized form
}

/* ----------------------------------------------------------------- sending */

function sendOptInToTicked() {
  var ui = SpreadsheetApp.getUi();
  var sender = senderState_();
  if (sender.mode === 'blocked') { checkSender(); return; }

  var index = localeIndex_();
  var sheets = responseSheets_();
  var quota = MailApp.getRemainingDailyQuota();
  var sent = 0, skipped = 0, hitQuota = false, byLocale = {};

  for (var s = 0; s < sheets.length && !hitQuota; s++) {
    var sh = sheets[s];
    var data = sh.getDataRange().getValues();
    if (data.length < 2) continue;
    var headers = data[0];
    var emailC = findEmailColumn_(headers);
    var addedC = headers.indexOf(ADDED_HEADER);
    var sentC = headers.indexOf(SENT_HEADER);
    if (addedC === -1 || sentC === -1) { continue; }   // tab not set up yet
    var locale = sheetLocale_(sh, index) || 'EN';
    var c = copyFor_(locale);

    for (var r = 1; r < data.length; r++) {
      var row = data[r];
      if (row[addedC] !== true) continue;
      if (String(row[sentC] || '').length > 0) continue;
      var email = String(row[emailC] || '').trim();
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { skipped++; continue; }
      if (sent >= quota) { hitQuota = true; break; }
      var opts = { name: FROM_NAME, replyTo: REPLY_TO };
      if (sender.mode === 'alias') opts.from = sender.from;
      GmailApp.sendEmail(email, c.subject, c.body, opts);
      sh.getRange(r + 1, sentC + 1).setValue(new Date());
      byLocale[locale] = (byLocale[locale] || 0) + 1;
      sent++;
    }
  }

  var breakdown = Object.keys(byLocale).sort().map(function (k) {
    return '  ' + k + ': ' + byLocale[k];
  }).join('\n');
  var msg = 'Отправлено ссылок: ' + sent + '. Пропущено (плохой email): ' + skipped +
            '. Остаток квоты на сегодня: ' + (quota - sent) + '.';
  if (breakdown) msg += '\n\nПо языкам:\n' + breakdown;
  if (hitQuota) msg += '\n\nДневная квота исчерпана — остальные уйдут завтра.';
  SpreadsheetApp.getUi().alert(msg);
}

/** Shows the exact mail one locale would receive — read it before the first real send. */
function previewEmail() {
  var ui = SpreadsheetApp.getUi();
  var res = ui.prompt('Preview', 'Locale code (EN, ru, de, ja, ...):', ui.ButtonSet.OK_CANCEL);
  if (res.getSelectedButton() !== ui.Button.OK) return;
  var loc = res.getResponseText().trim();
  var c = COPY[loc];
  if (!c) { ui.alert('No copy for "' + loc + '". Known: ' + Object.keys(COPY).join(' ')); return; }
  ui.alert(loc + '\n\nSubject: ' + c.subject + '\n\n' + c.body);
}

/* ------------------------------------------------------------------ digest */

function installDailyTrigger() {
  var existing = ScriptApp.getProjectTriggers();
  for (var i = 0; i < existing.length; i++) {
    if (existing[i].getHandlerFunction() === 'dailyDigest') ScriptApp.deleteTrigger(existing[i]);
  }
  ScriptApp.newTrigger('dailyDigest').timeBased().everyDays(1).atHour(13).create();
  SpreadsheetApp.getUi().alert(
    'Готово. Сводка будет приходить на ' + REPORT_TO + ' каждый день около 13:00 (часовой пояс — ' +
    Session.getScriptTimeZone() + '; поменять: File -> Project Settings).');
}

/** Daily digest across ALL localized tabs. */
function dailyDigest() {
  var index = localeIndex_();
  var sheets = responseSheets_();
  var now = new Date();
  var last24 = new Date(now.getTime() - 24 * 60 * 60 * 1000);
  var total = 0, newLast24 = 0, awaitingAdd = 0, linkSent = 0, perLocale = {};

  for (var s = 0; s < sheets.length; s++) {
    var sh = sheets[s];
    var data = sh.getDataRange().getValues();
    if (data.length < 2) continue;
    var headers = data[0];
    var addedC = headers.indexOf(ADDED_HEADER);
    var sentC = headers.indexOf(SENT_HEADER);
    var locale = sheetLocale_(sh, index) || '??';
    for (var r = 1; r < data.length; r++) {
      var row = data[r];
      if (!String(row[0] || '').length && !String(row[1] || '').length) continue;
      total++;
      perLocale[locale] = (perLocale[locale] || 0) + 1;
      var ts = row[0];
      if (ts instanceof Date && ts >= last24) newLast24++;
      if (addedC !== -1 && row[addedC] !== true) awaitingAdd++;
      if (sentC !== -1 && String(row[sentC] || '').length > 0) linkSent++;
    }
  }

  var tz = Session.getScriptTimeZone();
  var stamp = Utilities.formatDate(now, tz, 'dd.MM.yyyy HH:mm');
  var url = SpreadsheetApp.getActiveSpreadsheet().getUrl();
  var lines = [
    'SplitCam Remote — заявки в тестеры, сводка на ' + stamp,
    '',
    'Новых заявок за 24 часа: ' + newLast24,
    'Всего заявок с форм:     ' + total,
    'Ждут добавления в Console: ' + awaitingAdd,
    'Ссылка уже отправлена:     ' + linkSent,
    ''
  ];
  var locs = Object.keys(perLocale).sort(function (a, b) { return perLocale[b] - perLocale[a]; });
  if (locs.length) {
    lines.push('По языкам: ' + locs.map(function (k) { return k + ' ' + perLocale[k]; }).join(', '));
    lines.push('');
  }
  lines.push('Это только данные ФОРМ (кто подал запрос). Сколько opted-in / установили —');
  lines.push('смотреть в Play Console вручную, туда API нет.');
  lines.push('');
  lines.push('Таблица: ' + url);

  MailApp.sendEmail({
    to: REPORT_TO, replyTo: REPORT_TO, name: FROM_NAME,
    subject: 'SplitCam Remote — заявок за сутки: ' + newLast24 + ' (всего ' + total + ')',
    body: lines.join('\n')
  });
}
