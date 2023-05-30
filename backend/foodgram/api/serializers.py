from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import (
    Recipe, Tag, Favorite,
    Ingredient, IngredientAmount,
    TagRecipe,
    ShoppingCart,
    Subscription
)
from users.models import UserProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'username',
            'password',
            'is_subscribed'
        )
        read_only_fields = ('id', 'is_subscribed',)

    def subscriber_status(self, obj):
        self.context.get('request').user
        return obj.author.filter(user=obj.id).exist()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    # source='ingredient.id')
    name = serializers.ReadOnlyField()
    # source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField()
    # source='ingredient.measurement_unit'
    amount = serializers.ReadOnlyField()
    # source='ingredient.amount')

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.ReadOnlyField(source='ingredient.amount')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def validate_amount(self, amount):
        if amount is not int:
            amount = int(float(amount))
        return self.validate_amount(amount)

    def validate_ingredients(ingredients):
        for ingredient in ingredients:
            if int(ingredient.get('amount')) < 1:
                raise ValidationError(
                    'Количество ингредиента должно быть больше 1')
        return ingredients


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    is_favorite = serializers.BooleanField(read_only=True)
    ingredients = IngredientSerializer(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'name',
            'author',
            'pub_date',
            'text',
            'tags',
            'ingredients',
            'image',
            'cooking_time',
            'is_favorite',
            'is_in_shopping_cart'
            )
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('name',)
            )
        ]

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.author = validated_data.get('author', instance.author)
        instance.pub_date = validated_data.get(
            'pub_date', instance.pub_date
            )
        instance.image = validated_data.get('image', instance.image)
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            lst = []
            for tag in tags_data:
                current_tag, status = Tag.objects.get_or_create(
                    **tag
                    )
                lst.append(current_tag)
            instance.tags.set(lst)

        instance.save()
        return instance

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request').user.id
        if request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            _user=request.user, pk=obj.pk
        ).exists()

    def get_is_in_favorite(self, obj):
        request = self.context.get('request').user.id
        if request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, pk=obj.pk
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(
        slug_field='slug', queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = (
            'name',
            'tags',
            'cooking_time',
            'image',
            'ingredients',
            'text',
        )

    def create(self, validated_data):
        if 'tag' not in self.initial_data:
            recipe = Recipe.objects.create(**validated_data)
            return recipe

        tags = validated_data.pop('tag')
        recipe = Recipe.objects.create(**validated_data)

        for tag in range(tags):
            current_tag, status = Tag.objects.get_or_create(
                **tag)
            TagRecipe.objects.create(
                tag=current_tag, recipe=recipe)
        return recipe

    def add_ingredients(self, ingredients, recipe):
        requested_ingredients = {}
        for item in ingredients:
            requested_ingredients[item['pk']] = item['amount']

        ingredient_in_recipe_objs = []
        for ingredient in Ingredient.objects.all():
            if ingredient.pk in requested_ingredients.keys():
                ingredient_in_recipe_objs.append(
                    Ingredient(
                        ingredient=ingredient,
                        recipe=recipe,
                        amount=requested_ingredients[ingredient.pk],
                    )
                )

        Ingredient.objects.bulk_create(ingredient_in_recipe_objs)

    def get_recipe(self):
        return get_object_or_404(Recipe, id=self.kwargs.get('id'))

    def get_queryset(self):
        return self.get_recipe().ingredients.all()


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = {
            'recipe'
        }


class DownloadShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка покупок."""
    class Meta:
        model = ShoppingCart
        fields = {
            '__all__'
        }

    def to_representation(self, instance):
        response = {}
        shop_list = ''
        query = Ingredient.objects.filter(
            recipe__in=instance.values('recipe')
        ).values('ingredient').annotate(score=('amount'))
        for item in query:
            name = Ingredient.objects.get(id=item.get('ingredients')).name
            measurement_unit = Ingredient.objects.get(
                id=item.get('ingredients')).measurement_unit
            sum = item.get('score')
            str = f'{name} {measurement_unit} - {sum} \n'
            shop_list += str
        response['shop_list'] = shop_list
        return response


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('user', 'recipe')
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe')
            )
        ]

    def validate(self, data):
        if len(Favorite.objects.filter(user=self.context['request'].user,
                                       recipe=data['recipe'])) > 0:
            raise serializers.ValidationError(
                'Этот рецепт уже добавлен в избранное.'
            )
        return data


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('author', 'is_subscibed')
        model = Subscription
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('author', 'is_subscibed')
            )
        ]

    def validate(self, data):
        if self.context['request'].user == data['is_subscibed']:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя.'
            )
        if len(Favorite.objects.filter(user=self.context['request'].user,
                                       is_subscibed=data['is_subscibed'])) > 0:
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора.'
            )
        return data
