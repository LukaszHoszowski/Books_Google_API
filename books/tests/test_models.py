import pytest

from ..models import Language, Book, Author


@pytest.mark.django_db
def test_create_language_str_order(language_one, language_two):
    assert Language.objects.all().count() == 2
    assert str(Language.objects.all()[0]) == 'en'


@pytest.mark.django_db
def test_create_author_str_order(author_one, author_two):
    assert Author.objects.all().count() == 2
    assert str(Author.objects.all()[0]) == 'Antoni Macierewicz'


# @pytest.mark.django_db
# def test_create_book_object_str(book_one):
#     assert Book.objects.all().count() == 1
#     assert str(book_one) == 'Sex Offenders In Oregon'
#     assert book_one.title == 'Sex Offenders in Oregon'
#     assert book_one.published_date == 1994
#     assert book_one.isbn == '8380498240'
#     assert book_one.page_count == 100
#     assert book_one.cover_link == 'http://books.google.com/books/content?id=lwidpxMe-AIC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'
#     assert book_one.language.lang == 'pl'
#     assert len(book_one.author.all()) == 2
#     for author in book_one.author.all():
#         assert author.name in ('Antoni Macierewicz', 'Jas Fasola')
