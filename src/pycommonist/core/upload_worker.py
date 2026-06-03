"""Per-image MediaWiki upload worker."""

import logging
import os.path
import traceback

from PyQt6.QtCore import QObject, QTimer, pyqtSlot

from pycommonist.core.constants import URL

logger = logging.getLogger(__name__)


class UploadWorker(QObject):
    def __init__(self, element, session, path, http_session, index, wikitext_builder):
        super().__init__()
        self.element = element
        self.session_widget = session
        self.path = path
        self.http_session = http_session
        self.index = index
        self.wikitext_builder = wikitext_builder

    @pyqtSlot()
    def process(self):
        self.session_widget.main_window.clear_status()
        element = self.element
        path = self.path
        widget = self.session_widget
        text = self.wikitext_builder.build(element, widget)
        file_name = element.line_edit_file_name.text()
        real_file_name = element.lbl_real_file_name.text()
        file_path = path + '/' + real_file_name
        try:
            query_tokens_params = {
                "action": "query",
                "meta": "tokens",
                "format": "json",
            }
            http_ret = self.http_session.get(url=URL, params=query_tokens_params)
            logger.debug("CSRF token response: %s", http_ret.json())
            csrf_token = http_ret.json()["query"]["tokens"]["csrftoken"]

            if not os.path.isfile(file_path):
                element.lbl_upload_result.setText("FAILED")
                widget.set_upload_status(False)
                return

            physical_array = file_path.split('.')
            if len(physical_array) > 0:
                physical_ext = physical_array[-1]
                logical_array = file_name.split('.')
                if len(logical_array) > 1:
                    logical_ext = logical_array[-1]
                    if logical_ext != physical_ext:
                        file_name = str(file_name) + "." + str(physical_ext)
                else:
                    file_name = str(file_name) + "." + str(physical_ext)
            else:
                element.lbl_upload_result.setText("FAILED")
                widget.set_upload_status(False)
                return

            logger.debug("Uploading as: %s", file_name)
            params = {
                "action": "upload",
                "filename": file_name,
                "format": "json",
                "token": csrf_token,
                "ignorewarnings": 1,
                "comment": "PyCommonist upload: " + file_name,
                "text": text,
            }
            with open(file_path, 'rb') as f:
                files = {'file': (file_name, f, 'multipart/form-data')}
                http_ret = self.http_session.post(URL, files=files, data=params)
            logger.debug("Upload response: %s", http_ret.json())

            if 'upload' in http_ret.json():
                result = http_ret.json()['upload']['result']
                element.lbl_upload_result.setText(result)
                widget.set_upload_status(True)
                element.cb_import.setChecked(False)
            else:
                element.lbl_upload_result.setText("FAILED")
                widget.set_upload_status(False)
                element.cb_import.setChecked(False)
        except Exception:
            traceback.print_exc()
            element.lbl_upload_result.setText("FAILED")
            widget.set_upload_status(False)
        self._run_next_thread()

    def _run_next_thread(self):
        if self.index < self.session_widget.number_images_checked - 1:
            timer = QTimer()
            timer.setInterval(6)
            timer.start()
            self.session_widget.threads[self.index + 1].start()
        elif self.index == self.session_widget.number_images_checked - 1:
            self.session_widget.clean_threads()
