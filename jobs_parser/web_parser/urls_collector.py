import requests
from bs4 import BeautifulSoup


class UrlsCollector:
    def __init__(self, first_page_with_template, request_headers=None):
        self.request_headers = request_headers
        self.first_url = first_page_with_template

    def valid_url_pages(self):
        urls = []
        try:
            page_number_start = 39
            while True:
                response = requests.head(
                    self.first_url.format(page_number=page_number_start),
                    headers=self.request_headers,
                )
                response.raise_for_status()
                urls.append(self.first_url.format(page_number=page_number_start))
                page_number_start += 1
                print(page_number_start)
        except requests.exceptions.HTTPError:
            return urls

    def urls_from_page_by_class(self, url, block_class):
        response = requests.get(url, headers=self.request_headers)
        soup = BeautifulSoup(response.text, 'html.parser').body
        urls = soup.find_all('a', block_class, href=True)
        return [url['href'] for url in urls]
