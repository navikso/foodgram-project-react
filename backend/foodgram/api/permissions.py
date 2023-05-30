from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_moderator
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_moderator
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IfSafeRequest(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsMyUsername(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.is_authenticated
            and view.kwargs.get('username') == 'me'
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser
            or request.user.is_authenticated
            and view.kwargs.get('username') == 'me'
        )
