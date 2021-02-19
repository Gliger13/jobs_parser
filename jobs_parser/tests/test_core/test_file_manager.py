import pytest

from jobs_parser.core.file_manager import PageFile, TmpManager


@pytest.fixture(autouse=True)
def clear_tmp_dir():
    return TmpManager().clear_tmp_dir()


@pytest.fixture(params=[
    ('https://rabota.by/', 'c1b0263e80059570c3bae484f172e0f1.html'),
    ('https://google.com/', 'f82438a9862a39d642f39887b3e8e5b4.html'),
    ('https://yandex.ru/', '30b7df27e9f842b33cf9e517c98a075e.html'),
])
def url_filename(request):
    return request.param


@pytest.mark.smoke
class TestPageFile:
    def test_filename(self, url_filename):
        url, correct_filename = url_filename
        assert PageFile(url).filename == correct_filename

    def test_file_not_exist(self, url_filename):
        assert not PageFile(url_filename[0]).is_file_exist()

    def test_file_exist(self, url_filename):
        page_file = PageFile(url_filename[0])
        page_file.save_file('useless data')
        assert page_file.is_file_exist()
