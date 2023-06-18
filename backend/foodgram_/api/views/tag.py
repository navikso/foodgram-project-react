from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.serializers.tag.list import TagListSerializer
from api.services.tag.list import TagListService
from api.services.tag.show import TagGetService


class TagListView(APIView):

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(TagListService, {})
        return Response(
            TagListSerializer(outcome.result, many=True).data,
            status=status.HTTP_200_OK
        )


class TagGetView(APIView):

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(TagGetService, kwargs)
        return Response(
            TagListSerializer(outcome.result).data,
            status=status.HTTP_200_OK
        )
