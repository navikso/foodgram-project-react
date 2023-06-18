from django.urls import path
from api.views.favorite import FavoriteCreateDeleteView
from api.views.ingredient import IngredientListView, IngredientGetView
from api.views.recipe import RecipeDownloadView
from api.views.recipe import RecipeListCreateView, RecipeGetDeleteUpdateView
from api.views.shopping_list import ShoppingListDeleteView
from api.views.subscribe import SubscriptionCreateDeleteView
from api.views.tag import TagListView, TagGetView
from api.views.token import TokenGetView, TokenDeleteView
from api.views.user import (
    UserSetPasswordView, UserListCreateView,
    UserGetView, UserGetMeView
)

urlpatterns = [
    path("ingredients/", IngredientListView.as_view()),
    path("ingredients/<int:id>/", IngredientGetView.as_view()),

    path("tags/", TagListView.as_view()),
    path("tags/<int:id>/", TagGetView.as_view()),
    path("recipes/", RecipeListCreateView.as_view()),
    path("recipes/<int:id>/favorite/", FavoriteCreateDeleteView.as_view()),
    path("recipes/download_shopping_cart/", RecipeDownloadView.as_view()),
    path("auth/token/login/", TokenGetView.as_view()),
    path("recipes/<int:id>/", RecipeGetDeleteUpdateView.as_view()),
    path("recipes/<int:id>/shopping_cart/", ShoppingListDeleteView.as_view()),

    path("users/", UserListCreateView.as_view()),
    path("users/<int:id>/", UserGetView.as_view()),
    path("users/me/", UserGetMeView.as_view()),
    path("users/set_password/", UserSetPasswordView.as_view()),
    path("auth/token/logout/", TokenDeleteView.as_view()),

    path("users/<int:id>/subscribe/", SubscriptionCreateDeleteView.as_view())
]
