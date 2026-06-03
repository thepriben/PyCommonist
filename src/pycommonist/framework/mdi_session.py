"""MDI sub-window wrapper for an import session."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMdiSubWindow

from pycommonist.core.constants import SESSION_ARTWORK, SESSION_INFORMATION
from pycommonist.sessions.artwork import ArtworkSession
from pycommonist.sessions.information import InformationSession

SESSION_CLASSES = {
    SESSION_INFORMATION: InformationSession,
    SESSION_ARTWORK: ArtworkSession,
}


def create_session_window(main_window, session_type: str) -> QMdiSubWindow:
    session_cls = SESSION_CLASSES[session_type]
    session_widget = session_cls(main_window)
    sub = QMdiSubWindow()
    sub.setWidget(session_widget)
    sub.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    session_widget.mdi_sub_window = sub
    session_widget.update_window_title()
    return sub
