import logging

import requests

from core.file_manager import PageFile

module_logger = logging.getLogger('jobs_parser')


class Request:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def error_handling(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            module_logger.warning(f'Request, HTTPError. Page with url {self.url} was skipped')
        except requests.exceptions.Timeout:
            module_logger.warning(f'Request, timeout. Page with url {self.url} was skipped')
        except requests.exceptions.TooManyRedirects:
            module_logger.warning(f'Request, too many redirects. Page with url {self.url} was skipped')
        except requests.exceptions.RequestException:
            module_logger.warning(f'RequestException. Page with url {self.url} was skipped')

    def get(self):
        return resp if (resp := requests.get(self.url, headers=self.headers)).ok else self.error_handling(resp)

    def head(self):
        return requests.head(self.url, headers=self.headers)


class Page:
    def __init__(self, url, request_headers=None):
        self.url = url
        self.request_headers = request_headers

    def is_page_exist(self):
        return Request(self.url, self.request_headers).head().ok

    def get_page(self):
        return Request(self.url, self.request_headers).get().text if self.is_page_exist() else None

    def page_file(self):
        page_file = PageFile(self.url)
        if not page_file.is_file_exist():
            page = Page(self.url, self.request_headers)
            data = page.get_page()
            if data:
                page_file.save_file(data)
                module_logger.debug(f'Page with url {self.url} has been downloaded and saved')
        else:
            module_logger.debug(f'Using the cache for the page with url {self.url}')
        return page_file


class Pages:
    def __init__(self, urls, request_headers=None):
        self.urls = urls
        self.request_headers = request_headers

    def is_pages_exist(self):
        return all(map(Page.is_page_exist, [Page(url, self.request_headers) for url in self.urls]))

    def get_files(self):
        page_files = [Page(url, self.request_headers).page_file() for url in self.urls]
        return [page_file for page_file in page_files if page_file.is_file_exist()]
