import io

from django.db.models import Exists, F, OuterRef, Sum, Value
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.permissions import (
    BlockPermission, RecipeObjectPermission,
    RecipePermission)
from api.serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeSerializer,
    ShoppingListSerializer,
    SmallRecipeSerializer,
    SubscriptionSerializer,
    SubscriptionUserSerializer,
    TagSerializer,
    TokenLoginSerializer,
    UserSerializer,
    UserSetPasswordSerializer,
    UserSmallSerializer)
from models_app.models import (
    Favorites,
    Ingredient,
    Recipe,
    ShoppingList,
    Subscription, Tag
)
from users.models import User


class IngredientViewSet(ModelViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        return Ingredient.objects.filter(
            name__startswith=self.request.GET.get("name", ""))


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        BlockPermission,
        RecipePermission,
        RecipeObjectPermission
    )

    def get_queryset(self):
        author = self.request.GET.get("author")
        tags = self.request.GET.getlist("tags")
        recipes = Recipe.objects.all()
        if author:
            recipes = recipes.filter(author_id=author)
        if tags:
            recipes = recipes.filter(tags__slug__in=tags).distinct()

        is_in_shopping_cart = self.request.GET.get("is_in_shopping_cart")
        if is_in_shopping_cart and self.request.user.is_authenticated:
            shopping_list = get_object_or_404(
                ShoppingList,
                user=self.request.user
            )

            if is_in_shopping_cart == "0":
                recipes = recipes.exclude(
                    shoppinglist=shopping_list,
                )
            elif is_in_shopping_cart == "1":
                recipes = recipes.filter(
                    shoppinglist=shopping_list,
                )

        is_favorited = self.request.GET.get("is_favorited")
        if is_favorited and self.request.user.is_authenticated:
            if is_favorited == "0":
                recipes = recipes.exclude(
                    list_recipes_favorites__user=self.request.user
                )
            elif is_favorited == "1":
                recipes = recipes.filter(
                    list_recipes_favorites__user=self.request.user
                )
        if self.request.user.is_authenticated:
            recipes = recipes.annotate(
                is_favorited=Exists(
                    Favorites.objects.filter(
                        user_id=self.request.user.id,
                        recipe=OuterRef("id")
                    )
                ),
                is_in_shopping_cart=Exists(
                    get_object_or_404(
                        ShoppingList,
                        user_id=self.request.user.id,
                    ).recipes.filter(id=OuterRef("id"))
                )
            )
        return recipes

    @action(
        methods=("post", "delete"),
        detail=True,
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == "POST":
            serializer = FavoriteSerializer(
                instance=recipe,
                data=request.data,
                context={
                    "recipe": recipe,
                    "user": request.user,
                    "method": "post",
                }
            )
            serializer.is_valid(raise_exception=True)
            Favorites.objects.create(
                user=request.user,
                recipe=recipe
            )
            return Response(
                SmallRecipeSerializer(recipe).data,
                status=status.HTTP_201_CREATED
            )
        if request.method == "DELETE":
            serializer = FavoriteSerializer(
                instance=recipe,
                data=request.data,
                context={
                    "recipe": recipe,
                    "user": request.user,
                    "method": "delete",
                }
            )
            serializer.is_valid(raise_exception=True)
            Favorites.objects.get(
                user=request.user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=("get",),
        detail=False,
    )
    def download_shopping_cart(self, request):
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

        buffer = io.BytesIO()
        with io.TextIOWrapper(
                buffer, encoding="utf-8", write_through=True
        ) as file:
            for key, value in data_ingredients.items():
                file.write(f"{key} - {value}\n")
            response = HttpResponse(
                buffer.getvalue(),
                content_type="text/plain"
            )
            response[
                "Content-Disposition"
            ] = "attachment; filename=list-ingredients.txt"
            return response

    @action(
        methods=("post", "delete"),
        detail=True,
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        shopping_list = ShoppingList.objects.get(user=self.request.user)
        if request.method == "POST":
            serializer = ShoppingListSerializer(
                data=request.data,
                context={
                    "shopping_list": shopping_list,
                    "id": recipe.id,
                    "method": "post"
                }
            )
            serializer.is_valid(raise_exception=True)
            shopping_list.recipes.add(recipe)
            return Response(SmallRecipeSerializer(recipe).data,
                            status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            serializer = ShoppingListSerializer(
                instance=recipe,
                data=request.data,
                context={
                    "shopping_list": shopping_list,
                    "id": recipe.id,
                    "method": "delete"
                }
            )
            serializer.is_valid(raise_exception=True)
            shopping_list.recipes.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TokenViewSet(ModelViewSet):
    permission_classes = (BlockPermission,)

    @action(
        methods=("post",),
        detail=False,
    )
    def login(self, request):
        user = get_object_or_404(User, email=request.data["email"])
        serializer = TokenLoginSerializer(
            data=request.data,
            context={
                "user": user,
                "password": request.data["password"]
            }
        )
        serializer.is_valid(raise_exception=True)
        return Response({
            "auth_token": Token.objects.get_or_create(
                user=user
            )[0].key
        }, status=status.HTTP_201_CREATED)

    @action(
        methods=("post",),
        detail=False,
        permission_classes=[IsAuthenticated, ]
    )
    def logout(self, request):
        get_object_or_404(Token, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (BlockPermission, IsAuthenticated)

    @action(
        methods=("post",),
        detail=False,
    )
    def set_password(self, request):
        serializer = UserSetPasswordSerializer(
            data=request.data,
            context={
                "user": request.user
            }
        )
        serializer.is_valid(raise_exception=True)
        request.user.password = request.data["new_password"]
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=("get",),
        detail=False,
    )
    def me(self, request):
        return Response(
            self.get_serializer(request.user).data,
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(
            email=request.data["email"],
            username=request.data["username"],
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            password=request.data["password"]
        )
        Token.objects.create(user=user)
        ShoppingList.objects.create(user=user)
        Subscription.objects.create(user=user)
        user = get_object_or_404(User, email=request.data["email"])
        return Response(
            UserSmallSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    @action(
        methods=("get",),
        detail=False,
        pagination_class=PageNumberPagination,
    )
    def subscriptions(self, request):
        queryset = Subscription.objects.get(
            user=self.request.user
        ).authors.annotate(
            is_subscribed=Exists(
                Subscription.objects.get(
                    user=request.user
                ).authors.filter(id=OuterRef("id"))
            )
        ).all().order_by("id")
        paginator = self.pagination_class()
        return paginator.get_paginated_response(
            SubscriptionSerializer(paginator.paginate_queryset(
                queryset,
                request
            ), many=True).data
        )

    @action(
        methods=("post", "delete"),
        detail=True,
    )
    def subscribe(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        subscription = Subscription.objects.get(user=self.request.user)
        if request.method == "POST":
            serializer = SubscriptionUserSerializer(
                data=request.data,
                context={
                    "subscription": subscription,
                    "current_user": request.user,
                    "user": user,
                    "method": "post",
                }
            )
            serializer.is_valid(raise_exception=True)
            subscription.authors.add(user)
            user.is_subscribed = True
            return Response(
                SubscriptionSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        elif request.method == "DELETE":
            serializer = SubscriptionUserSerializer(
                data=request.data,
                context={
                    "subscription": subscription,
                    "user": user,
                    "method": "delete",
                }
            )
            serializer.is_valid(raise_exception=True)
            subscription.authors.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
