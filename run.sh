#!/usr/bin/env bash
# Launch PyCommonist.
#
# - Python 3.10-3.12 required (PyQt6 has no stable wheels for 3.14 on macOS).
# - The virtual environment lives OUTSIDE the repository, in
#   ~/.venvs/pycommonist by default (override with $PYCOMMONIST_VENV).
#   Reason: when the repository sits in an iCloud-synced folder such as
#   Desktop or Documents, iCloud silently evicts files inside .venv and
#   corrupts the Qt plugins ("Could not find the Qt platform plugin").
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

VENV="${PYCOMMONIST_VENV:-$HOME/.venvs/pycommonist}"

choose_python() {
  for cmd in /opt/homebrew/bin/python3.12 python3.12 python3.11 python3.10; do
    if [[ -x "$cmd" ]] || command -v "$cmd" >/dev/null 2>&1; then
      if "$cmd" -c 'import sys; exit(0 if sys.version_info < (3, 14) else 1)' 2>/dev/null; then
        echo "$cmd"
        return
      fi
    fi
  done
  echo "ERROR: no Python 3.10-3.12 found (PyQt6 does not support 3.14 yet)." >&2
  echo "Install one, e.g.: brew install python@3.12" >&2
  exit 1
}

venv_is_healthy() {
  [[ -x "$VENV/bin/python" ]] || return 1
  "$VENV/bin/python" - <<'EOF' 2>/dev/null || return 1
import os, sys
assert sys.version_info < (3, 14)
import PyQt6
platforms = os.path.join(os.path.dirname(PyQt6.__file__), "Qt6", "plugins", "platforms")
assert os.path.isdir(platforms) and os.listdir(platforms), "Qt platform plugins missing"
EOF
}

if ! venv_is_healthy; then
  PY_BOOT="$(choose_python)"
  echo "(Re)creating venv at $VENV with $PY_BOOT ..."
  rm -rf "$VENV"
  "$PY_BOOT" -m venv "$VENV"
  "$VENV/bin/pip" install -U pip
  "$VENV/bin/pip" install -r requirements.txt
  "$VENV/bin/pip" install -e .
fi

exec "$VENV/bin/python" main.py
