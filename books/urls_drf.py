from rest_framework.routers import SimpleRouter

from .views import BooksViewSet

app_name = "books_drf"

router = SimpleRouter()
router.register('books', BooksViewSet, basename='api_books')

urlpatterns = router.urls
