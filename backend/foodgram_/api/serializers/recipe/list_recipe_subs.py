from rest_framework import serializers

from models_app.models import Recipe


class SubscriptionRecipeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )
