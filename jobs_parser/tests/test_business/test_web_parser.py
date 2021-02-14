import pytest

from business.web_parser import WebParser


class TestWebParser:
    test_data = [
        ((['https://hh.ru/vacancy/40447045'], ['python', 'linux']), {'python': 3, 'linux': 0}),
        ((['https://rabota.by/vacancy/42154105'], ['Python', 'linux', 'flask']),
         {'Python': 7, 'linux': 0, 'flask': 1}),
        ((['https://rabota.by/vacancy/41595848'], ['Linux']), {'Linux': 2}),
    ]

    @pytest.mark.parametrize('test_input,expected', test_data)
    def test_parse_file(self, test_input, expected, classes_to_exclude, request_headers):
        urls, words_to_find = test_input
        assert WebParser(
            urls, words_to_find,
            classes_to_exclude=classes_to_exclude, request_headers=request_headers
        ).parse().count_words_occurrence() == expected

    @pytest.mark.parametrize(
        'test_input,expected', [
            ((['python'], 'python Pythonas mvfkvm fjf python'), ['python', 'Python', 'python']),
            ((['flask'], 'flaskFLASKfLask flask FLAK'), ['flask', 'FLASK', 'fLask', 'flask']),
            ((['linux'], 'linux, Linux, linux lin'), ['linux', 'Linux', 'linux'])
        ])
    def test__findall_in_page(self, test_input, expected):
        key, text = test_input
        assert WebParser([''], key)._findall_in_page(text) == expected
