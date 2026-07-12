"""Orchestrate Commons login and per-image upload threads."""

import logging
import traceback

from PyQt6.QtCore import QThread, QTimer

from pycommonist.core.commons_api import create_http_session, login
from pycommonist.core.constants import TIMESTAMP_STATUSBAR
from pycommonist.core.upload_worker import UploadWorker

logger = logging.getLogger(__name__)


class UploadService:
    def __init__(self):
        self.http_session = None
        self.session_widget = None
        self.check_thread_timer = None

    def upload_images(self, session_widget, login_name: str, password: str):
        self.session_widget = session_widget
        try:
            session_widget.main_window.clear_status()
            if not login_name:
                session_widget.btn_import.setEnabled(True)
                session_widget.main_window.set_status("Username is not filled")
                return
            if not password:
                session_widget.btn_import.setEnabled(True)
                session_widget.main_window.set_status("Password is not filled")
                return
            if len(session_widget.current_upload) == 0:
                session_widget.btn_import.setEnabled(True)
                session_widget.main_window.set_status("No image selected for upload")
                return

            session_widget.threads.clear()
            session_widget.workers.clear()
            self.http_session = create_http_session()

            ok, message = login(self.http_session, login_name, password)
            if not ok:
                session_widget.btn_import.setEnabled(True)
                session_widget.main_window.set_status(message)
                return

            checked_image_count = sum(
                1 for el in session_widget.current_upload if el.cb_import.isChecked()
            )
            session_widget.init_upload(checked_image_count)

            if self.check_thread_timer is None:
                self.check_thread_timer = QTimer()
            self.check_thread_timer.stop()
            self.check_thread_timer.setInterval(TIMESTAMP_STATUSBAR)
            self.check_thread_timer.timeout.connect(self._update_status_bar)
            self.check_thread_timer.start(TIMESTAMP_STATUSBAR)

            builder = session_widget.get_wikitext_builder()
            image_index = 0
            for element in session_widget.current_upload:
                if element.cb_import.isChecked():
                    path = session_widget.current_directory_path
                    thread = QThread()
                    session_widget.threads.append(thread)
                    worker = UploadWorker(
                        element,
                        session_widget,
                        path,
                        self.http_session,
                        image_index,
                        builder,
                    )
                    session_widget.workers.append(worker)
                    session_widget.workers[image_index].moveToThread(
                        session_widget.threads[image_index]
                    )
                    session_widget.threads[image_index].started.connect(
                        session_widget.workers[image_index].process
                    )
                    image_index += 1

            if image_index > 0:
                session_widget.threads[0].start()
        except ValueError:
            traceback.print_exc()

    def _update_status_bar(self):
        if not self.session_widget.update_uploading_status():
            self.check_thread_timer.stop()
