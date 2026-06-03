#!/usr/bin/env bash
# Launch PyCommonist from the repo.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
  .venv/bin/pip install -e .
fi

PY="$ROOT/.venv/bin/python"
QT_PLUGINS="$("$PY" -c "import os, PyQt6; print(os.path.join(os.path.dirname(PyQt6.__file__), 'Qt6', 'plugins'))")"
export QT_PLUGIN_PATH="$QT_PLUGINS"
export QT_QPA_PLATFORM_PLUGIN_PATH="$QT_PLUGINS/platforms"

exec "$PY" main.py
