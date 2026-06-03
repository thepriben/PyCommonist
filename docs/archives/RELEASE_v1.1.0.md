# Release notes — PyCommonist v1.1.0

## Highlights

- **PyPI package** `pycommonist` with console entry point `pycommonist`
- **Main window** with shared Commons login
- **MDI import sessions** (cascade / tile / multiple folders)
- **Information (Description)** session — `{{Information}}` (parity with v1.0)
- **Artwork** session — `{{Artwork}}` for GLAM / museum uploads
- Refactored upload pipeline (`UploadService`, injectable wikitext builders)

## Install

```bash
pip install pycommonist==1.1.0
pycommonist
```

## Build artifacts

From a clean tree:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m build
```

Artifacts: `dist/pycommonist-1.1.0-py3-none-any.whl`, `dist/pycommonist-1.1.0.tar.gz`

## PyPI upload (maintainers)

```bash
twine upload dist/pycommonist-1.1.0*
```

## Git tags

- `v1.1.0` — version semver (PyPI)
- `pycommonist-v1.1` — archive HAL / convention `pycommonist-v1.0`

## Archive HAL (zip)

```bash
./scripts/build_release_zip.sh 1.1
# → releases/pycommonist-v1.1.zip
```

Voir [HAL_v1.1.md](HAL_v1.1.md).
