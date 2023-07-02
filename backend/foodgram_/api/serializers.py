import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import ValidationError

from models_app.models import (
    Favorites,
    Ingredient,
    IngredientAmount,
    Recipe,
    Subscription,
    Tag
)
from users.models import User


class UserSerializer(serializers.ModelSerializer):
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
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            return Subscription.objects.get(
                user=request.user
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
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit"
    )
    name = serializers.CharField(source="ingredient.name")
    id = serializers.IntegerField(source="ingredient.id")

    class Meta:
        model = IngredientAmount
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class ShoppingListSerializer(serializers.Serializer):

    def validate(self, attrs):
        shopping_list = self.context["shopping_list"]
        if self.context["method"] == "post":
            if shopping_list.recipes.filter(
                    id=self.context["id"]
            ).exists():
                raise ValidationError(
                    {"errors": "Рецепт уже есть в списке покупок"})
        if self.context["method"] == "delete":
            if not shopping_list.recipes.filter(
                    id=self.context["id"]
            ).exists():
                raise ValidationError(
                    {"errors": "Рецепт не находится в списке покупок"})
        return attrs


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "color",
            "slug",
        )


class TokenLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if self.context["user"].password != self.context["password"]:
            raise ValidationError({
                "errors": "Введен не верный пароль"
            })
        return attrs


class FavoriteSerializer(serializers.Serializer):

    def validate(self, attrs):
        user = self.context["user"]
        recipe = self.context["recipe"]
        attrs = super().validate(attrs)
        if self.context["method"] == "post":
            if Favorites.objects.filter(
                    user=user,
                    recipe=recipe
            ):
                raise ValidationError(
                    {"errors": "Рецепт уже в избранном"})
        if self.context["method"] == "delete":
            if not Favorites.objects.filter(
                    user=user,
                    recipe=recipe
            ):
                raise ValidationError(
                    {"errors": "Рецепт не находится в избранном"})
        return attrs


class SmallRecipeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time"
        )

    def get_image(self, obj):
        return obj.get_image()


class SubscriptionUserSerializer(serializers.Serializer):

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if self.context["method"] == "post":
            if self.context["current_user"] == self.context["user"]:
                raise ValidationError(
                    {
                        "errors": "Вы не можете подписаться на самого себя"
                    }
                )
            if self.context["user"] in self.context[
                "subscription"
            ].authors.all():
                raise ValidationError(
                    {
                        "errors": "Вы уже подписаны на этого пользователя"
                    }
                )
        if self.context["method"] == "delete":
            if self.context["user"] not in self.context[
                "subscription"
            ].authors.all():
                raise ValidationError(
                    {
                        "errors": "Вы не подписаны на этого пользователя"
                    }
                )
        return attrs


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = SmallRecipeSerializer(
        source="user_recipes",
        read_only=True,
        many=True
    )
    recipes_count = serializers.IntegerField(
        source="user_recipes.count",
        read_only=True
    )
    is_subscribed = serializers.BooleanField()

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
        if not self.context["user"].password == attrs["current_password"]:
            raise ValidationError(
                {"current_password": "Неверный пароль"})
        return attrs


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountListSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    is_favorited = serializers.BooleanField(read_only=True, default=False)
    is_in_shopping_cart = serializers.BooleanField(
        read_only=True,
        default=False
    )

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
        return obj.get_image()

    def get_image_base64(self, recipe_id):
        format_image, imgstr = self.initial_data["image"].split(";base64,")
        ext = format_image.split("/")[-1]
        return ContentFile(
            base64.b64decode(imgstr),
            name=f"recipe_image_{recipe_id}." + ext
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        tags_data = validated_data.pop("tags")
        recipe = Recipe.objects.create(
            **validated_data,
            author=self.context["request"].user
        )
        recipe.image = self.get_image_base64(recipe.id)
        recipe.save()
        ingredients = (
            IngredientAmount.objects.create(
                ingredient=ingredient, amount=amount, recipe=recipe
            )
            for ingredient, amount in ingredients_data
        )
        recipe.ingredients.set(ingredients)
        recipe.tags.set(tags_data)
        recipe.is_favorited = False
        recipe.is_in_shopping_cart = False
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time",
            instance.cooking_time
        )
        image_data = self.initial_data.get("image")
        if image_data:
            instance.image = self.get_image_base64(instance.id)
        instance.save()
        ingredients_data = validated_data.get("ingredients")
        ingredients = (
            IngredientAmount.objects.get_or_create(
                ingredient=ingredient,
                amount=amount)
            for ingredient, amount in ingredients_data
        )
        instance.ingredients.set(ingredients)
        tags_data = validated_data.get("tags")
        if tags_data:
            instance.tags.set(tags_data)
        return instance

    def validate(self, data):
        data = super().validate(data)
        if self.initial_data.get("ingredients", None):
            data["ingredients"] = []
            for ingredient in self.initial_data["ingredients"]:
                ingredient_object = get_object_or_404(
                    Ingredient,
                    id=ingredient["id"]
                )
                try:
                    ingredient["amount"] = int(ingredient["amount"])
                except ValueError:
                    ingredient["amount"] = 1
                data["ingredients"].append(
                    (ingredient_object, ingredient["amount"])
                )
        else:
            raise ValidationError({"ingredients": "Обязательное поле."})

        if self.initial_data.get("tags", None):
            data["tags"] = []
            for tag_id in self.initial_data["tags"]:
                data["tags"].append(get_object_or_404(Tag, id=tag_id))
        else:
            raise ValidationError({"tags": "Обязательное поле."})

        return data
