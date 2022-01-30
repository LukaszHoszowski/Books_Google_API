from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView

from . import forms, models
from .models import Book


class BooksListView(ListView):
    model = Book
    template_name = 'books/books.html'
    context_object_name = 'books'
    paginate_by = 6


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
        form = forms.BookForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('books:books_list')

        return render(request, 'books/book_add_or_edit.html', {'form': form})
