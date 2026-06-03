"""MDI sub-window wrapper for an import session."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMdiSubWindow, QSizePolicy

from pycommonist.core.constants import SESSION_ARTWORK, SESSION_INFORMATION
from pycommonist.sessions.artwork import ArtworkSession
from pycommonist.sessions.information import InformationSession

SESSION_CLASSES = {
    SESSION_INFORMATION: InformationSession,
    SESSION_ARTWORK: ArtworkSession,
}

SESSION_MENU_LABELS = {
    SESSION_INFORMATION: "Description — {{Information}}",
    SESSION_ARTWORK: "Œuvre — {{Artwork}}",
}

SESSION_WINDOW_PREFIX = {
    SESSION_INFORMATION: "Import · {{Information}}",
    SESSION_ARTWORK: "Import · {{Artwork}}",
}


def create_session_window(main_window, session_type: str) -> QMdiSubWindow:
    session_cls = SESSION_CLASSES[session_type]
    session_widget = session_cls(main_window)
    session_widget.setSizePolicy(
        QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
    )
    session_widget.setMinimumSize(960, 640)
    sub = QMdiSubWindow()
    sub.setWidget(session_widget)
    sub.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    session_widget.mdi_sub_window = sub
    session_widget.session_type = session_type
    session_widget.update_window_title()
    return sub
