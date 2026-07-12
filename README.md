# PyCommonist

Desktop application (Python / PyQt6) for batch-uploading images and media to
[Wikimedia Commons](https://commons.wikimedia.org/), inspired by
[Commonist](https://commons.wikimedia.org/wiki/Commons:Commonist).

Version **1.2** — main window, MDI upload sessions, `{{Information}}` and
`{{Artwork}}` wikitext templates, hardened Commons API client.

![PyCommonist logo](img/PyCommonist.png)

## Installation

### From PyPI

```bash
pip install pycommonist
pycommonist
```

### From source

```bash
git clone https://github.com/thepriben/PyCommonist.git
cd PyCommonist
./run.sh
```

`run.sh` creates a virtual environment with **Python 3.10–3.12** if needed
(PyQt6 is unstable with Python 3.14 on macOS). Or manually:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
python main.py
```

## Usage

1. Enter your Wikimedia Commons credentials at the top of the window.
   With two-factor authentication, use a
   [bot password](https://commons.wikimedia.org/wiki/Special:BotPasswords)
   in the form `User@BotName`.
2. Open a session via **File → New session**, choosing a template:
   **Description — `{{Information}}`** (default) or **Artwork — `{{Artwork}}`**.
3. Pick a folder on the left, fill in the global and per-file fields,
   tick **Import**, and start the upload.

Default field values can be adjusted in
[`src/pycommonist/resources/config/general.yaml`](src/pycommonist/resources/config/general.yaml).

### Security

- Credentials are sent only to `commons.wikimedia.org` over HTTPS and are
  never stored on disk or written to logs.
- Every API request carries a descriptive `User-Agent` and an explicit
  timeout; authenticated calls use `assert=user` so an expired session fails
  visibly instead of uploading anonymously.
- Bot passwords are supported and recommended.

## Testing

An offscreen smoke test covers application start-up, both session types and
both wikitext builders — no display or Commons account needed:

```bash
QT_QPA_PLATFORM=offscreen .venv/bin/python scripts/smoke_test.py
```

## Releases

| Version | Archive | Tag |
|---------|---------|-----|
| 1.0 | `pycommonist-v1.0.zip` | `pycommonist-v1.0` |
| 1.1 | `pycommonist-v1.1.zip` | `pycommonist-v1.1` |
| 1.2 | `pycommonist-v1.2.zip` | `pycommonist-v1.2` |

## History

The project history — including all historical contributions — is maintained
in [`docs/archives/History.md`](docs/archives/History.md).

PyCommonist is the subject of a magazine article (in French):

> Benoît Prieur, *PyQt5 : développement d'une application de téléversement
> d'images vers Wikimedia Commons*, 2021, **Programmez!** n°246, pp. 33–39
> ([programmez.com](https://www.programmez.com/magazine/article/pyqt5-developpement-dune-application-de-televersement-dimages-vers-wikimedia-commons),
> listed on [benoit-prieur.fr](https://benoit-prieur.fr/tech_articles.html)).

## Credits and license

MIT — see [LICENSE](LICENSE). Maintained by
[@thepriben](https://github.com/thepriben) (Benoît Prieur).

- Historical code contributions by **Romain Behar** (`User:Romainbar`) are
  recorded in [`docs/archives/History.md`](docs/archives/History.md).
- Logo by **[Chabe01](https://commons.wikimedia.org/wiki/User:Chabe01)**
  (May 2021),
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) —
  [File:Logo PyCommonist.svg](https://commons.wikimedia.org/wiki/File:Logo_PyCommonist.svg)
  on Wikimedia Commons.
