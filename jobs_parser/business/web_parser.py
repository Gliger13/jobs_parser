import logging
import re

from bs4 import BeautifulSoup

from business.parse_results import ParseResult, ParseResults
from core.page_manager import Pages

module_logger = logging.getLogger('jobs_parser')


class WebParser:
    def __init__(self, urls, words_to_find, classes_to_exclude=(), request_headers=None):
        self.urls = urls
        self.words_to_find = words_to_find
        self.classes_to_exclude = classes_to_exclude
        self.request_headers = request_headers

        self.regex_templates = [re.compile(template, re.IGNORECASE) for template in self.words_to_find]

    def _user_content(self, page_file):
        return self._web_content(page_file).get_text()

    def _web_content(self, page_file):
        soup = BeautifulSoup(open(page_file.file_path), 'html.parser').body
        for block_class in self.classes_to_exclude:
            if found := soup.find('div', block_class):
                found.decompose()
        return soup

    def _findall_in_page(self, user_content: str):
        matched = []
        for template in self.regex_templates:
            matched.extend(re.findall(template, user_content))
        return matched

    def _parse_file(self, page_file):
        user_content = self._user_content(page_file)
        matched = self._findall_in_page(user_content)
        module_logger.debug(f'Page file parsed - {page_file.url}')
        return ParseResult(page_file.url, self.words_to_find, matched)

    def parse(self):
        pages = Pages(self.urls, self.request_headers)
        module_logger.info(f'Fetching page files by downloading or using the cache')
        page_files = pages.get_files()
        module_logger.info(f'Start scraping page files')
        parse_results = ParseResults(
            self.urls, self.words_to_find, [self._parse_file(page_file) for page_file in page_files]
        )
        module_logger.info(f'The scraping is over')
        return parse_results
