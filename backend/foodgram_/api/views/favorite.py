from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome
from api.serializers.favorite.show import FavoriteShowSerializer
from api.services.favorite.create import FavoriteCreateService
from api.services.favorite.delete import FavoriteDeleteService


class FavoriteCreateDeleteView(APIView):

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(FavoriteCreateService, kwargs | {"user": request.user})
        return Response(FavoriteShowSerializer(outcome.result).data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        ServiceOutcome(FavoriteDeleteService, kwargs | {"user": request.user})
        return Response({"INFO": "Рецепт успешно удален из избранного"}, status=status.HTTP_204_NO_CONTENT)
