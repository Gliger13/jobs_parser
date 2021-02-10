import requests
from bs4 import BeautifulSoup


class UrlsCollector:
    def __init__(self, first_page_with_template, request_headers=None):
        self.request_headers = request_headers
        self.first_url = first_page_with_template

    def is_page_exist(self, page_num):
        try:
            requests.head(
                self.first_url.format(page_number=page_num),
                headers=self.request_headers
            ).raise_for_status()
        except requests.exceptions.HTTPError:
            return False
        return True

    def valid_url_pages(self, page_start=0, page_end=None):
        urls = []
        if not page_end:
            while True:
                if self.is_page_exist(page_start):
                    urls.append(self.first_url.format(page_number=page_start))
                    page_start += 1
                else:
                    return urls
        else:
            for page_number in range(page_start, page_end):
                if self.is_page_exist(page_start):
                    urls.append(self.first_url.format(page_number=page_start))
                else:
                    raise requests.exceptions.HTTPError(f'Url on {page_start} page not exist')
            return urls

    def urls_from_page_by_class(self, url, block_class):
        response = requests.get(url, headers=self.request_headers)
        soup = BeautifulSoup(response.text, 'html.parser').body
        urls = soup.find_all('a', block_class, href=True)
        return [url['href'] for url in urls]
