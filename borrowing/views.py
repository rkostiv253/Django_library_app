from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowing.models import Borrowing, BorrowingItem
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingSerializer,
    BorrowingItemSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    """Handles CRUD operations for borrowing,
    Adds filter by status for user and by status and user id for admin.
    Adds additional return action for returning book."""
    permission_classes = (IsAuthenticated,)
    queryset = Borrowing.objects.prefetch_related("items__book")

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        user_filter = self.request.query_params.get("user")
        status_filter = self.request.query_params.get("status")

        if not user.is_staff:
            qs = qs.filter(user=user)
            if status_filter:
                status = self._params_to_ints(status_filter)
                qs = qs.filter(status__in=status)
            return qs.distinct()

        if user_filter:
            user_ids = self._params_to_ints(user_filter)
            qs = qs.filter(user__id__in=user_ids)

        if status_filter:
            status = self._params_to_ints(status_filter)
            qs = qs.filter(status__in=status)

        return qs.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="return-item")
    def return_item(self, request, pk=None):

        borrowing = self.get_object()

        item_id = request.data.get("item_id")
        if not item_id:
            return Response(
                {"detail": "item_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            item = borrowing.items.get(pk=item_id)
        except BorrowingItem.DoesNotExist:
            return Response(
                {"detail": "Borrowing item not found for this borrowing."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            item.return_item()
        except ValidationError as e:
            if hasattr(e, "message_dict"):
                data = e.message_dict
            else:
                data = {"detail": e.messages}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        serializer = BorrowingItemSerializer(
            item, context=self.get_serializer_context()
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
