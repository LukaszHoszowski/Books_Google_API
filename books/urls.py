from django.urls import path

from .views import BooksListView, BookDetailsView, BookOrCreateView, BookDeleteView, BookAddFromGoogleApi

app_name = "books"

urlpatterns = [
    path('', BooksListView.as_view(), name="books_list"),
    path('<int:pk>/', BookDetailsView.as_view(), name="book_detail"),
    path('add/', BookOrCreateView.as_view(), name="book_add"),
    path('add_google_api_books/', BookAddFromGoogleApi.as_view(), name="book_google_api_add"),
    path('edit/<int:pk>/', BookOrCreateView.as_view(), name="book_edit"),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name="book_delete"),
]
