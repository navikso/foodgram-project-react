from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RecipeViewSet, TagViewSet,
    UserViewSet, SubscriptionViewSet,
    IngredientViewSet, FavoriteViewSet,
    ShoppingCartViewSet,
    DownloadShoppingCartViewSet
)

app_name = 'api'
API_VERSION_V1 = 'v1'


class NoPutRouter(DefaultRouter):
    def get_method_map(self, viewset, method_map):
        bound_methods = super().get_method_map(viewset, method_map)
        bound_methods.pop('put', None)
        return bound_methods


router = NoPutRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register(
    r'recipes/(/P<recipe_id>\d+)/shopping_cart',
    ShoppingCartViewSet,
    basename='shopping_cart'
)
router.register(
    r'recipes/(/P<recipe_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorite'
)
router.register(
    'recipes/download_shopping_cart',
    DownloadShoppingCartViewSet,
    basename='download'
)

router.register('recipes', RecipeViewSet, basename='recipes')
router.register(
    'users/<int:author_id>/subscriptions',
    SubscriptionViewSet,
    basename='subscribe'
),
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(f'{API_VERSION_V1}/auth/', include('djoser.urls.authtoken')),
    path(f'{API_VERSION_V1}/', include(router.urls)),
    path('', RecipeViewSet, name='index'),
]
