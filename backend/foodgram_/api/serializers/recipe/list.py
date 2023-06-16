from rest_framework import serializers

from models_app.models import Recipe


class RecipeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"
