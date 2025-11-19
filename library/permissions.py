from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrAllowAny(BasePermission):
    """This permission allows to perform all operations
    and actions stated in safe methods for authenticated
    and unauthenticated users"""
    def has_permission(self, request, view):
        return bool(
            (request.method in SAFE_METHODS and request.user)
            or (request.user and request.user.is_staff)
        )
