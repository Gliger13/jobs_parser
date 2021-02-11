import requests

from web_parser.file_manager import PageFile


class Page:
    def __init__(self, url, request_headers=None):
        self.url = url
        self.request_headers = request_headers

    def is_page_exist(self):
        try:
            requests.head(self.url, headers=self.request_headers).raise_for_status()
        except requests.exceptions.HTTPError:
            return False
        return True

    def get_page(self):
        if self.is_page_exist():
            return requests.get(self.url, headers=self.request_headers).text
        else:
            raise requests.exceptions.HTTPError(f'Page on {self.url} not exist.')

    def page_file(self):
        page_file = PageFile(self.url)
        if not page_file.is_file_exist():
            page = Page(self.url, self.request_headers)
            data = page.get_page()
            page_file.save_file(data)
        return page_file


class Pages:
    def __init__(self, urls, request_headers=None):
        self.urls = urls
        self.request_headers = request_headers

    def is_pages_exist(self):
        return all(map(Page.is_page_exist, [Page(url, self.request_headers) for url in self.urls]))

    def get_files(self):
        return [Page(url).page_file for url in self.urls]
