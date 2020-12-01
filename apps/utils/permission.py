from rest_framework.permissions import BasePermission

from apps.utils.constants import RoleType


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == RoleType.ADMIN.value)
