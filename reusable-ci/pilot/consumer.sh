#!/usr/bin/env bash
set -euo pipefail
receipt=${1:?receipt path is required}
test -f "$receipt"
jq -e '.schema_version == 1 and .producer == "AI-Ascension/.github" and .contract == "reusable-ci-local-pilot"' "$receipt" >/dev/null
