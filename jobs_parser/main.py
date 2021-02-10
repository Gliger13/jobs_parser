from web_parser import web_parser, urls_collector


def amount_of_words(parsing_result, word):
    return [page_result.count(word) for page_result in parsing_result]


def average_num_of_occur(parsing_result, word):
    num_of_words = amount_of_words(parsing_result, word)
    return sum(num_of_words) / len(num_of_words)


if __name__ == '__main__':
    first_page_url_template = "https://rabota.by/search/vacancy?text=Python&page={page_number}"
    request_headers = {'user-agent': 'job_parser/0.0.0'}
    word_to_find = [r'python', r'linux', r'flask']

    url_collector = urls_collector.UrlsCollector(first_page_url_template, request_headers=request_headers)
    # Get urls of all pages
    # url_pages = url_collector.valid_url_pages()
    # all_urls = []
    # for url_page in url_pages:
    #     all_urls.extend(
    #         url_collector.urls_from_page_by_class(url_page, 'bloko-link HH-LinkModifier')
    #     )

    # Get url only for one page
    all_urls = url_collector.urls_from_page_by_class(
        'https://rabota.by/search/vacancy?text=Python&page=39',
        'bloko-link HH-LinkModifier'
    )

    spider = web_parser.WebParser([r'Python', r'linux', r'flask'], all_urls, request_headers=request_headers)
    result = spider.parse()

    print(f"Amount of occurrences of a word Linux per vacancy page: {amount_of_words(result, 'Linux')}")
    print(f"Amount of occurrences of a word Python per vacancy page: {amount_of_words(result, 'Python')}")
    print(f"Amount of occurrences of a word Flask per vacancy page: {amount_of_words(result, 'Flask')}")

    print(f"Average number of occurrence of a word Linux: {average_num_of_occur(result, 'Linux')}")
    print(f"Average number of occurrence of a word Python: {average_num_of_occur(result, 'Python')}")
    print(f"Average number of occurrence of a word Flask: {average_num_of_occur(result, 'Flask')}")
