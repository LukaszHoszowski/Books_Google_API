import json
from http import HTTPStatus

import pytest
from django.urls import reverse
from django.test import Client

from books.models import Language, Author, Book


# Model helpers

@pytest.fixture(params=('pl',))
def language_one(request) -> Language:
    return Language.objects.create(lang=request.param)


@pytest.fixture(params=('en',))
def language_two(request) -> Language:
    return Language.objects.create(lang=request.param)


@pytest.fixture(params=('Antoni Macierewicz',))
def author_one(request) -> Author:
    return Author.objects.create(name=request.param)


@pytest.fixture(params=('Jas Fasola',))
def author_two(request) -> Author:
    return Author.objects.create(name=request.param)


@pytest.fixture(params=('Sex Offenders in Oregon',))
def book_one(language_one, author_one, author_two, request) -> Book:
    sample_url = 'http://books.google.com/books/content?id=lwidpxMe-AIC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'

    book = Book.objects.create(title=request.param,
                               published_date=1994,
                               isbn='8380498240123',
                               page_count=100,
                               cover_link=sample_url,
                               language=language_one)
    book.author.add(author_one)
    book.author.add(author_two)

    return book


@pytest.fixture(params=('Bible',))
def book_two(language_two, author_two, request) -> Book:
    sample_url = 'http://books.google.com/books/content?id=lwidpxMe-AIC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'

    book = Book.objects.create(title=request.param,
                               published_date=1996,
                               isbn='1234567890123',
                               page_count=0,
                               cover_link=sample_url,
                               language=language_two)

    book.author.add(author_two)

    return book


# View helpers

@pytest.fixture
def get_books_empty_list_response(db):
    client = Client(enforce_csrf_checks=True)
    url = reverse('books_list')
    return client.get(url)


@pytest.fixture
def get_books_book_one_list_response(db, book_one):
    client = Client(enforce_csrf_checks=True)
    url = reverse('books_list')
    return client.get(url)


@pytest.fixture
def get_book_add_response(db):
    client = Client(enforce_csrf_checks=True)
    url = reverse('books:book_add')
    return client.get(url)


@pytest.fixture
def get_book_add_google_api_books_response():
    client = Client(enforce_csrf_checks=True)
    url = reverse('books:book_google_api_add')
    return client.get(url)


@pytest.fixture
def get_book_edit_response(db, book_one):
    client = Client(enforce_csrf_checks=True)
    url = reverse('books:book_edit', kwargs={'pk': book_one.pk})
    return client.get(url)


@pytest.fixture
def get_book_google_api_add_response():
    client = Client(enforce_csrf_checks=True)
    url = reverse('book_google_api_add')
    return client.get(url)


@pytest.fixture
def get_mocked_api_data_response_all():
    with open('books/tests/MVC/api_test_data_all.json') as f:
        return json.load(f)


@pytest.fixture
def get_mocked_api_data_response_one():
    with open('books/tests/MVC/api_test_data_one.json') as f:
        return json.load(f)


@pytest.fixture
def get_mocked_api_data_response_zero():
    with open('books/tests/MVC/api_test_data_zero.json') as f:
        return json.load(f)


@pytest.fixture()
def fake_api_call(mocker, get_mocked_api_data_response_one):
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=get_mocked_api_data_response_one)
    fake_resp.status_code = HTTPStatus.OK
    return fake_resp
