from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from borrowing.models import Borrowing, BorrowingItem
from library.models import Book
from library.tests.test_library_api import sample_author, sample_genre


def sample_book(**params):
    defaults = {
        "title": "Test Book",
        "author": sample_author(),
        "genre": sample_genre(),
        "cover": "HR",
        "inventory": 5,
        "daily_fee": "5",
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


BORROWING_URL = reverse("borrowing:borrowing-list")


def borrowing_return_item_url(borrowing_id):
    return reverse("borrowing:borrowing-return-item", args=[borrowing_id])


class UnauthenticatedBorrowingApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test123"
        )
        self.client.force_authenticate(user=self.user)
        self.book = sample_book()

    def test_borrowing_view(self):
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_borrowing_view(self):
        payload = {"items": [{"book": self.book.id, "quantity": 1}]}

        response = self.client.post(BORROWING_URL, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 4)

    def test_return_borrowing_item_view(self):
        borrowing = Borrowing.objects.create(user=self.user)
        item = BorrowingItem.objects.create(
            borrowing=borrowing,
            book=self.book,
            quantity=1,
        )

        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 4)

        url = borrowing_return_item_url(borrowing.id)
        payload = {"item_id": item.id}

        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item.refresh_from_db()
        self.assertIsNotNone(item.actual_return_date)
        self.assertEqual(item.actual_return_date, timezone.localdate())

        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 5)

        borrowing.refresh_from_db()
        self.assertEqual(borrowing.status, Borrowing.CLOSED)
