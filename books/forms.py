from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'published_date', 'page_count', 'cover_link', 'language']


class GoogleAPIBookForm(forms.Form):
    keyword = forms.CharField(max_length=50)
