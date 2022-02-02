import datetime
import json
import urllib.request

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView, DeleteView
from rest_framework import viewsets

from . import forms, models
from .models import Book, Language, Author
from .permissions import NotPostman
from .serializers import BookSerializer


# Template Views


class BooksListView(ListView):
    model = Book
    template_name = 'books/books.html'
    context_object_name = 'books'
    paginate_by = 4

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

                    if len(q_date) == 2 and len(q) == 9:
                        pass
                    elif len(q_date) == 1 and len(q) == 4:
                        q_date.append(datetime.date.today().year)

                    return books.filter(published_date__gte=q_date[0], published_date__lte=q_date[1]).distinct()
                case _:
                    books_q = books.filter(
                        Q(title__icontains=q) | Q(author__name__icontains=q) | Q(language__lang__icontains=q)
                    )
                    return books_q

        return super().get_queryset()


class BookDetailsView(DetailView):
    model = Book
    template_name = 'books/book.html'
    context_object_name = 'book'


class BookCreateView(CreateView):
    model = Book
    exclude = ['id']
    template_name = 'books/book_add_or_edit.html'
    success_url = reverse_lazy('books:books_list')


class BookUpdateView(UpdateView):
    model = Book
    exclude = ['id']
    template_name = 'books/book_update.html'


class BookCreateUpdateView(FormView):
    form_class = forms.BookForm
    template_name = 'books/book_add_or_edit.html'
    success_url = reverse_lazy('books:books_list')


class BookOrCreateView(View):
    def get(self, request, pk=None):
        book_pk = models.Book.objects.filter(pk=pk)
        if book_pk:
            form = forms.BookForm(instance=book_pk.first())
        else:
            form = forms.BookForm()

        return render(request, 'books/book_add_or_edit.html', {'form': form})

    def post(self, request, pk=None):
        if pk:
            form = forms.BookForm(request.POST, instance=Book.objects.get(pk=pk))
        else:
            form = forms.BookForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('books:books_list')

        return render(request, 'books/book_add_or_edit.html', {'form': form})


class BookDeleteView(DeleteView):
    model = Book

    def get_success_url(self):
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
                                          f"year: {book_vol.get('publishedDate')[:4]}"))
            form.fields['checked'].choices = books

        return form

    def form_valid(self, form):
        keyword = form.cleaned_data.get('keyword', '')

        def isbn_lookup(dick):
            for identifier in entry.get('industryIdentifiers', ''):
                if identifier['type'] == 'ISBN_13':
                    return identifier['identifier']
                if identifier['type'] == 'ISBN_10':
                    return identifier['identifier']
            return 'NA'

        def author_create(dick, book_obj):
            for author in entry.get('authors', ['NA']):
                author = ['NA'] if not author else author
                obj_author = Author.objects.get_or_create(name=author)[0]
                book_obj.author.add(obj_author)

        if keyword:
            with urllib.request.urlopen(url=f'{self.google_api_url}{keyword}') as r:
                response = r.read().decode('UTF-8')
                data = json.loads(response)

            if data.get('totalItems', 0) == 0:
                messages.error(self.request, "We couldn't find such book", extra_tags='danger')
                return redirect(reverse('books:book_google_api_add'))

            if data.get('totalItems') > 1:
                print(form.cleaned_data.get('checked'))
                self.request.session['data'] = data
                return redirect(reverse('books:book_google_api_add'))

            books = data.get('items')[0].get('volumeInfo')

        else:
            data = self.request.session.get('data', {}).get('items')
            self.request.session["data"] = None
            books = [book for book in data if book['id'] in form.cleaned_data.get('checked')]

        for book in books:
            entry = book.get('volumeInfo')

            new_book = Book.objects.get_or_create(title=entry.get('title', ''),
                                                  published_date=int(entry.get('publishedDate', '0')[:4]),
                                                  isbn=isbn_lookup(entry),
                                                  page_count=entry.get('pageCount', 0),
                                                  cover_link=entry.get('imageLinks', '').get('thumbnail')
                                                  if entry.get('imageLinks') else '',
                                                  language=Language.objects.get_or_create(
                                                      lang=entry.get('language', 'NA')[:2])[0]
                                                  )
            author_create(entry, new_book[0])
        return super().form_valid(form)


class BookSelectFromGoogleApi(FormView):
    form_class = forms.GoogleAPIBookSelectForm
    template_name = 'books/book_google_api_select.html'
    success_url = reverse_lazy('books:books_list')

    google_api_url = 'https://www.googleapis.com/books/v1/volumes?q='

    def form_valid(self, form, **kwargs):
        keyword = self.request.POST.get('keyword')
        # data = requests.get(f'{self.google_api_url}{keyword}').json()['items']
        with urllib.request.urlopen(url=f'https://www.googleapis.com/books/v1/volumes?q={keyword}') as r:
            result = r.read().decode('UTF-8')
            data = json.loads(result)

        def isbn_lookup(dick):
            for identifier in entry.get('industryIdentifiers', ''):
                if identifier['type'] == 'ISBN_13':
                    return identifier['identifier']
            return 'NA'

        def author_create(dick, book_obj):
            for author in entry.get('authors', ['NA']):
                author = ['NA'] if not author else author
                obj_author = Author.objects.get_or_create(name=author)[0]
                book_obj.author.add(obj_author)

        for book in data:
            if book:
                entry = book.get('volumeInfo')

                new_book = Book.objects.get_or_create(title=entry.get('title', ''),
                                                      published_date=int(entry.get('publishedDate', '0')[:4]),
                                                      isbn=isbn_lookup(entry),
                                                      page_count=entry.get('pageCount', 0),
                                                      cover_link=entry.get('imageLinks', '').get('thumbnail')
                                                      if entry.get('imageLinks') else '',
                                                      language=Language.objects.get_or_create(
                                                          lang=entry.get('language', 'NA'))[0]
                                                      )
                author_create(entry, new_book[0])
                print(form)
        return HttpResponseRedirect(self.get_success_url())


# DRF views

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    search_fields = ['title', 'language']
    permission_classes = (NotPostman,)
