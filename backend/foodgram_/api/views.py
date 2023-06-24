import json
from json import JSONDecodeError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Value, Sum, F, Exists, OuterRef
from django.db.models.functions import Concat
from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import (
    ValidationError, NotFound, PermissionDenied)
from api.permissions import UserAccessPermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from rest_framework.authentication import BasicAuthentication

from api.serializers import (
    FavoriteShowSerializer, IngredientSerializer,
    RecipeShowSerializer,
    SubscriptionUserGetSerializer, TagListSerializer,
    SubscriptionRecipeListSerializer, UserSetPasswordSerializer
)

from models_app.models import (
    Favorites, Ingredient, IngredientAmount,
    Recipe, ShoppingList, Subscription, Tag
)
from .serializers import (
    UserGetSerializer,
    UserSmallSerializer
)
from users.models import User


class FavoriteCreateDeleteView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            recipe = get_object_or_404(Recipe, id=kwargs["id"])
        except Recipe.DoesNotExist:
            raise ValidationError("Рецепта не существует")

        if not request.user.is_authenticated:
            raise PermissionDenied(
                "У вас недостаточно прав для "
                "выполнения данного действия."
            )

        if Favorites.objects.filter(
                user=request.user,
                recipe=recipe
        ).exists():
            raise ValidationError("Рецепт уже находится в избранном")

        Favorites.objects.create(
            user=request.user,
            recipe=recipe
        )
        return Response(
            FavoriteShowSerializer(recipe).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        try:
            recipe = Recipe.objects.get(id=kwargs["id"])
        except Recipe.DoesNotExist:
            raise ValidationError("Рецепта не существует")

        if not Favorites.objects.filter(
                recipe=recipe,
                user=request.user
        ).exists():
            raise ValidationError("Рецепта нет в избранном")
        Favorites.objects.get(recipe=recipe, user=request.user).delete()
        return Response(
            {"INFO": "Рецепт успешно удален из избранного"},
            status=status.HTTP_204_NO_CONTENT
        )


class IngredientListView(ListAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        return Ingredient.objects.filter(
            name__startswith=self.request.GET.get("name", ""))


class IngredientGetView(APIView):

    def get(self, request, *args, **kwargs):
        ingredient = Ingredient.objects.get(id=kwargs["id"])
        return Response(
            IngredientSerializer(ingredient).data,
            status=status.HTTP_200_OK)


class RecipeListCreateView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        author = request.GET.get("author")
        tags = request.GET.getlist("tags")
        recipes = Recipe.objects.all()
        if author:
            recipes = recipes.filter(author_id=author)
        if tags:
            recipes = recipes.filter(tags__slug__in=tags)

        is_in_shopping_cart = request.GET.get("is_in_shopping_cart")
        if is_in_shopping_cart and self.request.user.is_authenticated:
            shopping_list = ShoppingList.objects.get_or_create(
                user=self.request.user
            )[0]
            if is_in_shopping_cart == "0":
                recipes = recipes.exclude(
                    shoppinglist=shopping_list,
                )
            elif is_in_shopping_cart == "1":
                recipes = recipes.filter(
                    shoppinglist=shopping_list,
                )

        is_favorited = request.GET.get("is_favorited")
        if is_favorited and self.request.user.is_authenticated:
            if is_favorited == "0":
                recipes = recipes.exclude(
                    list_recipes_favorites__user=self.request.user
                )
            elif is_favorited == "1":
                recipes = recipes.filter(
                    list_recipes_favorites__user=self.request.user
                )
        if request.user.is_authenticated:
            recipes = recipes.annotate(
                is_favorited=Exists(
                    Favorites.objects.filter(
                        user=request.user,
                        recipe=OuterRef('id'))
                ),
            )

            recipes = recipes.annotate(
                is_in_shopping_cart=Exists(
                    ShoppingList.objects.get_or_create(
                        user=request.user
                    )[0].recipes.filter(id=OuterRef('id')))
            )

        paginator = self.pagination_class()
        paginated_recipes = paginator.paginate_queryset(
            recipes,
            request
        )
        serializer = RecipeShowSerializer(
            paginated_recipes,
            many=True, context={"user": request.user}
        )
        return paginator.get_paginated_response(serializer.data)

    def get_ingredients(self, request):
        data = request.data.dict() if isinstance(
            request.data, QueryDict) else request.data
        try:
            ingredients = json.loads(data["ingredients"])
        except JSONDecodeError:
            raise ValidationError(
                "Передайте корректный список ингредиентов")

        list_ingredients = []
        for dict_element in ingredients:
            try:
                list_ingredients.append(
                    [Ingredient.objects.get(
                        id=dict_element["id"]),
                        dict_element["amount"]])
            except ObjectDoesNotExist:
                raise NotFound(
                    "Страница не найдена. "
                    f"(Ингредиента с id {dict_element['id']} "
                    f"не найдено)"
                )

        return list_ingredients

    def get_tags(self, request):
        data = request.data.dict() if isinstance(
            request.data, QueryDict) else request.data
        tags = []
        for id_tag in data["tags"].split(","):
            try:
                tags.append(Tag.objects.get(id=id_tag))
            except ObjectDoesNotExist:
                raise NotFound(
                    f"Страница не найдена. "
                    f"(Тега с id {id_tag} не найдено)"
                )
        return tags

    def post(self, request, *args, **kwargs):
        data = request.data.dict() if isinstance(
            request.data, QueryDict) else request.data
        for field in (
                "ingredients", "name",
                "image", "text", "cooking_time", "tags"
        ):
            if field not in data.keys():
                raise ValidationError(
                    {"detail": f"{field} обязательное поле"})
        recipe = Recipe.objects.create(
            name=data["name"],
            image=data["image"],
            text=data["text"],
            cooking_time=data["cooking_time"],
            author=request.user
        )

        for element in self.get_ingredients(request):
            recipe.ingredients.add(
                IngredientAmount.objects.get_or_create(
                    ingredient=element[0],
                    amount=element[1]
                )[0]
            )

        for element in self.get_tags(request):
            recipe.tags.add(element)
        recipe.is_favorited = Favorites.objects.filter(
            user=request.user, recipe=recipe).exists()

        recipe.is_in_shopping_cart = ShoppingList.objects.get_or_create(
            user=request.user
        )[0].recipes.filter(id=recipe.id).exists()

        return Response(
            RecipeShowSerializer(recipe,
                                 context={"user": request.user}).data,
            status=status.HTTP_201_CREATED)


class RecipeDownloadView(APIView):
    permission_classes = (UserAccessPermission,)

    def get(self, request, *args, **kwargs):
        shopping_list = ShoppingList.objects.filter(user=request.user)
        data = shopping_list.values(name_measurement_unit=Concat(
            F("recipes__ingredients__ingredient__name"), Value(" ("),
            F("recipes__ingredients__ingredient__measurement_unit"),
            Value(")"))
        ).annotate(amount=Sum("recipes__ingredients__amount")).values(
            "name_measurement_unit", "amount")
        data_ingredients = {
            item["name_measurement_unit"]: item["amount"] for (
                item) in data if bool(item["amount"])}

        file = open(
            f"recipe/list-ingredients-{request.user.username}.txt",
            "w+")
        for key, value in data_ingredients.items():
            file.write(f"{key} - {value}\n")
        file.close()
        return HttpResponse(
            open(
                f"recipe/list-ingredients-{request.user.username}.txt"
            ),
            content_type="text/plain")


class RecipeGetDeleteUpdateView(APIView):

    def get(self, request, *args, **kwargs):
        recipe = Recipe.objects.get(id=kwargs["id"])
        if not recipe:
            raise NotFound("Страница не найдена.")
        if request.user.is_authenticated:
            recipe.is_favorited = bool(Favorites.objects.filter(
                user=request.user, recipe=recipe))
            recipe.is_in_shopping_cart = ShoppingList.objects.get_or_create(
                user=request.user
            )[0].recipes.filter(id=recipe.id).exists()

        return Response(RecipeShowSerializer(
            recipe, context={"user": request.user}).data,
            status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            recipe = Recipe.objects.get(id=kwargs["id"])
        except Recipe.DoesNotExist:
            raise NotFound({"detail": "Страница не найдена."})
        if request.user != recipe.author:
            raise PermissionDenied(
                "У вас недостаточно прав для "
                "выполнения данного действия."
            )
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_ingredients(self, request):
        data = request.data.dict() if isinstance(
            request.data, QueryDict) else request.data
        try:
            ingredients = json.loads(data["ingredients"])
        except JSONDecodeError:
            raise ValidationError(
                "Передайте корректный список ингредиентов")
        errors = []
        ingredient_list = []
        for element in ingredients:
            if element["amount"] <= 0:
                errors.append(
                    {
                        "id": element["id"],
                        "amount": "Убедитесь, что "
                                  "это значение больше нуля "
                    }
                )
            try:
                ingredient_list.append(
                    [Ingredient.objects.get(id=element["id"]),
                     element["amount"]])
            except ObjectDoesNotExist:
                raise NotFound(
                    "Страница не найдена. "
                    f"(Ингредиент с id {element['id']} не найден.)")
        if errors:
            raise ValidationError(errors)
        return ingredient_list

    def patch(self, request, *args, **kwargs):
        data = request.data if not isinstance(
            request.data, QueryDict) else request.data.dict()
        for field in (
                "ingredients", "name", "image", "text",
                "cooking_time",
                "tags"):
            if field not in data.keys():
                raise ValidationError(
                    {"detail": f"{field} обязательное поле"})

        try:
            recipe = Recipe.objects.get(id=kwargs["id"])
        except Recipe.DoesNotExist:
            raise NotFound({"detail": "Страница не найдена."})
        if recipe.author != request.user:
            raise PermissionDenied({
                "detail": "У вас недостаточно прав "
                          "для выполнения данного действия."
            })

        recipe.name = data["name"]
        recipe.image = data["image"]
        recipe.text = data["text"]
        recipe.cooking_time = data["cooking_time"]
        recipe.save()

        for ingredient, amount in self.get_ingredients(request):
            try:
                ing = recipe.ingredients.get(ingredient=ingredient)
            except ObjectDoesNotExist:
                ing = IngredientAmount.objects.create(
                    ingredient=ingredient, amount=amount)
            ing.amount = amount
            ing.save()
            recipe.ingredients.add(ing)

        return Response(
            RecipeShowSerializer(recipe, context={
                "user": request.user
            }).data,
            status=status.HTTP_200_OK)


class ShoppingCreateDeleteView(APIView):

    def post(self, request, *args, **kwargs):
        recipe = Recipe.objects.get(id=kwargs["id"])
        shopping_list = ShoppingList.objects.get_or_create(
            user=request.user
        )[0]
        shopping_recipe = shopping_list.recipes.filter(id=recipe.id)
        if shopping_recipe.exists():
            raise ValidationError(
                {"errors": "Рецепт уже есть в списке покупок"})
        shopping_list.recipes.add(recipe)
        return Response(SubscriptionRecipeListSerializer(recipe).data,
                        status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        try:
            shopping_list = ShoppingList.objects.get(
                user=request.user)
        except Recipe.DoesNotExist:
            raise NotFound(
                "Учетные данные не были предоставлены. "
                "(В корзине пусто)"
            )
        try:
            recipe = shopping_list.recipes.get(id=kwargs["id"])
        except Recipe.DoesNotExist:
            raise NotFound(
                "Учетные данные не были предоставлены. "
                "(Рецепт не найден)")
        shopping_list.recipes.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionListView(ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = (UserAccessPermission,)

    def list(self, request):
        subs = Subscription.objects.get_or_create(
            user=self.request.user
        )[0]
        paginator = self.pagination_class()
        paginated_authors = paginator.paginate_queryset(
            subs.authors.annotate(
                is_subscribed=Exists(
                    Subscription.objects.filter(
                        user=self.request.user,
                        authors=OuterRef("pk"))
                )
            ).all(),
            request
        )
        serializer = SubscriptionUserGetSerializer(
            paginated_authors,
            many=True, context={"user": request.user}
        )
        return paginator.get_paginated_response(serializer.data)


class SubscriptionCreateDeleteView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs["id"])
        except User.DoesNotExist:
            raise ValidationError({"detail": "Страница не найдена."})

        subscribe = (
            Subscription.objects.get_or_create(user=request.user)[0])

        if subscribe.authors.all().filter(id=kwargs["id"]):
            raise ValidationError(
                {"errors": "Вы уже подписаны на этого пользователя"})
        if request.user == user:
            raise ValidationError(
                {"errors": "Вы не можете подписаться на самого себя"})
        subscribe.authors.add(user)
        return Response(
            SubscriptionUserGetSerializer(
                user).data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        try:
            subscription = Subscription.objects.get(user=request.user)
        except Subscription.DoesNotExist:
            raise NotFound({"detail": "Страница не найдена."})
        try:
            user = User.objects.get(id=kwargs["id"])
        except User.DoesNotExist:
            raise ValidationError(
                {"errors": "Такого пользователя не существует"})
        if user not in subscription.authors.all():
            raise ValidationError(
                {
                    "errors": "Вы на этого пользователя "
                              "ещё не подписаны"})
        subscription.authors.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagListView(APIView):

    def get(self, request, *args, **kwargs):
        return Response(
            TagListSerializer(Tag.objects.all(), many=True).data)


class TagGetView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            tag = Tag.objects.get(id=kwargs["id"])
        except Tag.DoesNotExist:
            raise NotFound("Страница не найдена.")
        return Response(TagListSerializer(tag).data,
                        status=status.HTTP_200_OK)


class TokenGetView(APIView):
    authentication_classes = (BasicAuthentication,)

    def post(self, request, *args, **kwargs):
        data = request.data if not isinstance(
            request.data, QueryDict) else request.data.dict()
        user = User.objects.get(email=data["email"])
        key = Token.objects.get_or_create(user=user)[0].key
        if user.check_password(
                data["password"]
        ) or user.password == data["password"]:
            return Response(
                {"auth_token": key},
                status.HTTP_201_CREATED)


class TokenDeleteView(APIView):

    def post(self, request, *args, **kwargs):
        Token.objects.get(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSetPasswordView(APIView):

    def post(self, request, *args, **kwargs):
        current_user = request.user
        data = request.data if not isinstance(
            request.data, QueryDict) else request.data.dict()
        serializer = UserSetPasswordSerializer(data=data)
        if serializer.is_valid():
            for field in ("current_password", "new_password"):
                try:
                    data[field]
                except KeyError:
                    raise ValidationError(
                        {"error": f"{field} не заполнено"})

            current_pass = data["current_password"]
            if not current_user.check_password(
                    current_pass) and (
                    current_user.password != current_pass):
                raise ValidationError("Текущий пароль не верный")

            current_user.set_password(data["new_password"])
            current_user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListCreateView(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination
    queryset = User.objects.all()
    serializer_class = UserGetSerializer

    def post(self, request, *args, **kwargs):
        data = request.data if not isinstance(
            request.data, QueryDict) else request.data.dict()
        for field in (
                "email", "username", "first_name", "last_name",
                "password",
        ):
            try:
                data[field]
            except KeyError:
                raise ValidationError(
                    {"error": f"{field} не заполнено"})
        user = User.objects.create(
            email=data["email"],
            username=data["username"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            password=data["password"]
        )
        Token.objects.create(user=user)
        return Response(
            UserSmallSerializer(user).data,
            status=status.HTTP_201_CREATED)


class UserGetView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(User, id=kwargs["id"])
        except User.DoesNotExist:
            raise NotFound("Пользователь не найден.")
        return Response(
            UserGetSerializer(user).data, status=status.HTTP_200_OK)


class UserGetMeView(APIView):
    permission_classes = (UserAccessPermission,)

    def get(self, request, *args, **kwargs):
        return Response(
            UserGetSerializer(request.user).data,
            status=status.HTTP_200_OK)
