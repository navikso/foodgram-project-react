from rest_framework import serializers

from models_app.models import Ingredient


class IngredientShowSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("name", "measurement_unit", )
