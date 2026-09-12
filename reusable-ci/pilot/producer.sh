#!/usr/bin/env bash
set -euo pipefail
output=${1:?receipt output path is required}
printf '{"schema_version":1,"producer":"AI-Ascension/.github","contract":"reusable-ci-local-pilot"}\n' > "$output"
