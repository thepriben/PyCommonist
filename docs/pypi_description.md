# PyCommonist

Desktop application (Python / PyQt6) for batch-uploading images and media to
[Wikimedia Commons](https://commons.wikimedia.org/), inspired by
[Commonist](https://commons.wikimedia.org/wiki/Commons:Commonist).

![PyCommonist logo](https://raw.githubusercontent.com/thepriben/PyCommonist/main/img/PyCommonist.png)

## Installation

```bash
pip install pycommonist
pycommonist
```

Requires Python 3.10–3.12 (PyQt6 has no stable wheels for 3.14 yet).

## Usage

1. Enter your Wikimedia Commons credentials at the top of the window.
   With two-factor authentication, use a
   [bot password](https://commons.wikimedia.org/wiki/Special:BotPasswords)
   in the form `User@BotName`.
2. Open a session via **File → New session**, choosing a template:
   **Description — `{{Information}}`** (default) or **Artwork — `{{Artwork}}`**.
3. Pick a folder on the left, fill in the global and per-file fields,
   tick **Import**, and start the upload.

## Security

- Credentials are sent only to `commons.wikimedia.org` over HTTPS and are
  never stored on disk or written to logs.
- Every API request carries a descriptive `User-Agent` and an explicit
  timeout; authenticated calls use `assert=user` so an expired session fails
  visibly instead of uploading anonymously.
- Bot passwords are supported and recommended.

---

Source code, full project history and license:
[github.com/thepriben/PyCommonist](https://github.com/thepriben/PyCommonist)
