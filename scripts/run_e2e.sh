#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
npm install --silent
npx playwright install chromium --with-deps 2>/dev/null || npx playwright install chromium
exec npx playwright test "$@"
