from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import BooksListView, BookEditView, BookDeleteView, BookAddFromGoogleApi, BooksViewSet, BookAddView

app_name = "books"

router = SimpleRouter()
router.register('books', BooksViewSet, basename='api_books')

urlpatterns = [
    path('', BooksListView.as_view(), name="books_list"),
    path('add/', BookAddView.as_view(), name="book_add"),
    path('add_google_api_books/', BookAddFromGoogleApi.as_view(), name="book_google_api_add"),
    path('edit/<int:pk>/', BookEditView.as_view(), name="book_edit"),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name="book_delete"),
] + router.urls
