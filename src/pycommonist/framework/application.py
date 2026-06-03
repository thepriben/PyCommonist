"""QApplication bootstrap."""

import os
import sys


def _configure_qt_paths():
    """macOS/Linux: ensure Qt finds platform plugins and frameworks."""
    try:
        import PyQt6
    except ImportError:
        return
    qt6 = os.path.join(os.path.dirname(PyQt6.__file__), 'Qt6')
    plugins = os.path.join(qt6, 'plugins')
    lib = os.path.join(qt6, 'lib')
    os.environ.setdefault('QT_PLUGIN_PATH', plugins)
    os.environ.setdefault(
        'QT_QPA_PLATFORM_PLUGIN_PATH', os.path.join(plugins, 'platforms')
    )
    if sys.platform == 'darwin' and os.path.isdir(lib):
        current = os.environ.get('DYLD_FRAMEWORK_PATH', '')
        if lib not in current.split(os.pathsep):
            os.environ['DYLD_FRAMEWORK_PATH'] = (
                lib + (os.pathsep + current if current else '')
            )
    from PyQt6.QtCore import QCoreApplication
    QCoreApplication.setLibraryPaths([plugins])


_configure_qt_paths()

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from pycommonist.core.constants import PYCOMMONIST_VERSION
from pycommonist.core.resources import resource_path
from pycommonist.framework.main_window import MainWindow
from pycommonist.framework.styles import APP_STYLESHEET


def create_app(argv=None):
    if argv is None:
        argv = sys.argv
    app = QApplication(argv)
    app.setStyleSheet(APP_STYLESHEET)
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
