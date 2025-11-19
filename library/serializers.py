from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers

from library.models import Author, Genre, Book


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for converting author model to JSON and back"""
    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name", "full_name")


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for converting genre model to JSON and back"""
    class Meta:
        model = Genre
        fields = ("id", "name")


class BookSerializer(serializers.ModelSerializer):
    """Serializer for converting book model to JSON and back"""
    daily_fee = MoneyField(
        max_digits=5,
        decimal_places=2,
    )

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "genre",
            "cover",
            "inventory",
            "daily_fee"
        )


class BookListSerializer(serializers.ModelSerializer):
    """Serializer for converting book list to JSON and back."""
    daily_fee = MoneyField(
        max_digits=5,
        decimal_places=2,
    )

    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="full_name",
    )

    genre = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "genre",
            "cover",
            "inventory",
            "daily_fee"
        )


class BookDetailSerializer(serializers.ModelSerializer):
    """Serializer for converting book detail to JSON and back"""
    daily_fee = MoneyField(
        max_digits=5,
        decimal_places=2,
    )
    author = AuthorSerializer(many=False, read_only=True)
    genre = GenreSerializer(many=False, read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "genre",
            "cover",
            "inventory",
            "daily_fee"
        )
