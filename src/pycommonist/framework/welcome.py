"""Empty-state panel before any upload session is opened."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from pycommonist.framework.styles import WELCOME_STYLE


class WelcomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("welcomePage")
        self.setStyleSheet(WELCOME_STYLE)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title = QLabel("PyCommonist")
        title.setObjectName("welcomeTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint = QLabel(
            "Use the menu\n"
            "File → New session\n"
            "then pick a Wikimedia template:\n"
            "{{Information}} (description) or {{Artwork}} (artwork)."
        )
        hint.setObjectName("welcomeHint")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(12)
        layout.addWidget(hint)
