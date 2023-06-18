from django.http import QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.serializers.subscription.list import SubscriptionListSerializer
from api.serializers.user.subscription import SubscriptionUserGetSerializer
from api.services.subscription.create import SubscriptionCreateService
from api.services.subscription.list import SubscriptionListService


class SubscriptionListView(APIView):

    def get(self, request, *args, **kwargs):
        data = (
            request.data
            if not isinstance(request.data, QueryDict)
            else request.data.dict()
        )
        outcome = ServiceOutcome(SubscriptionListService, data)
        return Response({
            "count": outcome.result.get("count", 0),
            "next": outcome.result.get("next"),
            "previous": outcome.result.get("previous"),
            "results": SubscriptionListSerializer(
                outcome.result["results"],
                many=True
            ).data
        }, status=status.HTTP_200_OK)


class SubscriptionCreateDeleteView(APIView):

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            SubscriptionCreateService, kwargs | {"user": request.user}
        )
        return Response(
            SubscriptionUserGetSerializer(outcome.result).data,
            status=status.HTTP_201_CREATED
        )
