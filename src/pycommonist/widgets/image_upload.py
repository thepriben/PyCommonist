"""Per-image row widget."""

from PyQt6.QtWidgets import QWidget


class ImageUpload(QWidget):
    def on_pressed(self):
        content = str(self.line_edit_categories.text())
        searchbox = str(self.searchBoxCategory.text())
        if content == "":
            self.line_edit_categories.setText(searchbox)
        else:
            self.line_edit_categories.setText(content + "|" + searchbox)
