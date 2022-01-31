from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import BooksListView, BookDetailsView, BookOrCreateView, BookDeleteView, BookAddFromGoogleApi, BooksViewSet

app_name = "books"

router = SimpleRouter()
router.register('books', BooksViewSet, basename='api_books')

urlpatterns = [
    path('books/', BooksListView.as_view(), name="books_list"),
    path('<int:pk>/', BookDetailsView.as_view(), name="book_detail"),
    path('add/', BookOrCreateView.as_view(), name="book_add"),
    path('add_google_api_books/', BookAddFromGoogleApi.as_view(), name="book_google_api_add"),
    path('edit/<int:pk>/', BookOrCreateView.as_view(), name="book_edit"),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name="book_delete"),
] + router.urls
