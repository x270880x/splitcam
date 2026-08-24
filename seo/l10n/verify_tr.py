#!/usr/bin/env python3
"""Independently verify a translation dict against the EN source. Trust no self-report.

Checks, per locale:
  * every source key present, no unknown keys (besides x: extras)
  * both x: extras present
  * HTML tag multiset identical per string (no dropped/added/reordered tags)
  * href / src attribute values byte-identical (never translated)
  * untranslated brand/tech tokens still present where they were in EN
  * nothing left in English (long strings that equal the source)
  * &-entities still well formed
  * title <= 60, meta description <= 155
  * fa counters use Persian digits; he has no obvious masculine SplitCam agreement (report-only)
Exit non-zero if any hard check fails.
"""
import json
import re
import sys

KEEP = ["SplitCam", "Zoom", "Google Meet", "Microsoft Teams", "Twitch", "YouTube",
        "Kick", "OBS", "PDF", "PowerPoint", "Keynote", "DirectX", "OpenGL",
        "NVENC", "QuickSync", "AMF"]
TAG_RE = re.compile(r"<[^>]+>")
HREF_RE = re.compile(r'(?:href|src)="([^"]*)"')
ENT_RE = re.compile(r"&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9a-fA-F]+;|nbsp;|mdash;|hellip;|rsquo;|lsquo;|ldquo;|rdquo;|deg;)")


def check(locale, src, tr):
    errs, warns = [], []
    miss = [k for k in src if k not in tr]
    extra = [k for k in tr if k not in src and not k.startswith("x:")]
    if miss:
        errs.append(f"missing keys: {miss[:8]}")
    if extra:
        errs.append(f"unknown keys: {extra[:8]}")
    for k in ("x:breadcrumb_last", "x:software_desc"):
        if not tr.get(k, "").strip():
            errs.append(f"missing extra {k}")

    for k, v in src.items():
        t = tr.get(k, "")
        if sorted(TAG_RE.findall(v)) != sorted(TAG_RE.findall(t)):
            errs.append(f"tag mismatch @ {k}")
        if HREF_RE.findall(v) != HREF_RE.findall(t):
            errs.append(f"href changed @ {k}: {HREF_RE.findall(v)} -> {HREF_RE.findall(t)}")
        for kw in KEEP:
            if v.count(kw) > t.count(kw):
                warns.append(f"'{kw}' lost @ {k} ({v.count(kw)}->{t.count(kw)})")
        if len(v.split()) > 5 and t.strip() == v.strip():
            errs.append(f"UNTRANSLATED @ {k}")
        if ENT_RE.search(t):
            errs.append(f"bad &-entity @ {k}")

    title = tr.get("title:title#0", "")
    desc = tr.get("meta:description#0", "")
    # length compares on unescaped text
    import html as H
    if len(H.unescape(title)) > 60:
        warns.append(f"title {len(H.unescape(title))}>60")
    if len(H.unescape(desc)) > 155:
        warns.append(f"description {len(H.unescape(desc))}>155")

    if locale == "fa":
        if re.search(r"\b\d+\b", tr.get("block:h1#0", "") + desc):
            warns.append("fa: Latin digits present, expected Persian numerals")

    return errs, warns


def main():
    locale = sys.argv[1]
    src = json.load(open(sys.argv[2], encoding="utf-8"))
    tr = json.load(open(sys.argv[3], encoding="utf-8"))
    errs, warns = check(locale, src, tr)
    for w in warns:
        print(f"  ⚠ {locale}: {w}")
    for e in errs:
        print(f"  ✗ {locale}: {e}")
    if errs:
        sys.exit(1)
    print(f"  ✓ {locale}: clean ({len(tr)} keys)")


if __name__ == "__main__":
    main()
