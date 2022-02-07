import pytest
from django.core.exceptions import ValidationError

from books.models import Language, Book, Author
from books.validators import validate_year, validate_isbn


@pytest.mark.django_db
def test_create_language_str_order(language_one, language_two):
    assert Language.objects.all().count() == 2
    assert str(Language.objects.all()[0]) == 'en'


@pytest.mark.django_db
def test_create_author_str_order(author_one, author_two):
    assert Author.objects.all().count() == 2
    assert str(Author.objects.all()[0]) == 'Antoni Macierewicz'


@pytest.mark.django_db
def test_create_book_object_str(book_one):
    assert Book.objects.all().count() == 1
    assert str(book_one) == 'Sex Offenders In Oregon'
    assert book_one.title == 'Sex Offenders in Oregon'
    assert book_one.published_date == 1994
    assert book_one.isbn == '8380498240123'
    assert book_one.page_count == 100
    assert book_one.cover_link == \
           'http://books.google.com/books/content?id=lwidpxMe-AIC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'
    assert book_one.language.lang == 'pl'
    assert len(book_one.author.all()) == 2
    for author in book_one.author.all():
        assert author.name in ('Antoni Macierewicz', 'Jas Fasola')


@pytest.mark.parametrize(
    'value, exc_msg',
    [(2050, 'proper year of publication'),
     (3000, 'proper year of publication'),
     ])
def test_validate_year_model_validators_positive(value, exc_msg):
    with pytest.raises(ValidationError) as exc:
        validate_year(value)
    assert exc_msg in str(exc.value)


@pytest.mark.parametrize(
    'value, exc_msg',
    [(1999, None),
     (2022, None),
     ])
def test_validate_year_model_validators_negative(value, exc_msg):
    assert not validate_year(value)


@pytest.mark.parametrize(
    'value, validity',
    [('123456', 'ISBN should have 13 chars'),
     ('12345678901234', 'ISBN should have 13 chars'),
     ('NAS', 'ISBN should have 13 chars')
     ])
def test_validate_isbn_model_validators_positive(value, validity):
    with pytest.raises(ValidationError) as exc:
        validate_isbn(value)
    assert validity in str(exc.value)


@pytest.mark.parametrize(
    'value, exc_msg',
    [('1234567890123', None),
     ('1234567890999', None),
     ('NA', None)
     ])
def test_validate_year_model_validators_negative(value, exc_msg):
    assert not validate_isbn(value)
