import pytest

from business.web_parser import WebParser


@pytest.fixture
def additional_parser_params():
    return {
        'request_headers': {'user-agent': 'job_parser/0.1.0'},
        'classes_to_exclude': ['recommended-vacancies', 'related-vacancies-wrapper']
    }


class TestWebParser:
    test_data = [
        ((['https://hh.ru/vacancy/40447045'], ['python', 'linux']), {'python': 3, 'linux': 0}),
        ((['https://rabota.by/vacancy/42154105'], ['Python', 'linux', 'flask']),
         {'Python': 7, 'linux': 0, 'flask': 1}),
        ((['https://rabota.by/vacancy/41595848'], ['Linux']), {'Linux': 2}),
    ]

    @pytest.mark.parametrize('test_input,expected', test_data)
    def test_parse_file(self, test_input, expected, additional_parser_params):
        urls, words_to_find = test_input
        assert WebParser(urls, words_to_find, **additional_parser_params).parse().count_words_occurrence() == expected

    @pytest.mark.parametrize(
        'test_input,expected', [
            ((['python'], 'python Pythonas mvfkvm fjf python'), ['python', 'Python', 'python']),
            ((['flask'], 'flaskFLASKfLask flask FLAK'), ['flask', 'FLASK', 'fLask', 'flask']),
            ((['linux'], 'linux, Linux, linux lin'), ['linux', 'Linux', 'linux'])
        ])
    def test__findall_in_page(self, test_input, expected):
        key, text = test_input
        assert WebParser([''], key)._findall_in_page(text) == expected
