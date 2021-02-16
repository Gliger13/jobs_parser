import pytest
import requests

from business.urls_collector import PaginatorUrlsCollector, UrlsCollector


@pytest.fixture(params=[
    'https://rabota.by/search/vacancy?text=Python&page={page_number}',
    'https://rabota.by/search/vacancy?text=ShotgunFFFFF&page={page_number}',
])
def paginator_urls_collector(request, request_headers):
    return PaginatorUrlsCollector(request.param, request_headers)


@pytest.fixture(params=[
    (0, 1), (0, 2), (0, 3)
])
def start_end_number(request):
    return request.param


class TestPaginatorUrlsCollector:
    @pytest.mark.smoke
    def test_valid_paginator_urls(self, paginator_urls_collector, start_end_number):
        start_number, end_number = start_end_number
        assert len(paginator_urls_collector.valid_paginator_urls(start_number, end_number)) == end_number - start_number

    @pytest.mark.smoke
    def test_not_valid_paginator_urls(self, paginator_urls_collector):
        with pytest.raises(requests.exceptions.HTTPError):
            paginator_urls_collector.valid_paginator_urls(page_start=150, page_end=200)

    @pytest.mark.smoke
    def test_page_urls(self, paginator_urls_collector, start_end_number):
        start_number, end_number = start_end_number
        assert len(paginator_urls_collector.page_urls(start_number, end_number)) == end_number - start_number

    @pytest.mark.advance
    def test_count_max_valid_page(self, paginator_urls_collector):
        assert int(paginator_urls_collector.count_max_valid_page()) >= 0


class TestUrlsCollector:
    @pytest.mark.smoke
    @pytest.mark.parametrize('test_input,expected', [
        (['https://rabota.by/search/vacancy?text=Python&page=0'], 50),
        (['https://rabota.by/search/vacancy?text=ShotgunFFFFF&page=0'], 0),
    ])
    def test_urls_from_page_by_class(self, test_input, expected, request_headers, block_class):
        urls_collector = UrlsCollector(test_input, block_class, request_headers)
        assert len(urls_collector.urls_from_page_by_class(urls_collector.urls[0])) == expected

    @pytest.mark.smoke
    @pytest.mark.parametrize('test_input,expected', [
        (['https://rabota.by/search/vacancy?text=Python&page=0',
          'https://rabota.by/search/vacancy?text=Python&page=1'], 100),
        (['https://rabota.by/search/vacancy?text=ShotgunFFFFF&page=0'], 0),
        (['https://rabota.by/search/vacancy?text=Python&page=0'], 50),
    ])
    def test_collect_urls(self, test_input, expected, request_headers, block_class):
        urls_collector = UrlsCollector(test_input, block_class, request_headers)
        assert len(urls_collector.collect_urls()) == expected
