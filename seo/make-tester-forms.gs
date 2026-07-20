/**
 * Creates ONE minimal tester-signup form per locale (35 total) and points them all at a
 * SINGLE spreadsheet, so every signup still lands in one place (one tab per locale).
 *
 * WHY per-locale forms: the "Become a tester" button lives on 35 localized pages. A German
 * or Japanese visitor used to land on a RU/EN form at the very last step — exactly where
 * people drop off. The load-bearing string is HELP: it must be unmistakable, in the reader's
 * own language, that the address has to be the Google account signed in on their ANDROID
 * PHONE. Any other address and the Play opt-in link answers "app not available", and the
 * person concludes our app is broken.
 *
 * HOW TO RUN (once):
 *   1. Open the responses spreadsheet -> Extensions -> Apps Script.
 *   2. Paste this file as a new script file (or replace Code.gs), Save.
 *   3. Run `createAllForms`. Approve the one-time Google authorization.
 *   4. Read the log (View -> Logs) or the "FORM URLS" sheet it writes: 35 locale -> URL rows.
 *      Hand those URLs back to Claude to wire each locale's button and strip.
 *
 * Re-running is safe-ish but NOT idempotent: it creates NEW forms every time. If you need to
 * redo it, delete the previously created forms from Drive first, or you will end up with
 * duplicates competing for the same button.
 */

// The spreadsheet every form writes into (the existing tester-signup responses sheet).
var DEST_SPREADSHEET_ID = '1qEGIHXiwP0od9o8RXmZ_VGQ6ObeFszZBOMDOJttfm5o';

// Filled from the translation pass. EN first, then the 34 locales.
// title / desc / label / help / confirm
var COPY = {
  EN: {
    title: 'SplitCam Remote — Android test',
    desc: 'SplitCam Remote runs your SplitCam stream from your phone. Sign up to test it.',
    label: 'Your e-mail',
    help: 'The one on your Android phone (Play Store -> avatar)',
    confirm: 'Done. We will email you the link within 24 hours. Then it is two taps: Become a tester, then Install.'
  },
  ru: { title: "SplitCam Remote — тест Android-версии", desc: "Управляйте стримом SplitCam прямо с телефона. Запишитесь в тестировщики.", label: "Ваш e-mail", help: "Адрес Google-аккаунта, под которым вы вошли на Android-телефоне (Google Play -> аватар) — другой не подойдёт.", confirm: "Готово. Ссылку пришлём на почту в течение 24 часов. Дальше два нажатия: Стать тестировщиком, затем Установить." },
  es: { title: "SplitCam Remote — prueba para Android", desc: "Con SplitCam Remote controlas tu directo desde el teléfono. Apúntate a la prueba.", label: "Tu correo", help: "Tiene que ser la cuenta de Google de tu teléfono Android (Play Store -> tu avatar)", confirm: "Listo. Te enviaremos el enlace por correo en menos de 24 horas. Luego son dos toques: Convertirme en tester e Instalar." },
  de: { title: "SplitCam Remote — Android-Test", desc: "SplitCam Remote steuert deinen Stream vom Handy aus. Melde dich an und teste mit.", label: "Deine E-Mail-Adresse", help: "Muss das Google-Konto von deinem Android-Handy sein, keine andere E-Mail (Play Store -> Profilbild).", confirm: "Fertig. Den Link bekommst du innerhalb von 24 Stunden per E-Mail. Danach nur noch zweimal tippen: Tester werden, dann Installieren." },
  fr: { title: "SplitCam Remote — test Android", desc: "SplitCam Remote pilote votre stream depuis votre téléphone. Inscrivez-vous pour le tester.", label: "Votre e-mail", help: "L'e-mail du compte Google connecté sur votre téléphone Android (Play Store -> photo de profil)", confirm: "C'est noté. Vous recevrez le lien par e-mail sous 24 h. Ensuite, il suffit d'appuyer sur Devenir testeur, puis Installer." },
  pt: { title: "SplitCam Remote — teste para Android", desc: "O SplitCam Remote controla sua transmissão do SplitCam pelo celular. Inscreva-se para testar.", label: "Seu e-mail", help: "Use a conta Google conectada no seu celular Android (Play Store -> foto do perfil)", confirm: "Pronto. Enviaremos o link por e-mail em até 24 horas. Depois são só dois toques: Tornar-se testador e Instalar." },
  tr: { title: "SplitCam Remote — Android testi", desc: "SplitCam Remote ile yayınınızı telefonunuzdan yönetin. Test etmek için kaydolun.", label: "E-posta adresiniz", help: "Android telefonunuzda oturum açtığınız Google hesabı (Play Store -> profil resmi); başka bir adres çalışmaz.", confirm: "Tamamdır. Bağlantıyı 24 saat içinde e-postayla göndereceğiz. Sonrası iki dokunuş: Test kullanıcısı ol, ardından Yükle." },
  fil: { title: "SplitCam Remote — pagsubok sa Android", desc: "Kontrolin ang SplitCam stream mo mula sa phone. Mag-sign up para masubukan ito.", label: "Email mo", help: "Dapat ang Google account na naka-sign in sa Android phone mo (Play Store -> avatar) — hindi ang ibang email mo.", confirm: "Tapos na. Ipapadala namin ang link sa loob ng 24 oras. Dalawang tap na lang: Maging tester, tapos I-install." },
  uk: { title: "SplitCam Remote — тестування на Android", desc: "SplitCam Remote керує вашою трансляцією прямо з телефона. Запишіться на тестування.", label: "Ваш e-mail", help: "Саме той Google-акаунт, у який ви увійшли на телефоні Android (Google Play -> аватар) — інша пошта не спрацює.", confirm: "Готово. Надішлемо посилання на пошту протягом 24 годин. Далі — два натискання: Стати тестувальником, потім Встановити." },
  it: { title: "SplitCam Remote — test su Android", desc: "SplitCam Remote controlla la tua diretta dal telefono. Iscriviti per provarlo.", label: "La tua email", help: "Deve essere l'account Google del Play Store sul tuo telefono Android (tocca la foto del profilo), non un'altra email.", confirm: "Fatto. Ti inviamo il link entro 24 ore. Poi bastano due tocchi: Diventa un tester e Installa." },
  vi: { title: "SplitCam Remote — thử nghiệm trên Android", desc: "SplitCam Remote giúp bạn điều khiển buổi stream ngay từ điện thoại. Đăng ký để dùng thử.", label: "Email của bạn", help: "Phải đúng tài khoản Google đang đăng nhập trên điện thoại Android của bạn (Play Store -> ảnh đại diện); email khác sẽ không cài được ứng dụng.", confirm: "Xong! Trong vòng 24 giờ chúng tôi sẽ gửi link qua email. Sau đó chỉ hai bước: bấm Trở thành người thử nghiệm, rồi Cài đặt." },
  id: { title: "SplitCam Remote — uji coba Android", desc: "SplitCam Remote mengontrol stream SplitCam kamu dari HP. Daftar jadi penguji.", label: "Email kamu", help: "Wajib akun Google yang login di HP Android kamu (cek: Play Store -> ketuk foto profil) — email lain tidak akan bisa dipakai.", confirm: "Selesai. Kami kirim link ke email kamu dalam 24 jam. Setelah itu tinggal dua kali ketuk: Jadi penguji, lalu Instal." },
  nl: { title: "SplitCam Remote — Android-test", desc: "Met SplitCam Remote bedien je je stream vanaf je telefoon. Meld je aan om mee te testen.", label: "Je e-mailadres", help: "Het Google-account op je Android-telefoon, niet je gewone e-mailadres (Play Store -> avatar)", confirm: "Gelukt. Je krijgt de link binnen 24 uur per e-mail. Daarna is het twee tikken: 'Tester worden', dan 'Installeren'." },
  ro: { title: "SplitCam Remote — testare pe Android", desc: "Cu SplitCam Remote îți controlezi streamul de pe telefon. Înscrie-te ca să-l testezi.", label: "E-mailul tău", help: "Contul Google cu care ești conectat pe telefonul Android (Play Store -> avatar) — cu alt e-mail nu merge.", confirm: "Gata. Îți trimitem linkul pe e-mail în cel mult 24 de ore. Apoi doar două apăsări: Deveniți tester și Instalați." },
  hi: { title: "SplitCam Remote — Android टेस्ट", desc: "SplitCam Remote आपके फ़ोन से आपकी SplitCam स्ट्रीम चलाता है। टेस्ट करने के लिए साइन अप करें।", label: "आपका ईमेल", help: "वही Google खाता जो आपके Android फ़ोन के Play Store में साइन इन है (Play Store → ऊपर प्रोफ़ाइल फ़ोटो) — दूसरा ईमेल दिया तो ऐक्सेस नहीं मिलेगा।", confirm: "हो गया। 24 घंटे के अंदर हम आपको ईमेल पर लिंक भेज देंगे। फिर बस दो टैप: टेस्टर बनें और इंस्टॉल करें।" },
  ja: { title: "SplitCam Remote — Android テスター募集", desc: "SplitCam Remote を使えば、PC の SplitCam 配信をスマホから操作できます。テストにご参加ください。", label: "メールアドレス", help: "Android スマホで実際に使っている Google アカウント（Play ストア → 右上のアイコンで確認）。別のアドレスでは参加できません。", confirm: "登録を受け付けました。24時間以内に招待リンクをメールでお送りします。あとは「テスターになる」→「インストール」の2タップだけです。" },
  ms: { title: "SplitCam Remote — ujian Android", desc: "SplitCam Remote mengawal siaran SplitCam anda terus dari telefon. Daftar untuk mengujinya.", label: "E-mel anda", help: "Guna e-mel akaun Google yang log masuk pada telefon Android anda (Play Store -> avatar) — akaun lain tidak akan dapat akses.", confirm: "Selesai. Kami akan menghantar pautan melalui e-mel dalam masa 24 jam. Selepas itu dua ketikan sahaja: 'Jadi penguji', kemudian 'Pasang'." },
  bg: { title: "SplitCam Remote — тест за Android", desc: "SplitCam Remote управлява стрийма ви в SplitCam от телефона. Запишете се, за да го тествате.", label: "Вашият имейл", help: "Google акаунтът, с който сте влезли в Google Play на Android телефона си (докоснете профилната снимка). Друг адрес няма да работи.", confirm: "Готово. До 24 часа ще получите линка по имейл. После са само две докосвания: Станете тестер, след това Инсталиране." },
  ar: { title: "SplitCam Remote — اختبار نسخة Android", desc: "SplitCam Remote يتيح لك التحكّم في بثّ SplitCam من هاتفك. سجّل لتجربته.", label: "بريدك الإلكتروني", help: "بريد حساب Google الذي تسجّل الدخول به على هاتف Android (متجر Play ← صورة حسابك) — أي بريد آخر لن يعمل.", confirm: "تمّ. سنرسل الرابط إلى بريدك خلال 24 ساعة. بعدها نقرتان: الانضمام كمُختبِر ثم تثبيت." },
  ko: { title: "SplitCam Remote — Android 테스터 모집", desc: "SplitCam Remote는 휴대폰으로 PC의 SplitCam 방송을 제어하는 앱입니다. 테스트에 참여하려면 신청해 주세요.", label: "이메일 주소", help: "평소 쓰는 이메일이 아니라, 앱을 설치할 Android 휴대폰에 로그인된 Google 계정을 적어 주세요 (Play 스토어 -> 프로필 아이콘).", confirm: "신청이 접수되었습니다. 24시간 안에 링크를 이메일로 보내 드립니다. 링크를 열고 '테스터 되기' -> '설치' 두 번만 누르면 됩니다." },
  th: { title: "SplitCam Remote — ทดสอบบน Android", desc: "SplitCam Remote ให้คุณควบคุมสตรีม SplitCam ได้จากมือถือ สมัครเพื่อร่วมทดสอบ", label: "อีเมลของคุณ", help: "ต้องเป็นบัญชี Google ที่ลงชื่อเข้าใช้อยู่บนมือถือ Android ของคุณ (ดูได้ที่ Play Store -> รูปโปรไฟล์) อีเมลอื่นใช้ไม่ได้", confirm: "เรียบร้อย เราจะส่งลิงก์ไปที่อีเมลของคุณภายใน 24 ชั่วโมง จากนั้นแค่แตะ 2 ปุ่ม คือ เป็นผู้ทดสอบ แล้ว ติดตั้ง" },
  pl: { title: "SplitCam Remote — testy na Androidzie", desc: "SplitCam Remote steruje streamem w SplitCam z telefonu. Zapisz się na testy.", label: "Twój e-mail", help: "Adres konta Google, na którym jesteś zalogowany w telefonie z Androidem (Sklep Play -> awatar) — inny adres nie zadziała.", confirm: "Gotowe. Link wyślemy Ci mailem w ciągu 24 godzin. Potem wystarczą dwa kliknięcia: Zostań testerem i Zainstaluj." },
  hu: { title: "SplitCam Remote — Android-teszt", desc: "A SplitCam Remote a telefonodról vezérli a streamedet. Jelentkezz tesztelőnek.", label: "E-mail-címed", help: "Az Android-telefonodon használt Google-fiók címe (Play Áruház -> profilkép) — másikkal nem működik.", confirm: "Kész. A linket 24 órán belül elküldjük e-mailben. Ott két koppintás: jelentkezés tesztelőnek, majd Telepítés." },
  sv: { title: "SplitCam Remote — Android-test", desc: "SplitCam Remote styr din SplitCam-stream från telefonen. Anmäl dig som testare.", label: "Din e-postadress", help: "Ange det Google-konto du är inloggad med på Android-telefonen (Play Store -> profilbilden) — annars fungerar inte länken.", confirm: "Klart! Du får länken via e-post inom 24 timmar. Sedan är det två tryck: Bli testare och Installera." },
  zh: { title: "SplitCam Remote——Android 封闭测试报名", desc: "SplitCam Remote 让你用手机遥控电脑上的 SplitCam 直播。填写邮箱即可报名测试。", label: "你的邮箱", help: "必须是你 Android 手机上登录的那个 Google 账号（Google Play → 右上角头像），不是别的常用邮箱，否则无法安装。", confirm: "已提交。24 小时内我们会把测试链接发到这个邮箱。之后只需两步：点 成为测试人员，再点 安装。" },
  el: { title: "SplitCam Remote — δοκιμή για Android", desc: "Με το SplitCam Remote ελέγχετε το stream σας από το κινητό σας. Δηλώστε συμμετοχή για να το δοκιμάσετε.", label: "Το e-mail σας", help: "Το e-mail του λογαριασμού Google που έχετε συνδεδεμένο στο κινητό σας Android (Play Store -> εικόνα προφίλ) — με άλλο ο σύνδεσμος δεν θα δουλέψει.", confirm: "Έτοιμο. Θα σας στείλουμε τον σύνδεσμο με e-mail μέσα σε 24 ώρες. Μετά χρειάζονται δύο πατήματα: Γίνετε δοκιμαστής και Εγκατάσταση." },
  cs: { title: "SplitCam Remote — test pro Android", desc: "SplitCam Remote ovládá váš stream ve SplitCamu z telefonu. Zapojte se do testování.", label: "Váš e-mail", help: "Účet Google z vašeho telefonu s Androidem (Google Play -> ikona profilu vpravo nahoře) — s jiným to nefunguje.", confirm: "Hotovo. Odkaz vám pošleme e-mailem do 24 hodin. Pak už jen dvě klepnutí: Stát se testerem a Instalovat." },
  he: { title: "SplitCam Remote — בטא ל-Android", desc: "SplitCam Remote שולטת בשידור של SplitCam מהטלפון. הירשמו כדי לנסות אותה.", label: "האימייל שלכם", help: "חייב להיות חשבון Google שמחובר לטלפון ה-Android שלכם (Play Store, תמונת הפרופיל). כתובת אחרת לא תעבוד.", confirm: "קיבלנו, תודה! נשלח לכם את הקישור למייל תוך 24 שעות. משם זה שתי הקשות: הצטרפות לבדיקה, ואז התקנה." },
  sr: { title: "SplitCam Remote — testiranje za Android", desc: "Telefonom upravljate strimom u SplitCamu na računaru. Prijavite se za testiranje.", label: "Vaš imejl", help: "Mora biti Google nalog kojim ste prijavljeni na Android telefonu (Google Play -> slika profila) — sa drugom adresom nema pristupa.", confirm: "Gotovo. Link vam šaljemo na imejl u roku od 24 sata. Zatim samo dva dodira: Postani tester, pa Instaliraj." },
  hr: { title: "SplitCam Remote - testiranje na Androidu", desc: "SplitCam Remote upravlja vašim SplitCam streamom s telefona. Prijavite se za testiranje.", label: "Vaša e-mail adresa", help: "Mora biti Google račun s kojim ste prijavljeni na Android telefonu (Google Play -> avatar) - inače pristup neće raditi.", confirm: "Gotovo. Link vam šaljemo e-mailom u roku od 24 sata. Zatim samo dva dodira: Postani tester, pa Instaliraj." },
  da: { title: "SplitCam Remote — Android-test", desc: "Med SplitCam Remote styrer du din stream fra telefonen. Tilmeld dig testen.", label: "Din e-mail", help: "Skal være den Google-konto, du er logget ind med på din Android-telefon (Google Play -> dit profilbillede). Ikke en anden mail.", confirm: "Tak! Du får linket på mail inden for 24 timer. Så er det bare to tryk: 'Bliv tester' og derefter 'Installer'." },
  fi: { title: "SplitCam Remote — Android-testaus", desc: "SplitCam Remote ohjaa striimiäsi puhelimella. Ilmoittaudu testaajaksi.", label: "Google-tilisi sähköpostiosoite", help: "Juuri se Google-tili, joka on käytössä Android-puhelimessasi (Google Play -> profiilikuva), ei mikään muu osoite.", confirm: "Valmis! Lähetämme linkin sähköpostiisi 24 tunnin sisällä. Sitten enää kaksi napautusta: Ryhdy testaajaksi ja Asenna." },
  no: { title: "SplitCam Remote — Android-test", desc: "SplitCam Remote lar deg styre SplitCam-streamen fra telefonen. Meld deg på for å teste.", label: "E-posten din", help: "Må være Google-kontoen du er logget inn med på Android-telefonen (Play Store -> profilbildet). Andre adresser fungerer ikke.", confirm: "Takk! Du får lenken på e-post innen 24 timer. Så er det bare to trykk: Bli tester, deretter Installer." },
  sk: { title: "SplitCam Remote — test pre Android", desc: "SplitCam Remote ovláda váš stream priamo z telefónu. Zapojte sa do testovania.", label: "Váš e-mail", help: "Účet Google, ktorý používate v Obchode Play na svojom Androide — iný nebude fungovať.", confirm: "Hotovo. Odkaz vám pošleme e-mailom do 24 hodín. Potom stačí dvakrát klepnúť: Stať sa testerom a Inštalovať." },
  fa: { title: "SplitCam Remote — تست نسخه اندروید", desc: "SplitCam Remote استریم SplitCam را از روی گوشی کنترل می‌کند. برای تست آن ثبت‌نام کنید.", label: "ایمیل شما", help: "دقیقاً همان حساب Google که با آن روی گوشی اندرویدتان وارد شده‌اید (در Google Play، عکس پروفایل). با ایمیل دیگر دسترسی تست فعال نمی‌شود.", confirm: "ثبت شد. لینک را تا 24 ساعت آینده برایتان ایمیل می‌کنیم. بعد کافی است دو بار ضربه بزنید: Become a tester و سپس Install." }
};

function createAllForms() {
  var ss = SpreadsheetApp.openById(DEST_SPREADSHEET_ID);
  var out = [['locale', 'form URL (give this to the site button)', 'edit URL']];
  var locales = Object.keys(COPY);

  for (var i = 0; i < locales.length; i++) {
    var loc = locales[i];
    var c = COPY[loc];
    try {
      var form = FormApp.create(c.title);
      form.setTitle(c.title)
          .setDescription(c.desc)
          .setCollectEmail(false)          // deliberate: the typed phone account is what we need,
          .setLimitOneResponsePerUser(false) // and people must be able to resubmit a typo
          .setConfirmationMessage(c.confirm)
          .setShowLinkToRespondAgain(false);

      form.addTextItem().setTitle(c.label).setHelpText(c.help).setRequired(true);

      // all forms -> one spreadsheet, one tab each
      form.setDestination(FormApp.DestinationType.SPREADSHEET, DEST_SPREADSHEET_ID);

      out.push([loc, form.getPublishedUrl(), form.getEditUrl()]);
      Logger.log(loc + '  ' + form.getPublishedUrl());
    } catch (e) {
      out.push([loc, 'ERROR: ' + e.message, '']);
      Logger.log(loc + '  ERROR ' + e.message);
    }
  }

  // write the URL table into a sheet so it is easy to copy back
  var sh = ss.getSheetByName('FORM URLS');
  if (!sh) sh = ss.insertSheet('FORM URLS');
  sh.clear();
  sh.getRange(1, 1, out.length, 3).setValues(out);
  sh.setFrozenRows(1);
  SpreadsheetApp.getUi().alert('Created ' + (out.length - 1) + ' forms. See the "FORM URLS" sheet.');
}
