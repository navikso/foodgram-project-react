from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class BlockPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_authenticated or request.user.is_active


class RecipePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS or (
            view.action == "download_shopping_cart"
        ):
            return request.user.is_authenticated
        return True


class RecipeObjectPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method.lower() in ("delete", "patch",):
            return obj.author == request.user and request.user.is_authenticated
        return True


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in (
            "set_password", "subscriptions", "subscribe", "me"
        ):
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated
