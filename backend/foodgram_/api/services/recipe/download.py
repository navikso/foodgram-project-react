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
        file = open(f"recipe/list-ingredients-{self.cleaned_data['user'].username}.txt", "w+")
        for key, value in self._data.items():
            file.write(f"{key} - {value}\n")
        file.close()
        return open(f"recipe/list-ingredients-{self.cleaned_data['user'].username}.txt", "r")

    @property
    def _data(self):
        data = {}
        for element in self._shopping_list:
            for recipe in element.recipes.all():
                for ingredientAmount in recipe.ingredients.select_related("ingredient").all():
                    if f'{ingredientAmount.ingredient.name} ({ingredientAmount.ingredient.measurement_unit})' in data:
                        data[f'{ingredientAmount.ingredient.name} ({ingredientAmount.ingredient.measurement_unit})'] += \
                            ingredientAmount.amount
                    else:
                        data[f'{ingredientAmount.ingredient.name} ({ingredientAmount.ingredient.measurement_unit})'] = \
                            ingredientAmount.amount
        return data
