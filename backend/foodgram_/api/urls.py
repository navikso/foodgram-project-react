from django.urls import path

from api.views import (IngredientListView, IngredientGetView,
                       TagListView, RecipeListCreateView,
                       RecipeDownloadView, FavoriteCreateDeleteView,
                       TagGetView, ShoppingCreateDeleteView,
                       RecipeGetDeleteUpdateView, TokenGetView,
                       TokenDeleteView, SubscriptionCreateDeleteView,
                       SubscriptionListView
                       )

urlpatterns = [
    path("ingredients/", IngredientListView.as_view()),
    path("ingredients/<int:id>/", IngredientGetView.as_view()),

    path("tags/", TagListView.as_view()),
    path("tags/<int:id>/", TagGetView.as_view()),

    path("recipes/", RecipeListCreateView.as_view()),
    path("recipes/<int:id>/favorite/",
         FavoriteCreateDeleteView.as_view()),
    path("recipes/download_shopping_cart/",
         RecipeDownloadView.as_view()),
    path("recipes/<int:id>/", RecipeGetDeleteUpdateView.as_view()),
    path("recipes/<int:id>/shopping_cart/",
         ShoppingCreateDeleteView.as_view()),

    path("auth/token/logout/", TokenDeleteView.as_view()),
    path("auth/token/login/", TokenGetView.as_view()),

    path("users/<int:id>/subscribe/",
         SubscriptionCreateDeleteView.as_view()),
    path("users/subscriptions/",
         SubscriptionListView.as_view({"get": "list"})),
]
