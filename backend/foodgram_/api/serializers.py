from rest_framework import serializers
from rest_framework.validators import ValidationError

from models_app.models import (
    Ingredient, IngredientAmount, Recipe,
    Subscription, Tag)
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
            return Subscription.objects.get_or_create(
                user=self.context["user"]
            )[0].authors.filter(id=obj.id).exists()
        return False


class FavoriteShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time"
        )


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
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
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

    def get_is_favorited(self, obj):
        return getattr(obj, "is_favorited", False)

    def get_is_in_shopping_cart(self, obj):
        return getattr(obj, "is_in_shopping_cart", False)


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
            )[0].authors.filter(id=obj.id).exists()
        return False


class UserSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
        )


class UserSetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if 'current_password' not in attrs:
            raise ValidationError({
                "current_password": "Обязательное поле."
            })
        if 'new_password' not in attrs:
            raise ValidationError({
                "new_password": "Обязательное поле."
            })
        return attrs
