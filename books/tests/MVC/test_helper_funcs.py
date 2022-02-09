import pytest
import json

from books.helper_func import api_call, author_create, isbn_lookup, book_search
from books.models import Book

GOOGLE_API_URL = 'https://www.googleapis.com/books/v1/volumes?q='
KEYWORD = '8326841218'


def dump_json_api_data_to_file(func):
    with open('books/tests/MVC/api_test_data.json', 'w', encoding='utf-8') as f:
        json.dump(func, f, ensure_ascii=False, indent=4)


def test_api_call_response():
    # dump_json_api_data_to_file(api_call(GOOGLE_API_URL, KEYWORD))
    assert api_call(GOOGLE_API_URL, KEYWORD), "Books Google API out of service"


@pytest.mark.django_db
def test_author_create_model(book_one, get_mocked_api_data_response_all):
    entry = get_mocked_api_data_response_all.get('items')[0].get('volumeInfo')
    author_create(entry, book_one)
    assert len(book_one.author.all()) == 4


def test_isbn_13_lookup(get_mocked_api_data_response_all):
    entry = get_mocked_api_data_response_all.get('items')[0].get('volumeInfo')

    assert isbn_lookup(entry) == '9788326841217'


def test_isbn_na_lookup(get_mocked_api_data_response_all):
    entry = get_mocked_api_data_response_all.get('items')[3].get('volumeInfo')

    assert isbn_lookup(entry) == 'NA'


def test_api_call_on_mocked_data(mocker, fake_api_call, get_mocked_api_data_response_one):
    mocker.patch("books.helper_func.api_call", return_value=fake_api_call)
    api_call_keyword = api_call(GOOGLE_API_URL, KEYWORD)
    assert api_call_keyword["totalItems"] == get_mocked_api_data_response_one["totalItems"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    'q, , option, book_model_class, validity',
    [('oregon', 'title', Book, True),
     ('Sex', 'title', Book, True),
     ('bib', 'title', Book, False),
     ('i', 'title', Book, True),
     ('Adult', 'title', Book, False),
     ('fsdhrjzhdfhzdf', 'title', Book, False),
     ])
def test_book_search_title(q, option, book_model_class, validity, book_one, book_two):
    assert bool(book_one in list(book_search(q, option, book_model_class))) == validity


@pytest.mark.django_db
@pytest.mark.parametrize(
    'q, , option, book_model_class, validity',
    [('Macierewicz', 'author', Book, True),
     ('Jas', 'author', Book, True),
     ('Fasola', 'author', Book, True),
     ('Antoni', 'author', Book, True),
     ('Pitt', 'author', Book, False),
     ])
def test_book_search_author(q, option, book_model_class, validity, book_one, book_two):
    assert bool(book_one in list(book_search(q, option, book_model_class))) == validity


@pytest.mark.django_db
@pytest.mark.parametrize(
    'q, , option, book_model_class, validity',
    [('en', 'language', Book, False),
     ('pl', 'language', Book, True),
     ('pt', 'language', Book, False),
     ('e', 'language', Book, False),
     ])
def test_book_search_language(q, option, book_model_class, validity, book_one, book_two):
    assert bool(book_one in list(book_search(q, option, book_model_class))) == validity


@pytest.mark.django_db
@pytest.mark.parametrize(
    'q, , option, book_model_class, validity',
    [('1994-1995', 'date', Book, True),
     ('1994', 'date', Book, True),
     ('1990', 'date', Book, True),
     ('1996', 'date', Book, False),
     ('2000-2010', 'date', Book, False),
     ('1990-2010', 'date', Book, True),
     ])
def test_book_search_year(q, option, book_model_class, validity, book_one, book_two):
    assert bool(book_one in list(book_search(q, option, book_model_class))) == validity


@pytest.mark.django_db
@pytest.mark.parametrize(
    'q, , option, book_model_class, validity',
    [('1994', 'What are you looking for?', Book, False),
     ('Sex', 'What are you looking for?', Book, True),
     ('OREGON', 'What are you looking for?', Book, True),
     ('Bible', 'What are you looking for?', Book, False),
     ('Fasola', 'What are you looking for?', Book, True),
     ('1996', 'bla bla', Book, False),
     ])
def test_book_search_wild(q, option, book_model_class, validity, book_one, book_two):
    assert bool(book_one in list(book_search(q, option, book_model_class))) == validity
