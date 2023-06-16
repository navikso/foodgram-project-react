from rest_framework import serializers
from models_app.models import Ingredient


class IngredientListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"
