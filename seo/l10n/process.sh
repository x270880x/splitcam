#!/bin/zsh
# Verify + build + hub-activate one locale. Skips if the JSON is not there yet.
# Idempotent: safe to re-run as more translations arrive.
set -e
cd "$(dirname "$0")/../.."
SRC=/private/tmp/claude-501/-Users-splitcam/d197211a-7800-4b93-91ab-2b5ee7e18a73/scratchpad/edu_src.json
TR=/private/tmp/claude-501/-Users-splitcam/d197211a-7800-4b93-91ab-2b5ee7e18a73/scratchpad/tr
for l in "$@"; do
  [ -f "$TR/$l.json" ] || { echo "  — $l: перевод ещё не готов"; continue; }
  if ! python3 seo/l10n/verify_tr.py "$l" "$SRC" "$TR/$l.json"; then
    echo "  ✗ $l: перевод не прошёл проверку — пропуск"; continue
  fi
  python3 seo/l10n/build_locale.py "$l" for/educators/index.html "$TR/$l.json" "$l/for/churches/index.html" "$l/for/educators/index.html" >/dev/null
  python3 seo/l10n/verify_page.py "$l" "$l/for/educators/index.html" >/dev/null && echo "  ✓ $l: страница собрана и проверена"
  python3 seo/l10n/hub_activate.py "$l" "$l/for/index.html" 🎓 >/dev/null
done
