from business.web_parser import WebParser


class TestWebParser:
    def setup(self):
        headers = {'user-agent': 'job_parser/0.1.0'}
        self.words = [r'Python']
        self.web_parser = WebParser(
            self.words,
            ['https://rabota.by/vacancy/41569979?query=python'],
            request_headers=headers
        )

    def test_page_parse(self):
        assert self.web_parser._findall_in_page('python Pythonss Pnton python') == ['python', 'Python', 'python']

    def test_parse(self):
        assert self.web_parser.parse().count_word_occurrence(self.words.pop()) == 18
