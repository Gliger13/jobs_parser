import pytest
import requests

from web_parser.urls_collector import UrlsCollector, PaginatorUrlsCollector


class TestPaginatorUrlsCollector:
    def setup(self):
        self.start_paginator_template = 'https://rabota.by/search/vacancy?text=Python&page={page_number}'
        self.headers = {'user-agent': 'job_parser/0.1.0'}
        self.paginator_urls_collector = PaginatorUrlsCollector(self.start_paginator_template, self.headers)

    def test_valid_paginator_urls(self):
        assert len(self.paginator_urls_collector.valid_paginator_urls(0, 3)) == 3

    def test_not_valid_url_pages(self):
        with pytest.raises(requests.exceptions.HTTPError):
            self.paginator_urls_collector.valid_paginator_urls(page_start=150, page_end=200)


class TestUrlsCollector:
    def setup(self):
        headers = {'user-agent': 'job_parser/0.1.0'}
        start_paginator_template = 'https://rabota.by/search/vacancy?text=Python&page={page_number}'

        paginator_urls_collector = PaginatorUrlsCollector(start_paginator_template, headers)
        self.page_urls = paginator_urls_collector.page_urls(0, 2)

        block_class = 'bloko-link HH-LinkModifier'
        self.urls_collector = UrlsCollector(self.page_urls, headers, block_class)

    def test_urls_from_page_by_class(self):
        assert len(self.urls_collector.urls_from_page_by_class(self.page_urls[0])) == 50

    def test_collect_urls(self):
        assert len(self.urls_collector.collect_urls()) == 100
