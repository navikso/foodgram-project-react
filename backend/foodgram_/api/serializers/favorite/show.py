from rest_framework import serializers

from models_app.models import Recipe


class FavoriteShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time"
        )
