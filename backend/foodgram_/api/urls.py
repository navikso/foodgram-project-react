from django.urls import include, path
from rest_framework import routers
from api.views import (
    IngredientViewSet, RecipeViewSet, TagViewSet, TokenViewSet)

router = routers.DefaultRouter()
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("tags", TagViewSet, basename="tags")
router.register("recipes", RecipeViewSet, basename="recipes")
router.register("auth/token", TokenViewSet, basename="auth")

urlpatterns = [
    path("", include(router.urls)),
    path("", include("users.urls")),
]
