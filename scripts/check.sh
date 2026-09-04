#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/daemon.py" --check
bash -n "$ROOT/cb" "$ROOT/install.sh"
if command -v node >/dev/null 2>&1; then
  node --check "$ROOT/extension/background.js"
  node --check "$ROOT/extension/popup.js"
else
  echo "node not found; skipped JavaScript syntax check"
fi
python3 -m json.tool "$ROOT/extension/manifest.json" >/dev/null
echo "all checks passed"
