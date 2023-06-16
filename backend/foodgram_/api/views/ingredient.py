from django.http import QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.serializers.ingredient.list import IngredientListSerializers
from api.serializers.ingredient.show import IngredientShowSerializers
from api.services.ingredient.get import IngredientGetService
from api.services.ingredient.list import IngredientListService


class IngredientListView(APIView):

    def get(self, request, *args, **kwargs):
        data = request.data if not isinstance(request.data, QueryDict) else request.data.dict()
        outcome = ServiceOutcome(IngredientListService, data)
        return Response(IngredientListSerializers(outcome.result, many=True).data, status=status.HTTP_200_OK)


class IngredientGetView(APIView):

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(IngredientGetService, kwargs)
        return Response(IngredientShowSerializers(outcome.result).data, status=status.HTTP_200_OK)
