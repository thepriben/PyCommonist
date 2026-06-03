# PyCommonist

[![Version](https://img.shields.io/badge/version-1.1.0-blue)](https://github.com/thepriben/PyCommonist)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**PyCommonist** is a desktop application for batch-uploading images and media to [Wikimedia Commons](https://commons.wikimedia.org/). It is written in Python with **PyQt6** and is inspired by the excellent [Commonist](https://commons.wikimedia.org/wiki/Commons:Commonist/fr) tool (which no longer works on Commons since 2021).

Version **1.1** introduces a small PyQt6 framework, a main window with **MDI import sessions**, and built-in support for **`{{Information}}`** (description) and **`{{Artwork}}`** wikitext templates.

---

## Features

- Batch upload from a folder tree (JPEG, PNG, SVG, OGV, WEBM)
- EXIF date, GPS location, category autocomplete (Commons API)
- Copy/paste metadata between images, optional filename numbering
- **MDI sessions**: work on several imports side by side (cascade / tile windows)
- **Session types**
  - **Information (Description)** — classic `{{Information}}` block (same behaviour as v1.0)
  - **Artwork** — `{{Artwork}}` for museum / GLAM-style uploads
- Central login (username / password) shared across all sessions

---

## Installation

### From PyPI (recommended after publish)

```bash
pip install pycommonist
pycommonist
```

### From source (development)

```bash
git clone https://github.com/thepriben/PyCommonist.git
cd PyCommonist
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
pycommonist
# or: python -m pycommonist
# or: python main.py
```

---

## Quick start

1. Enter your Wikimedia Commons **username** and **password** in the top bar.
2. A default **Information** session opens. Select a folder in the tree on the left.
3. Fill global fields (source, author, license, categories, description) and per-image rows.
4. Check **Import** on the files to upload, then click the large **Import** button.
5. **Fichier → Nouvelle session** to add an **Artwork** or another **Information** session.

Default metadata values are loaded from the packaged file `config/general.yaml` inside the `pycommonist` package. To customise defaults for development, edit [`src/pycommonist/resources/config/general.yaml`](src/pycommonist/resources/config/general.yaml) before installing.

---

## Project structure

```
src/pycommonist/
  framework/     # MainWindow, MDI, BaseImportSession
  sessions/      # InformationSession, ArtworkSession
  core/          # Upload, wikitext builders, EXIF, config
  widgets/       # Image rows, category search
  resources/     # general.yaml, logos
```

---

## History and contributors

Detailed contribution history (French) is kept in **[docs/archives/History.md](docs/archives/History.md)** — please preserve archive markdown under `docs/archives/` when evolving the project.

---

## Releases and HAL Software Archive

| Version | Source archive | Tags |
|---------|----------------|------|
| **1.0** | `pycommonist-v1.0.zip` | `pycommonist-v1.0` |
| **1.1** | `pycommonist-v1.1.zip` | `pycommonist-v1.1`, `v1.1.0` |

Build the v1.1 zip (README, AUTHORS, LICENSE included for [HAL](https://doc.hal.science/deposer/deposer-le-code-source)):

```bash
./scripts/build_release_zip.sh 1.1
```

See [releases/README.md](releases/README.md) and [docs/archives/HAL_v1.1.md](docs/archives/HAL_v1.1.md). Archive notes: [docs/archives/](docs/archives/).

---

## Publishing to PyPI (maintainers)

```bash
pip install build twine
python -m build
twine check dist/*
twine upload dist/*
```

Tag releases as `v1.1.0` on GitHub; attach `dist/*.whl`, `dist/*.tar.gz`, and **`releases/pycommonist-v1.1.zip`** for HAL.

---

## Roadmap

- Additional session types (`{{Photograph}}`, `{{Book}}`, YAML-defined presets)
- CI and automated tests
- Broader OS support for Preview / GIMP shortcuts (currently macOS-oriented)

---

## License

MIT — see [LICENSE](LICENSE).

---

## English summary

PyCommonist helps Wikimedia Commons contributors upload many files at once with structured wikitext. Use **Information** sessions for general photos and **Artwork** sessions for cultural heritage. Install with `pip install pycommonist` and run `pycommonist`.
