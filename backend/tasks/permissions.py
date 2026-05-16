from rest_framework import permissions
from accounts.models import User


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.ADMIN
        )


class IsAdminOrAssignedUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == User.ADMIN:
            return True

        return obj.assigned_to == request.user