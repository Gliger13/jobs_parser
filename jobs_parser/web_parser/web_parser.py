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

    def _get_page(self, url):
        page = requests.get(url, headers=self.request_headers)
        page.raise_for_status()
        return page

    @staticmethod
    def _save_page(url, url_number, page):
        dir_name = 'downloaded_pages'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        filename = f"{hashlib.md5(url.encode('utf-8')).hexdigest()[:8]}_{url_number}.html"
        path_to_save = os.path.join(dir_name, filename)
        with open(path_to_save, 'w') as file:
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
