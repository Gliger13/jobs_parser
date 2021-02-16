from bs4 import BeautifulSoup

from core.file_manager import PageFile


class SoupMaker:
    """
    Processes html files

    Parameters
    ----------
    page_file: PageFile
        The html file for processing
    """
    def __init__(self, page_file: PageFile):
        self.page_file = page_file

        with open(self.page_file.file_path, 'r', encoding='utf-8') as file:
            self.soup = BeautifulSoup(file, 'html.parser').body

    def remove_from_soup(self, classes_to_exclude: [str]) -> BeautifulSoup:
        for block_class in classes_to_exclude:
            if found := self.soup.find('div', block_class):
                found.decompose()
        return self.soup

    def find_urls_by_class(self, block_class: str) -> list:
        return self.soup.find_all('a', block_class, href=True)

    def get_text(self) -> str:
        return self.soup.get_text()
