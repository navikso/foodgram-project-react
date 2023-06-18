from rest_framework import serializers

from api.serializers.ingredientAmount.list import (
    IngredientAmountListSerializer
)
from api.serializers.tag.list import TagListSerializer
from api.serializers.user.show import UserGetSerializer
from models_app.models import Recipe
from models_app.models import Favorites
from models_app.models import ShoppingList


class RecipeShowSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountListSerializer(read_only=True, many=True)
    tags = TagListSerializer(read_only=True, many=True)
    user = UserGetSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time"
        )

    def get_is_favorited(self, obj):
        return Favorites.objects.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        return ShoppingList.objects.filter(recipe=obj).exists()
