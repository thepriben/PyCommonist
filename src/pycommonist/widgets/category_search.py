"""Commons category prefix search autocomplete."""

import json

from PyQt6.QtCore import QEvent, QMetaObject, QObject, QPoint, Qt, QTimer, QUrl
from PyQt6.QtGui import QPalette
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QLineEdit,
    QTreeWidget,
    QTreeWidgetItem,
)

from pycommonist.core.constants import WIDTH_WIDGET_RIGHT


class SuggestCompletion(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.editor = parent
        self.popup = QTreeWidget()
        self.popup.setWindowFlags(Qt.WindowType.Popup)
        self.popup.setFocusProxy(self.parent)
        self.popup.setMouseTracking(True)
        self.popup.setColumnCount(1)
        self.popup.setFixedWidth(WIDTH_WIDGET_RIGHT)
        self.popup.setUniformRowHeights(True)
        self.popup.setRootIsDecorated(False)
        self.popup.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.popup.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.popup.setFrameStyle(QFrame.Shape.Box)
        self.popup.setLineWidth(1)
        self.popup.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.popup.header().hide()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(500)
        self.network_manager = QNetworkAccessManager(self)
        self.popup.installEventFilter(self)
        self.popup.itemClicked.connect(self.done_completion)
        self.timer.timeout.connect(self.auto_suggest)
        self.editor.textEdited.connect(self.timer.start)
        self.network_manager.finished.connect(self.handle_network_data)

    def eventFilter(self, obj, event):
        if obj != self.popup:
            return False
        if event.type() == QEvent.Type.MouseButtonPress:
            self.popup.hide()
            self.editor.setFocus()
            return True
        if event.type() == QEvent.Type.KeyPress:
            key = event.key()
            if key in [Qt.Key.Key_Enter, Qt.Key.Key_Return]:
                self.done_completion()
                return True
            if key == Qt.Key.Key_Escape:
                self.editor.setFocus()
                self.popup.hide()
                return True
            if key in [
                Qt.Key.Key_Up, Qt.Key.Key_Down, Qt.Key.Key_Home,
                Qt.Key.Key_End, Qt.Key.Key_PageUp, Qt.Key.Key_PageDown,
            ]:
                return False
            self.editor.setFocus()
            self.editor.event(event)
            self.popup.hide()
            return True
        return False

    def show_completion(self, choices):
        if not choices:
            return
        self.popup.setUpdatesEnabled(False)
        self.popup.clear()
        for choice in choices:
            item = QTreeWidgetItem(self.popup)
            item.setText(0, choice)
        self.popup.setCurrentItem(self.popup.topLevelItem(0))
        self.popup.setUpdatesEnabled(True)
        self.popup.move(self.editor.mapToGlobal(QPoint(0, self.editor.height())))
        self.popup.setFocus()
        self.popup.show()

    def done_completion(self):
        self.timer.stop()
        self.popup.hide()
        self.editor.setFocus()
        item = self.popup.currentItem()
        if item:
            self.editor.setText(item.text(0))
            QMetaObject.invokeMethod(self.editor, 'returnPressed')

    def auto_suggest(self):
        text = self.editor.text()
        req = (
            "https://commons.wikimedia.org/w/api.php?action=query"
            "&list=prefixsearch&format=json&pssearch=Category:" + text
        )
        self.network_manager.get(QNetworkRequest(QUrl(req)))

    def handle_network_data(self, network_reply):
        choices = []
        if network_reply.error() == QNetworkReply.NetworkError.NoError:
            data = json.loads(network_reply.readAll().data())
            for location in data['query']['prefixsearch']:
                choice = location['title']
                choices.append(choice.replace("Category:", ""))
            self.show_completion(choices)
        network_reply.deleteLater()


class SearchBox(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.completer = SuggestCompletion(self)
        self.setFixedWidth(round(WIDTH_WIDGET_RIGHT / 2))
        self.setClearButtonEnabled(True)
