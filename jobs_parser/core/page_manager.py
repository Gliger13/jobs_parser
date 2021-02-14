import requests

from core.file_manager import PageFile


class Request:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def error_handling(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise requests.exceptions.HTTPError(f'Page on {self.url} not exist.')
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.TooManyRedirects:
            pass
        except requests.exceptions.RequestException:
            pass

    def get(self):
        return resp if (resp := requests.get(self.url, headers=self.headers)).ok else self.error_handling(resp)

    def head(self):
        return resp if (resp := requests.head(self.url, headers=self.headers)).ok else self.error_handling(resp)


class Page:
    def __init__(self, url, request_headers=None):
        self.url = url
        self.request_headers = request_headers

    def is_page_exist(self):
        try:
            Request(self.url, self.request_headers).head()
        except requests.exceptions.HTTPError:
            return False
        return True

    def get_page(self):
        return Request(self.url, self.request_headers).get().text if self.is_page_exist() else None

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
        return [Page(url, self.request_headers).page_file() for url in self.urls]
