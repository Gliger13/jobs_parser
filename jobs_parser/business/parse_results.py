class ParseResult:
    """
    Store parsing result of page

    Parameters
    ----------
    url: str
        URL to the page that has been parsed
    words_to_find: [str]
        The list of words to find in page
    found_words: [str]
        The list of words which were found
    """
    def __init__(self, url: str, words_to_find: [str], found_words: [str]):
        self.url = url
        self.words_to_find = words_to_find
        self.found_words = found_words

    def __str__(self):
        return f"On {self.url}: " + self.count_words_str()

    def __repr__(self):
        return self.__str__()

    def count_word(self, word: str) -> int:
        return (list(map(str.title, self.found_words))).count(word.title())

    def count_word_str(self, word: str) -> str:
        return f"{word} - {self.count_word(word)}"

    def count_words(self) -> dict:
        return {word: self.count_word(word) for word in self.words_to_find}

    def count_words_str(self) -> str:
        return ", ".join([self.count_word_str(word) for word in self.words_to_find])


class ParseResults:
    """
    Store parsing result of page

    Parameters
    ----------
    urls: [str]
        Urls to the pages that has been parsed
    words_to_find: [str]
        The list of words to find in page
    parse_results: [ParseResult]
        The list of parse result of urls
    """
    def __init__(self, urls: [str], words_to_find: [str], parse_results: [ParseResult]):
        self.urls = urls
        self.words_to_find = words_to_find
        self.parse_results = parse_results

    def count_word_occurrence(self, word: str) -> int:
        return sum([parse_result.count_word(word) for parse_result in self.parse_results])

    def count_words_occurrence(self) -> dict:
        return {word: self.count_word_occurrence(word) for word in self.words_to_find}

    def average_num_of_word_occur(self, word):
        return round(self.count_word_occurrence(word) / len(self.urls), 2) if len(self.urls) else 0

    def average_num_of_words_occur(self) -> dict:
        return {word: self.average_num_of_word_occur(word) for word in self.words_to_find}

    def json(self) -> dict:
        return {
            'urls': self.urls,
            'words_to_find': self.words_to_find,
            'parse_results': self.count_words_occurrence(),
        }
