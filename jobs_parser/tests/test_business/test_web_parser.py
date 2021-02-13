import pytest

from business.web_parser import WebParser


@pytest.fixture
def request_headers():
    return {'user-agent': 'job_parser/0.1.0'}


@pytest.fixture(params=[
    ('python Pythonas mvfkvm fjf python', ['python', 'Python', 'python']),
    ('flaskFLASKfLask flask FLAK', ['flask', 'FLASK', 'fLask', 'flask']),
    ('linux, Linux, linux lin', ['linux', 'Linux', 'linux'])
])
def text_to_find(request):
    return request.param


def (request):
    return request.param


@pytest.fixture
def web_parser(request_headers):
    words = [r'rabota']
    return WebParser(
        words,
        ['https://rabota.by/feedback'],
        request_headers=request_headers
    )


def text_to_find(request):
    return request.param


class TestWebParser:
    def test__findall_in_page(self, web_parser, text_to_find):
        text, result = text_to_find
        assert web_parser._findall_in_page(text) == result

    # def test_parse(self, web_parser):
    #     assert web_parser.parse().count_word_occurrence(self.words.pop()) == 18
