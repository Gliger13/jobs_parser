import pytest


@pytest.fixture
def request_headers():
    return {'user-agent': 'job_parser/1.0.0'}


@pytest.fixture
def classes_to_exclude():
    return ['recommended-vacancies', 'related-vacancies-wrapper']


@pytest.fixture
def block_class():
    return 'bloko-link HH-LinkModifier'
