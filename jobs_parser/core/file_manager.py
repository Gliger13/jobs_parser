import hashlib
import logging
import os
import shutil
import tempfile

module_logger = logging.getLogger('jobs_parser')


class TmpManager:
    tmp_dir_name = 'jobs_parser'  # Folder name to save in it

    @property
    def _tmp_dir_path(self):
        return os.path.join(tempfile.gettempdir(), self.tmp_dir_name)

    def _is_tmp_dir_exist(self):
        return True if os.path.exists(self._tmp_dir_path) else False

    def get_tmp_dir_path(self):
        if not self._is_tmp_dir_exist():
            os.mkdir(self._tmp_dir_path)
        return self._tmp_dir_path

    def clear_tmp_dir(self):
        if self._is_tmp_dir_exist():
            shutil.rmtree(self._tmp_dir_path)
            module_logger.debug('Temp folder cleared')


class PageFile(TmpManager):
    def __init__(self, url):
        self.url = url

    @property
    def filename(self):
        return f"{hashlib.md5(self.url.encode('utf-8')).hexdigest()}.html"

    @property
    def file_path(self):
        return os.path.join(self.get_tmp_dir_path(), self.filename)

    def is_file_exist(self):
        return True if os.path.exists(self.file_path) else False

    def save_file(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(data)
