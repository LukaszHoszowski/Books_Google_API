from django.db import models

from .validators import validate_year, validate_isbn


class Book(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.SmallIntegerField(validators=[validate_year])
    isbn = models.CharField(max_length=13, validators=[validate_isbn])
    page_count = models.PositiveIntegerField(help_text='Page count')
    cover_link = models.URLField()
    language = models.ForeignKey('Language', on_delete=models.DO_NOTHING)
    author = models.ManyToManyField('Author', related_name="authors")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['title']


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']


class Language(models.Model):
    lang = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.lang}'

    class Meta:
        ordering = ['lang']
