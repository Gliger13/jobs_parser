import itertools
import logging

import requests
from bs4 import BeautifulSoup

from core.page_manager import Pages, Page
from core.soup_maker import SoupMaker

module_logger = logging.getLogger('jobs_parser')


class PaginatorUrlsCollector:
    def __init__(self, first_url_template, request_headers=None):
        self.first_url_template = first_url_template
        self.request_headers = request_headers

    def count_max_valid_page(self, exist_page_number=0):
        module_logger.info('Starting finding the maximum page of paginator')
        while True:
            page = Page(self.first_url_template.format(page_number=exist_page_number), self.request_headers)
            if page.is_page_exist():
                exist_page_number += 1
            else:
                module_logger.info(f'Maximum existing page of a paginator is {exist_page_number}')
                return exist_page_number

    def page_urls(self, page_start, page_end):
        return [self.first_url_template.format(page_number=page_number) for page_number in range(page_start, page_end)]

    def valid_paginator_urls(self, page_start=0, page_end=None):
        module_logger.info('Collecting urls from paginator. Checking for page existence')
        if not page_end:
            page_end = self.count_max_valid_page()
            return self.page_urls(page_start, page_end)
        else:
            urls = self.page_urls(page_start, page_end)
            pages = Pages(urls, request_headers=self.request_headers)
            if pages.is_pages_exist():
                module_logger.info('Urls from paginator collected')
                return urls
            else:
                raise requests.exceptions.HTTPError(f'Some page in [{page_start}, {page_end}] not exist.')


class UrlsCollector:
    def __init__(self, urls, request_headers=None, block_class=None):
        self.urls = urls
        self.request_headers = request_headers
        self.block_class = block_class

    def urls_from_page_by_class(self, url):
        urls = SoupMaker(Page(url, self.request_headers).page_file()).find_urls_by_class(self.block_class)
        module_logger.debug(f'Urls from the page {url} collected')
        return [url['href'] for url in urls]

    def collect_urls(self):
        module_logger.info('Collecting urls from all available pages')
        all_urls = [self.urls_from_page_by_class(url) for url in self.urls]
        module_logger.info('Urls from all available pages collected')
        return list(itertools.chain.from_iterable(all_urls))  # Join list of lists: [[1]], [2, 3]] -> [1, 2, 3]
