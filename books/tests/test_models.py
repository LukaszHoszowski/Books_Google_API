import pytest

from ..models import Language, Book, Author


@pytest.fixture
def book(db) -> Book:
    language = Language.objects.create(lang='en')

    book = Book.objects.create(title='Adult Sex Offenders in Oregon',
                               published_date=1994,
                               isbn='8380498240',
                               page_count=100,
                               cover_link='http://books.google.com/books/content?id=lwidpxMe-AIC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api',
                               language=language)

    for author in ('Jas Fasola', 'Antoni Macierewicz'):
        author = Author.objects.create(name=author)
        book.author.add(author)

    return book


def test_create_book(book):
    print(book.title)
    assert book.title == 'Adult Sex Offenders in Oregon'

# @pytest.mark.django_db
# def test_create_superuser():
#     User = get_user_model()
#     user = User.objects.create_superuser(
#         username='test_super_user',
#         email='test@super_user.com',
#         password='test'
#     )
#
#     assert User.objects.filter(is_superuser=True).count() == 1
#     assert user.username == 'test_super_user'
#     assert user.email == 'test@super_user.com'
#     assert user.is_staff
#     assert user.is_active
