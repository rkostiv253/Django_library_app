import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint, Q, F
from django.utils import timezone

from library.models import Book
from library_service import settings


def return_date():
    return timezone.localdate() + datetime.timedelta(days=20)


class Borrowing(models.Model):
    """This model represents borrowing object,
    user: foreign key to user using AUTH_USER_MODEL
    created_at: date and time of borrowing
    status: borrowing status open or closed
    books: many to many field representing borrowed books"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    OPEN = "OP"
    CLOSED = "CL"
    STATUS_CHOICES = [
        (OPEN, "Open"),
        (CLOSED, "Closed"),
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=OPEN,
    )
    books = models.ManyToManyField(
        Book, through="BorrowingItem", related_name="borrowings"
    )


class BorrowingItem(models.Model):
    """This model represents borrowing item,
    borrowing: foreign key to borrowing object
    book: foreign key to book object
    quantity: number of borrowed copies
    borrow_date: date and time of borrowing
    expected_return date: date and time of return
    actual_return date: date and time of return"""
    borrowing = models.ForeignKey(
        Borrowing, on_delete=models.CASCADE, related_name="items"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(default=return_date)
    actual_return_date = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["borrowing", "book"],
                name="unique_borrowing_item",
            ),
            CheckConstraint(
                check=Q(quantity__gt=0),
                name="borrowingitem_quantity_gt_0",
            ),
            CheckConstraint(
                check=Q(expected_return_date__gte=F("borrow_date")),
                name="borrowingitem_expected_gte_borrow",
            ),
            CheckConstraint(
                check=Q(actual_return_date__isnull=True)
                | Q(actual_return_date__gte=F("borrow_date")),
                name="borrowingitem_actual_gte_borrow_or_null",
            ),
        ]

    def clean(self):
        if (
            self.actual_return_date
            and self.borrow_date
            and self.actual_return_date < self.borrow_date
        ):
            raise ValidationError("Return date cannot be before borrow date.")
        if (
            self.expected_return_date
            and self.borrow_date
            and self.expected_return_date < self.borrow_date
        ):
            raise ValidationError(
                "Expected return date cannot be before borrow date."
            )
        if self.quantity is not None and self.quantity < 1:
            raise ValidationError("Quantity cannot be less than one.")
        if (self.book and self.quantity and
                self.book.inventory < self.quantity):
            raise ValidationError(
                "Book inventory cannot be less than quantity."
            )

    def return_item(self, date=None):
        if self.actual_return_date:
            raise ValidationError("Item already returned")

        return_date = date or timezone.now().date()

        if return_date < self.borrow_date:
            raise ValidationError("Return date cannot be before borrow date.")

        self.book.inventory += self.quantity
        self.book.save(
            update_fields=["inventory"]
        )

        self.actual_return_date = return_date
        super().save(update_fields=["actual_return_date"])
        if not self.borrowing.items.filter(
                actual_return_date__isnull=True).exists(

        ):
            self.borrowing.status = Borrowing.CLOSED
            self.borrowing.save(update_fields=["status"])

    def save(self, *args, **kwargs):

        is_new = self._state.adding

        self.full_clean()

        if is_new:
            if self.book.inventory < self.quantity:
                raise ValidationError(
                    f"Not enough copies of '{self.book.title}' available."
                )
            self.book.inventory -= self.quantity
            self.book.save(update_fields=["inventory"])

        super().save(*args, **kwargs)
