from django.http import HttpResponse, QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.errors import AuthenticationFailed
from service_objects.services import ServiceOutcome

from api.serializers.recipe.list import RecipeListSerializer
from api.serializers.recipe.show import RecipeShowSerializer
from api.services.recipe.create import RecipeCreateService
from api.services.recipe.delete import RecipeDeleteService
from api.services.recipe.download import RecipeDownloadService
from api.services.recipe.list import RecipeListService
from api.services.recipe.show import RecipeGetService
from api.services.recipe.update import RecipeUpdateService


class RecipeListCreateView(APIView):

    def get(self, request, *args, **kwargs):
        data = (
            request.data
            if not isinstance(request.data, QueryDict)
            else request.data.dict()
        )
        outcome = ServiceOutcome(RecipeListService, data)
        return Response({
            "count": outcome.result.get("count", 0),
            "next": outcome.result.get("next"),
            "previous": outcome.result.get("previous"),
            "results": RecipeListSerializer(
                outcome.result["results"], many=True
            ).data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = (
            request.data
            if not isinstance(request.data, QueryDict)
            else request.data.dict()
        )
        outcome = ServiceOutcome(
            RecipeCreateService, data | {"user": request.user}, data
        )
        return Response(
            RecipeShowSerializer(outcome.result).data,
            status=status.HTTP_201_CREATED
        )


class RecipeDownloadView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                RecipeDownloadService, {"user": request.user}
            )
            return HttpResponse(outcome.result, content_type="text/plain")
        except Exception:
            raise AuthenticationFailed(
                message="Учетные данные не были предоставлены."
            )


class RecipeGetDeleteUpdateView(APIView):

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(RecipeGetService, kwargs)
        return Response(
            RecipeListSerializer(outcome.result).data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        ServiceOutcome(RecipeDeleteService, kwargs | {"user": request.user})
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        data = (
            request.data
            if not isinstance(request.data, QueryDict)
            else request.data.dict()
        )
        outcome = ServiceOutcome(RecipeUpdateService,
                                 kwargs | {"user": request.user} | data, data)
        return Response(
            RecipeShowSerializer(outcome.result).data,
            status=status.HTTP_200_OK
        )
