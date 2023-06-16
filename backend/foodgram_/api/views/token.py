from django.http import QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.services.token.delete import TokenDeleteService
from api.services.token.get import TokenGetService
from rest_framework.authentication import BasicAuthentication


class TokenGetView(APIView):

    authentication_classes = (BasicAuthentication, )

    def post(self, request, *args, **kwargs):
        data = request.data if not isinstance(request.data, QueryDict) else request.data.dict()
        outcome = ServiceOutcome(TokenGetService, data)
        return Response({"auth_token": outcome.result.key}, status=status.HTTP_201_CREATED)


class TokenDeleteView(APIView):
    def post(self, request, *args, **kwargs):
        ServiceOutcome(TokenDeleteService, {"user": request.user})
        return Response({}, status=status.HTTP_204_NO_CONTENT)
