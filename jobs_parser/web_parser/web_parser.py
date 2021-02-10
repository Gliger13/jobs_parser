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

    def filename_path(self, url):
        filename = f"{hashlib.md5(url.encode('utf-8')).hexdigest()}.html"
        return os.path.join(self.path_to_save, filename)

    def _get_page(self, url):
        page_path = self.filename_path(url)
        if os.path.exists(page_path):
            return
        else:
            page = requests.get(url, headers=self.request_headers)
            page.raise_for_status()
            return page.text

    def _save_page(self, url, page):
        if not os.path.exists(self.path_to_save):
            os.mkdir(self.path_to_save)

        if not os.path.exists(self.filename_path(url)):
            with open(self.filename_path(url), 'w') as file:
                file.write(page)

    def _user_content(self, url):
        return BeautifulSoup(open(self.filename_path(url)), 'html.parser').body.get_text()

    def _parse_page(self, user_content: str):
        matched = []
        for template in self.regex_templates:
            matched.extend(re.findall(template, user_content))
        return matched

    def parse(self):
        parse_result = []
        for url_number, url in enumerate(self.urls):
            page = self._get_page(url)
            self._save_page(url, page)
            user_content = self._user_content(url)
            parse_result.append(self._parse_page(user_content))
        return parse_result
