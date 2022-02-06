from django.db import models

from .validators import validate_year, validate_isbn


class Book(models.Model):
    """
    Stores a single Book entry, related to :model:`books.Author` and :model:`books.Language` ordered ascending by title

    **Return** : capitalized title
    """
    title = models.CharField(max_length=54, help_text='Title')
    published_date = models.SmallIntegerField(null=True, blank=True, validators=[validate_year], help_text='Publish year')
    isbn = models.CharField(max_length=13, null=True, blank=True,  validators=[validate_isbn], help_text='ISBN')
    page_count = models.PositiveIntegerField(null=True, blank=True, help_text='Page count')
    cover_link = models.URLField(null=True, blank=True, help_text='Link to cover of the book')
    language = models.ForeignKey('Language', on_delete=models.DO_NOTHING, related_name='languages', help_text='Book language')
    author = models.ManyToManyField('Author', related_name="authors", blank=True, help_text='Authors list')

    def __str__(self):
        return f'{self.title.title()}'

    class Meta:
        ordering = ['title']


class Author(models.Model):
    """
    Stores a single Author entry, related to :model:`books.Book` ordered ascending by name

    **Return** : capitalized name
    """
    name = models.CharField(max_length=200, help_text='Author name')

    def __str__(self):
        return f'{self.name.title()}'

    class Meta:
        ordering = ['name']


class Language(models.Model):
    """
    Stores a single Language entry, related to :model:`books.Book` ordered ascending by lang

    **Return** : lowered name, in ISO 639-1 format (two-letter code)
    """
    lang = models.CharField(max_length=2, help_text='Language')

    def __str__(self):
        return f'{self.lang}'

    class Meta:
        ordering = ['lang'.lower()]
