#!/usr/bin/env bash
# Launch PyCommonist (Python 3.10–3.12 ; éviter 3.14 avec PyQt6 sur macOS).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

choose_python() {
  for cmd in /opt/homebrew/bin/python3.12 python3.12 python3.11 python3.10; do
    if [[ -x "$cmd" ]] || command -v "$cmd" >/dev/null 2>&1; then
      if "$cmd" -c 'import sys; exit(0 if sys.version_info < (3, 14) else 1)' 2>/dev/null; then
        echo "$cmd"
        return
      fi
    fi
  done
  echo python3
}

PY_BOOT="$(choose_python)"

if [[ ! -d .venv ]] || ! .venv/bin/python -c 'import sys; assert sys.version_info < (3, 14)' 2>/dev/null; then
  echo "Creating venv with $PY_BOOT ..."
  rm -rf .venv
  "$PY_BOOT" -m venv .venv
  .venv/bin/pip install -U pip
  .venv/bin/pip install -r requirements.txt
  .venv/bin/pip install -e .
fi

exec .venv/bin/python main.py
