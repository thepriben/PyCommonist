"""Information / Description import session ({{Information}})."""

from PyQt6.QtWidgets import QLineEdit, QPlainTextEdit

from pycommonist.core.config import LeftFrameConfig
from pycommonist.core.constants import SESSION_INFORMATION
from pycommonist.core.wikitext import InformationWikitextBuilder
from pycommonist.framework.base_session import BaseImportSession


class InformationSession(BaseImportSession):
    session_type = SESSION_INFORMATION
    session_label = "Information (Description)"

    def get_wikitext_builder(self):
        return InformationWikitextBuilder()

    def _add_session_fields(self):
        self.line_edit_source = QLineEdit()
        self.line_edit_source.setText(LeftFrameConfig.source)
        self._add_form_row("Source: ", self.line_edit_source)

        self.line_edit_author = QLineEdit()
        self.line_edit_author.setText(LeftFrameConfig.author)
        self._add_form_row("Author: ", self.line_edit_author)

        self.line_edit_categories = QLineEdit()
        self.line_edit_categories.setText(LeftFrameConfig.categories)
        self._add_form_row("Categories: ", self.line_edit_categories)

        self.line_edit_license = QLineEdit()
        self.line_edit_license.setText(LeftFrameConfig.license)
        self._add_form_row("License: ", self.line_edit_license)

        self.line_edit_language = QLineEdit()
        self.line_edit_language.setText(LeftFrameConfig.language)
        self._add_form_row("Language code: ", self.line_edit_language)

        self.line_edit_description = QPlainTextEdit()
        self._add_form_row("Description: ", self.line_edit_description)

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
