from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView, DeleteView

from . import forms, models
from .models import Book


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

            # books_q = books.filter(
            #     Q(title__icontains=q) | Q(author__name__icontains=q) | Q(language__lang__icontains=q)
            # )
            books_q = books.filter(title__icontains=q) | \
                      books.filter(author__name__icontains=q) | \
                      books.filter(language__lang__icontains=q)

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
                    q = sorted([int(year) for year in q.split('-')])
                    return books.filter(published_date__gte=q[0], published_date__lte=q[1]).distinct()

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
