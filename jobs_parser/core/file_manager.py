import hashlib
import logging
import os
import shutil
import tempfile

module_logger = logging.getLogger('jobs_parser')


class TmpManager:
    """
    Responsible for creating, processing and cleaning up the temporary directory
    """
    _tmp_dir_name = 'jobs_parser'  # Folder name of temporary directory

    @property
    def _tmp_dir_path(self) -> str:
        return os.path.join(tempfile.gettempdir(), self._tmp_dir_name)

    def _is_tmp_dir_exist(self) -> bool:
        return True if os.path.exists(self._tmp_dir_path) else False

    def get_tmp_dir_path(self) -> str:
        if not self._is_tmp_dir_exist():
            os.mkdir(self._tmp_dir_path)
        return self._tmp_dir_path

    def clear_tmp_dir(self):
        if self._is_tmp_dir_exist():
            shutil.rmtree(self._tmp_dir_path)
            module_logger.debug('Temp folder cleared')


class PageFile(TmpManager):
    """
    Responsible for storing and getting the page file path
    """
    def __init__(self, url: str):
        self.url = url

    @property
    def filename(self) -> str:
        """Using the hash of the url as the file name"""
        return f"{hashlib.md5(self.url.encode('utf-8')).hexdigest()}.html"

    @property
    def file_path(self) -> str:
        return os.path.join(self.get_tmp_dir_path(), self.filename)

    def is_file_exist(self) -> bool:
        return True if os.path.exists(self.file_path) else False

    def save_file(self, data: str):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(data)
