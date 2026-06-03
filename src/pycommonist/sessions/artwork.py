"""Artwork import session ({{Artwork}})."""

from PyQt6.QtWidgets import QLineEdit, QPlainTextEdit

from pycommonist.core.config import LeftFrameConfig
from pycommonist.core.constants import SESSION_ARTWORK
from pycommonist.core.wikitext import ArtworkWikitextBuilder
from pycommonist.framework.base_session import BaseImportSession


class ArtworkSession(BaseImportSession):
    session_type = SESSION_ARTWORK
    session_label = "Artwork"

    def get_wikitext_builder(self):
        return ArtworkWikitextBuilder()

    def _add_session_fields(self):
        self.line_edit_artist = QLineEdit()
        self._add_form_row("Artist: ", self.line_edit_artist)

        self.line_edit_title = QLineEdit()
        self._add_form_row("Title: ", self.line_edit_title)

        self.line_edit_object_type = QLineEdit()
        self._add_form_row("Object type: ", self.line_edit_object_type)

        self.line_edit_description = QPlainTextEdit()
        self._add_form_row("Description: ", self.line_edit_description)

        self.line_edit_date = QLineEdit()
        self._add_form_row("Date (global): ", self.line_edit_date)

        self.line_edit_medium = QLineEdit()
        self._add_form_row("Medium: ", self.line_edit_medium)

        self.line_edit_institution = QLineEdit()
        self._add_form_row("Institution: ", self.line_edit_institution)

        self.line_edit_source = QLineEdit()
        self.line_edit_source.setText(LeftFrameConfig.source)
        self._add_form_row("Source: ", self.line_edit_source)

        self.line_edit_wikidata = QLineEdit()
        self._add_form_row("Wikidata (Q…): ", self.line_edit_wikidata)

        self.line_edit_categories = QLineEdit()
        self.line_edit_categories.setText(LeftFrameConfig.categories)
        self._add_form_row("Categories: ", self.line_edit_categories)

        self.line_edit_license = QLineEdit()
        self.line_edit_license.setText(LeftFrameConfig.license)
        self._add_form_row("License: ", self.line_edit_license)

        self.line_edit_language = QLineEdit()
        self.line_edit_language.setText(LeftFrameConfig.language)
        self._add_form_row("Language code: ", self.line_edit_language)

    def validate_before_upload(self) -> bool:
        empty_descriptions = 0
        empty_categories = 0
        file_names = []
        for element in self.current_upload:
            if not element.cb_import.isChecked():
                continue
            desc = self.get_global_description_text() + element.line_edit_description.toPlainText()
            if not (desc and desc.strip()):
                empty_descriptions += 1
            categs = self.line_edit_categories.text() + element.line_edit_categories.text()
            if not (categs and categs.strip()):
                empty_categories += 1
            file_names.append(element.line_edit_file_name.text())

        if not self._check_duplicate_names_and_commons(file_names):
            return False
        return self._confirm_empty_fields(empty_descriptions, empty_categories)
