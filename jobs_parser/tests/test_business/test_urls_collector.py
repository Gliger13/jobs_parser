import pytest
import requests

from business.urls_collector import PaginatorUrlsCollector, UrlsCollector


@pytest.fixture
def request_headers():
    return {'user-agent': 'job_parser/0.1.0'}


@pytest.fixture
def paginator_urls_collector(request_headers):
    start_paginator_template = 'https://rabota.by/search/vacancy?text=Python&page={page_number}'
    return PaginatorUrlsCollector(start_paginator_template, request_headers)


@pytest.fixture(params=[
    (0, 1), (0, 2), (0, 3)
])
def start_end_number(request):
    return request.param


class TestPaginatorUrlsCollector:
    def test_valid_paginator_urls(self, paginator_urls_collector, start_end_number):
        start_number, end_number = start_end_number
        assert len(paginator_urls_collector.valid_paginator_urls(start_number, end_number)) == end_number - start_number

    def test_not_valid_paginator_urls(self, paginator_urls_collector):
        with pytest.raises(requests.exceptions.HTTPError):
            paginator_urls_collector.valid_paginator_urls(page_start=150, page_end=200)

    def test_page_urls(self, paginator_urls_collector, start_end_number):
        start_number, end_number = start_end_number
        assert len(paginator_urls_collector.page_urls(start_number, end_number)) == end_number - start_number

    @pytest.mark.advance
    def test_count_max_valid_page(self, paginator_urls_collector):
        start_page = 30
        assert int(paginator_urls_collector.count_max_valid_page(start_page)) >= start_page


@pytest.fixture
def page_urls(start_end_number, paginator_urls_collector):
    page_start, page_end = start_end_number
    return paginator_urls_collector.page_urls(page_start, page_end)


@pytest.fixture
def urls_collector(page_urls, request_headers):
    block_class = 'bloko-link HH-LinkModifier'
    return UrlsCollector(page_urls, request_headers, block_class)


class TestUrlsCollector:
    def test_urls_from_page_by_class(self, urls_collector, page_urls):
        assert len(urls_collector.urls_from_page_by_class(page_urls[0])) == 50

    def test_collect_urls(self, urls_collector):
        assert len(urls_collector.collect_urls()) == len(urls_collector.urls) * 50
