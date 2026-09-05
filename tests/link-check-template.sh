#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Synthetic checks of the actual starter workflow run block; no network requests.
set -euo pipefail
repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
fixture=$(mktemp -d "$repo_root/.link-check-fixture.XXXXXX")
trap 'rm -rf "$fixture"' EXIT
awk '
  /^        run: \|$/ { copying=1; next }
  copying { sub(/^          /, ""); print }
' "$repo_root/workflow-templates/link-check.yml" > "$fixture/check.sh"
bash -n "$fixture/check.sh"

# Supply a deterministic tracked-file list and intercept all external URL checks.
git() { printf '%s\n' README.md; }
curl() { return "${URL_EXIT:-0}"; }
export -f git curl
touch "$fixture/existing.txt" "$fixture/with spaces (copy).txt"

check() {
  local name=$1 expected=$2 markdown=$3 actual=0
  printf '%s\n' "$markdown" > "$fixture/README.md"
  (cd "$fixture" && bash check.sh) > "$fixture/output" 2>&1 || actual=$?
  if [[ "$actual" != "$expected" ]]; then
    printf 'FAIL %s: expected exit %s, got %s\n' "$name" "$expected" "$actual"
    cat "$fixture/output"
    exit 1
  fi
  if [[ "$expected" == 1 && "${URL_EXIT:-0}" == 0 ]]; then
    grep -q 'missing relative link target:' "$fixture/output"
  fi
  printf 'PASS %s (exit %s)\n' "$name" "$actual"
}

check inline-existing 0 '[file](existing.txt)'
check inline-missing 1 '[file](missing.txt)'
check inline-title 0 '[file](existing.txt "Title")'
check reference-existing 0 $'[file][ref]\n\n[ref]: existing.txt'
check reference-missing 1 $'[file][ref]\n\n[ref]: missing.txt'
check reference-title 0 $'[file][ref]\n\n  [ref]: existing.txt "Title"'
check angle-existing 0 '[file](<with spaces (copy).txt>)'
check angle-missing 1 '[file](<missing file (copy).txt>)'
check angle-reference-existing 0 $'[file][ref]\n\n[ref]: <with spaces (copy).txt> "Title"'
check angle-reference-missing 1 $'[file][ref]\n\n[ref]: <missing file (copy).txt>'
check angle-title 0 '[file](<with spaces (copy).txt> "Title")'
check anchor-only 0 '[section](#section)'
check file-anchor 0 '[section](existing.txt#section)'
check external-and-mail 0 '[web](https://example.invalid/page) [mail](mailto:example@example.invalid)'
URL_EXIT=22 check external-failure 1 '[web](https://example.invalid/missing)'
