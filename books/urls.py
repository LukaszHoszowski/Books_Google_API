from django.urls import path, include

urlpatterns = [
    path('', BooksList.as_view(), name="get_books"),
    path('<int:id>/', BookDetails.as_view(), name="book_detail")
]
