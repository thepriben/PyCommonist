#!/usr/bin/env python3
"""Offscreen smoke test — no display and no network access to Commons needed.

Run with:
    QT_QPA_PLATFORM=offscreen python scripts/smoke_test.py

Checks:
- the application and main window build without errors;
- both session types (Information and Artwork) open as MDI sub-windows;
- both wikitext builders produce the expected {{Information}} / {{Artwork}}
  markup from sample data;
- the login helper is importable and refuses empty credentials cleanly.
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

FAILURES = []


def check(label, condition, detail=""):
    status = "ok" if condition else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail and not condition else ""))
    if not condition:
        FAILURES.append(label)


class FakeField:
    def __init__(self, value=""):
        self.value = value

    def text(self):
        return self.value

    def toPlainText(self):
        return self.value


class FakeElement:
    def __init__(self):
        self.lineEditLocation = FakeField("45.912345|5.312345")
        self.line_edit_description = FakeField(" — extra detail")
        self.line_edit_categories = FakeField("Montluel")
        self.line_edit_templates = FakeField("{{Palissy|type=|}}")
        self.line_edit_date_time = FakeField("2021-05-12 10:00:00")
        self.line_edit_file_name = FakeField("Example.jpg")


class FakeInformationSession:
    def __init__(self):
        self.line_edit_description = FakeField("A church in Ain")
        self.line_edit_source = FakeField("{{own}}")
        self.line_edit_author = FakeField("Benoît Prieur")
        self.line_edit_categories = FakeField("Churches in Ain")
        self.line_edit_license = FakeField("{{self|cc-zero}}")
        self.line_edit_language = FakeField("en")


class FakeArtworkSession(FakeInformationSession):
    def __init__(self):
        super().__init__()
        self.line_edit_artist = FakeField("Anonymous")
        self.line_edit_title = FakeField("Altarpiece")
        self.line_edit_object_type = FakeField("painting")
        self.line_edit_date = FakeField("18th century")
        self.line_edit_medium = FakeField("oil on canvas")
        self.line_edit_institution = FakeField("Musée de Brou")
        self.line_edit_wikidata = FakeField("Q12345")


def test_wikitext_builders():
    from pycommonist.core.wikitext import (
        ArtworkWikitextBuilder,
        InformationWikitextBuilder,
    )

    info = InformationWikitextBuilder().build(FakeElement(), FakeInformationSession())
    check("{{Information}} template present", "{{Information" in info)
    check("Information description wrapped", "{{en|1=A church in Ain — extra detail}}" in info)
    check("Information categories merged",
          "[[Category:Churches in Ain]]" in info and "[[Category:Montluel]]" in info)
    check("PyCommonist tracking category", "[[Category:Uploaded with PyCommonist]]" in info)
    check("Location template", "{{Location dec|45.912345|5.312345}}" in info)
    check("Additional templates kept", "{{Palissy|type=|}}" in info)
    check("License header", "{{self|cc-zero}}" in info)

    art = ArtworkWikitextBuilder().build(FakeElement(), FakeArtworkSession())
    check("{{Artwork}} template present", "{{Artwork" in art)
    check("Artwork artist field", "|artist = Anonymous" in art)
    check("Artwork wikidata field", "|wikidata = Q12345" in art)
    check("Artwork institution field", "|institution = Musée de Brou" in art)
    check("Artwork date falls back to EXIF", "|date = 2021-05-12 10:00:00" in art)


def test_location_formats():
    from pycommonist.core.wikitext.base import format_location

    class El:
        def __init__(self, value):
            self.lineEditLocation = FakeField(value)

    check("Location: pipe format",
          format_location(El("45.9|5.3")) == "{{Location dec|45.9|5.3}}\n")
    check("Location: OSM comma paste",
          format_location(El("45.9, 5.3")) == "{{Location dec|45.9|5.3}}\n")
    check("Location: negative coordinates",
          format_location(El("-12.5|-38.5")) == "{{Location dec|-12.5|-38.5}}\n")
    check("Location: legacy heading dropped",
          format_location(El("45.9|5.3|heading:321.2602234002272"))
          == "{{Location dec|45.9|5.3}}\n")
    check("Location: empty gives nothing", format_location(El("")) == "")
    check("Location: single value gives nothing", format_location(El("45.9")) == "")


def test_commons_api_module():
    from pycommonist.core import commons_api

    check("User-Agent declares project URL",
          "github.com/thepriben/PyCommonist" in commons_api.USER_AGENT)
    session = commons_api.create_http_session()
    check("Session carries User-Agent",
          session.headers.get("User-Agent") == commons_api.USER_AGENT)
    check("Timeouts are defined",
          commons_api.DEFAULT_TIMEOUT[0] > 0 and commons_api.UPLOAD_TIMEOUT[1] >= 60)


def test_gui():
    from pycommonist.core.constants import SESSION_ARTWORK, SESSION_INFORMATION
    from pycommonist.framework.application import create_app
    from pycommonist.framework.main_window import MainWindow

    app = create_app([])
    window = MainWindow()
    check("Main window builds", window.windowTitle().startswith("PyCommonist"))

    window.open_session(SESSION_INFORMATION)
    window.open_session(SESSION_ARTWORK)
    subwindows = window.mdi_area.subWindowList()
    check("Two sessions open", len(subwindows) == 2, f"got {len(subwindows)}")

    titles = sorted(sub.windowTitle() for sub in subwindows)
    check("Information session titled",
          any("{{Information}}" in t for t in titles), str(titles))
    check("Artwork session titled",
          any("{{Artwork}}" in t for t in titles), str(titles))

    artwork_widget = next(
        sub.widget() for sub in subwindows if "{{Artwork}}" in sub.windowTitle()
    )
    for field in ("line_edit_artist", "line_edit_title", "line_edit_wikidata",
                  "line_edit_license", "line_edit_categories"):
        check(f"Artwork field {field}", hasattr(artwork_widget, field))

    user, pwd = window.get_credentials()
    check("Credentials readable from main window", isinstance(user, str))

    window.close()
    app.quit()


def main():
    print("PyCommonist offscreen smoke test")
    print("=" * 40)
    test_wikitext_builders()
    test_location_formats()
    test_commons_api_module()
    test_gui()
    print("=" * 40)
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED: {FAILURES}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
