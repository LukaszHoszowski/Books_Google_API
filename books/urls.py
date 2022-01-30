from django.urls import path

from .views import BooksListView, BookDetailsView, BookOrCreateView, BookDeleteView

app_name = "books"

urlpatterns = [
    path('', BooksListView.as_view(), name="books_list"),
    path('<int:pk>/', BookDetailsView.as_view(), name="book_detail"),
    path('add/', BookOrCreateView.as_view(), name="book_add"),
    path('edit/<int:pk>/', BookOrCreateView.as_view(), name="book_edit"),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name="book_delete"),
]
