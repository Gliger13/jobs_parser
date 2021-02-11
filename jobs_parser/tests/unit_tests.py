import os
import unittest
from collections import namedtuple

import requests

from web_parser.urls_collector import UrlsCollector
from web_parser.web_parser import WebParser


class TestUrlsCollector(unittest.TestCase):
    def setUp(self):
        start_url = 'https://rabota.by/search/vacancy?text=Python&page={page_number}'
        headers = {'user-agent': 'job_parser/0.0.0'}
        self.urls_collector = UrlsCollector(
            start_url,
            request_headers=headers
        )

    def test_page_exist(self):
        self.assertEqual(self.urls_collector.is_page_exist(0), True)

    def test_page_not_exist(self):
        self.assertEqual(self.urls_collector.is_page_exist(10000), False)

    def test_valid_url_pages(self):
        self.assertEqual(len(self.urls_collector.valid_url_pages(page_start=0, page_end=2)), 2)

    def test_not_valid_url_pages(self):
        self.assertRaises(requests.exceptions.HTTPError, self.urls_collector.valid_url_pages, page_start=150, page_end=200)

    def test_urls_from_page_by_class(self):
        url = "https://rabota.by/search/vacancy?&text=python&page=0"
        block_class = 'bloko-link HH-LinkModifier'
        self.assertEqual(len(self.urls_collector.urls_from_page_by_class(url, block_class)), 50)


class TestWebParser(unittest.TestCase):
    def setUp(self):
        headers = {'user-agent': 'job_parser/0.0.0'}
        self.web_parser = WebParser(
            [r'Python'],
            ['https://rabota.by/vacancy/41569979?query=python'],
            request_headers=headers
        )

    def test_page_downloading_and_saving(self):
        self.web_parser._save_page('https://www.google.com', self.web_parser._get_page('https://www.google.com'))
        file_path = os.path.join(self.web_parser.path_to_save, '8ffdefbdec956b595d257f0aaeefd623.html')
        self.assertEqual(os.path.exists(file_path), True)

    def test_page_parser(self):
        self.assertEqual(self.web_parser._parse_page('python Pythonss Pnton python'), ['python', 'Python', 'python'])

    def test_parser(self):
        self.assertEqual(len(self.web_parser.parse().pop()), 18)


if __name__ == "__main__":
    unittest.main()
