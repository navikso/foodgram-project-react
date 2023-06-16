from django.http import QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.errors import AuthenticationFailed
from service_objects.services import ServiceOutcome

from api.serializers.user.get_profile import UserGetProfileSerializer
from api.serializers.user.list import UserListSerializer
from api.serializers.user.show import UserGetSerializer
from api.services.subscription.list import SubscriptionListService
from api.services.user.set_password import UserSetPasswordService
from api.services.user.list import UserListService
from api.services.user.create import UserCreateService
from api.services.user.show import UserGetService
from rest_framework.authentication import BasicAuthentication


class UserSetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data if not isinstance(request.data, QueryDict) else request.data.dict()
        ServiceOutcome(UserSetPasswordService, data | {"user": request.user})
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class UserListCreateView(APIView):
    authentication_classes = (BasicAuthentication,)

    def get(self, request, *args, **kwargs):
        data = request.data if not isinstance(request.data, QueryDict) else request.data.dict()
        outcome = ServiceOutcome(UserListService, data)
        return Response({
            "count": outcome.result.get("count", 0),
            "next": outcome.result.get("next"),
            "previous": outcome.result.get("previous"),
            "results": UserListSerializer(outcome.result["results"], many=True).data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data if not isinstance(request.data, QueryDict) else request.data.dict()
        outcome = ServiceOutcome(UserCreateService, data)
        return Response(UserGetSerializer(outcome.result).data, status=status.HTTP_201_CREATED)


class UserGetView(APIView):

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(UserGetService, kwargs)
        return Response(UserGetProfileSerializer(outcome.result).data, status=status.HTTP_200_OK)


class UserGetMeView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            return Response(UserGetSerializer(request.user).data,
                            status=status.HTTP_200_OK)
        except Exception:
            raise AuthenticationFailed(message="Учетные данные не были предоставлены.")
