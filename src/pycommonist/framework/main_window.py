"""Main window with auth panel, MDI area, and menus."""

import webbrowser

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMdiArea,
    QMenuBar,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from pycommonist.core.config import LeftFrameConfig
from pycommonist.core.constants import (
    PYCOMMONIST_VERSION,
    SESSION_ARTWORK,
    SESSION_INFORMATION,
    STYLE_STATUSBAR,
    WIDTH_WIDGET,
)
from pycommonist.framework.mdi_session import create_session_window


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            f"PyCommonist {PYCOMMONIST_VERSION} — Wikimedia Commons"
        )
        self.resize(1200, 800)

        self._build_menus()

        self.mdi_area = QMdiArea()
        self.mdi_area.setViewMode(QMdiArea.ViewMode.TabbedView)
        self.mdi_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.mdi_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(4, 4, 4, 4)
        central_layout.addWidget(self._build_auth_panel())
        central_layout.addWidget(self.mdi_area, stretch=1)
        self.setCentralWidget(central)

        self.status_label = QLabel()
        self.status_label.setStyleSheet(STYLE_STATUSBAR)
        status = QStatusBar()
        status.addWidget(self.status_label, 1)
        self.setStatusBar(status)

        self.open_session(SESSION_INFORMATION)

    def _build_auth_panel(self):
        auth_widget = QWidget()
        layout = QFormLayout()
        layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        self.line_edit_user_name = QLineEdit()
        self.line_edit_user_name.setText(LeftFrameConfig.username)
        self.line_edit_user_name.setFixedWidth(WIDTH_WIDGET)
        self.line_edit_password = QLineEdit()
        self.line_edit_password.setFixedWidth(WIDTH_WIDGET)
        self.line_edit_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Username:", self.line_edit_user_name)
        layout.addRow("Password:", self.line_edit_password)
        help_btn = QPushButton("Commons upload help")
        help_btn.clicked.connect(
            lambda: webbrowser.open(
                "https://commons.wikimedia.org/wiki/Commons:Commonist/fr"
            )
        )
        row = QHBoxLayout()
        row.addLayout(layout)
        row.addWidget(help_btn)
        row.addStretch()
        auth_widget.setLayout(row)
        return auth_widget

    def _build_menus(self):
        bar = QMenuBar()
        file_menu = bar.addMenu("Fichier")
        new_info = file_menu.addAction("Nouvelle session — Information (Description)")
        new_info.triggered.connect(lambda: self.open_session(SESSION_INFORMATION))
        new_art = file_menu.addAction("Nouvelle session — Artwork")
        new_art.triggered.connect(lambda: self.open_session(SESSION_ARTWORK))
        file_menu.addSeparator()
        file_menu.addAction("Quitter", self.close)

        window_menu = bar.addMenu("Fenêtre")
        window_menu.addAction("Cascade", self.mdi_area.cascadeSubWindows)
        window_menu.addAction("Mosaïque", self.mdi_area.tileSubWindows)
        window_menu.addAction("Fermer la session active", self._close_active_subwindow)

        self.setMenuBar(bar)

    def _close_active_subwindow(self):
        sub = self.mdi_area.activeSubWindow()
        if sub:
            sub.close()

    def open_session(self, session_type: str):
        sub = create_session_window(self, session_type)
        self.mdi_area.addSubWindow(sub)
        sub.show()
        sub.showMaximized()

    def get_credentials(self):
        return (
            self.line_edit_user_name.text(),
            self.line_edit_password.text(),
        )

    def set_status(self, message: str):
        self.status_label.setText(message)

    def clear_status(self):
        self.status_label.setText("")
