from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.validators import ValidationError, UniqueTogetherValidator

from models_app.models import (
    Ingredient, IngredientAmount, Recipe,
    Favorites, Subscription, Tag)
from users.models import User
from conf.settings.django import env


class UserGetSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        user = self.context.get("user")
        if user and user.is_authenticated:
            return Subscription.objects.get(
                user=self.context["user"]
            ).authors.filter(id=obj.id).exists()
        return False


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
        )


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


class SubscriptionRecipeListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )

    def get_image(self, obj):
        return f"{env('DOMAIN')}{obj.image.url}"


class RecipeListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_image(self, obj):
        return f"{env('DOMAIN')}{obj.image.url}"


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "color",
            "slug",
        )


class RecipeShowSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountListSerializer(
        read_only=True,
        many=True
    )
    tags = TagListSerializer(read_only=True, many=True)
    author = UserGetSerializer(read_only=True)
    is_favorited = serializers.ReadOnlyField()
    is_in_shopping_cart = serializers.ReadOnlyField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time"
        )

    def get_image(self, obj):
        return f"{env('DOMAIN')}{obj.image.url}"

    # def validate(self, data):
    #     data = super().validate(data)
    #     # if not self.context['data'].get('image', None):
    #     #     raise ValidationError({'image': 'Обязательное поле.'})

    #     # if self.context['data'].get('ingredients', None):
    #     data['ingredients'] = []
    #     for ingredient in json.loads(self.context['data']['ingredients']):
    #         try:
    #             ingredient_object = Ingredient.objects.get(
    #                 id=ingredient['id']
    #             )
    #         except Ingredient.DoesNotExist:
    #             raise NotFound({'detail': 'Страница не найдена.'})
    #         if ingredient['amount'] < 0:
    #             raise ValidationError(
    #                 {'detail': 'Количество ингредиента '
    #                             'не может быть <= 0'}
    #             )
    #         data['ingredients'].append(
    #             [ingredient_object, ingredient['amount']]
    #         )
    #     # else:
    #     #     raise ValidationError({'ingredients': 'Обязательное поле.'})

    #     # if self.context['data'].get('tags', None):
    #     data['tags'] = []
    #     for tag_id in self.context['data']['tags'].split(','):
    #         try:
    #             data['tags'].append(Tag.objects.get(id=tag_id))
    #         except Tag.DoesNotExist:
    #             raise NotFound(
    #                 {
    #                     'detail': f'Страница не найдена.(Тег. id:{tag_id})'
    #                 }
    #             )
    #     # else:
    #     #     raise ValidationError({'tags': 'Обязательное поле.'})


class FavoriteShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time"
        )
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Favorites.objects.all(),
        #         fields=("favorites__recipe__id", "favorites__user__id")
        #     )
        # ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if self.context['recipe'] == attrs["recipe"]:
            raise ValidationError(
                {"current_password": "Рецепт уже в избранном"})
        return attrs


class SubscriptionUserGetSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.IntegerField(
        source="user_recipes.count",
        read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count"
        )

    def get_recipes(self, obj):
        return SubscriptionRecipeListSerializer(
            Recipe.objects.filter(author=obj), many=True
        ).data

    def get_is_subscribed(self, obj):
        user = self.context.get("user")
        if user and user.is_authenticated:
            return Subscription.objects.get_or_create(
                user=self.context["user"]
            ).authors.filter(id=obj.id)
        return False


class UserSmallSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
        )

    def validate(self, attrs):
        if self.email == attrs["email"]:
            raise ValidationError(
                {"email": "Такой email уже зарегистрирован"})
        return attrs


class UserSetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not self.context['user'].check_password(attrs["current_password"]):
            raise ValidationError(
                {"current_password": "Неверный пароль"})
        return attrs
