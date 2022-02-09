import pytest
import json

from books.helper_func import api_call, author_create, isbn_lookup, book_search, book_create
from books.models import Book, Language

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


def test_api_call_on_mocked_data(mocker, fake_api_call_one, get_mocked_api_data_response_one):
    mocker.patch("books.helper_func.api_call", return_value=fake_api_call_one)
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
     ('1990-2010-2000', 'date', Book, True),
     ('blabla', 'date', Book, True),
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


@pytest.mark.django_db
def test_one_book_create(get_mocked_api_data_response_one):
    books = get_mocked_api_data_response_one.get('items')[0].get('volumeInfo')
    book = book_create(books, Book, Language, 50, 'book_placeholder.jpg')
    assert book.title == 'Slow sex'
    assert Book.objects.all().count() == 1
    assert Book.objects.all().first().cover_link == "/static/images/book_placeholder.jpg"
    assert Book.objects.all().first().language.lang == 'pl'


@pytest.mark.django_db
def test_all_book_create(get_mocked_api_data_response_all):
    books = get_mocked_api_data_response_all.get('items')
    for item in books:
        book_create(item.get('volumeInfo'), Book, Language, 50, 'book_placeholder.jpg')
    book_w_long_title = Book.objects.all().filter(title__icontains='Nicolai').first().title
    exp_title_strip = 'Nicolai Copernici Torunensis De revolutionibus orbium coelestium libri sex'[:50] + '...'
    assert book_w_long_title == exp_title_strip
    assert Book.objects.all().count() == 10
