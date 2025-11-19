from django.db import transaction
from rest_framework import serializers

from borrowing.models import Borrowing, BorrowingItem
from library.serializers import BookDetailSerializer, BookListSerializer


class BorrowingItemSerializer(serializers.ModelSerializer):
    """Serializer for converting borrowing item model to JSON and back"""
    book = BookDetailSerializer(read_only=True)

    class Meta:
        model = BorrowingItem
        fields = (
            "id",
            "borrowing",
            "book",
            "quantity",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class BorrowingItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for borrowing item creation"""
    class Meta:
        model = BorrowingItem
        fields = (
            "id",
            "book",
            "quantity",
            "borrow_date",
            "expected_return_date"
        )
        extra_kwargs = {
            "borrow_date": {"required": False},
            "expected_return_date": {"required": False},
        }

    def validate(self, attrs):
        book = attrs.get("book")
        quantity = attrs.get("quantity")

        if quantity is None or quantity < 1:
            raise serializers.ValidationError(
                "Quantity must be greater than 0."
            )

        if book and quantity > book.inventory:
            raise serializers.ValidationError(
                f"Only {book.inventory} items of {book.title} are available."
            )

        return attrs


class BorrowingSerializer(serializers.ModelSerializer):
    """Serializer for converting borrowing model to JSON and back"""
    items = BorrowingItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Borrowing
        fields = ("id", "created_at", "status", "items")
        read_only_fields = ("id", "created_at", "status")

    def create(self, validated_data):
        items_data = validated_data.pop("items")

        with transaction.atomic():
            borrowing = Borrowing.objects.create(**validated_data)
            for item_data in items_data:
                BorrowingItem.objects.create(
                    borrowing=borrowing,
                    **item_data,
                )

        return borrowing


class BorrowingListSerializer(BorrowingSerializer):
    """Serializer for converting borrowing list to JSON and back"""
    books = BookListSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowing
        fields = ("id", "created_at", "status", "books")


class BorrowingDetailSerializer(BorrowingSerializer):
    """Serializer for converting borrowing detail to JSON and back"""
    items = BorrowingItemSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowing
        fields = ("id", "created_at", "status", "items")
        read_only_fields = ("id", "created_at", "status")
