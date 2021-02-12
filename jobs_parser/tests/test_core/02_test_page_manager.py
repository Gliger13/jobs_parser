from core.page_manager import Page, Pages


class TestPage:
    def setup(self):
        self.request_headers = {'user-agent': 'job_parser/0.1.0'}

    def test_is_page_exist(self):
        assert Page('https://rabota.by/', self.request_headers).is_page_exist()

    def test_is_not_page_exist(self):
        assert not Page('https://google.com/404', self.request_headers).is_page_exist()


class TestPages:
    def setup(self):
        self.request_headers = {'user-agent': 'job_parser/0.1.0'}
        self.urls = ['https://rabota.by/', 'https://google.com/']
        self.url_with_404 = 'https://google.com/404'

    def test_is_pages_exist(self):
        assert Pages(self.urls, self.request_headers).is_pages_exist()

    def test_is_not_pages_exist(self):
        self.urls.append(self.url_with_404)
        assert not Pages(self.urls, self.request_headers).is_pages_exist()

    def test_get_files(self):
        assert len(Pages(self.urls, self.request_headers).get_files()) == 2
