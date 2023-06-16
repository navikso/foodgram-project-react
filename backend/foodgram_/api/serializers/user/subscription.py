from rest_framework import serializers

from api.serializers.recipe.list_recipe_subs import SubscriptionRecipeListSerializer
from models_app.models import User
from models_app.models import Subscription
from models_app.models import Recipe


class SubscriptionUserGetSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.IntegerField(
        source='user_recipes.count',
        read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name", "is_subscribed", "recipes", "recipes_count")

    def get_recipes(self, obj):
        return SubscriptionRecipeListSerializer(Recipe.objects.filter(user=obj), many=True).data

    def get_is_subscribed(self, obj):
        subs = Subscription.objects.get(authors=obj)
        return True if subs else False
