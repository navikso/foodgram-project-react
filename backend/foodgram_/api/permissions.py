from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework.exceptions import (
    AuthenticationFailed, PermissionDenied
)


class UserAccessPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            raise AuthenticationFailed({
                "detail": "Учетные данные не были предоставлены."})
        return True


class BlockPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return True
        if request.user.is_blocked:
            raise PermissionDenied(
                {
                    "detail": "Учетные данные не "
                              "были предоставлены. Вы заблокированы"
                }
            )
        return True
