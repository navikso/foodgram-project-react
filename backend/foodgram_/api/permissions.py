from rest_framework import permissions


class BlockPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return not getattr(request.user, "is_blocked", False)


class RecipePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method.lower() == "post":
            return request.user.is_authenticated
        return True


class RecipeObjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method.lower() in ("delete", "patch",):
            return obj.author == request.user and request.user.is_authenticated
        return True


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method.lower() == "get" and view.action == ("me",):
            return request.user.is_authenticated
        elif view.action == (
            "set_password",
            "subscriptions",
            "subscribe"
        ):
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated
