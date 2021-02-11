import pytest
import requests

from web_parser.urls_collector import UrlsCollector


class TestUrlsCollector:
    def setup(self):
        self.start_url = 'https://rabota.by/search/vacancy?text=Python&page={page_number}'
        self.headers = {'user-agent': 'job_parser/0.0.0'}
        self.block_class = 'bloko-link HH-LinkModifier'
        self.urls_collector = UrlsCollector(
            self.start_url,
            request_headers=self.headers
        )

    def test_page_exist(self):
        assert self.urls_collector.is_page_exist(0)

    def test_page_not_exist(self):
        assert not self.urls_collector.is_page_exist(10000)

    def test_valid_url_pages(self):
        assert len(self.urls_collector.valid_url_pages(page_start=0, page_end=2)) == 2

    def test_not_valid_url_pages(self):
        with pytest.raises(requests.exceptions.HTTPError):
            self.urls_collector.valid_url_pages(page_start=150, page_end=200)

    def test_urls_from_page_by_class(self):
        url = "https://rabota.by/search/vacancy?&text=python&page=0"
        assert len(self.urls_collector.urls_from_page_by_class(url, self.block_class)) == 50

    def test_no_results_by_key(self):
        url = 'https://rabota.by/search/vacancy?text=shotgunFFFFFF&page={page_number}'
        assert not self.urls_collector.urls_from_page_by_class(url, self.block_class)
