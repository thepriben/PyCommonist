"""QApplication bootstrap."""

import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from pycommonist.core.constants import PYCOMMONIST_VERSION
from pycommonist.core.resources import resource_path
from pycommonist.framework.main_window import MainWindow


def create_app(argv=None):
    if argv is None:
        argv = sys.argv
    app = QApplication(argv)
    app.setApplicationName("PyCommonist")
    app.setApplicationVersion(PYCOMMONIST_VERSION)
    icon_path = resource_path("img", "Logo PyCommonist.svg")
    app.setWindowIcon(QIcon(icon_path))
    return app


def run(argv=None):
    app = create_app(argv)
    window = MainWindow()
    window.showMaximized()
    return app.exec()
