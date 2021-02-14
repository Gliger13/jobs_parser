import pytest


from app import App


@pytest.mark.smoke
class TestApp:
    def test_parse(self, block_class, classes_to_exclude, request_headers):
        url_template = 'https://rabota.by/search/vacancy?text=Python&page={page_number}'
        words = ['Linux']
        parser_results = App(
            url_template, words,
            block_link_class=block_class, classes_to_exclude=classes_to_exclude,
            request_headers=request_headers, start_page=0, end_page=1
        ).parse()
        assert 2 > parser_results.average_num_of_word_occur(words.pop()) > 0
