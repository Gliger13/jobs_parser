import re

from bs4 import BeautifulSoup

from core.page_manager import Pages


class WebParser:
    def __init__(self, regex_templates, urls, request_headers=None):
        self.urls = urls
        self.regex_templates = [re.compile(template, re.IGNORECASE) for template in regex_templates]
        self.request_headers = request_headers

    @staticmethod
    def _user_content(page_file):
        return BeautifulSoup(open(page_file().file_path), 'html.parser').body.get_text()

    def _parse_page(self, user_content: str):
        matched = []
        for template in self.regex_templates:
            matched.extend(re.findall(template, user_content))
        return matched

    def parse(self):
        pages = Pages(self.urls, self.request_headers)
        page_files = pages.get_files()

        parse_results = []
        for page_file in page_files:
            user_content = self._user_content(page_file)
            parse_results.append(self._parse_page(user_content))
        return parse_results
