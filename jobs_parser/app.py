from business.urls_collector import UrlsCollector, PaginatorUrlsCollector
from business.web_parser import WebParser


def parse_required(func):
    def wrapper(self, *args, **kwargs):
        if not self.parse_results:
            self.parse()
        return func(self, *args, **kwargs)
    return wrapper


class App:
    def __init__(
            self, first_paginator_url_template, words_to_find, /,
            block_link_class=None, classes_to_exclude=(),
            request_headers=None, start_page=None, end_page=None
    ):
        self.first_paginator_url_template = first_paginator_url_template
        self.words_to_find = words_to_find

        self.block_link_class = block_link_class
        self.classes_to_exclude = classes_to_exclude

        self.request_headers = request_headers
        self.start_page = start_page
        self.end_page = end_page

        self.parse_results = None

    def _paginator_urls(self):
        collector = PaginatorUrlsCollector(self.first_paginator_url_template, self.request_headers)
        return collector.valid_paginator_urls(self.start_page, self.end_page)

    def _urls_to_parse(self):
        return UrlsCollector(self._paginator_urls(), self.request_headers, self.block_link_class).collect_urls()

    def parse(self):
        self.parse_results = WebParser(
            self._urls_to_parse(), self.words_to_find, self.classes_to_exclude, self.request_headers
        ).parse()
        return self.parse_results

    @parse_required
    def num_of_word_occur_str(self):
        text_template = "Amount of occurrences of a word {0} per vacancy page is {1}."
        text = [text_template.format(w, num) for w, num in self.parse_results.count_words_occurrence().items()]
        return '\n'.join(text)

    @parse_required
    def average_num_of_occur_str(self):
        text_template = "Average number of occurrence of a word {0} per vacancy page is {1}."
        text = [text_template.format(w, num) for w, num in self.parse_results.average_num_of_words_occur().items()]
        return '\n'.join(text)


if __name__ == '__main__':
    paginator_url_template = "https://rabota.by/search/vacancy?text=Python&page={page_number}"
    words = [r'python', r'linux', r'flask']

    link_class = 'bloko-link HH-LinkModifier'
    div_classes = ['recommended-vacancies', 'related-vacancies-wrapper']
    headers = {'user-agent': 'job_parser/0.1.0'}

    app = App(
        paginator_url_template, words,
        block_link_class=link_class, classes_to_exclude=div_classes,
        request_headers=headers, start_page=0, end_page=1
    )
    app.parse()
    print(app.average_num_of_occur_str())
    print(app.num_of_word_occur_str())
