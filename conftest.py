import pytest

from books.models import Language, Author, Book


@pytest.fixture(params=('pl',))
def language_one(db, request) -> Language:
    return Language.objects.create(lang=request.param)


@pytest.fixture(params=('en',))
def language_two(db, request) -> Language:
    return Language.objects.create(lang=request.param)


@pytest.fixture(params=('Antoni Macierewicz',))
def author_one(db, request) -> Author:
    return Author.objects.create(name=request.param)


@pytest.fixture(params=('Jas Fasola',))
def author_two(db, request) -> Author:
    return Author.objects.create(name=request.param)


@pytest.fixture(params=('Sex Offenders in Oregon',))
def book_one(db, language_one, author_one, author_two, request) -> Book:
    sample_url = 'http://books.google.com/books/content?id=lwidpxMe-AIC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'

    book = Book.objects.create(title=request.param,
                               published_date=1994,
                               isbn='8380498240',
                               page_count=100,
                               cover_link=sample_url,
                               language=language_one)
    book.author.add(author_one)
    book.author.add(author_two)

    return book


@pytest.fixture(params=('Bible',))
def book_two(db, language_two, authors_variable, request) -> Book:
    sample_url = 'http://books.google.com/books/content?id=lwidpxMe-AIC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'

    book = Book.objects.create(title=request.param,
                               published_date=1994,
                               isbn='1234567890123',
                               page_count=0,
                               cover_link=sample_url,
                               language=language_two)

    for author in authors_variable:
        author = Author.objects.create(name=author)
        book.author.add(author)

    return book
