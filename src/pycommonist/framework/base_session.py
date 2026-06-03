"""Base import session widget (folder tree + image list + upload)."""

import logging
import os
import platform
import re
import subprocess
import traceback
import webbrowser
from os.path import isfile, join

import exifread
import requests
from PyQt6.QtCore import QDir, QProcess, QSize, Qt
from PyQt6.QtGui import QCursor, QFileSystemModel, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QStyle,
    QTreeView,
    QVBoxLayout,
    QWidget,
)
from send2trash import send2trash

from pycommonist.core.config import RightFrameConfig
from pycommonist.core.constants import (
    CHECK_BUTTON_ALL,
    CHECK_BUTTON_NONE,
    HORIZONTAL_LEFT_SIZE,
    HORIZONTAL_RIGHT_SIZE,
    IMAGE_CATEGORIES,
    IMAGE_DATE_TIME,
    IMAGE_DESCRIPTION,
    IMAGE_DIMENSION,
    IMAGE_NAME,
    IMAGE_LOCATION,
    IMAGE_SIZE,
    IMAGE_TEMPLATES,
    IMPORT_BUTTON_N_IMAGES,
    IMPORT_BUTTON_NO_IMAGE,
    MENU_DELETE_IMAGE,
    MENU_EDIT_IMAGE_GIMP,
    MENU_REMOVE_IMAGE,
    RELOAD_BUTTON,
    SORT_BUTTON_BY_DATE,
    SORT_BUTTON_BY_NAME,
    STYLE_IMPORT_BUTTON,
    STYLE_IMPORT_STATUS,
    VERTICAL_BOTTOM_SIZE,
    VERTICAL_TOP_SIZE,
    WIDTH_WIDGET,
    WIDTH_WIDGET_RIGHT,
)
from pycommonist.core.exif_image import EXIFImage
from pycommonist.core.gps_location import get_exif_location
from pycommonist.core.resources import resource_path
from pycommonist.core.upload_service import UploadService
from pycommonist.widgets.category_search import SearchBox
from pycommonist.widgets.image_upload import ImageUpload

logger = logging.getLogger(__name__)

MEDIA_EXTENSIONS = (".JPEG", ".JPG", ".OGV", ".SVG", ".WEBM", ".PNG")


class BaseImportSession(QWidget):
    """Shared MDI session: splitter layout, media loading, image rows, upload."""

    session_type: str = "base"
    session_label: str = "Session"

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.mdi_sub_window = None
        self.upload_service = UploadService()
        self.threads = []
        self.workers = []
        self.current_directory_path = ''
        self.copied_name = ''
        self.copied_description = ''
        self.copied_categories = ''
        self.copied_templates = ''
        self.upload_failures = 0
        self.upload_status_dots = 0
        self.current_upload = []
        self.exif_image_collection = []
        self.image_sort_order = RightFrameConfig.default_image_sort
        self.number_images_checked = 0
        self.upload_successes = 0

        self._build_layout()
        self.init_upload(0)
        self.update_window_title()

    def get_wikitext_builder(self):
        raise NotImplementedError

    def _build_layout(self):
        self.left_top_frame = QFrame()
        self.left_top_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.right_widget = QWidget()
        self.right_widget.setMinimumWidth(480)
        self.right_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.layout_right = QVBoxLayout()
        self.right_widget.setLayout(self.layout_right)
        self._build_right_toolbar()
        self.scroll = QScrollArea()
        self.layout_right.addWidget(self.scroll)
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget(self.scroll)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll.setWidget(self.scroll_content)

        self._build_left_top_frame()

        self.left_bottom_frame = QFrame()
        self.left_bottom_frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout_left_bottom = QVBoxLayout()
        self.model_tree = QFileSystemModel()
        self.model_tree.setRootPath(QDir.currentPath())
        self.model_tree.setFilter(QDir.Filter.Dirs)
        self.tree_left_bottom = QTreeView()
        self.tree_left_bottom.setModel(self.model_tree)
        self.tree_left_bottom.setAnimated(False)
        self.tree_left_bottom.setIndentation(10)
        self.tree_left_bottom.setColumnWidth(0, 300)
        self.tree_left_bottom.expandAll()
        self.tree_left_bottom.selectionModel().selectionChanged.connect(
            self.on_select_folder
        )
        layout_left_bottom.addWidget(self.tree_left_bottom)
        self.left_bottom_frame.setLayout(layout_left_bottom)

        self.splitter_left = QSplitter(Qt.Orientation.Vertical)
        self.splitter_left.addWidget(self.left_top_frame)
        self.splitter_left.addWidget(self.left_bottom_frame)
        self.splitter_left.setSizes([VERTICAL_TOP_SIZE, VERTICAL_BOTTOM_SIZE])

        self.splitter_central = QSplitter(Qt.Orientation.Horizontal)
        self.splitter_central.addWidget(self.splitter_left)
        self.splitter_central.addWidget(self.right_widget)
        self.splitter_central.setStretchFactor(0, 1)
        self.splitter_central.setStretchFactor(1, 3)
        self.splitter_central.setSizes([HORIZONTAL_LEFT_SIZE, HORIZONTAL_RIGHT_SIZE])
        self.splitter_central.setCollapsible(1, False)

        root = QVBoxLayout()
        root.addWidget(self.splitter_central)
        self.setLayout(root)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        total = max(self.splitter_central.width(), 800)
        self.splitter_central.setSizes([int(total * 0.32), int(total * 0.68)])

    def _build_left_top_frame(self):
        self.layout_left_top = QFormLayout()
        self.layout_left_top.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        self._add_session_fields()
        sep = QLabel()
        self.layout_left_top.addWidget(sep)
        import_widget = QWidget()
        import_layout = QHBoxLayout()
        import_widget.setLayout(import_layout)
        self.btn_import = QPushButton(IMPORT_BUTTON_NO_IMAGE)
        self.btn_import.clicked.connect(self.on_click_import)
        import_layout.addWidget(self.btn_import)
        self.layout_left_top.addWidget(import_widget)
        import_widget.setStyleSheet("border:1px solid #808080;")
        self.btn_import.setStyleSheet(STYLE_IMPORT_BUTTON)
        self.left_top_frame.setLayout(self.layout_left_top)

    def _add_session_fields(self):
        """Override in subclasses to add type-specific form fields."""
        pass

    def _add_form_row(self, label_text: str, widget):
        lbl = QLabel(label_text)
        lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        if isinstance(widget, QLineEdit):
            widget.setFixedWidth(WIDTH_WIDGET)
            widget.setAlignment(Qt.AlignmentFlag.AlignLeft)
        elif isinstance(widget, QPlainTextEdit):
            widget.setFixedWidth(WIDTH_WIDGET)
        self.layout_left_top.addRow(lbl, widget)

    def _build_right_toolbar(self):
        import_command_widget = QWidget()
        import_command_layout = QHBoxLayout()
        import_command_widget.setLayout(import_command_layout)
        self.btn_toggle_image_sort = QPushButton(SORT_BUTTON_BY_NAME)
        self.btn_toggle_image_sort.clicked.connect(self.btn_toggle_image_sort_order)
        self.btn_import_check_none = QPushButton(CHECK_BUTTON_NONE)
        self.btn_import_check_none.clicked.connect(self.btn_select_no_image)
        self.btn_import_check_all = QPushButton(CHECK_BUTTON_ALL)
        self.btn_import_check_all.clicked.connect(self.btn_select_all_images)
        self.btn_reload_folder = QPushButton(RELOAD_BUTTON)
        self.btn_reload_folder.clicked.connect(self.load_media_from_current_folder)
        for btn in (
            self.btn_toggle_image_sort,
            self.btn_import_check_none,
            self.btn_import_check_all,
            self.btn_reload_folder,
        ):
            import_command_layout.addWidget(btn)
        self.layout_right.addWidget(import_command_widget)

    def update_window_title(self):
        folder = os.path.basename(self.current_directory_path) if self.current_directory_path else ""
        title = f"{self.session_label}"
        if folder:
            title += f" — {folder}"
        if self.mdi_sub_window:
            self.mdi_sub_window.setWindowTitle(title)

    def on_select_folder(self, selected):
        try:
            current_index = selected.indexes()[0]
            self.current_directory_path = self.model_tree.filePath(current_index)
            logger.debug("Selected directory: %s", self.current_directory_path)
        except (ValueError, IndexError):
            traceback.print_exc()
        self.load_media_from_current_folder()

    def load_media_from_current_folder(self):
        try:
            self.main_window.clear_status()
            self.exif_image_collection = []
            if self.current_directory_path.strip() == "":
                self.generate_right_frame()
                return
            list_dir = os.listdir(self.current_directory_path)
            files = [f for f in sorted(list_dir) if isfile(join(self.current_directory_path, f))]
            for file in files:
                full_file_path = os.path.join(self.current_directory_path, file)
                if not full_file_path.upper().endswith(MEDIA_EXTENSIONS):
                    continue
                current_exif_image = EXIFImage()
                current_exif_image.full_file_path = full_file_path
                current_exif_image.filename = file
                filesize = os.path.getsize(full_file_path)
                current_exif_image.filesize = "%.1f MB" % (filesize / 1e6)
                tags = None
                try:
                    with open(full_file_path, 'rb') as f_exif:
                        tags = exifread.process_file(f_exif)
                except ValueError:
                    logger.warning("EXIF read failed for %s", full_file_path)
                try:
                    current_exif_image.lat, current_exif_image.long, current_exif_image.heading = (
                        get_exif_location(tags)
                    )
                except (ValueError, TypeError):
                    pass
                dt_timestamp = None
                try:
                    if tags and 'EXIF DateTimeOriginal' in tags:
                        dt_timestamp = tags['EXIF DateTimeOriginal']
                except ValueError:
                    pass
                self.exif_image_collection.append(current_exif_image)
                if dt_timestamp is not None:
                    dt_timestamp = str(dt_timestamp)
                    index_space = dt_timestamp.find(" ")
                    current_exif_image.date = dt_timestamp[0:index_space].replace(":", "-")
                    current_exif_image.time = dt_timestamp[index_space + 1:]
                else:
                    current_exif_image.date = ''
                    current_exif_image.time = ''
            self.generate_right_frame()
        except ValueError:
            logger.exception("load_media_from_current_folder failed")
        self.update_window_title()

    def btn_toggle_image_sort_order(self):
        if not hasattr(self, 'current_upload') or len(self.current_upload) == 0:
            return
        if self.image_sort_order == "file_name":
            self.image_sort_order = "exif_date"
        else:
            self.image_sort_order = "file_name"
        self.generate_right_frame()

    def btn_select_no_image(self):
        if hasattr(self, 'current_upload') and self.current_upload:
            for element in self.current_upload:
                element.cb_import.setChecked(False)

    def btn_select_all_images(self):
        if hasattr(self, 'current_upload') and self.current_upload:
            for element in self.current_upload:
                element.cb_import.setChecked(True)

    def on_toggle_import(self):
        selected = sum(1 for el in self.current_upload if el.cb_import.isChecked())
        if selected == 0:
            self.btn_import.setText(IMPORT_BUTTON_NO_IMAGE)
        else:
            self.btn_import.setText(IMPORT_BUTTON_N_IMAGES.format(selected))
            self.btn_import.setEnabled(True)

    def get_global_description_text(self) -> str:
        return self.line_edit_description.toPlainText()

    def validate_before_upload(self) -> bool:
        """Return False if upload should abort."""
        return True

    def on_click_import(self):
        try:
            self.btn_import.setEnabled(False)
            if not self.current_upload:
                self.btn_import.setEnabled(True)
                return
            if not self.validate_before_upload():
                self.btn_import.setEnabled(True)
                return
            login, password = self.main_window.get_credentials()
            self.upload_service.upload_images(self, login, password)
        except ValueError:
            self.btn_import.setEnabled(True)
            traceback.print_exc()

    def _check_duplicate_names_and_commons(self, file_names) -> bool:
        if not self._is_unique_values_array(file_names):
            msg = QMessageBox(self)
            msg.setWindowTitle('Problem with local file names')
            msg.setText('At least two files locally have the same name')
            msg.exec()
            return False
        try:
            for file_name in file_names:
                response = requests.get(
                    'https://commons.wikimedia.org/wiki/File:' + file_name,
                    timeout=30,
                )
                if response.status_code == 200:
                    msg = QMessageBox(self)
                    msg.setWindowTitle('File name already exists on Wikimedia Commons')
                    msg.setText(
                        file_name + ': file name already exists on Wikimedia Commons'
                    )
                    msg.exec()
                    return False
        except requests.exceptions.RequestException:
            logger.exception("Commons filename check failed")
            return False
        return True

    def _confirm_empty_fields(self, empty_descriptions, empty_categories) -> bool:
        if empty_descriptions > 0:
            confirmation = QMessageBox.question(
                self,
                'Incomplete Descriptions',
                f'There are {empty_descriptions} image(s) without description, continue upload?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if confirmation == QMessageBox.StandardButton.No:
                return False
        if empty_categories > 0:
            confirmation = QMessageBox.question(
                self,
                'Incomplete Categories',
                f'There are {empty_categories} image(s) without category, continue upload?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if confirmation == QMessageBox.StandardButton.No:
                return False
        return True

    def _is_unique_values_array(self, mylist):
        return len(mylist) == len(set(mylist))

    def on_click_clear_location(self, image_widget):
        image_widget.lineEditLocation.setText("")

    def on_click_view_location(self, image_widget):
        loc = image_widget.lineEditLocation.text()
        if loc:
            numbers = re.findall(r"-?\d+\.?\d*", loc)
            if len(numbers) >= 2:
                url = "https://www.openstreetmap.org/search?query={}%2C{}".format(
                    numbers[0], numbers[1]
                )
                webbrowser.open(url)

    def on_click_preview_image(self, image_widget):
        process = QProcess()
        process.start('open', ['-a', 'Preview', image_widget.full_file_path])
        process.waitForFinished(-1)

    def on_thumbnail_context_menu(self, image_widget):
        menu = QMenu()
        delete_action = menu.addAction(MENU_DELETE_IMAGE)
        remove_action = menu.addAction(MENU_REMOVE_IMAGE)
        edit_action = menu.addAction(MENU_EDIT_IMAGE_GIMP)
        action = menu.exec(QCursor.pos())
        file_path = image_widget.full_file_path
        if action == delete_action:
            send2trash(file_path)
            self.remove_file_from_list(file_path)
        elif action == remove_action:
            self.remove_file_from_list(file_path)
        elif action == edit_action:
            if platform.system() == 'Darwin':
                gimp_path = subprocess.check_output([
                    "find", "/Applications", "-type", "f", "-perm", "+111",
                    "-name", "gimp", "-print", "-quit",
                ])
                gimp_path = gimp_path.decode('UTF-8').strip()
                if gimp_path.endswith("gimp"):
                    subprocess.Popen([gimp_path, image_widget.full_file_path])

    def remove_file_from_list(self, file_path):
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i)
            widget = item.widget()
            if widget and widget.full_file_path == file_path:
                widget.deleteLater()
                removed_image = next(
                    (e for e in self.exif_image_collection if e.full_file_path == file_path),
                    None,
                )
                if removed_image:
                    self.exif_image_collection.remove(removed_image)
                removed_widget = next(
                    (w for w in self.current_upload if w.full_file_path == file_path),
                    None,
                )
                if removed_widget:
                    self.current_upload.remove(removed_widget)
                self.on_toggle_import()
                self.update_sort_button()
                break

    def clean_threads(self):
        try:
            for thread in self.threads:
                thread.quit()
                thread.wait()
        except ValueError:
            logger.warning("Problem cleaning upload threads")

    def update_sort_button(self):
        image_count = len(self.exif_image_collection)
        suffix = f" ({image_count})"
        if self.image_sort_order == "exif_date":
            self.btn_toggle_image_sort.setText(SORT_BUTTON_BY_DATE + suffix)
        else:
            self.btn_toggle_image_sort.setText(SORT_BUTTON_BY_NAME + suffix)

    def generate_right_frame(self):
        self.current_upload = []
        layout = self.scroll_layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if self.image_sort_order == "exif_date":
            self.exif_image_collection.sort(
                key=lambda image: image.date + ' ' + image.time
            )
        else:
            self.exif_image_collection.sort(key=lambda image: image.filename)
        self.update_sort_button()

        logo_path = resource_path("img", "Logo PyCommonist.svg")

        for current_exif_image in self.exif_image_collection:
            local_widget = ImageUpload()
            local_layout = QHBoxLayout()
            local_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            local_widget.setLayout(local_layout)
            self.scroll_layout.addWidget(local_widget)
            self.current_upload.append(local_widget)

            local_left_widget = QWidget()
            local_left_layout = QFormLayout()
            local_left_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            local_left_widget.setLayout(local_left_layout)
            local_layout.addWidget(local_left_widget)

            cb_import = QCheckBox("Import")
            cb_import.toggled.connect(self.on_toggle_import)
            lbl_upload_result = QLabel()
            lbl_upload_result.setStyleSheet(STYLE_IMPORT_STATUS)
            btn_copy_paste = QPushButton("Copy/Paste")
            result_layout = QHBoxLayout()
            result_layout.addWidget(lbl_upload_result, 3)
            result_layout.addWidget(btn_copy_paste, 1)
            copy_paste_menu = QMenu()
            copy_action = copy_paste_menu.addAction("Copy")
            paste_action = copy_paste_menu.addAction(
                "Paste name, description and categories"
            )
            paste_with_numbering_action = copy_paste_menu.addAction(
                "Paste name with numbering, description and categories"
            )
            btn_copy_paste.setMenu(copy_paste_menu)
            local_left_layout.addRow(cb_import, result_layout)
            local_widget.cb_import = cb_import
            local_widget.lbl_upload_result = lbl_upload_result
            local_widget.btn_copy_paste = btn_copy_paste

            line_edit_file_name = QLineEdit()
            line_edit_file_name.setFixedWidth(WIDTH_WIDGET_RIGHT)
            line_edit_file_name.setText(current_exif_image.filename)
            line_edit_file_name.textChanged.connect(
                lambda _state, w=cb_import: w.setChecked(True)
            )
            local_left_layout.addRow(QLabel(IMAGE_NAME), line_edit_file_name)
            local_widget.line_edit_file_name = line_edit_file_name
            lbl_real_file_name = QLineEdit()
            lbl_real_file_name.setText(current_exif_image.filename)
            lbl_real_file_name.setVisible(False)
            local_widget.lbl_real_file_name = lbl_real_file_name

            line_edit_description = QPlainTextEdit()
            line_edit_description.setFixedWidth(WIDTH_WIDGET_RIGHT)
            local_left_layout.addRow(QLabel(IMAGE_DESCRIPTION), line_edit_description)
            local_widget.line_edit_description = line_edit_description

            search_box_category = SearchBox()
            search_box_category.setFixedWidth(WIDTH_WIDGET_RIGHT)
            local_left_layout.addRow(QLabel(IMAGE_CATEGORIES), search_box_category)
            local_widget.searchBoxCategory = search_box_category
            line_edit_categories = QLineEdit()
            line_edit_categories.setFixedWidth(WIDTH_WIDGET_RIGHT)
            local_left_layout.addRow(QLabel(""), line_edit_categories)
            local_widget.line_edit_categories = line_edit_categories
            local_widget.searchBoxCategory.returnPressed.connect(local_widget.on_pressed)

            line_edit_location = QLineEdit()
            line_edit_location.setFixedWidth(WIDTH_WIDGET_RIGHT - 80)
            if current_exif_image.lat is None or current_exif_image.long is None:
                line_edit_location.setText('')
            else:
                line_edit_location.setText(
                    f"{current_exif_image.lat}|{current_exif_image.long}"
                    f"|heading:{current_exif_image.heading}"
                )
            local_widget.lineEditLocation = line_edit_location
            btn_clear_location = QPushButton("")
            btn_clear_location.setFixedWidth(25)
            btn_clear_location.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)
            )
            btn_clear_location.clicked.connect(
                lambda _s, w=local_widget: self.on_click_clear_location(w)
            )
            btn_view_location = QPushButton("")
            btn_view_location.setFixedWidth(25)
            btn_view_location.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
            )
            btn_view_location.clicked.connect(
                lambda _s, w=local_widget: self.on_click_view_location(w)
            )
            location_layout = QHBoxLayout()
            location_layout.addWidget(line_edit_location)
            location_layout.addWidget(btn_clear_location)
            location_layout.addWidget(btn_view_location)
            local_left_layout.addRow(QLabel(IMAGE_LOCATION), location_layout)

            line_edit_date_time = QLineEdit()
            line_edit_date_time.setFixedWidth(WIDTH_WIDGET_RIGHT - 100)
            line_edit_date_time.setText(
                current_exif_image.date + ' ' + current_exif_image.time
            )
            local_widget.line_edit_date_time = line_edit_date_time
            lbl_image_size = QLabel(IMAGE_SIZE + current_exif_image.filesize)
            date_size_layout = QHBoxLayout()
            date_size_layout.addWidget(line_edit_date_time)
            date_size_layout.addSpacing(5)
            date_size_layout.addWidget(lbl_image_size)
            local_left_layout.addRow(QLabel(IMAGE_DATE_TIME), date_size_layout)

            line_edit_templates = QLineEdit()
            line_edit_templates.setFixedWidth(WIDTH_WIDGET_RIGHT)
            local_left_layout.addRow(QLabel(IMAGE_TEMPLATES), line_edit_templates)
            local_widget.line_edit_templates = line_edit_templates

            copy_action.triggered.connect(
                lambda _s, w=local_widget: self.copy_image_info(w)
            )
            paste_action.triggered.connect(
                lambda _s, w=local_widget: self.paste_image_info(w, False)
            )
            paste_with_numbering_action.triggered.connect(
                lambda _s, w=local_widget: self.paste_image_info(w, True)
            )

            thumbnail = QPushButton()
            if current_exif_image.full_file_path.upper().endswith((".OGV", ".WEBM")):
                pixmap = QPixmap(logo_path)
            else:
                pixmap = QPixmap(current_exif_image.full_file_path)
            pixmap_resized = pixmap.scaled(
                IMAGE_DIMENSION, IMAGE_DIMENSION,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.FastTransformation,
            )
            thumbnail.setFlat(True)
            thumbnail.setIcon(QIcon(pixmap_resized))
            thumbnail.setIconSize(QSize(IMAGE_DIMENSION, IMAGE_DIMENSION))
            thumbnail.clicked.connect(
                lambda _s, w=local_widget: self.on_click_preview_image(w)
            )
            local_layout.addWidget(thumbnail)
            local_widget.full_file_path = current_exif_image.full_file_path
            thumbnail.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            thumbnail.customContextMenuRequested.connect(
                lambda _s, w=local_widget: self.on_thumbnail_context_menu(w)
            )

    def copy_image_info(self, image_widget):
        self.copied_name = image_widget.line_edit_file_name.text()
        self.copied_description = image_widget.line_edit_description.toPlainText()
        self.copied_categories = image_widget.line_edit_categories.text()
        self.copied_templates = image_widget.line_edit_templates.text()

    def paste_image_info(self, image_widget, increase_number):
        name = self.copied_name
        if increase_number:
            number_list = re.findall(r'\d+', name)
            if number_list:
                val = number_list[-1]
                next_val = str(int(val) + 1)
                if len(next_val) < len(val):
                    next_val = next_val.zfill(len(val))
                remove_last_number = name.rsplit(val, 1)
                name = next_val.join(remove_last_number)
                self.copied_name = name
        image_widget.line_edit_file_name.setText(name)
        image_widget.line_edit_description.setPlainText(self.copied_description)
        image_widget.line_edit_categories.setText(self.copied_categories)
        image_widget.line_edit_templates.setText(self.copied_templates)

    def init_upload(self, count):
        self.number_images_checked = count
        self.upload_successes = 0
        self.upload_failures = 0
        self.upload_status_dots = 0

    def update_uploading_status(self):
        total = self.upload_successes + self.upload_failures
        if total >= self.number_images_checked:
            return False
        self.upload_status_dots = (self.upload_status_dots + 1) % 11
        message = f"{total}/{self.number_images_checked} " + "." * self.upload_status_dots
        self.main_window.set_status(message)
        return True

    def set_upload_status(self, success):
        if success:
            self.upload_successes += 1
        else:
            self.upload_failures += 1
        message = ""
        if self.upload_successes > 0:
            message += (
                f" {self.upload_successes}/{self.number_images_checked}"
                " image(s) successfully uploaded"
            )
        if self.upload_failures > 0:
            if message:
                message += "; "
            message += f"{self.upload_failures} upload(s) failed!"
        self.main_window.set_status(message)
        self.btn_import.setEnabled(True)
