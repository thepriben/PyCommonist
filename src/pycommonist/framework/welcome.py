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
            "Utilisez le menu\n"
            "Fichier → Nouvelle session\n"
            "puis choisissez un modèle Wikimedia :\n"
            "{{Information}} (description) ou {{Artwork}} (œuvre)."
        )
        hint.setObjectName("welcomeHint")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(12)
        layout.addWidget(hint)
