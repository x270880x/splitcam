# -*- coding: utf-8 -*-
"""Собирает тексты рассылки 2026-09-07 из утверждённого tester-email-i18n.json.
Две правки: (1) из ШАГА 3 убирается фраза «ответьте на это письмо…», она
переезжает в (2) новый блок контактов перед просьбой не удалять приложение.
Для первой волны дополнительно заменяется вводный абзац."""
import json, pathlib, sys

BASE = pathlib.Path("tester-email-i18n.json")
OUT  = pathlib.Path("/private/tmp/claude-501/-Users-splitcam/03521f8c-519c-44fa-955a-70bcc62a9e60/scratchpad/mailout-2026-09-07.json")

CUT = {
"EN": " Reply\nto this email and tell us what felt awkward or broke — that is the most valuable\nthing for us, we fix things based on your reports.",
"ru": " Ответьте на это письмо и напишите, что оказалось неудобным или\nсломалось, — это для нас ценнее всего, мы чиним по вашим отзывам.",
"es": " Responde a este correo y cuéntanos qué te resultó\nincómodo o qué falló: es lo más valioso para nosotros y es así como\narreglamos las cosas.",
"fr": " Répondez à cet e-mail et\ndites-nous ce qui vous a paru pénible ou ce qui n'a pas marché : c'est ce\nqui nous aide le plus, et c'est comme ça que nous corrigeons les choses.",
"nl": " Antwoord op deze mail en vertel wat er onhandig\naanvoelde of wat er kapotging — daar hebben we het meest aan, we verbeteren\nde app op basis van jullie meldingen.",
"pl": " Odpowiedz na tego maila\ni napisz, co było niewygodne albo co się zepsuło – to dla nas\nnajcenniejsze, poprawiamy dokładnie na podstawie tego, co nam napiszesz.",
"tr": " Bu e-postayı yanıtlayıp nerede zorlandığınızı ya da neyin bozuk\nolduğunu yazın; bizim için en değerlisi bu, gelen geri bildirimlere göre\ndüzeltiyoruz.",
}

ANCHOR = {
"EN": "One request: please do not uninstall",
"ru": "И просьба: не удаляйте приложение",
"es": "Y una petición: no desinstales",
"fr": "Une demande pour finir :",
"nl": "Nog één ding: verwijder de app niet",
"pl": "I jeszcze prośba: nie usuwaj",
"tr": "Bir ricamız var:",
}

BLOCK = {
"EN": """IDEAS, BUGS, REQUESTS — TELL US.
If something is missing, something breaks, or you have an idea for the app, we
want to hear it. Whichever is easiest for you:
  - reply straight to this email
  - support@splitcam.com
  - Telegram: @splitcam
We read every message, and we fix things based on your reports.""",
"ru": """ИДЕИ, ОШИБКИ, ПОЖЕЛАНИЯ — НАПИШИТЕ НАМ.
Если чего-то не хватает, что-то сломалось или есть идея для приложения — нам
это нужно знать. Как вам удобнее:
  - ответьте прямо на это письмо
  - support@splitcam.com
  - Telegram: @splitcam
Мы читаем каждое сообщение и чиним по вашим отзывам.""",
"es": """IDEAS, ERRORES, PETICIONES: CUÉNTANOSLO.
Si echas algo en falta, si algo se rompe o si se te ocurre una idea para la
aplicación, queremos saberlo. Como te resulte más cómodo:
  - responde directamente a este correo
  - support@splitcam.com
  - Telegram: @splitcam
Leemos todos los mensajes y arreglamos las cosas gracias a ellos.""",
"fr": """IDÉES, BUGS, DEMANDES : DITES-NOUS TOUT.
S'il manque quelque chose, si quelque chose casse ou si vous avez une idée pour
l'application, nous voulons le savoir. Au choix :
  - répondez directement à cet e-mail
  - support@splitcam.com
  - Telegram : @splitcam
Nous lisons chaque message et c'est ainsi que nous corrigeons les choses.""",
"nl": """IDEEËN, BUGS, WENSEN — LAAT HET ONS WETEN.
Mis je iets, gaat er iets kapot of heb je een idee voor de app? Dan horen we dat
graag. Wat jou het beste uitkomt:
  - antwoord gewoon op deze mail
  - support@splitcam.com
  - Telegram: @splitcam
We lezen elk bericht en verbeteren de app op basis daarvan.""",
"pl": """POMYSŁY, BŁĘDY, PROŚBY – NAPISZ DO NAS.
Jeśli czegoś brakuje, coś się psuje albo masz pomysł na aplikację, chcemy o tym
wiedzieć. Jak Ci wygodniej:
  - odpowiedz po prostu na tego maila
  - support@splitcam.com
  - Telegram: @splitcam
Czytamy każdą wiadomość i na tej podstawie poprawiamy aplikację.""",
"tr": """FİKİRLER, HATALAR, İSTEKLER — BİZE YAZIN.
Eksik bir şey varsa, bir şey bozuluyorsa ya da uygulama için bir fikriniz varsa
bunu duymak istiyoruz. Size hangisi kolaysa:
  - doğrudan bu e-postayı yanıtlayın
  - support@splitcam.com
  - Telegram: @splitcam
Her mesajı okuyoruz ve gelen geri bildirimlere göre düzeltiyoruz.""",
}

STEP1 = {"EN": "STEP 1.", "ru": "ШАГ 1.", "es": "PASO 1.", "fr": "ÉTAPE 1.",
         "nl": "STAP 1.", "pl": "KROK 1.", "tr": "ADIM 1."}

# --- только для первой волны (получили письмо 12.08): другое начало и тема ---
REMIND_SUBJ = {
"EN": "SplitCam Remote: a reminder, and how to reach us",
"ru": "SplitCam Remote: напоминание и наши контакты",
"fr": "SplitCam Remote : rappel et comment nous joindre",
"nl": "SplitCam Remote: herinnering en hoe je ons bereikt",
"pl": "SplitCam Remote: przypomnienie i kontakt do nas",
}
REMIND_INTRO = {
"EN": """Hi!

On 12 August we sent you the links for the SplitCam Remote test. This is a short
reminder — the links below have not changed — and, more to the point, here is how
to reach us if you have anything to say about the app.

If you are already testing, thank you — skip straight to the last part. If you
never got round to it, both steps are below.""",
"ru": """Здравствуйте!

12 августа мы присылали вам ссылки на тест SplitCam Remote. Это короткое
напоминание — ссылки ниже не изменились, — и, главное, наши контакты на случай,
если вам есть что сказать о приложении.

Если вы уже тестируете — спасибо, тогда сразу к последней части. Если руки не
дошли, оба шага ниже.""",
"fr": """Bonjour !

Le 12 août, nous vous avons envoyé vos liens pour le test de SplitCam Remote.
Voici un petit rappel — les liens ci-dessous n'ont pas changé — et surtout nos
coordonnées si vous avez quelque chose à nous dire sur l'application.

Si vous testez déjà, merci : passez directement à la dernière partie. Si vous
n'avez pas eu le temps, les deux étapes sont ci-dessous.""",
"nl": """Hallo!

Op 12 augustus stuurden we je de links voor de test van SplitCam Remote. Dit is
een korte herinnering — de links hieronder zijn ongewijzigd — en vooral: zo
bereik je ons als je iets over de app kwijt wilt.

Test je al mee? Bedankt, ga dan meteen door naar het laatste deel. Ben je er nog
niet aan toegekomen? Beide stappen staan hieronder.""",
"pl": """Cześć!

12 sierpnia wysłaliśmy Ci linki do testów SplitCam Remote. To krótkie
przypomnienie – linki poniżej się nie zmieniły – a przede wszystkim nasze
kontakty, jeśli masz coś do powiedzenia o aplikacji.

Jeśli już testujesz – dziękujemy, przejdź od razu do ostatniej części. Jeśli
jeszcze nie, oba kroki są poniżej.""",
}

base = json.loads(BASE.read_text(encoding="utf-8"))
out = {"new": {}, "reminder": {}}
errs = []

for loc in ["EN", "ru", "es", "fr", "nl", "pl", "tr"]:
    body = base[loc]["body"]
    if CUT[loc] not in body:
        errs.append(f"{loc}: не найдена вырезаемая фраза шага 3")
        continue
    body = body.replace(CUT[loc], "")
    if ANCHOR[loc] not in body:
        errs.append(f"{loc}: не найден якорь «{ANCHOR[loc]}»")
        continue
    i = body.index(ANCHOR[loc])
    body = body[:i] + BLOCK[loc] + "\n\n" + body[i:]
    out["new"][loc] = {"subject": base[loc]["subject"], "body": body}

    if loc in REMIND_INTRO:
        j = body.index(STEP1[loc])
        rbody = REMIND_INTRO[loc] + "\n\n" + body[j:]
        out["reminder"][loc] = {"subject": REMIND_SUBJ[loc], "body": rbody}

if errs:
    print("ОШИБКИ:"); [print(" ", e) for e in errs]; sys.exit(1)

# проверки: ссылки на месте, каждая на своей строке, порядок шагов не нарушен
OPTIN = "https://play.google.com/apps/testing/com.splitcam.remote"
STORE = "https://play.google.com/store/apps/details?id=com.splitcam.remote"
for kind, d in out.items():
    for loc, c in d.items():
        b = c["body"]
        assert b.count(OPTIN) == 1 and b.count(STORE) == 1, f"{kind}/{loc}: ссылки"
        assert OPTIN in b.split("\n") and STORE in b.split("\n"), f"{kind}/{loc}: ссылка не на отдельной строке"
        assert b.index(OPTIN) < b.index(STORE), f"{kind}/{loc}: шаги переставлены"
        assert "support@splitcam.com" in b and "@splitcam" in b, f"{kind}/{loc}: контакты"
        assert c["subject"] and len(c["subject"]) < 60, f"{kind}/{loc}: сабжект"
        assert max(len(x) for x in b.split("\n")) <= 82, f"{kind}/{loc}: длинная строка"
        assert "  " not in b.replace("  - ", ""), f"{kind}/{loc}: двойной пробел (след вырезанной фразы)"
        assert not any(x != x.rstrip() for x in b.split("\n")), f"{kind}/{loc}: пробел в конце строки"
        assert "\n\n\n" not in b, f"{kind}/{loc}: тройной перевод строки"

OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"OK. new: {sorted(out['new'])}  reminder: {sorted(out['reminder'])}")
print("→", OUT)
