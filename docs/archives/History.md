# PyCommonist History

GitHub repository: [thepriben/PyCommonist](https://github.com/thepriben/PyCommonist)
— maintained by **[@thepriben](https://github.com/thepriben)** (Benoît Prieur).

The git history is kept under the single maintainer identity `thepriben`.
This page is the authoritative record of **all** historical contributions,
using the **Wikimedia Commons** usernames (`User:…`) as they were at the time.
In particular:

- **Romain Behar** (`User:Romainbar`) contributed numerous features between
  2021 and 2023 — every one of them is listed below.
- The PyCommonist **logo** was created by **Chabe01** (May 2021).

The project is also the subject of a magazine article (in French):
Benoît Prieur, *PyQt5 : développement d'une application de téléversement
d'images vers Wikimedia Commons*, 2021, **Programmez!** n°246, pp. 33–39
([programmez.com](https://www.programmez.com/magazine/article/pyqt5-developpement-dune-application-de-televersement-dimages-vers-wikimedia-commons)).

---

* July 2026: [@thepriben](https://github.com/thepriben) / User:Benoît Prieur — v1.2
  * hardened Commons API client (`core/commons_api.py`): descriptive
    User-Agent, explicit timeouts on every request, `assert=user` on
    authenticated calls, bot-password (`action=login`) support, no
    credentials or tokens in the logs
  * clear sign-in error messages (including a two-factor / bot-password hint)
  * show/hide password toggle and security hint in the auth panel
  * filename-existence check switched to the Commons API
  * URL-encoded category autocompletion queries
  * fixed a crash when closing the application with open sessions
  * user interface and all documentation translated to English
  * offscreen smoke test (`scripts/smoke_test.py`)
* June 2026: [@thepriben](https://github.com/thepriben) / User:Benoît Prieur — v1.1, major overhaul
  * PyPI package `pycommonist` (`src/` layout, `pyproject.toml`)
  * `QMainWindow` main window with centralized credentials
  * upload sessions as MDI sub-windows (`QMdiArea`)
  * built-in session types: **Information (Description)** (`{{Information}}`)
    and **Artwork** (`{{Artwork}}`)
  * small PyQt6 framework (`framework/`, `sessions/`, `core/wikitext/`)
  * refactored upload service (`UploadService`, injected wikitext builders, logging)
  * source archive **`pycommonist-v1.1.zip`** (same convention as `pycommonist-v1.0`)
  * archive documents in `docs/archives/`, `codemeta.json` metadata
* 4 September 2024: User:Benoît Prieur
  * updated `requirements.txt` (PyQt6 and dependencies)
* July 2023: User:Benoît Prieur
  * migration from PyQt5 to PyQt6
* 16 February 2023: User:Romainbar
  * image context menu: option to edit the image in Gimp
* 15 February 2023: User:Romainbar
  * display of the image size in megabytes (after the date)
* 17 November 2022: User:Romainbar
  * OGV video format support
* 14 October 2022: User:Romainbar
  * button to open the geographic location in OpenStreetMap, and button to clear it
* 22 August 2022: User:Romainbar
  * new per-image input: additional templates, e.g. for `{{Palissy|type=|}}`
* 23 July 2022: User:Romainbar
  * image context menu: option to move the image to the trash
* 19 June 2022: User:Romainbar
  * template support in the category list
* 10 June 2022: User:Romainbar
  * image count added to the sort button
* 6 June 2022: User:Romainbar
  * image context menu: option to remove the image from the list
* 29 May 2022: User:Romainbar
  * display of the image in Preview (macOS) by clicking on it
* 29 May 2022: User:Benoît Prieur
  * more PEP8 work
  * check that the file name is not already in use (locally and on Wikimedia Commons)
* 28 May 2022: User:Benoît Prieur
  * PEP8 formatting pass (pylint under VS Code)
  * added a PyCommonist version number
  * wider autocompletion popup
* 10 May 2022: User:Romainbar
  * number of images ready for upload displayed in the import button
* 6 December 2021: User:Romainbar
  * display of the number of images processed during upload
* 13 June 2021: User:Romainbar
  * confirmation dialog before upload when a description or category is empty
  * successfully uploaded images are unchecked
* 12 June 2021: User:Romainbar
  * button to copy and paste name, description and categories from one image to another
  * option to automatically increment the last number contained in the name
* 2 June 2021: User:Romainbar
  * button to reload the image list from the last selected folder
* 31 May 2021: User:Romainbar
  * correct display of the total of successful and failed uploads
* 21 May 2021: Chabe01
  * new PyCommonist logo
* 14 May 2021: User:Romainbar
  * button to toggle the image sort order, between file name (default) and EXIF date
  * import checkboxes turned into buttons and moved to the right frame
  * import checkbox automatically set to True when the image name is changed
* 12 May 2021: User:Romainbar
  * support for addresses copied from OSM
  * if the default categories box is empty, the line is not created on the page
  * language code added for the description
* 2 May 2021: User:Benoît Prieur
  * category auto-suggestion (idea by User:Romainbar, thanks to him)
* 20 April 2021: User:Benoît Prieur
  * external configuration file (largely inspired by code from User:Deansfa, thanks to him)
* January 2021: User:Benoît Prieur
  * initial versions of PyCommonist (PyQt5), described in the
    Programmez! n°246 article
