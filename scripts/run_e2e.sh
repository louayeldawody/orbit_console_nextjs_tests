#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
.venv/bin/pip install -q -r requirements.txt
.venv/bin/playwright install chromium --with-deps 2>/dev/null || .venv/bin/playwright install chromium
exec .venv/bin/pytest e2e/ -v -m e2e "$@"
