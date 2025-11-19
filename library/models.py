from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money


class Author(models.Model):
    """This model represents author"""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    """This model represents genre"""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """This models represents book object,
    title: title of the book
    author: foreign key to author object
    genre: foreign key to genre object
    cover: book cover soft or hard
    inventory: number of books available
    daily_fee: price of book borrowing per day"""

    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    HARD = "HR"
    SOFT = "SO"
    COVER_CHOICES = [
        (HARD, "Hard"),
        (SOFT, "Soft"),
    ]
    cover = models.CharField(choices=COVER_CHOICES, max_length=2, default=HARD)
    inventory = models.PositiveIntegerField(default=0)
    daily_fee = MoneyField(
        max_digits=5,
        decimal_places=2,
        default=Money(0, "USD"),
        default_currency="USD"
    )

    def __str__(self):
        return self.title
