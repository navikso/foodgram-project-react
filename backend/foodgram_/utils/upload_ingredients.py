import json
import os
from models_app.models import Ingredient

from conf.settings.django import BASE_DIR


def upload_ingredients():
    with open(
        os.path.join(BASE_DIR, "utils", "ingredients.json"),
        "r", encoding="UTF-8"
    ) as file:
        data = json.loads(file.read())
        for ingredient in data:
            Ingredient.objects.get_or_create(
                name=ingredient["name"],
                measurement_unit=ingredient["measurement_unit"]
            )
