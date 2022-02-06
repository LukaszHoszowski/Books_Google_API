from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'published_date', 'page_count', 'cover_link', 'language']


class GoogleAPIBookForm(forms.Form):
    keyword = forms.CharField(max_length=50)


class GoogleAPIBookSelectForm(forms.Form):
    checked = forms.MultipleChoiceField(label='Select books',
                                        widget=forms.CheckboxSelectMultiple(attrs={'checked': True}),
                                        help_text='Choose as many you want :P',
                                        initial=True)
