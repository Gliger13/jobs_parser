import itertools

import requests
from bs4 import BeautifulSoup

from core.page_manager import Pages, Page


class PaginatorUrlsCollector:
    def __init__(self, first_url_template, request_headers=None):
        self.first_url_template = first_url_template
        self.request_headers = request_headers

    def count_max_valid_page(self):
        page_number = 0
        while True:
            page = Page(self.first_url_template.format(page_number=page_number), self.request_headers)
            if page.is_page_exist():
                page_number += 1
            else:
                return page_number

    def page_urls(self, page_start, page_end):
        return [self.first_url_template.format(page_number=page_number) for page_number in range(page_start, page_end)]
        
    def valid_paginator_urls(self, page_start=0, page_end=None):
        if not page_end:
            page_end = self.count_max_valid_page()
            return self.page_urls(page_start, page_end)
        else:
            urls = self.page_urls(page_start, page_end)
            pages = Pages(urls, request_headers=self.request_headers)
            if pages.is_pages_exist():
                return urls
            else:
                raise requests.exceptions.HTTPError(f'Some page in [{page_start}, {page_end}] not exist.')


class UrlsCollector:
    def __init__(self, urls, request_headers=None, block_class=None):
        self.urls = urls
        self.request_headers = request_headers
        self.block_class = block_class

    def urls_from_page_by_class(self, url):
        page = Page(url, self.request_headers)
        page_file = page.page_file()

        soup = BeautifulSoup(open(page_file.file_path), 'html.parser').body

        urls = soup.find_all('a', self.block_class, href=True)
        return [url['href'] for url in urls]

    def collect_urls(self):
        all_urls = [self.urls_from_page_by_class(url) for url in self.urls]
        return list(itertools.chain.from_iterable(all_urls))  # Join list of lists: [[1]], [2, 3]] -> [1, 2, 3]
