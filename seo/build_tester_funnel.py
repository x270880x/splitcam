#!/usr/bin/env python3
"""Собирает рабочий seo/tester-funnel.gs из логики + переводов письма.

Источники:
  seo/tester-funnel-v2.gs      — логика скрипта с маркерной областью //<!--COPY-->
  seo/tester-email-i18n.json   — тексты писем: locale -> {subject, body}
  seo/make-tester-forms.gs     — подписи вопросов в формах (запасной способ
                                 определить язык вкладки, если лист FORM URLS потеряли)

Результат: seo/tester-funnel.gs — файл, который целиком вставляется в Apps Script.

Идемпотентен и маркерный, как seo/i18n_wire.py: правится ТОЛЬКО область между
//<!--COPY--> и //<!--/COPY-->, остальное берётся из v2 как есть.

Запуск:  python3 seo/build_tester_funnel.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
LOGIC = ROOT / "tester-funnel-v2.gs"
COPY_JSON = ROOT / "tester-email-i18n.json"
FORMS = ROOT / "make-tester-forms.gs"
OUT = ROOT / "tester-funnel.gs"

OPT_IN = "https://play.google.com/apps/testing/com.splitcam.remote"
PLAY = "https://play.google.com/store/apps/details?id=com.splitcam.remote"

BEGIN, END = "//<!--COPY-->", "//<!--/COPY-->"


def js_string(s):
    """Строковый литерал JS. Апострофы, кавычки и переводы строк — экранируются."""
    return json.dumps(s, ensure_ascii=False)


def form_labels():
    """locale -> подпись поля из make-tester-forms.gs (для запасного определения языка)."""
    src = FORMS.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"^\s*(\w+):\s*\{(.+?)\}\s*,?\s*$", src, re.M):
        loc, body = m.group(1), m.group(2)
        lab = re.search(r"label:\s*(['\"])(.*?)\1", body)
        if lab:
            out[loc] = lab.group(2)
    return out


def main():
    for p in (LOGIC, COPY_JSON, FORMS):
        if not p.exists():
            sys.exit(f"нет файла: {p}")

    copy = json.loads(COPY_JSON.read_text(encoding="utf-8"))

    # --- проверки, без которых собирать нельзя -----------------------------
    problems = []
    for loc, item in sorted(copy.items()):
        subj, body = item.get("subject", ""), item.get("body", "")
        lines = [l.strip() for l in body.split("\n")]
        if not subj.strip():
            problems.append(f"{loc}: пустой сабжект")
        if OPT_IN not in lines:
            problems.append(f"{loc}: opt-in ссылка отсутствует или не на отдельной строке")
        if PLAY not in lines:
            problems.append(f"{loc}: ссылка на магазин отсутствует или не на отдельной строке")
        if OPT_IN in body and PLAY in body and body.find(OPT_IN) > body.find(PLAY):
            problems.append(f"{loc}: ПОРЯДОК ССЫЛОК ПЕРЕПУТАН — магазин раньше opt-in")
    if problems:
        print("СБОРКА ОСТАНОВЛЕНА:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        sys.exit(1)

    # --- запасная карта «подпись поля -> локаль» ---------------------------
    labels = form_labels()
    by_label = {}
    for loc, lab in labels.items():
        by_label.setdefault(lab, []).append(loc)
    ambiguous = {lab: locs for lab, locs in by_label.items() if len(locs) > 1}
    label_map = {lab: locs[0] for lab, locs in by_label.items() if len(locs) == 1}

    # --- генерируемый блок -------------------------------------------------
    lines = [
        BEGIN,
        "// Generated block — DO NOT EDIT HERE. Edit seo/tester-email-i18n.json and rerun",
        "// `python3 seo/build_tester_funnel.py`. Everything between the COPY markers is",
        "// overwritten by that script.",
        "",
        "/** locale -> the exact mail that locale's signups receive. */",
        "var COPY = {",
    ]
    for loc in sorted(copy, key=lambda x: (x != "EN", x != "ru", x)):
        item = copy[loc]
        lines.append(f"  {loc}: {{")
        lines.append(f"    subject: {js_string(item['subject'])},")
        lines.append(f"    body: {js_string(item['body'])}")
        lines.append("  },")
    lines.append("};")
    lines.append("")
    lines.append("/**")
    lines.append(" * Fallback only. The primary locale lookup matches sheet.getFormUrl() against the")
    lines.append(f" * '{'FORM URLS'}' sheet; this map is what remains if that sheet is gone. The form's")
    lines.append(" * question label is localized, so it fingerprints the form.")
    if ambiguous:
        for lab, locs in sorted(ambiguous.items()):
            lines.append(f" * Ambiguous, deliberately omitted: {js_string(lab)} is used by {', '.join(locs)}.")
        lines.append(" * An omitted label means that tab falls through to the English copy.")
    lines.append(" */")
    lines.append("var LABEL_TO_LOCALE = {")
    for lab in sorted(label_map):
        lines.append(f"  {js_string(lab)}: {js_string(label_map[lab])},")
    lines.append("};")
    lines.append(END)
    block = "\n".join(lines)

    logic = LOGIC.read_text(encoding="utf-8")
    if BEGIN not in logic or END not in logic:
        sys.exit(f"в {LOGIC.name} нет маркеров {BEGIN} … {END}")
    head, rest = logic.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    OUT.write_text(head + block + tail, encoding="utf-8")

    print(f"собрано: {OUT.relative_to(ROOT.parent)}")
    print(f"  локалей: {len(copy)}  ({', '.join(sorted(copy))})")
    print(f"  запасная карта подписей: {len(label_map)} однозначных"
          + (f", {len(ambiguous)} неоднозначных пропущено" if ambiguous else ""))
    print(f"  размер: {OUT.stat().st_size} байт")


if __name__ == "__main__":
    main()
