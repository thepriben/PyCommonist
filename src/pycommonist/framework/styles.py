"""Application-wide Qt styles."""

APP_STYLESHEET = """
QMainWindow, QWidget {
    background-color: #f4f4f5;
    color: #18181b;
    font-size: 13px;
}
QMenuBar {
    background-color: #ffffff;
    border-bottom: 1px solid #d4d4d8;
    padding: 2px 0;
}
QMenuBar::item:selected {
    background-color: #e4e4e7;
}
QMenu {
    background-color: #ffffff;
    border: 1px solid #d4d4d8;
}
QLineEdit, QPlainTextEdit {
    background-color: #ffffff;
    border: 1px solid #d4d4d8;
    border-radius: 4px;
    padding: 4px 8px;
    selection-background-color: #3b82f6;
}
QMdiArea {
    background-color: #e4e4e7;
    border: 1px solid #d4d4d8;
}
QMdiSubWindow {
    background-color: #ffffff;
}
QTreeView {
    background-color: #ffffff;
    border: 1px solid #d4d4d8;
    border-radius: 4px;
}
QScrollArea {
    border: none;
    background-color: #fafafa;
}
QStatusBar, QLabel#statusBarLabel {
    background-color: #ffffff;
    border-top: 1px solid #d4d4d8;
}
QPushButton {
    background-color: #ffffff;
    border: 1px solid #d4d4d8;
    border-radius: 4px;
    padding: 6px 12px;
}
QPushButton:hover {
    background-color: #f4f4f5;
}
QPushButton#btnImport {
    background-color: #16a34a;
    color: #ffffff;
    border: none;
    font-size: 18px;
    font-weight: 600;
    padding: 10px 16px;
}
QPushButton#btnImport:hover {
    background-color: #15803d;
}
QPushButton#btnImport:pressed {
    background-color: #166534;
}
"""

AUTH_BAR_STYLE = """
#authBar {
    background-color: #ffffff;
    border: 1px solid #d4d4d8;
    border-radius: 6px;
    margin: 0 0 6px 0;
}
#authHint {
    color: #71717a;
    font-size: 11px;
}
"""

WELCOME_STYLE = """
#welcomePage {
    background-color: #e4e4e7;
}
#welcomeTitle {
    font-size: 22px;
    font-weight: 600;
    color: #18181b;
}
#welcomeHint {
    font-size: 14px;
    color: #52525b;
}
"""
