from business.urls_collector import UrlsCollector, PaginatorUrlsCollector
from business.web_parser import WebParser


def amount_of_words(parsing_result, word):
    return [page_result.count(word) for page_result in parsing_result]


def average_num_of_occur(parsing_result, word):
    num_of_words = amount_of_words(parsing_result, word)
    return sum(num_of_words) / len(num_of_words)


if __name__ == '__main__':
    first_paginator_url_template = "https://rabota.by/search/vacancy?text=Python&page={page_number}"
    request_headers = {'user-agent': 'job_parser/0.1.0'}
    word_to_find = [r'python', r'linux', r'flask']
    block_link_class = 'bloko-link HH-LinkModifier'

    paginator_urls_collector = PaginatorUrlsCollector(first_paginator_url_template, request_headers)
    paginator_urls = paginator_urls_collector.valid_paginator_urls(0, 2)

    urls_collector = UrlsCollector(paginator_urls, request_headers, block_link_class)
    urls_to_parse = urls_collector.collect_urls()

    spider = WebParser([r'Python', r'linux', r'flask'], urls_to_parse, request_headers)
    results = spider.parse()

    print(f"Amount of occurrences of a word Linux per vacancy page: {amount_of_words(results, 'Linux')}")
    print(f"Amount of occurrences of a word Python per vacancy page: {amount_of_words(results, 'Python')}")
    print(f"Amount of occurrences of a word Flask per vacancy page: {amount_of_words(results, 'Flask')}")

    print(f"Average number of occurrence of a word Linux: {average_num_of_occur(results, 'Linux')}")
    print(f"Average number of occurrence of a word Python: {average_num_of_occur(results, 'Python')}")
    print(f"Average number of occurrence of a word Flask: {average_num_of_occur(results, 'Flask')}")
