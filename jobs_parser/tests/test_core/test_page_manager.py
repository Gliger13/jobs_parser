import pytest

from jobs_parser.core.page_manager import Page, Pages


@pytest.fixture(params=[
    'https://rabota.by/', 'https://google.com/', 'https://yandex.ru/'
])
def valid_url(request):
    return request.param


@pytest.fixture(params=[
    'https://rabota.by/404', 'https://google.com/404', 'https://yandex.ru/404'
])
def url_with_404(request, request_headers):
    return request.param


@pytest.fixture
def valid_urls():
    return ['https://rabota.by/', 'https://google.com/', 'https://yandex.ru/']


@pytest.mark.smoke
class TestPage:
    def test_is_page_exist(self, valid_url, request_headers):
        assert Page(valid_url, request_headers).is_page_exist()

    def test_is_not_page_exist(self, url_with_404, request_headers):
        assert not Page(url_with_404, request_headers).is_page_exist()


@pytest.mark.critical
class TestPages:
    def test_is_pages_exist(self, valid_urls, request_headers):
        assert Pages(valid_urls, request_headers).is_pages_exist()

    def test_is_not_pages_exist(self, valid_urls, url_with_404, request_headers):
        valid_urls.append(url_with_404)
        assert not Pages(valid_urls, request_headers).is_pages_exist()

    def test_get_files(self, valid_urls, request_headers):
        assert len(Pages(valid_urls, request_headers).get_files()) == 3
