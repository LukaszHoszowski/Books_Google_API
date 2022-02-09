import re

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, FormView, DeleteView, UpdateView, CreateView
from rest_framework import viewsets

from . import forms
from .forms import BookForm
from .helper_func import api_call, isbn_lookup, author_create, book_search, book_create
from .models import Book, Language
from .permissions import NotPostman
from .serializers import BookSerializer


# Template Views


class BooksListView(ListView):
    """
    Display list of :model:`books.Book`, with optional search by title, author and language, paginated by given number

    **Context**

    ``books.Book``
    List of :model:`books.Book` filtered by queried phrase.

    **Template:**

    :template:`books/books.html`
    """
    model = Book
    template_name = 'books/books.html'
    context_object_name = 'books'
    paginate_by = 8

    def get_queryset(self):
        """
        Support for search engine / filtering
        Args:
            self (instance): User request with:
                q (key): Query phrase,
                option (key): Search type,
        Returns:
            queryset: List of searched books from the model.
        """
        self.request.session["data"] = None

        q = self.request.GET.get('q')
        option = self.request.GET.get('option')

        if q:
            return book_search(q, option, self.model)
        return super().get_queryset()


class BookAddView(CreateView):
    """
        Display Form to add instance of :model:`books.Book`

        **Context**

        ``books.Book``
        Post data with book details.

        **Template:**

        :template:`books/books_add.html`
    """
    model = Book
    form_class = BookForm
    template_name = 'books/book_add.html'

    def get(self, request, *args, **kwargs):
        """
            Clearing API data from session.
            Args:
                request (dict): User request.
        """
        self.request.session["data"] = None
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        """
            Success Url with message on success.
            Args:
                self (instance): User request:
            Returns:
                url: Url to list of all books on success.
        """
        messages.success(self.request, "Book has been added", extra_tags='success')
        return reverse_lazy("books:books_list")


class BookEditView(UpdateView):
    """
        Display Form to update instance of :model:`books.Book` by pk

        **Context**

        ``books.Book``
        pk of book instance

        **Template:**

        :template:`books/books_edit.html`
    """
    model = Book
    form_class = BookForm
    template_name = 'books/book_edit.html'

    def get(self, request, *args, **kwargs):
        """
            Clearing API data from session.
            Args:
                request (dict): User request.
        """
        self.request.session["data"] = None
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        """
            Success Url with message on success.
            Args:
                self (instance): User request.
            Returns:
                url: Url to list of all books on success.
        """
        self.request.session["data"] = None
        messages.success(self.request, "Book has been modified", extra_tags='success')
        return reverse_lazy("books:books_list")


class BookDeleteView(DeleteView):
    """
        POST request to delete selected :model:`books.Book` by pk.

        **Context**

        ``books.Book``
        pk of book instance
    """
    model = Book

    def get_success_url(self):
        """
            Success URL with message on success.
            Args:
                self (instance): User request with:
            Returns:
                url: Url to list of all books on success.
        """
        messages.success(self.request, 'Book was deleted successfully', extra_tags='success')
        return reverse('books:books_list')

    def get(self, request, *args, **kwargs):
        """
            Handling of the GET View. GET View is being immediately redirected to POST View, seamless deleting.
            Clearing API data in session
            Args:
                request (dict): User request with:
                    pk (int): Book item id.
        """
        self.request.session["data"] = None
        return self.post(request, *args, **kwargs)


class BookAddFromGoogleApi(FormView):
    """
        Display:
            1) Form with keyword input, User has to enter query phrase for Books Google API,
            2) Form with list of 10 books retrieved from the API expressed as Selects. User has to choose which would
            like to add to the database,
            3) Redirects to list of all books,

        Logic:
            User enters keyword phrase, engine parse Books Google API url with keyword, engine make API call
            and retrieve up to 10 records (API limitation). Whole API response is saved in Session. Engine prepare
            extract from data and render second form with items to select. User selects books which would like to add
            to database. Once submitted engine destructure data and performs data normalization. Author is related to
            Book by many-to-many relation, Language by foreign key. Once completed results are presented on the list of
            all books.

        **Context**

        ``books.Book``
        request with keyword phrase,
        retrieved records stored in session,
        keyword form and retrieved records form,

        **Template:**

        :template:`books/book_google_api_add.html`
    """
    form_class = forms.GoogleAPIBookForm
    template_name = 'books/book_google_api_add.html'
    success_url = reverse_lazy('books:books_list')
    google_api_url = 'https://www.googleapis.com/books/v1/volumes?q='

    def get_form_class(self):
        """
            Select form_class based on app state. If data from API call isn't yet present in session keyword form
            is selected, otherwise form with books to be selected by User.
            Args:
                self (instance): User request with:
                    data (json): API response
            Returns:
                form_class: form prototype.
        """
        return forms.GoogleAPIBookSelectForm if self.request.session.get('data') else forms.GoogleAPIBookForm

    def get_form(self, *args, **kwargs):
        """
            Display title, authors and year of publication as select tags in form based on data stored in session.
            Args:
                self (instance): User request with:
                    data (json): API response
            Returns:
                form: form with initials.
        """
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
        """
            Engine performs keyword transformation (special signs and spaces replaced with "+" according to Google API
            specification). If keyword is valid engine make API call with given keyword. If results are present API
            response is saved in session, if not engine send message about lack of results. Retrieved results are
            extracted, engine prepares list of title, authors, year of publication to present the data and let the User
            select which records should be stored in database. Once submitted data is structured, authors, language
            and rest of data is stored in seperated tables with relations. If success redirect to list of all books with
            success message.

            Args:
                form (form): empty form,
                'session' (dict): session with data from API call in json,
                'title' (str): truncated if exceed 50 chars,
                'published_date' (int): truncated to 4 digits,
                'isbn' (str): 13 or 10 chars, default: "NA",
                'page_count' (int): has to be positive, default: 0,
                'cover_link' (str): has to be Url like,
                'language' (str): foreign key,
                'author' (str): many-to-many,
            Returns:
                form_valid: True/False.
        """
        keyword = re.sub('[^a-zA-Z]', '+', form.cleaned_data.get('keyword', ''))

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
            print(books)
        for book in books:
            entry = book.get('volumeInfo')

            new_book = book_create(entry, Book, Language, 50, 'book_placeholder.jpg')
            author_create(entry, new_book)
        return super().form_valid(form)


# DRF views

class BooksViewSet(viewsets.ModelViewSet):
    """
        Display:
            CRUD methods for Book instances as RestAPI.

        **Context**

        ``books.Book``
        Postman queries not allowed.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    search_fields = ['title', 'language']
    permission_classes = (NotPostman,)
