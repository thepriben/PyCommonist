"""Main window with auth panel, MDI upload sessions, and menus."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMdiArea,
    QMenu,
    QMenuBar,
    QStackedWidget,
    QStatusBar,
    QStyle,
    QVBoxLayout,
    QWidget,
)

from pycommonist.core.config import LeftFrameConfig
from pycommonist.core.constants import (
    PYCOMMONIST_VERSION,
    SESSION_ARTWORK,
    SESSION_INFORMATION,
    WIDTH_WIDGET,
)
from pycommonist.framework.mdi_session import (
    SESSION_MENU_LABELS,
    create_session_window,
)
from pycommonist.framework.styles import AUTH_BAR_STYLE
from pycommonist.framework.welcome import WelcomePage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"PyCommonist {PYCOMMONIST_VERSION}")
        self.resize(1280, 840)
        self._session_counter = 0

        self.mdi_area = QMdiArea()
        self.mdi_area.setViewMode(QMdiArea.ViewMode.SubWindowView)
        self.mdi_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.mdi_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.mdi_area.subWindowActivated.connect(self._on_subwindow_activated)

        self._welcome_page = WelcomePage()
        self._workspace = QStackedWidget()
        self._workspace.addWidget(self._welcome_page)
        self._workspace.addWidget(self.mdi_area)

        self._build_menus()

        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(8, 8, 8, 8)
        central_layout.setSpacing(6)
        central_layout.addWidget(self._build_auth_panel())
        central_layout.addWidget(self._workspace, stretch=1)
        self.setCentralWidget(central)

        self.status_label = QLabel()
        self.status_label.setObjectName("statusBarLabel")
        status = QStatusBar()
        status.addWidget(self.status_label, 1)
        self.setStatusBar(status)

        self._show_welcome()

    def _build_auth_panel(self):
        auth_widget = QWidget()
        auth_widget.setObjectName("authBar")
        auth_widget.setStyleSheet(AUTH_BAR_STYLE)
        layout = QFormLayout(auth_widget)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.line_edit_user_name = QLineEdit()
        self.line_edit_user_name.setText(LeftFrameConfig.username)
        self.line_edit_user_name.setFixedWidth(WIDTH_WIDGET)
        self.line_edit_user_name.setPlaceholderText("Commons username (or User@BotName)")

        self.line_edit_password = QLineEdit()
        self.line_edit_password.setFixedWidth(WIDTH_WIDGET)
        self.line_edit_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.line_edit_password.setPlaceholderText("Password or bot password")
        toggle_action = self.line_edit_password.addAction(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogYesButton),
            QLineEdit.ActionPosition.TrailingPosition,
        )
        toggle_action.setToolTip("Show / hide password")
        toggle_action.triggered.connect(self._toggle_password_visibility)

        layout.addRow("Username:", self.line_edit_user_name)
        layout.addRow("Password:", self.line_edit_password)
        return auth_widget

    def _toggle_password_visibility(self):
        if self.line_edit_password.echoMode() == QLineEdit.EchoMode.Password:
            self.line_edit_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.line_edit_password.setEchoMode(QLineEdit.EchoMode.Password)

    def _build_menus(self):
        bar = QMenuBar()

        file_menu = bar.addMenu("File")
        new_menu = QMenu("New session", self)
        new_menu.addAction(
            SESSION_MENU_LABELS[SESSION_INFORMATION],
            lambda: self.open_session(SESSION_INFORMATION),
        )
        new_menu.addAction(
            SESSION_MENU_LABELS[SESSION_ARTWORK],
            lambda: self.open_session(SESSION_ARTWORK),
        )
        file_menu.addMenu(new_menu)
        file_menu.addSeparator()
        file_menu.addAction("Quit", self.close)

        window_menu = bar.addMenu("Window")
        window_menu.addAction("Cascade", self.mdi_area.cascadeSubWindows)
        window_menu.addAction("Tile", self.mdi_area.tileSubWindows)
        window_menu.addSeparator()
        window_menu.addAction("Close active session", self._close_active_subwindow)

        self.setMenuBar(bar)

    def _show_welcome(self):
        self._workspace.setCurrentWidget(self._welcome_page)

    def _show_workspace(self):
        self._workspace.setCurrentWidget(self.mdi_area)

    def _on_subwindow_activated(self, sub):
        if not self.mdi_area.subWindowList():
            self._show_welcome()

    def _close_active_subwindow(self):
        sub = self.mdi_area.activeSubWindow()
        if sub:
            sub.close()

    def open_session(self, session_type: str):
        self._session_counter += 1
        sub = create_session_window(self, session_type)
        widget = sub.widget()
        widget.session_index = self._session_counter
        widget.update_window_title()
        sub.destroyed.connect(lambda *_: self._check_sessions_empty())
        self.mdi_area.addSubWindow(sub)
        self._show_workspace()
        sub.show()
        sub.showMaximized()
        self.set_status(f"Session opened: {SESSION_MENU_LABELS[session_type]}")

    def _check_sessions_empty(self):
        try:
            if not self.mdi_area.subWindowList():
                self._show_welcome()
                self.clear_status()
        except RuntimeError:
            # Qt objects already destroyed during application shutdown.
            pass

    def get_credentials(self):
        return (
            self.line_edit_user_name.text(),
            self.line_edit_password.text(),
        )

    def set_status(self, message: str):
        self.status_label.setText(message)

    def clear_status(self):
        self.status_label.setText("")
