#!/usr/bin/env bash
# Build a HAL / GitHub–style source archive: pycommonist-vX.Y.zip
# Usage: ./scripts/build_release_zip.sh [version]   (default: 1.1)

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="${1:-1.1}"
ARCHIVE_NAME="pycommonist-v${VERSION}"
OUT_DIR="${ROOT}/releases"
ZIP_PATH="${OUT_DIR}/${ARCHIVE_NAME}.zip"

cd "$ROOT"
mkdir -p "$OUT_DIR"
rm -f "$ZIP_PATH"

# Required for HAL option 1: README, AUTHORS, LICENSE at archive root
zip -r "$ZIP_PATH" . \
  -x '*.git*' \
  -x '.venv/*' \
  -x 'dist/*' \
  -x 'releases/*.zip' \
  -x '*__pycache__*' \
  -x '*.pyc' \
  -x '*.egg-info/*' \
  -x '.DS_Store' \
  -x '*/.DS_Store'

echo "Created: $ZIP_PATH ($(du -h "$ZIP_PATH" | cut -f1))"
