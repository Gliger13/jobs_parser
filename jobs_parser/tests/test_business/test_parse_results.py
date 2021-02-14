import pytest

from business.parse_results import ParseResult


@pytest.mark.smoke
class TestParseResult:
    @pytest.mark.parametrize('test_input,expected', [
        (['Linux', 'linux', 'flask', 'Linux', 'Flask', 'Linux', 'Flask', 'linux', 'Flask'],
         {'python': 0, 'linux': 5, 'flask': 4}),
        (['Linux', 'Linux', 'Linux', 'Linux', 'Linux'],
         {'python': 0, 'linux': 5, 'flask': 0}),
        (['Python', 'Linux', 'Flask', 'Python', 'Linux', 'Python'],
         {'python': 3, 'linux': 2, 'flask': 1})
    ])
    def test_count_word(self, test_input, expected):
        return ParseResult('', ['python', 'linux', 'Flask'], test_input) == expected
