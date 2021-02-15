from bs4 import BeautifulSoup


class SoupMaker:
    def __init__(self, page_file):
        self.page_file = page_file

        with open(self.page_file.file_path, 'r', encoding='utf-8') as file:
            self.soup = BeautifulSoup(file, 'html.parser').body

    def remove_from_soup(self, classes_to_exclude):
        for block_class in classes_to_exclude:
            if found := self.soup.find('div', block_class):
                found.decompose()
        return self.soup

    def find_urls_by_class(self, block_class):
        return self.soup.find_all('a', block_class, href=True)

    def get_text(self):
        return self.soup.get_text()
