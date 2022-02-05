import datetime
import json
import re
import urllib.request

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, FormView, DeleteView, UpdateView, CreateView
from rest_framework import viewsets

from . import forms
from .forms import BookForm
from .models import Book, Language, Author
from .permissions import NotPostman
from .serializers import BookSerializer


# Template Views


class BooksListView(ListView):
    model = Book
    template_name = 'books/books.html'
    context_object_name = 'books'
    paginate_by = 8

    def get_queryset(self):
        q = self.request.GET.get('q')
        option = self.request.GET.get('option')

        books = self.model.objects.select_related().all()

        if q and not option:
            books_q = books.filter(title__icontains=q) | books.filter(author__name__icontains=q) | books.filter(
                language__lang__icontains=q)
            return books_q.distinct()
        elif option:
            match option:
                case "title":
                    return books.filter(title__icontains=q).distinct()
                case "author":
                    return books.filter(author__name__icontains=q).distinct()
                case "language":
                    return books.filter(language__lang__icontains=q).distinct()
                case "date":
                    try:
                        q_date = sorted([int(year) for year in q.split('-')])
                    except ValueError('Year in wrong format'):
                        return HttpResponse('Year in wrong format')

                    if len(q_date) == 1 and len(q) == 4:
                        q_date.append(datetime.date.today().year)

                    return books.filter(published_date__gte=q_date[0], published_date__lte=q_date[1]).distinct()
                case _:
                    books_q = books.filter(
                        Q(title__icontains=q) | Q(author__name__icontains=q) | Q(language__lang__icontains=q)
                    )
                    return books_q

        return super().get_queryset()


class BookAddView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_add.html'

    def get_success_url(self):
        messages.success(self.request, "Book has been added", extra_tags='success')
        return reverse_lazy("books:books_list")


class BookEditView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_edit.html'

    def get_success_url(self):
        messages.success(self.request, "Book has been modified", extra_tags='success')
        return reverse_lazy("books:books_list")


class BookDeleteView(DeleteView):
    model = Book

    def get_success_url(self):
        messages.success(self.request, 'Book was deleted successfully')
        return reverse('books:books_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class BookAddFromGoogleApi(FormView):
    form_class = forms.GoogleAPIBookForm
    template_name = 'books/book_google_api_add.html'
    success_url = reverse_lazy('books:books_list')

    google_api_url = 'https://www.googleapis.com/books/v1/volumes?q='

    def get_form_class(self):
        return forms.GoogleAPIBookSelectForm if self.request.session.get('data') else forms.GoogleAPIBookForm

    def get_form(self, *args, **kwargs):
        data = self.request.session.get('data')
        form = super().get_form(*args, **kwargs)

        if data:
            books = []
            for book in data['items']:
                book_vol = book['volumeInfo']
                books.append((book['id'], f"'{book_vol.get('title')}' by {'| '.join(book_vol.get('authors', ''))}, "
                                          f"year: {book_vol.get('publishedDate', 'NA')[:4]}"))
            form.fields['checked'].choices = books

        return form

    def form_valid(self, form):
        keyword = re.sub('[^a-zA-Z]', '+', form.cleaned_data.get('keyword', ''))

        def isbn_lookup(dick):
            for identifier in entry.get('industryIdentifiers', ''):
                if identifier['type'] in ['ISBN_13', 'ISBN_10']:
                    return identifier['identifier']
            return 'NA'

        def author_create(dick, book_obj):
            for author in entry.get('authors', ['NA']):
                author = ['NA'] if not author else author
                obj_author = Author.objects.get_or_create(name=author)[0]
                book_obj.author.add(obj_author)

        def api_call(api_url, q):
            with urllib.request.urlopen(url=f'{self.google_api_url}{keyword}') as r:
                response = r.read().decode('UTF-8')
            return json.loads(response)

        if keyword:
            data = api_call(self.google_api_url, keyword)

            if not data.get('totalItems', 0):
                messages.error(self.request, "We couldn't find any books matching your query", extra_tags='danger')
                return redirect(reverse('books:book_google_api_add'))

            if data.get('totalItems') > 1:
                self.request.session['data'] = data
                return redirect(reverse('books:book_google_api_add'))

            books = data.get('items')[0].get('volumeInfo')

        else:
            data = self.request.session.get('data', {}).get('items')
            self.request.session["data"] = None
            books = [book for book in data if book['id'] in form.cleaned_data.get('checked')]

        for book in books:
            entry = book.get('volumeInfo')

            title = f"{entry.get('title', '')[:50]}{'...' if len(entry.get('title', '')) > 50 else ''}"
            published_date = int(entry.get('publishedDate', '0')[:4])
            isbn = isbn_lookup(entry)
            page_count = entry.get('pageCount', 0)
            cover_link = entry.get('imageLinks').get('thumbnail') if entry.get(
                'imageLinks') else '/static/images/book_placeholder.jpg'
            language = Language.objects.get_or_create(lang=entry.get('language', 'NA')[:2])[0]

            new_book = Book.objects.get_or_create(title=title,
                                                  published_date=published_date,
                                                  isbn=isbn,
                                                  page_count=page_count,
                                                  cover_link=cover_link,
                                                  language=language)
            author_create(entry, new_book[0])
        return super().form_valid(form)


# DRF views

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    search_fields = ['title', 'language']
    permission_classes = (NotPostman,)
