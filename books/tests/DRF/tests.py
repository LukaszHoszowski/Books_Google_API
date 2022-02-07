from django.test import TestCase

from books.models import Book, Author, Language


class BookTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        language = Language.objects.create(lang='en')
        author = Author.objects.create(name='Jan Kowalski')
        book = Book.objects.create(title='costam',
                                   published_date=1999,
                                   isbn='1111222233334',
                                   page_count=100,
                                   cover_link='http://books.google.com/books/content?id=mnkbAQAAMAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api',
                                   language=language)
        book.author.add(author)

    def test_post_content(self):
        book = Book.objects.first()
        self.assertEqual(book.title, 'costam')
        self.assertEqual(book.published_date, 1999)
        self.assertEqual(book.isbn, '1111222233334')
        self.assertEqual(book.page_count, 100)
        self.assertEqual(book.cover_link, 'http://books.google.com/books/content?id=mnkbAQAAMAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api')
        self.assertEqual(book.language.lang, 'en')
        self.assertEqual(book.author.first().name, 'Jan Kowalski')
