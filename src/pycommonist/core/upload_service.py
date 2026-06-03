"""Orchestrate Commons login and per-image upload threads."""

import logging
import traceback

import requests
from PyQt6.QtCore import QThread, QTimer

from pycommonist.core.constants import TIMESTAMP_STATUSBAR, URL
from pycommonist.core.upload_worker import UploadWorker

logger = logging.getLogger(__name__)


class UploadService:
    def __init__(self):
        self.http_session = None
        self.session_widget = None
        self.check_thread_timer = None

    def upload_images(self, session_widget, login: str, password: str):
        self.session_widget = session_widget
        try:
            session_widget.main_window.clear_status()
            if not login:
                session_widget.btn_import.setEnabled(True)
                session_widget.main_window.set_status("Login is not filled")
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
            self.http_session = requests.Session()
            logger.debug("HTTP session created")

            params_1 = {
                "action": "query",
                "meta": "tokens",
                "type": "login",
                "format": "json",
            }
            try:
                http_ret = self.http_session.get(url=URL, params=params_1)
            except requests.exceptions.RequestException:
                logger.exception("Login token request failed")
                session_widget.btn_import.setEnabled(True)
                return

            login_token = http_ret.json()["query"]["tokens"]["logintoken"]
            params_2 = {
                'action': "clientlogin",
                'username': login,
                'password': password,
                'loginreturnurl': URL,
                'logintoken': login_token,
                'format': "json",
            }
            http_ret = self.http_session.post(URL, data=params_2)
            logger.debug("Client login response: %s", http_ret.json())
            if http_ret.json()['clientlogin']['status'] != 'PASS':
                session_widget.btn_import.setEnabled(True)
                session_widget.main_window.set_status("Client login failed")
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
