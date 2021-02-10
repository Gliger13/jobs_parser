import hashlib
import os
import re

import requests
from bs4 import BeautifulSoup


class WebParser:
    def __init__(self, regex_templates, urls, request_headers=None):
        self.urls = urls
        self.regex_templates = [re.compile(template, re.IGNORECASE) for template in regex_templates]
        self.request_headers = request_headers

    @property
    def path_to_save(self):
        dir_name = 'downloaded_pages'
        if os.path.split(os.path.abspath(os.path.curdir))[1] != "jobs_parser":
            source_dir_path = os.path.split(os.path.abspath(os.path.curdir))[0]
            return os.path.join(source_dir_path, dir_name)
        else:
            source_dir_path = os.path.abspath(os.path.curdir)
            return os.path.join(source_dir_path, dir_name)

    def _get_page(self, url):
        page = requests.get(url, headers=self.request_headers)
        page.raise_for_status()
        return page

    def _save_page(self, url, page):
        if not os.path.exists(self.path_to_save):
            os.mkdir(self.path_to_save)

        filename = f"{hashlib.md5(url.encode('utf-8')).hexdigest()}.html"
        file_path = os.path.join(self.path_to_save, filename)

        with open(file_path, 'w') as file:
            file.write(page.text)

    @staticmethod
    def _user_content(page):
        return BeautifulSoup(page.text, 'html.parser').body.get_text()

    def _parse_page(self, user_content: str):
        matched = []
        for template in self.regex_templates:
            matched.extend(re.findall(template, user_content))
        return matched

    def parse(self):
        parse_result = []
        for url_number, url in enumerate(self.urls):
            page = self._get_page(url)
            self._save_page(url, url_number, page)
            user_content = self._user_content(page)
            parse_result.append(self._parse_page(user_content))
        return parse_result
