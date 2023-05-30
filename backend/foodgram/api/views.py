# from rest_framework.decorators import action
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from recipes.models import (
    Tag, Recipe, Ingredient,
    Favorite, IngredientAmount,
    ShoppingCart, Subscription
)
from users.models import UserProfile
from .permissions import (IfSafeRequest, IsAdmin, IsMyUsername, )
# IsAuthor
from .serializers import (
                          RecipeSerializer,
                          IngredientSerializer,
                          TagSerializer,
                          RecipeCreateSerializer,
                          FavoriteSerializer,
                          IngredientAmountSerializer,
                          UserSerializer,
                          ShoppingCartSerializer,
                          DownloadShoppingCartSerializer,
                          SubscriptionSerializer
                          )


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    search_fields = ('id',)
    permission_classes = [IsAdmin | IfSafeRequest, ]
    lookup_field = 'slug'


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ('id',)
    permission_classes = [IsAdmin | IfSafeRequest, ]
    pagination_class = LimitOffsetPagination
    lookup_field = 'id'


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin | IfSafeRequest | IsMyUsername, ]
    pagination_class = LimitOffsetPagination
    serializer_class = RecipeSerializer
    filterset_fields = ('tags', 'name',)

    def get_queryset(self):
        queryset = Recipe.objects.all().order_by('pub_date')
        queryset = self.annotate_qs_is_favorite_field(queryset)
        return queryset

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE'):
            return RecipeCreateSerializer(many=True)
        return RecipeSerializer

    # def is_favourite(self, request, pk):
    #     recipe = get_object_or_404(Recipe, pk=self.pk)
    #     if request.method == 'POST':
    #         favourite, created = Favourite.objects.get_or_create(
    #             user=request.user,
    #             recipe=recipe
    #         )
    #         if created:
    #             serializer = FavouriteSerializer(favourite)
    #             return Response(
    #                 serializer.data,
    #                 status=status.HTTP_201_CREATED
    #             )
    #         else:
    #             return Response(
    #                 {'errors': (
    #                                 f'Рецепт "{recipe}" '
    #                                 'уже добавлен в Избранное'
    #                             )},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )


class IngredientAmountViewSet(viewsets.ModelViewSet):
    queryset = IngredientAmount.objects.all()
    serializer_class = IngredientAmountSerializer
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination

    def get_recipe(self):
        return get_object_or_404(Recipe, pk=self.kwargs.get('pk'))

    def get_queryset(self):
        return self.get_recipe().ingredients.select_related('pk').all()


class ShoppingCartViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartSerializer
    permission_classes = [AllowAny]

    def get_recipe(self):
        return get_object_or_404(Recipe, pk=self.kwargs.get('pk'))

    def get_queryset(self):
        return self.get_recipe().is_in_shopping_cart.select_related('pk').all()

    def shopping_cart(self, request, id):
        """Добавить / удалить рецепт в список покупок"""
        try:
            recipe = Recipe.objects.get(id=id)
            shop_cart = ShoppingCart.objects.get(
                user=request.user, recipe=recipe
            )
            if request.method == 'DELETE':
                shop_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except (Recipe.DoesNotExist, ShoppingCart.DoesNotExist):
            if request.method == 'POST':
                shop_cart = ShoppingCart.objects.create(
                    user=request.user, recipe=recipe
                )
                serializer = SubscriptionSerializer(shop_cart.recipe)
                return Response(
                    {'message': 'Рецепт успешно добавлен в список покупок!',
                     'data': serializer.data},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'message': 'Ошибка! Рецепт не найден в списке покупок',
                 'data': {}},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST
        )
    # def get_queryset(self):
    #     queryset = ShoppingCart.objects.all().order_by('pub_date')
    #     queryset = self.annotate_qs_is_in_shopping_cart_field(queryset)
    #     return queryset

    # def shopping_cart(request):
    #     recipes = request.user.purchases.all()
    #     return render(
    # request,
    # 'recipes/shopping_list.html',
    # {'recipes': recipes})

    # def shop_cart_add(request, pk):
    #     recipe = Recipe.objects.all()
    #     ingredient = Ingredient.objects.filter(recipe=recipe)
    #     shop_cart = ShoppingCart.objects.filter(
    #         user=request.user, ingredient=ingredient
    #     ).first()
    #     if not shop_cart:
    #         shop_cart = ShoppingCart(
    #             user=request.user, ingredient=ingredient)
    #         shop_cart.amount += ingredient['amount']
    #         shop_cart.save()


class DownloadShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = DownloadShoppingCartSerializer
    permission_classes = [AllowAny]

    def shopping_list_download(request):
        title = 'recipe__ingredients__title'
        measurement_unit = 'recipe__ingredients__measurement_unit'
        amount = 'recipe__ingredients__amount'
        ingredients = request.user.purchases.select_related('recipe').order_by(
            title).values(
                title, measurement_unit).annotate(amount=Sum(amount)).all()

        if not ingredients:
            return render(request, 'misc/400.html', status=400)

        text = 'Список покупок:\n\n'
        for number, ingredient in enumerate(ingredients, start=1):
            amount = ingredient['amount']
            text += (
                f'{number}) '
                f'{ingredient[title]} - '
                f'{amount} '
                f'{ingredient[measurement_unit]}\n'
            )

        response = HttpResponse(text, content_type='text/plain')
        filename = 'shopping_list.txt'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    search_fields = ('id',)
    lookup_field = 'id'

    def get_object(self):
        if self.kwargs.get('username') == 'me':
            username = self.request.user
        else:
            username = self.kwargs.get('username')
        obj = get_object_or_404(UserProfile, username=username)
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('username').lower() == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    search_fields = ('recipe',)

    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(
            user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class SubscriptionViewSet(viewsets.ModelViewSet):
#     serializer_class = SubscriptionSerializer
#     pagination_class = LimitOffsetPagination
#     lookup_field = 'author_id'

#     def get_queryset(self):
#         return Subscription.objects.filter(
#             user=self.request.user)

#     def get_object(self):
#         return get_object_or_404(
#             Subscription,
#             user=self.request.user,
#             author=self.kwargs.get('author_id'),
#         )

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data={
#             **request.data,
#             'author': kwargs.get('author_id')
#         })
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
