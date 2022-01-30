from django.urls import path, include

from .views import BooksListView, BookDetailsView

urlpatterns = [
    path('', BooksListView.as_view(), name="get_books"),
    path('<int:id>/', BookDetailsView.as_view(), name="book_detail")
]
