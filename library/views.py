from rest_framework import viewsets

from library.models import Author, Genre, Book
from library.permissions import IsAdminOrAllowAny
from library.serializers import (
    AuthorSerializer,
    GenreSerializer,
    BookSerializer
)


class AuthorViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for authors.
    Only admin users can perform POST/PUT/PATCH/DELETE operations."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminOrAllowAny,)


class GenreViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for genres.
    Only admin users can perform POST/PUT/PATCH/DELETE operations."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrAllowAny,)


class BookViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for books.
    Only admin users can perform POST/PUT/PATCH/DELETE operations."""
    queryset = Book.objects.prefetch_related("authors", "genres")
    permission_classes = (IsAdminOrAllowAny,)
    serializer_class = BookSerializer
