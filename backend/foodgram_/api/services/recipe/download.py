from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from models_app.models import User, ShoppingList


class RecipeDownloadService(ServiceWithResult):
    user = ModelField(User)

    def process(self):
        self.result = self._file
        return self

    @property
    def _shopping_list(self):
        return ShoppingList.objects.filter(
            user=self.cleaned_data["user"]
        )

    @property
    def _file(self):
        client = self.cleaned_data['user'].username
        file = open(f"recipe/list-ingredients-{client}.txt", "w+")
        for key, value in self._data.items():
            file.write(f"{key} - {value}\n")
        file.close()
        return open(f"recipe/list-ingredients-{client}.txt", "r")

    @property
    def _data(self):
        data = {}
        for element in self._shopping_list:
            for recipe in element.recipes.all():
                for ingredientAmount in recipe.ingredients.select_related(
                    "ingredient"
                ).all():
                    ing_name = ingredientAmount.ingredient.name
                    ing_measure = ingredientAmount.ingredient.measurement_unit
                    ing_amount = ingredientAmount.amount
                    if f'{ing_name} ({ing_measure}' in data:
                        data[f'{ing_name} ({ing_measure})'] += \
                            ing_amount
                    else:
                        data[f'{ing_name} ({ing_measure})'] = \
                            ing_amount
        return data
