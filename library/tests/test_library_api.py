from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from library.models import Author, Genre

BOOK_URL = reverse("library:book-list")


def sample_author(**params):
    defaults = {
        "first_name": "Test",
        "last_name": "Author",
    }
    defaults.update(params)
    return Author.objects.create(**defaults)


def sample_genre(**params):
    defaults = {
        "name": "Poem",
    }
    defaults.update(params)
    return Genre.objects.create(**defaults)


class UnauthenticatedLibraryApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_book_view(self):
        response = self.client.get(BOOK_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_unauthorized(self):

        payload = {
            "title": "Test Book",
            "author": sample_author().id,
            "genre": sample_genre().id,
            "cover": "HR",
            "inventory": 5,
            "daily_fee": "5",
        }

        response = self.client.post(BOOK_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedLibraryApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test123"
        )
        self.client.force_authenticate(user=self.user)

    def test_book_view(self):
        response = self.client.get(BOOK_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_forbidden(self):

        payload = {
            "title": "Test Book",
            "author": sample_author().id,
            "genre": sample_genre().id,
            "cover": "HR",
            "inventory": 5,
            "daily_fee": "5",
        }

        response = self.client.post(BOOK_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminLibraryApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test123", is_staff=True
        )
        self.client.force_authenticate(user=self.user)

    def test_create_book(self):

        payload = {
            "title": "Test Book",
            "author": sample_author().id,
            "genre": sample_genre().id,
            "cover": "HR",
            "inventory": 5,
            "daily_fee": "5",
        }

        response = self.client.post(BOOK_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
