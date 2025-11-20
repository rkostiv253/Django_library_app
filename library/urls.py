from django.urls import path, include
from rest_framework import routers

from library.views import AuthorViewSet, GenreViewSet, BookViewSet

router = routers.DefaultRouter()
router.register("authors", AuthorViewSet)
router.register("genres", GenreViewSet)
router.register("books", BookViewSet)
urlpatterns = [
    path("", include(router.urls)),
]

app_name = "library"
