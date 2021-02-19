import logging
import re

from bs4 import BeautifulSoup

from jobs_parser.core.file_manager import PageFile
from jobs_parser.core.page_manager import Pages
from jobs_parser.core.soup_maker import SoupMaker
from .parse_results import ParseResult, ParseResults

module_logger = logging.getLogger('jobs_parser')


class WebParser:
    """
    Finds specific words on specified pages. Can exclude blocks of text by the name of their div class

    Parameters
    ----------
    urls: [str]
        Urls to the pages that has been parsed
    words_to_find: [str]
        The list of words to find in page
    classes_to_exclude: [str], optional
        Exclude blocks of text by the name of their class divs
    request_headers: dict, optional
        The headers of request
    """
    def __init__(self, urls: [str], words_to_find: [str], classes_to_exclude: [str] = (), request_headers: dict = None):
        self.urls = urls
        self.words_to_find = words_to_find
        self.classes_to_exclude = classes_to_exclude
        self.request_headers = request_headers

        self.regex_templates = [re.compile(template, re.IGNORECASE) for template in self.words_to_find]

    def _user_content(self, page_file: PageFile) -> str:
        """Return only text from page"""
        return self._web_content(page_file).get_text()

    def _web_content(self, page_file: PageFile) -> BeautifulSoup:
        """Removes specific blocks from content"""
        return SoupMaker(page_file).remove_from_soup(self.classes_to_exclude)

    def _findall_in_page(self, user_content: str) -> [str]:
        """Searches for words in the page content"""
        matched = []
        for template in self.regex_templates:
            matched.extend(re.findall(template, user_content))
        return matched

    def _parse_file(self, page_file: PageFile) -> ParseResult:
        user_content = self._user_content(page_file)
        matched = self._findall_in_page(user_content)
        module_logger.debug(f'Page file parsed - {page_file.url}')
        return ParseResult(page_file.url, self.words_to_find, matched)

    def parse(self) -> ParseResults:
        """Finds specific words on specified pages and exclude blocks of text by the name of their div class"""
        pages = Pages(self.urls, self.request_headers)
        module_logger.info(f'Fetching page files by downloading or using the cache')
        page_files = pages.get_files()
        module_logger.info(f'Start scraping page files')
        parse_results = ParseResults(
            self.urls, self.words_to_find, [self._parse_file(page_file) for page_file in page_files]
        )
        module_logger.info(f'The scraping is over')
        return parse_results
