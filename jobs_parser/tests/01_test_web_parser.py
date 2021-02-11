from web_parser.web_parser import WebParser


class TestWebParser:
    def setup(self):
        headers = {'user-agent': 'job_parser/0.0.0'}
        self.web_parser = WebParser(
            [r'Python'],
            ['https://rabota.by/vacancy/41569979?query=python'],
            request_headers=headers
        )

    def test_page_parse(self):
        assert self.web_parser._parse_page('python Pythonss Pnton python') == ['python', 'Python', 'python']

    def test_parse(self):
        assert len(self.web_parser.parse().pop()) == 18
