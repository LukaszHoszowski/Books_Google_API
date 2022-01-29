from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    published_date = models.DateTimeField()
    isbn = models.CharField(max_length=13)
    page_count = models.IntegerField(help_text='Page count')
    cover_link = models.CharField(max_length=300)
    language = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['title']
