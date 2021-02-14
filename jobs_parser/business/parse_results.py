class ParseResult:
    def __init__(self, url: str, words_to_find, found_words: list):
        self.url = url
        self.words_to_find = words_to_find
        self.found_words = found_words

    def __str__(self):
        return f"On {self.url}: " + self.count_words_str()

    def __repr__(self):
        return self.__str__()

    def count_word(self, word):
        return (list(map(str.title, self.found_words))).count(word.title())

    def count_word_str(self, word):
        return f"{word} - {self.count_word(word)}"

    def count_words(self):
        return {word: self.count_word(word) for word in self.words_to_find}

    def count_words_str(self):
        return ", ".join([self.count_word_str(word) for word in self.words_to_find])


class ParseResults:
    def __init__(self, urls, words_to_find, parse_result):
        self.urls = urls
        self.words_to_find = words_to_find
        self.parse_results = parse_result

    def count_word_occurrence(self, word):
        return sum([parse_result.count_word(word) for parse_result in self.parse_results])

    def count_words_occurrence(self):
        return {word: self.count_word_occurrence(word) for word in self.words_to_find}

    def average_num_of_word_occur(self, word):
        return round(self.count_word_occurrence(word) / len(self.urls), 2)

    def average_num_of_words_occur(self):
        return {word: self.average_num_of_word_occur(word) for word in self.words_to_find}
