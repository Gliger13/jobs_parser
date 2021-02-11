import os

from web_parser.web_parser import WebParser


class TestWebParser:
    def setup(self):
        headers = {'user-agent': 'job_parser/0.0.0'}
        self.web_parser = WebParser(
            [r'Python'],
            ['https://rabota.by/vacancy/41569979?query=python'],
            request_headers=headers
        )

    def test_page_downloading_and_saving(self):
        self.web_parser._save_page('https://www.google.com', self.web_parser._get_page('https://www.google.com'))
        file_path = os.path.join(self.web_parser.path_to_save, '8ffdefbdec956b595d257f0aaeefd623.html')
        assert os.path.exists(file_path)

    def test_page_parser(self):
        assert self.web_parser._parse_page('python Pythonss Pnton python') == ['python', 'Python', 'python']

    def test_parser(self):
        assert len(self.web_parser.parse().pop()) == 18
