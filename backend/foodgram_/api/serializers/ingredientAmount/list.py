from rest_framework import serializers

from models_app.models import IngredientAmount


class IngredientAmountListSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = IngredientAmount
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    def get_name(self, obj):
        return obj.ingredient.name
